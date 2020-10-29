from django.urls import path
from .views import postWord,getStories,getStoryDetails,StoriesListView,StoriesListViewFilter

urlpatterns = [
    path('POST/add/', postWord),
    path('GET/stories/', getStories),
    path('GET/stories/<int:id>', getStoryDetails),
    path('GetStories/', StoriesListView.as_view()),
    path('GetStoriesFilter/', StoriesListViewFilter.as_view())
]
