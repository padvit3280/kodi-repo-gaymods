# -*- coding: utf-8 -*-
import json, urllib
try:
    import http.client as httpclient
except:
    import httplib as httpclient
try:
    quote = urllib.quote
except:
    from urllib import parse
    quote = urllib.parse.quote

def bingSearch(searchterms, options={}):
    bing_api_key = 'a2bbbe20b19543b9ab6dee3bac81d3da' # read_bing_key()
    host = "api.cognitive.microsoft.com"
    path = "/bing/v7.0/videos/search?"
    headers = {'Ocp-Apim-Subscription-Key': bing_api_key}
    headers.update(options)
    conn = httpclient.HTTPSConnection(host)
    query = quote(searchterms)
    for k,v in options.items():
        path += "{0}={1}&".format(k,quote(v))
    conn.request("GET", path + "safeSearch=Off&q=" + query, headers=headers)
    response = conn.getresponse()
    # headers = [k + ": " + v for (k, v) in response.getheaders()
    #           if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
    result = response.read() #.decode('latin', errors='ignore') #.encode("utf-8")
    print(result)
    json_response = json.loads(result)
    results = []
    dur = None
    th = 'DefaultVideo.png'
    resultsraw = json_response.get('value', [])
    for v in resultsraw:
        urlname = ''
        lbl = ''
        lbl2 = ''
        vpath = ''
        try:
            dur = str(v.get('duration', None))
            if dur is not None:
                dur = dur.replace('PT', '')[0:-1]
                dur = dur.replace('M', ':')
                dur = dur.replace('H', ':')
                dur = " [COLOR yellow]({0})[/COLOR]".format(dur)
            else:
                dur = ""
            urlname = v.get('contentUrl', v.get('hostPageDisplayUrl', '').rpartition('/')[-1].replace('_', ' ').replace('-', ' '))
            lbl = "{0}{1}".format(v.get('name', ''), dur)
            lbl2 = urlname + u'\n' + v.get('description', '')
            vpath = 'plugin://plugin.video.hubgay/playmovie/{0}'.format(quote(v.get('contentUrl', ''), safe=':'))
            th = v.get('thumbnailUrl', 'DefaultVideo.png')
        except Exception as ex:
            print (str(ex)+"\n"+str(repr(v)))
        li = {'label': lbl, 'label2': lbl2, 'thumbnail': th, 'icon': th, 'path': vpath}
        results.append(li)
    return results

