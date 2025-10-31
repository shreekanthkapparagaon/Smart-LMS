import os
import pandas as pd
import joblib
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from books.models import Book, bookTag, issueBook
from shelf.models import Shelf

class Command(BaseCommand):
    help = "Set up test user, books, shelves, and train offline recommendation vectors"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # 1. Create or update test user
        test_user, _ = User.objects.update_or_create(
            email="test@example.com",
            defaults={
                "is_active": True,
                "is_staff": True,
                "password": "testpass"
            }
        )
        self.stdout.write(self.style.SUCCESS("✅ Test user ready"))

        # 2. Create normalized tags
        tag_names = [
            "Fantasy", "Horror", "Motivational", "Short (<200 pages)",
            "Friendship", "Religion", "Romance", "Children", "Beginner Friendly",
            "Python", "AI", "ML", "Databases", "Networking", "Algorithms",
            "Software Engineering", "Data Science", "Theory"
        ]
        tags = {}
        for name in tag_names:
            normalized = name.strip().lower().replace(" ", "_")
            tag, _ = bookTag.objects.get_or_create(name=normalized)
            tags[name] = tag
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(tags)} tags"))

        # 3. Get all shelves
        shelves = Shelf.objects.all()[:10]
        if not shelves.exists():
            self.stdout.write(self.style.ERROR("❌ No shelves found. Run shelf generation first."))
            return

        # 4. Create books with multiple tags
        book_data = [
            {"title": "Old Empire: Burning Forest", "author": "Karan Rao", "tags": ["Short (<200 pages)", "Horror"]},
            {"title": "Lost Memory: Rising Bridge", "author": "Aarav Garcia", "tags": ["Religion", "Fantasy", "Friendship", "Short (<200 pages)"]},
            {"title": "Burning Song: Lonely House", "author": "Vihaan Kumar", "tags": ["Motivational", "Romance", "Religion", "Children", "Beginner Friendly"]},
            {"title": "Old Bridge", "author": "Anaya Rodriguez", "tags": ["Motivational", "Fantasy"]},
            {"title": "Fluent Python", "author": "Luciano Ramalho", "tags": ["Python", "Software Engineering"]},
            {"title": "Deep Learning with PyTorch", "author": "Eli Stevens", "tags": ["AI", "ML", "Python"]},
            {"title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann", "tags": ["Databases", "Software Engineering"]},
            {"title": "Hands-On Machine Learning", "author": "Aurélien Géron", "tags": ["ML", "AI", "Python"]},
            {"title": "Clean Code", "author": "Robert C. Martin", "tags": ["Software Engineering", "Theory"]},
        ]

        books = []
        for i, entry in enumerate(book_data):
            shelf = shelves[i % len(shelves)]

            book, _ = Book.objects.update_or_create(
                name=entry["title"],
                auther=entry["author"],
                defaults={
                    "discription": "Test description",
                    "addr": shelf
                }
            )

            tag_objs = []
            for tag_name in entry["tags"]:
                normalized = tag_name.strip().lower().replace(" ", "_")
                tag_obj, _ = bookTag.objects.get_or_create(name=normalized)
                tag_objs.append(tag_obj)

            book.catagory.set(tag_objs)
            books.append(book)

        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(books)} books"))

        # 5. Issue first two books to test user
        for book in books[:2]:
            issueBook.objects.get_or_create(user=test_user, book=book)

        self.stdout.write(self.style.SUCCESS("✅ Issued 2 books to test user"))

        # 6. Train and save offline vectors
        output_dir = "data"
        os.makedirs(output_dir, exist_ok=True)

        book_entries = [{
            "id": book.id,
            "title": book.name,
            "tags": " ".join([
                tag.name.lower().replace(" ", "_")
                for tag in book.catagory.all()
            ])
        } for book in Book.objects.prefetch_related('catagory').all()]

        df = pd.DataFrame(book_entries)
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(df["tags"])

        joblib.dump(vectorizer, os.path.join(output_dir, "tfidf_vectorizer.pkl"))
        joblib.dump(X, os.path.join(output_dir, "tfidf_matrix.pkl"))
        df.to_json(os.path.join(output_dir, "book_metadata.json"), orient="records", indent=2)

        self.stdout.write(self.style.SUCCESS(f"🎉 Training complete. Saved {len(df)} vectors to '{output_dir}'"))

        # 7. Evaluate top-k recommendation accuracy
        issued_books = issueBook.objects.filter(user=test_user).values_list("book_id", flat=True)

        if not issued_books:
            self.stdout.write(self.style.WARNING("⚠️ No issued books found for accuracy check."))
        else:
            issued_tags = [
                " ".join([
                    tag.name.lower().replace(" ", "_")
                    for tag in Book.objects.get(id=book_id).catagory.all()
                ])
                for book_id in issued_books
            ]

            query_vectors = vectorizer.transform(issued_tags)
            similarities = cosine_similarity(query_vectors, X)

            top_k = 5
            correct = 0
            for i, sim in enumerate(similarities):
                top_indices = sim.argsort()[::-1][:top_k]
                top_ids = df.iloc[top_indices]["id"].values
                if issued_books[i] in top_ids:
                    correct += 1

            accuracy = correct / len(issued_books)
            self.stdout.write(self.style.SUCCESS(f"📊 Top-{top_k} recommendation accuracy: {accuracy:.2%}"))