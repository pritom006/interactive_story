from django import forms
from .models import Story, StoryNode, StoryChoice

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'description']

class StoryNodeForm(forms.ModelForm):
    class Meta:
        model = StoryNode
        fields = ['text', 'parent']

class StoryChoiceForm(forms.ModelForm):
    class Meta:
        model = StoryChoice
        fields = ['from_node', 'to_node', 'choice_text']