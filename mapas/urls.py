from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('gmaps.views',
	# Examples:
	# url(r'^$', 'mapas.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),

	url(r'^$', 'index', name='index'),
	url(r'^region/', 'region',  name='region'),

	url(r'^listAllCIDs/', 'listAllCIDs',  name='listAllCIDs'),
	url(r'^listAllHealths/', 'listAllHealths',  name='listAllHealths'),
	url(r'^listAllDocuments/', 'listAllDocuments',  name='listAllDocuments'),
	url(r'^listAllPlaces/', 'listAllPlaces',  name='listAllPlaces'),

	url(r'^analysis', 'analysis',  name='analysis'),
	url(r'^filter$', 'filter',  name='filter'),
	
	url(r'^coords/loc$', 'locations', name='index'),
	url(r'^coords/loc$', 'locations', name='coords/loc'),

	# url(r'^regionSave$', 'saveNewPoints', name='region'),
	url(r'^region$', 'region', name='region'),

	url(r'^maps_regions$', 'maps_regions', name='maps_regions'),

	url(r'^filterAnalysis$', 'filter', name='filterAnalysis'),

	url(r'^upload_files$', 'uploadFilesToMediaFolder', name='index'),
	url(r'^upload_files$', 'uploadFilesToMediaFolder', name='coords/loc'),

	url(r'^admin/', include(admin.site.urls)),
)	+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
