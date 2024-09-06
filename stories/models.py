from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Story(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.title

class StoryNode(models.Model):
    story = models.ForeignKey(Story, related_name='nodes', on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.SET_NULL)
    views = models.IntegerField(default=0)
    total_time_spent = models.DurationField(default=timezone.timedelta(0))
    start_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.text[:50]

class StoryChoice(models.Model):
    from_node = models.ForeignKey(StoryNode, related_name='choices_from', on_delete=models.CASCADE)
    to_node = models.ForeignKey(StoryNode, related_name='choices_to', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text
