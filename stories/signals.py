from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import StoryNode

@receiver(pre_save, sender=StoryNode)
def track_node_entry(sender, instance, **kwargs):
    # Track the time when the user starts reading a node
    instance.enter_time = timezone.now()

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StoryNode

@receiver(post_save, sender=StoryNode)
def track_node_exit(sender, instance, created, **kwargs):
    if not created:  # Avoid infinite recursion by only acting on existing instances
        time_spent = timezone.now() - instance.enter_time
        instance.total_time_spent += time_spent
        instance.views += 1
        # Disconnect the signal temporarily
        post_save.disconnect(track_node_exit, sender=StoryNode)
        instance.save()
        # Reconnect the signal
        post_save.connect(track_node_exit, sender=StoryNode)