from django.db import models


class RatingChoice(models.TextChoices):
    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, null=True, default=None)
    rating = models.CharField(
        max_length=20, choices=RatingChoice.choices, default=RatingChoice.G, null=True
    )
    synopsis = models.TextField(null=True, default=None)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="movies"
    )
    user_order = models.ManyToManyField(
        "users.User", related_name="movie_order", through="movies.MovieOrder"
    )


class MovieOrder(models.Model):
    user_order = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="movies_order"
    )
    movie_order = models.ForeignKey(
        "movies.Movie", on_delete=models.CASCADE, related_name="owner"
    )
    buyed_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
