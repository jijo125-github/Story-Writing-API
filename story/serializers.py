from rest_framework import serializers
from .models import Story,Paragraph,Sentence

POSSIBLE_WORD = ['word']

class StorySerializer(serializers.Serializer):
    word = serializers.CharField(allow_blank=True,required=False)

    def validate_word_action(self,value):
        if not value in POSSIBLE_WORD:
            raise serializers.ValidationError("Post with 'word' only")
        return value

class ParagraphSerializer(serializers.ModelSerializer):
    sentences = serializers.SlugRelatedField(many = True, read_only = True, slug_field = 'sentence' )
    
    class Meta:
        model = Paragraph
        fields = ['sentences']

class GetStoriesSerializer(serializers.ModelSerializer):
    paragraphs = ParagraphSerializer(read_only = True, many = True)

    class Meta:
        model = Story
        fields = ['id','story_title','story_date_created','story_date_updated','paragraphs']


    
    


