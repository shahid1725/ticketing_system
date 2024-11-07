from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from dashboard.models import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='admin_loginview')
def addtag(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        if Tag.objects.filter(name=name).exists():
            messages.error(request, 'This name already exists')
            return render(request, 'Tag/Tag_Add.html', {'tags': Tag.objects.all()})
        try:
            Tag.objects.create(name=name)
            messages.success(request, 'Tag created successfully')
            return redirect('addtag')
        except Exception as e:
            return HttpResponse(f'An error occurred: {str(e)}')

    tags = Tag.objects.all()
    return render(request, 'Tag/Tag_Add.html', {'tags': tags})

@login_required(login_url='admin_loginview')
def taglist(request):
    tag_list = Tag.objects.all()
    return render(request, 'Tag/Tag_Add.html', {'tag_list': tag_list})

@login_required(login_url='admin_loginview')
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    if request.method == 'POST':
        try:
            tag.delete()
            messages.success(request, 'Tag deleted successfully')
            return redirect('addtag')
        except Exception as e:
            messages.error(request, f'Failed to delete tag: {str(e)}')
    
    # If GET request or deletion failed, render the page with existing tags
    tags = Tag.objects.all()
    return render(request, 'Tag/Tag_Add.html', {'tags': tags})