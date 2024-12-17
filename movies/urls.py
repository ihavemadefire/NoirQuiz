from django.urls import path
from .views import TestListView

urlpatterns = [
    path('tests/', TestListView.as_view(), name='test-list'),

]