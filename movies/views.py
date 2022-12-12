from .permissions import IsEmployeeOrReadOnly
from .models import Movie
from .serializers import MovieSerializer, MovieOrderSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView, Response, Request, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly]

    def get(self, req: Request) -> Response:
        movies = Movie.objects.all()
        result_pages = self.paginate_queryset(movies, req, view=self)
        serializer = MovieSerializer(result_pages, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, req: Request) -> Response:
        movie = MovieSerializer(data=req.data)
        movie.is_valid(raise_exception=True)
        movie.save(user=req.user)

        return Response(movie.data, status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly]

    def get(self, req: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, req: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, req: Request, movie_id) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        movie_order = MovieOrderSerializer(data=req.data)
        movie_order.is_valid(raise_exception=True)
        movie_order.save(user_order=req.user, movie_order=movie)
        return Response(movie_order.data, status.HTTP_201_CREATED)
