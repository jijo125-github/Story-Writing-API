from django.urls import path
from .views import postWord,getStories,getStoryDetails

urlpatterns = [
    path('POST/add/', postWord),
    path('GET/stories/', getStories),
    path('GET/stories/<int:id>', getStoryDetails),
]
