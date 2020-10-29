from django.shortcuts import render
from django.http import JsonResponse
from django_filters import FilterSet
from django_filters import rest_framework as filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework import status
from rest_framework import generics
from .models import Story,Paragraph,Sentence
from .serializers import StorySerializer,GetStoriesSerializer


# Create your views here.

@api_view(['POST'])
def postWord(request):
    serializer = StorySerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        serialized_data = serializer.validated_data
        word = serialized_data.get('word')

        # Checking the length of the word posted by the client 
        if len(word.split()) > 1:
            data = {'error':'multiple words sent'}
            return JsonResponse(data, status = status.HTTP_400_BAD_REQUEST)

    story = Story.objects.last()
    # if there is no story at the begginning 
    if story is None:
        Story.objects.create(story_title = word)
        story = Story.objects.last()
        data = {"id":story.id, "title":story.story_title, "current_sentence":""}
        return JsonResponse(data, status = status.HTTP_201_CREATED)

    # if there are some stories 
    try:   
        story_title = story.story_title
        title_word_count = len(story_title.split())

        # if count of words in title less than 3
        if title_word_count < 2:
            story_obj = Story.objects.get(id = story.id)
            story_obj.story_title += ' ' + word
            story_obj.save()
            story = Story.objects.last()
            data = {"id":story.id, "title":story.story_title, "current_sentence":""}
            return JsonResponse(data, status = status.HTTP_201_CREATED)

        else:
            # we need to get access to sentence to append word
            paragraph = Paragraph.objects.filter(story = story.id).last()
            if paragraph is None:
                Paragraph.objects.create(story = story)
                paragraph = Paragraph.objects.last()
                Sentence.objects.create(story = story, paragraph = paragraph, sentence = word)
            else:
                paragraph_id = Paragraph.objects.last().id
                sentence_obj = Sentence.objects.last()
                if sentence_obj is None:
                    paragraph = Paragraph.objects.last()
                    Sentence.objects.create(story = story, paragraph = paragraph, sentence = word)
                else:
                    sentence = sentence_obj.sentence
                    current_sentence_word_count = len(sentence.split())

                    # if the word count in sentence greater than 5 
                    sentences_count = Sentence.objects.count()
                    if current_sentence_word_count == 5:

                        # if the total sentences count is 3
                        if sentences_count % 3 == 0:
                            paragraph_count = Paragraph.objects.count()

                            # if the paragraph count is more than 2
                            if paragraph_count % 2 == 0:
                                Story.objects.create(story_title = word)
                                story = Story.objects.last()
                                data = {"id":story.id, "title":story.story_title, "current_sentence":""}
                                return JsonResponse(data, status = status.HTTP_201_CREATED)

                            # if the paragraph count less than or equal to 2
                            else:
                                Paragraph.objects.create(story = story)
                                paragraph = Paragraph.objects.last()
                                Sentence.objects.create(story = story, paragraph = paragraph, sentence = word)

                        # if total sentence count less than 4        
                        else:
                            Sentence.objects.create(story = story, paragraph = paragraph, sentence = word)
                    # if word count in sentence less than or equal to 5        
                    else:
                        sentence_obj = Sentence.objects.last()
                        sentence_obj.sentence += ' ' + word
                        sentence_obj.save()
            
            story = Story.objects.latest('id')
            current_sentence_obj = Sentence.objects.last()
            if current_sentence_obj is None:
                return JsonResponse({'error':'no sentence obj'}, status = status.HTTP_404_NOT_FOUND)
            current_sentence = current_sentence_obj.sentence
            data = {
                "id":story.id,
                "title":story.story_title,
                "current_sentence":current_sentence
            }
            return JsonResponse(data,status=status.HTTP_201_CREATED)

    except Story.DoesNotExist:
        data = {'errors':'No values in tables'}
        return JsonResponse(data,status = status.HTTP_404_NOT_FOUND)
            
@api_view(['GET'])
def getStories(request):
    try:
        stories = Story.objects.all()
        serializer = GetStoriesSerializer(stories, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    except Story.DoesNotExist:
        return JsonResponse({'error':'Story does not exist'},status = status.HTTP_404_NOT_FOUND)        

@api_view(['GET'])
def getStoryDetails(request,id):
    try:
        story_obj = Story.objects.get(id = id)
        serializer = GetStoriesSerializer(story_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Story.DoesNotExist:
        error_data = {'error':'Story does not exist'}
        return JsonResponse(error_data, status = status.HTTP_404_NOT_FOUND)


class StoriesListView(generics.ListAPIView):
    serializer_class = GetStoriesSerializer

    def get_queryset(self):
        ''' filter the queryset based on Story_title or date created which are query params '''
        queryset = Story.objects.all()
        title = self.request.query_params.get('story_title', None)
        created_on = self.request.query_params.get('date_created', None)

        if title:
            queryset = queryset.filter(story_title = title)
            return queryset
        elif created_on:
            queryset = queryset.filter(story_date_created__contains = created_on)
            return queryset
        return queryset


class StoryFilter(FilterSet):
    title = filters.CharFilter('story_title')
    created_on = filters.CharFilter(field_name='story_date_created', method = 'filter_created_on')

    def filter_created_on(self, queryset, name, value):
        queryset = queryset.filter(story_date_created__contains = value)
        return queryset

    class Meta:
        model = Story
        fields = ('title', 'created_on',)
    
    
class StoriesListViewFilter(generics.ListAPIView):
    queryset = Story.objects.all()
    serializer_class = GetStoriesSerializer
    filter_backends = (filters.DjangoFilterBackend,OrderingFilter,SearchFilter)
    filter_class = StoryFilter
    ordering_fields  = ['story_date_created','story_date_updated']
    search_fields  = ['story_title']
