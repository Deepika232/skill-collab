from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Count
from .models import Skill
from .forms import SkillForm
from users.models import UserProfile

# Create your views here.

def index(request):
    query = request.GET.get('q', '')
    skills = Skill.objects.all()
    if query:
        skills = skills.filter(name__icontains=query)
    skills = skills.annotate(
        teach_count=Count('teachers', distinct=True),
        learn_count=Count('learners', distinct=True)
    )
    return render(request, 'skills/index.html', {'skills': skills, 'query': query})

@login_required
def create_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('skills:index')
    else:
        form = SkillForm()
    return render(request, 'skills/create_skill.html', {'form': form})

@login_required
def edit_skill(request, pk):
    if not request.user.is_staff and not request.user.is_superuser:
        return HttpResponseForbidden('You are not authorized to edit skills.')
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('skills:index')
    else:
        form = SkillForm(instance=skill)
    return render(request, 'skills/edit_skill.html', {'form': form, 'skill': skill})

@login_required
def delete_skill(request, pk):
    if not request.user.is_staff and not request.user.is_superuser:
        return HttpResponseForbidden('You are not authorized to delete skills.')
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        skill.delete()
        return redirect('skills:index')
    return render(request, 'skills/delete_skill.html', {'skill': skill})
