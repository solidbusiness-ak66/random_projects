
#ts script is completely ai made ( -- learn later --)


import random

from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from library.models import Author, Book, Review


class Command(BaseCommand):
    help = "Generate 5000 sample library records"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        # Clear previous sample data before generating new data
        Review.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()

        random.seed(42)

        # Create 100 authors
        authors = [
            Author(
                name=f"Author {i}",
                email=f"author{i}@example.com",
                bio=f"Biography of author {i}"
            )
            for i in range(1, 101)
        ]

        Author.objects.bulk_create(authors)

        authors = list(Author.objects.all())

        # Create 1000 books
        books = []

        for i in range(1, 1001):
            price = Decimal(random.randint(200, 1500))

            books.append(
                Book(
                    title=f"Book {i}",
                    author=random.choice(authors),
                    price=price,
                    discount_price=price * Decimal("0.90"),
                    published_date=(
                        date.today() -
                        timedelta(days=random.randint(0, 3000))
                    )
                )
            )

        Book.objects.bulk_create(books)

        books = list(Book.objects.all())

        # Create 3900 reviews
        reviews = []

        for i in range(1, 3901):
            reviews.append(
                Review(
                    book=random.choice(books),
                    reviewer_name=f"Reviewer {i}",
                    rating=random.randint(1, 5),
                    comment=f"Review comment {i}"
                )
            )

        Review.objects.bulk_create(reviews)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully created 5000 records!"
            )
        )
