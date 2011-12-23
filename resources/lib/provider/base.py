import socket
import sys
import simplejson
import urllib2
from urllib2 import HTTPError, URLError, urlopen
from resources.lib.script_exceptions import HTTP404Error, HTTP503Error, DownloadError, HTTPTimeout
from resources.lib.utils import _log as log

###required info labels in the imagelist: id, type, type2, url, preview, height, width, season, language, rating,series_name

### adjust default timeout to stop script hanging
timeout = 20
socket.setdefaulttimeout(timeout)

class BaseProvider:

    """
    Creates general structure for all fanart providers.  This will allow us to
    very easily add multiple providers for the same media type.
    """
    name = ''
    api_key = ''
    api_limits = False
    url = ''
    data = {}
    fanart_element = ''
    fanart_root = ''
    url_prefix = ''


    def get_json(self, url):
        try:
            log('API: %s'% url)
            req = urllib2.urlopen(url)
            log('Requested data:%s'% req)
            json_string = req.read()
            req.close()
        except HTTPError, e:
            if e.code == 404:
                raise HTTP404Error(url)
            elif e.code == 503:
                raise HTTP503Error(url)
            else:
                raise DownloadError(str(e))
        except:
            json_string = ''
        try:
            parsed_json = simplejson.loads(json_string)
        except:
            parsed_json = ''
        return parsed_json


    def get_xml(self, url):
        try:
            client = urlopen(url)
            data = client.read()
            client.close()
            return data
        except HTTPError, e:
            if e.code == 404:
                raise HTTP404Error(url)
            elif e.code == 503:
                raise HTTP503Error(url)
            else:
                raise DownloadError(str(e))
        except URLError:
            raise HTTPTimeout(url)
        except socket.timeout, e:
            raise HTTPTimeout(url)


    def get_image_list(self, media_id):
        pass
