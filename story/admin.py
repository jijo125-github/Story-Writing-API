from django.contrib import admin
from .models import Story,Paragraph,Sentence

# Register your models here.
admin.site.register(Story)
admin.site.register(Paragraph)
admin.site.register(Sentence)
