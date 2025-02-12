from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MediaFile
from .forms import MediaFileForm
from django.http import HttpResponseForbidden
import os
# Create your views here.


@login_required
def media_list(request):
    media_files = MediaFile.objects.filter(user=request.user).order_by("-uploaded_at")
    return render(request, "media/media_list.html", {"media_files": media_files})


@login_required
def media_upload(request):
    if request.method == "POST":
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            media_file = form.save(commit=False)
            media_file.user = request.user
            media_file.save()
            return redirect("media:media_list")
    else:
        form = MediaFileForm()
    return render(
        request, "media/media_form.html", {"form": form, "title": "Upload Media"}
    )

@login_required
def media_edit(request, pk):
    media_file = get_object_or_404(MediaFile, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES, instance=media_file)
        if form.is_valid():
            form.save()
            return redirect('media:media_list')
    else:
        form = MediaFileForm(instance=media_file)
    return render(request, 'media/media_form.html', {'form': form, 'title': 'Edit Media'})


@login_required
def media_delete(request, pk):
    media_file = get_object_or_404(MediaFile, pk=pk, user=request.user)
    
    if media_file.user != request.user:
        return HttpResponseForbidden("You don't have permission to delete this file")
    
    if media_file.file:
        if os.path.isfile(media_file.file.path):
            os.remove(media_file.file.path)
            
    if media_file.thumbnail:
        if os.path.isfile(media_file.thumbnail.path):
            os.remove(media_file.thumbnail.path)
    
    media_file.delete()
    return redirect('media:media_list')