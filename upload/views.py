from django.http import HttpResponse
from django.shortcuts import render
from .forms import *
import time
import os
from django.conf import settings
from upload.bulkUploader import *
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.templatetags.staticfiles import static
import tempfile, zipfile
from wsgiref.util import FileWrapper
import mimetypes

error_message=0
def index(request):
	upload_form = UploadFileForm()
	global error_message
	temp_error_message=error_message
	error_message=0
	return render(request,"upload/index.html", {"upload_form":upload_form, 'error_message':str(temp_error_message)})

def upload_file(request):
	global error_message
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			email_id = request.POST["email_id"]
			filepath = handle_uploaded_file(request.FILES['file'])
			if filepath != False:
				error_message = Check(filepath,email_id) + 1
				return HttpResponseRedirect(reverse('upload:index'))
			return HttpResponse("Provide Valid File")
		else:
			print form.error
	return HttpResponse("Not success")

def handle_uploaded_file(f):
	fileName, fileExtension = os.path.splitext(f.name)
	filepath='temp/file_'+str(time.time()*1000)+fileExtension;
	with open(filepath, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
		return filepath
	return False
	
def send_file(request):
	filename     =  settings.BASE_DIR+'/static/'+settings.UPLOAD_TEMPLATE
	download_name = settings.UPLOAD_TEMPLATE
	wrapper      = FileWrapper(open(filename))
	content_type = mimetypes.guess_type(filename)[0]
	response     = HttpResponse(wrapper,content_type=content_type)
	response['Content-Length']      = os.path.getsize(filename)    
	response['Content-Disposition'] = "attachment; filename=%s"%download_name
	return response
