from django.urls import path
from .views import CreateQuizView, QuizListView, QuizDetailView

"""URL configuration providing endpoints for creating, listing, and retrieving individual quiz objects via class-based views."""
urlpatterns = [
    path('createQuiz/', CreateQuizView.as_view(), name='create-quiz'),
    path('quizzes/', QuizListView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
]