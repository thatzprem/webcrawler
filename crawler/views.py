from django.shortcuts import render
from django.http import HttpResponse
import requests
import time
import sys
import os, django
from bs4 import BeautifulSoup, SoupStrainer
import urllib.parse
import json
from urllib.parse import urlparse
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
# Create your views here.

def index(request, template_name=None):
#     return HttpResponse("Hello, world. You're at the crawler index.")
    if template_name is None:
        template_name = 'index.html'
        
    return render(request, template_name, None)



def getSiteImages(request_url, soup_image):
    d = set()
    tags = soup_image.findAll('img')
    for tag in tags:
        try:
            source_url = tag['src']
            if source_url is not None:
                abs_url = urllib.parse.urljoin(request_url, source_url)
                d.add(abs_url)
        except Exception as e:
            print (e)
    return d

def getSiteLinks(request_url):
    h = set()
    url = urllib2.urlopen(request_url).read()
    soup = BeautifulSoup(url)
    for line in soup.find_all('a'):
        result = bool(urlparse(line.get('href')).netloc)
        if result:
            full_path = line.get('href')
            h.add(full_path)
    return h

def getCrawlData(request_url):

    try:
        django.setup()
    except Exception as e:
        print (e)
    session = requests.Session()
    request = session.get(request_url)
    soup_image = BeautifulSoup(request.content, "html.parser")
    
    d = getSiteImages(request_url, soup_image)
    
    h = getSiteLinks(request_url)
    
    result = {}
    result['data'] = d
    result['hyperlinks'] = h
    result['link'] = request_url
    return result

def contest(request):
    
    sys.path.append("/home/ubuntu/web/")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsknit.settings")
    print ("Setting django environment")
    
    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError
    
    request_url = request.GET.get('url', None)
    print ('URL:' + request_url)
    depth = int(request.GET.get('depth', None))
    print ('DEPTH:' + str(depth))
    
    result_final = []
    result = getCrawlData(request_url)
    print (result['hyperlinks'])
    
    if depth > 1:
        for link in result['hyperlinks']: 
            print ('######crawling:' + link)           
            result = getCrawlData(link)
            result_final.append(result)
    else:
        result_final.append(result)
                 
    return HttpResponse(json.dumps(result_final, default=set_default) , content_type="application/json")


        