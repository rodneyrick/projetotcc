from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models heres
 
# class UploadFile(models.Model):
# 	type = models.CharField()
# 	title = models.CharField()
# 	date = models.DateTimeField(auto_now_add=True)
# 	path = models.CharField()
# 	docfile = models.FileField(upload_to='documents/')

# 	def __unicode__(self):
# 		return self.title