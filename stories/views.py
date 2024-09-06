from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Story, StoryNode, StoryChoice
from .forms import StoryChoiceForm, StoryForm, StoryNodeForm
from django.contrib.auth.decorators import login_required

def story_list(request):
    stories = Story.objects.all()
    return render(request, 'stories/story_list.html', {'stories': stories})

def story_detail(request, pk):
    story = get_object_or_404(Story, pk=pk)
    nodes = story.nodes.all()
    
    # Track time spent on current node (if it's a GET request, i.e., loading the node)
    if request.method == 'GET':
        for node in nodes:
            if node.start_time is None:  # Track time start if it wasn't already tracked
                node.start_time = timezone.now()
                node.save()

    return render(request, 'stories/story_detail.html', {'story': story})

def node_detail(request, node_id):
    node = get_object_or_404(StoryNode, pk=node_id)
    # choices = StoryChoice.objects.filter(from_node=node)
    choices = node.choices_from.all()

    if request.method == 'POST':
        form = StoryChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.from_node = node
            choice.save()
            return redirect('node_detail', node_id=node.id)
    else:
        form = StoryChoiceForm()

    # Track views and time spent on this node
    if request.method == 'GET':
        if node.start_time is None:  # Start tracking time
            node.start_time = timezone.now()
        node.views += 1
        node.save()

    elif request.method == 'POST':
        # Calculate time spent and update the total time spent on the node
        if node.start_time:
            time_spent = timezone.now() - node.start_time
            node.total_time_spent += time_spent
            node.start_time = None  # Reset start time for next session
            node.save()
    
    return render(request, 'stories/node_detail.html', {'node': node, 'choices': choices, 'form': form})

@login_required
def create_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            return redirect('story_detail', pk=story.pk)
    else:
        form = StoryForm()
    return render(request, 'stories/create_story.html', {'form': form})

@login_required
def create_story_node(request, story_pk):
    story = get_object_or_404(Story, pk=story_pk)
    if request.method == 'POST':
        form = StoryNodeForm(request.POST)
        if form.is_valid():
            node = form.save(commit=False)
            node.story = story
            node.save()
            return redirect('story_detail', pk=story.pk)
    else:
        form = StoryNodeForm()
    return render(request, 'stories/create_story_node.html', {'form': form, 'story': story})

@login_required
def story_analytics(request, pk):
    story = get_object_or_404(Story, pk=pk, author=request.user)
    nodes = story.nodes.all()
    return render(request, 'stories/story_analytics.html', {'story': story, 'nodes': nodes})


@login_required
def create_story_choice(request, node_id):
    node = get_object_or_404(StoryNode, pk=node_id)
    if request.method == 'POST':
        form = StoryChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.from_node = node
            choice.save()
            return redirect('node_detail', node_id=node_id)
    else:
        form = StoryChoiceForm()
    return render(request, 'stories/create_story_choice.html', {'form': form, 'node': node})

@login_required
def edit_story_choice(request, choice_id):
    choice = get_object_or_404(StoryChoice, pk=choice_id)
    if request.method == 'POST':
        form = StoryChoiceForm(request.POST, instance=choice)
        if form.is_valid():
            form.save()
            return redirect('node_detail', node_id=choice.from_node.id)
    else:
        form = StoryChoiceForm(instance=choice)
    return render(request, 'stories/edit_story_choice.html', {'form': form, 'choice': choice})


