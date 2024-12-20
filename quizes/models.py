from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    difficulty = models.CharField(max_length=255)
    questions = models.ManyToManyField('QuizQuestion', related_name='quizes')

    def __str__(self):
        return self.title

class QuizQuestion(models.Model):
    question = models.TextField()
    question_type = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=255)
    points = models.IntegerField()
    answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
