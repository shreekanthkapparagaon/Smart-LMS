from books.models import Book
from shelf.models import Shelf

def recommend_shelf_for_book(name, categories, author):
    shelves = Shelf.objects.filter(qunt__lt=5)
    shelf_scores = []

    for shelf in shelves:
        books = Book.objects.filter(addr=shelf)

        tag_score = sum(books.filter(catagory=tag).count() for tag in categories)
        author_score = books.filter(auther=author).count()
        crowd_penalty = books.count() * 0.2

        score = tag_score * 2 + author_score * 1.5 - crowd_penalty
        shelf_scores.append((shelf, score))

    shelf_scores.sort(key=lambda x: x[1], reverse=True)

    if not shelf_scores or shelf_scores[0][1] <= 0:
        fallback = shelves.order_by("qunt").first()
        return fallback

    best = shelf_scores[0][0]
    return best

