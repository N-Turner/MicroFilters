from django.shortcuts import render, redirect
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden, HttpResponseRedirect
from dropbox.client import DropboxOAuth2Flow
import utils
import urllib2, json

def index(request):
	if "dropbox-access-token" not in  request.session:
		return render(request, "core/index.html", { "dropbox_not_authorized": "true" })
	#REMEMBER TO REMOVE
	#request.session.pop("dropbox-access-token")
	return render(request, "core/index.html")

def downloadPage(request):
	if request.method == "POST":
		cacheKey = "%s_%s" % (request.META['REMOTE_ADDR'], request.GET.get("X-Progress-ID") )
		if request.FILES.get('data-file'):
			return utils.generateData(request.FILES.get('data-file'),request.POST.get('app'), "file", cacheKey, request.session["dropbox-access-token"])
		elif request.POST.get("data-url"):
			return utils.generateData(request.POST.get("data-url"),request.POST.get('app'), "url", cacheKey, request.session["dropbox-access-token"])
		else:
			return HttpResponse(status=400)
	else:
		return 	HttpResponse(status=405)

# Fetch the applist from AIDR API
# CORS issue, can't fetch directly from front-end
def getAppList(request):
	try:
		appList = urllib2.urlopen("http://pybossa-dev.qcri.org/AIDRTrainerAPI/rest/deployment/active")
		responseString = appList.read()

		#backup the applist locally
		appListFile = open('static/fallback/applist.json', 'w')
		appListFile.write(responseString)
		appListFile.close()

		return HttpResponse(responseString, status=200, content_type="application/json")
	except:
		appList = urllib2.urlopen("http://localhost:8000/static/fallback/applist.json")
		return HttpResponse(appList.read(), status=200, content_type="application/json")


def uploadProgress(request, uuid=None):
	"""
	Return JSON object with information about the progress of an upload.
	"""
	cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], uuid)
	data = cache.get(cache_key)
	if data:
		return HttpResponse(json.dumps(data))
	return HttpResponse(json.dumps({"progress": 5, "received": 0, "size": 0, "state": "starting"}))
