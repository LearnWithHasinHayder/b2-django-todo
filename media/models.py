from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from PIL import Image
from io import BytesIO
import os
# Create your models here.

class MediaFile(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='media_files')
    thumbnail = models.ImageField(upload_to='uploads/thumbnails/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.make_thumbnail():
            # Set to None if there isn't an image for this instance
            self.thumbnail = None
        super().save(*args, **kwargs)
        
    def make_thumbnail(self):
        try:
            # Open and create thumbnail
            image = Image.open(self.file)
            image.thumbnail((300, 300))

            # Get file name and extension
            thumb_name, thumb_extension = os.path.splitext(self.file.name)
            thumb_filename = f"{thumb_name}_thumb{thumb_extension.lower()}"

            # Supported image formats
            image_types = {
                '.jpg': 'JPEG',
                '.jpeg': 'JPEG',
                '.png': 'PNG',
                '.gif': 'GIF'
            }

            # Check if file type is supported
            if thumb_extension.lower() not in image_types:
                return False

            # Save thumbnail
            temp_thumb = BytesIO()
            image.save(temp_thumb, image_types[thumb_extension.lower()])
            temp_thumb.seek(0)

            self.thumbnail.save(thumb_filename, File(temp_thumb), save=False)
            temp_thumb.close()
            return True
            
        except Exception as e:
            print(f"Thumbnail creation failed: {str(e)}")
            return False
        
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-uploaded_at']