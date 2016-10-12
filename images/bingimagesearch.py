
# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import pprint
import os


def main(name):
    query = name
    #print bing_search(query, 'Web')
    urls = bing_search(query, 'Image')
    return urls

def bing_search(query, search_type):
    #search_type: Web, Image, News, Video
    key= 'Fcojk/2qC2kkd3ibDY/l3JSWtEOeiVVwU9yQR41mE5Q'
    query = urllib.quote(query)
    # create credential for authentication
    user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
    credentials = (':%s' % key).encode('base64')[:-1]
    auth = 'Basic %s' % credentials
    url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/'+search_type+'?Query=%27'+query+'%27&$top=50&$format=json'
    request = urllib2.Request(url)
    request.add_header('Authorization', auth)
    request.add_header('User-Agent', user_agent)
    request_opener = urllib2.build_opener()
    response = request_opener.open(request)
    response_data = response.read()
    json_result = json.loads(response_data)
    result_list = json_result['d']['results']

    # Write results to list
    urls = []
    for res in result_list:
        try:
            urls.append(res['MediaUrl'])
        except TypeError:
            print 'coudlnt make urls'
            pass

    return urls
