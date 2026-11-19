from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):

    title = models.CharField(max_length=200)

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE, related_name="books" ## deletes the book if aurthor deleted and this "cascades" into the reviews aswell
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    published_date = models.DateField()

    discount_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,related_name="reviews"
    )

    reviewer_name = models.CharField(max_length=100)

    rating = models.PositiveSmallIntegerField()

    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return f"{self.book.title} - {self.rating}/5"
