# -*- coding: utf-8 -*-
from django import forms

class FileUploadForm(forms.Form):
    file_source = forms.FileField()