from django.contrib import admin
from .models import Story, StoryNode, StoryChoice

admin.site.register(Story)
admin.site.register(StoryNode)
admin.site.register(StoryChoice)
