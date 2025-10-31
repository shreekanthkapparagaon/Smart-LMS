import os
import pandas as pd
import joblib
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from books.models import Book, bookTag, issueBook
from shelf.models import Shelf

class Command(BaseCommand):
    help = "Set up test user, books, shelves, and issued records for recommendation testing"

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
            "Friendship", "Religion", "Romance", "Children", "Beginner Friendly"
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

        # 4. Create books
        book_data = [
            {"title": "Old Empire: Burning Forest", "author": "Karan Rao", "tags": ["Short (<200 pages)", "Horror"]},
            {"title": "Lost Memory: Rising Bridge", "author": "Aarav Garcia", "tags": ["Religion", "Fantasy", "Friendship", "Short (<200 pages)"]},
            {"title": "Burning Song: Lonely House", "author": "Vihaan Kumar", "tags": ["Motivational", "Romance", "Religion", "Children", "Beginner Friendly"]},
            {"title": "Old Bridge", "author": "Anaya Rodriguez", "tags": ["Motivational", "Fantasy"]},
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

        # 6. Evaluate test accuracy using saved TF-IDF model
        try:
            vectorizer = joblib.load("data/tfidf_vectorizer.pkl")
            X = joblib.load("data/tfidf_matrix.pkl")
            df = pd.read_json("data/book_metadata.json")

            issued_books = issueBook.objects.filter(user=test_user).values_list("book_id", flat=True)

            if not issued_books:
                self.stdout.write(self.style.WARNING("⚠️ No issued books found for test accuracy check."))
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
                self.stdout.write(self.style.SUCCESS(f"📊 Test Top-{top_k} recommendation accuracy: {accuracy:.2%}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Accuracy check failed: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("🎉 Test setup complete. Ready for recommendation evaluation."))