from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import QuizQuestion
from .serializers import QuizQuestionSerializer

class QuizQuestionViewSet(ReadOnlyModelViewSet):
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer