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
    """
    Create a `Quiz` from a given video URL.

    Behavior
    --------
    - Accepts POST body containing a `url` (YouTube or supported source).
    - Uses `create_quiz_from_video(url)` to derive quiz data (title, questions, etc.).
    - Injects `video_url` into the payload and persists via `CreateQuizPostSerializer`.
    - Associates the created quiz with the authenticated `request.user` as `owner`.

    Authentication & Permissions
    ----------------------------
    - Requires cookie-based authentication: `IsAuthenticatedFromCookie`.
    - Expects a valid session/JWT cookie available to the request.

    Responses
    ---------
    - 201: Returns serialized quiz (including nested questions) on success.
    - 400: Missing or invalid `url`, or download/parsing error from `yt_dlp`.

    Security
    --------
    - Validates input through DRF serializers; raises on invalid nested data.
    - Does not expose internal error traces—returns a generic, localized message
      for `DownloadError`.

    Notes
    -----
    - Consider wrapping the `serializer.save()` call in a transaction if
      downstream logic introduces additional writes.
    """

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
    """
    List quizzes owned by the authenticated user.

    Behavior
    --------
    - Returns only quizzes where `owner == request.user`.
    - Uses `QuizGetPatchSerializer` for a concise, read-focused payload.
    - Supports standard DRF pagination, ordering, and filtering if enabled globally.

    Authentication & Permissions
    ----------------------------
    - Requires cookie-based authentication: `IsAuthenticatedFromCookie`.

    Responses
    ---------
    - 200: Array of quiz objects (possibly paginated).
    """

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

