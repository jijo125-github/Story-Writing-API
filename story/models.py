from django.db import models

# Create your models here.

class Story(models.Model):
    story_title = models.CharField(max_length=100)
    story_date_created = models.DateTimeField(auto_now_add = True)
    story_date_updated = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "Stories"

    def __str__(self):
        return self.story_title

class Paragraph(models.Model):
    story = models.ForeignKey('Story', on_delete=models.CASCADE,related_name='paragraphs')
    paragraph_date_created = models.DateTimeField(auto_now_add = True)
    paragraph_date_updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        story_title = self.story.story_title
        return f'{story_title} - Paragraph {self.id}'

class Sentence(models.Model):
    story = models.ForeignKey('Story',on_delete = models.CASCADE)
    paragraph = models.ForeignKey('Paragraph',on_delete = models.CASCADE,related_name='sentences')
    sentence = models.TextField(blank = True)
    sentence_date_created = models.DateTimeField(auto_now_add = True)
    sentence_date_updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        para_title = self.paragraph
        return f'{para_title} - Sentence {self.id}'

