from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from yt_dlp.utils import DownloadError
from quiz_app.models import Quiz
from .permissions import IsAuthenticatedFromCookie, CookieJWTAuthentication, IsQuizOwner
from .serializers import CreateQuizPostSerializer, QuizGetPatchSerializer
from services.quiz_service import create_quiz_from_video

class CreateQuizView(generics.CreateAPIView):
    serializer_class = CreateQuizPostSerializer
    permission_classes = [IsAuthenticatedFromCookie]

    def create(self, request, *args, **kwargs):
        """Create a quiz from a video URL and associated data."""
        url = request.data.get("url")
        if not url:
            return Response(
                {"error": "URL is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            quiz_data = create_quiz_from_video(url)
        except DownloadError as e:
            return Response(
                {"error": f"Ungültige URL oder YouTube-ID: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        quiz_data["video_url"] = url

        serializer = self.get_serializer(data=quiz_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class QuizListView(generics.ListAPIView):
    serializer_class = QuizGetPatchSerializer
    permission_classes = [IsAuthenticatedFromCookie]

    def get_queryset(self):
        """Return a list of quizzes owned by the authenticated user."""
        return Quiz.objects.filter(owner=self.request.user)
    
class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizGetPatchSerializer
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated, IsQuizOwner]
    
    """Retrieve, update, or delete a quiz, restricted to quiz owner."""

