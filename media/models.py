from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files import File
import os

class MediaFile(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='uploads/')
    thumbnail = models.ImageField(upload_to='uploads/thumbnails/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='media_files')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.make_thumbnail():
            # Set to None if there isn't an image for this instance
            self.thumbnail = None
        super().save(*args, **kwargs)

    def make_thumbnail(self):
        try:
            image = Image.open(self.file)
            image.thumbnail((300, 300))
            thumb_name, thumb_extension = os.path.splitext(self.file.name)
            thumb_extension = thumb_extension.lower()
            thumb_filename = f"{thumb_name}_thumb{thumb_extension}"

            if thumb_extension in [".jpg", ".jpeg"]:
                FTYPE = "JPEG"
            elif thumb_extension == ".gif":
                FTYPE = "GIF"
            elif thumb_extension == ".png":
                FTYPE = "PNG"
            else:
                return False

            temp_thumb = BytesIO()
            image.save(temp_thumb, FTYPE)
            temp_thumb.seek(0)

            self.thumbnail.save(thumb_filename, File(temp_thumb), save=False)
            temp_thumb.close()
            return True
        except:
            return False

    class Meta:
        ordering = ['-uploaded_at']
