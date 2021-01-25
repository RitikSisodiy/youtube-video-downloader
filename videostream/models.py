from django.db import models
class video(models.Model):
	"""docstring for video"""
	video_name = models.CharField(max_length=50)
	video_file  = models.FileField(upload_to='videostream/video',default = "" )
	