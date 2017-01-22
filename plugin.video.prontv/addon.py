# -*- coding: utf-8 -*-
import json, urlparse, os.path as path
from resources.jsonpron import Result, PronApi, Metatags, Hosterurls,  Filedata
from urllib import urlencode, quote_plus, quote, unquote_plus, unquote
from xbmcswift2 import Plugin, xbmc, xbmcaddon, ListItem, download_page as DL
from base64 import decodestring


APIKEY = "be4548a385c354cc02ca6135ae57b65f"
COUNT = 20
urlsearch = "http://pron.tv/api/search/stream/?apikey={0}&count={1}&from=0&getmeta=1&query=".format(APIKEY, COUNT)
urlimages = "http://pron.tv/api/thumbnail/{0}?apikey=" + APIKEY
plugin = Plugin()
__addondir__ = xbmc.translatePath(plugin.addon.getAddonInfo('path'))
__resdir__ = path.join(__addondir__, 'resources')
__imgsearch__ = path.join(__resdir__, 'search.png')
__imgnext__ = __imgsearch__.replace('search.png', 'next.png')

def searchstreams(query='staxus', offset=0):
    vids = []
    img = 'DefaultVideo.png'
    apiurl = urlsearch.replace("from=0", "from={0}".format(offset)) + quote_plus(query)
    results = DL(apiurl).decode("utf-8")
    res = json.loads(results)
    pornresults = PronApi(**res)
    #plugin.log.info("***{0} JSON {1}".format(apiurl, str(repr(pornresults))))
    #plugin.log.info(json.dumps(res, sort_keys=True, indent=1))
    if isinstance(res, dict) and res.get('result'):
        items = res.get('result')
        for item in items:
            mov = Result()
            hoster = Hosterurls()
            filedata = Filedata()
            meta = Metatags(**item.get('metatags'))
            hoster = Hosterurls(**item.get('hosterurls')[0])
            filedata = Filedata(**item.get('hosterurls')[0].get('filedata'))
            filedatalist = []
            for fdata in item.get('hosterurls')[0].get('filedata').get('filedata'):
                filedataitem = Filedata(**fdata)
                if filedataitem.name == 'pic':
                    img = filedataitem.value
                filedatalist.append(filedataitem)
            filedata.filedata = filedatalist
            hoster.filedata = filedata
            mov = Result(**item)
            #plugin.log.info("!! Before assign others " + str(mov))
            mov.hosterurls = hoster
            mov.metatags = meta
            #plugin.log.info("--Assigned lower objects {0}\nImage found {1}".format(str(mov), img))

            datemod = mov.modified
            title = mov.title
            filename = mov.sourcetitle
            url = unquote(mov.hosterurls.url)
            imgid = mov.imageid
            lbl = "[COLOR white]" + filename + "[/COLOR]\n" + title
            playpath = plugin.url_for(endpoint=play, url=url)
            litem = ListItem(label=lbl, label2=filename, icon=img, thumbnail=img, path=playpath)
            litem.set_info(type='video', info_labels={'Date': datemod, 'Title': title, 'Plot': mov.sourcetitle})
            litem.set_property('genre', str(repr(mov.hosterurls)))
            litem.set_property('date', datemod)
            litem.is_folder = False
            litem.playable = True
            litem.set_info(type='video', info_labels={'Title': title})
            vids.append(litem)
    vids.sort(key=lambda item : item.label)
    sitem = ListItem(label="[COLOR green]Search Pron.TV[/COLOR]", icon=__imgsearch__, thumbnail=__imgsearch__, path=plugin.url_for(endpoint=search))
    nitem = ListItem(label="[COLOR green]-> Next Results ->[/COLOR]", icon=__imgnext__, thumbnail=__imgnext__, path=plugin.url_for(endpoint=nextpage, query=query, offset=str(int(offset)+COUNT)))
    vids.insert(0, sitem)
    vids.insert(1, nitem)
    return vids

def get_thumb(imageid):
    filepath = ''
    url = urlimages.format(imageid)
    datapath = path.abspath(xbmc.translatePath('special://profile/addon_data/plugin.video.prontv/'))
    imagename = "{0}.png".format(imageid)
    imagefile = path.join(datapath, imagename)
    #plugin.log.info ("**GET THUMB: PluginID={0} Path={1} Imagefilename={2}".format(plugin.id, datapath, imagefile))
    if path.exists(imagefile) and path.isfile(imagefile):
        return imagefile
    else:
        try:
            results = DL(url).decode("utf-8")
            res = json.loads(results)
            plugin.log.debug(res)
            #res = res.get('result')
            imagedata = res.get('result').get("thumbnail_base64").decode('base64')
            #print("**IMAGE DATA**\n"+imagedata)
            #plugin.log.debug("**IMAGE DATA**\n"+imagedata)
            fh = open(imagefile, "wb")
            fh.write(decodestring(imagedata))
            fh.close()
            return imagefile
        except:
            return 'DefaultVideo.png'


@plugin.route('/')
def index():
    return searchstreams()


@plugin.route('/nextpage/<query>/<offset>')
def nextpage(query, offset):
    litems = []
    litems = searchstreams(query=query, offset=offset)
    img = 'DefaultVideo.png'
    return litems


@plugin.route('/search')
def search():
    searchterm = ''
    kb = plugin.keyboard(default=None, heading="Search pron.tv")
    if kb is not None:
        searchterm = quote_plus(kb)
        items = searchstreams(query=searchterm)
        return items
    else:
        return []


@plugin.route('/play/<url>')
def play(url):
    url = unquote_plus(url)
    try:
        import urlresolver
        HMF = urlresolver.HostedMediaFile
    except:
        HMF = None
    try:
        resolved = HMF(url).resolve()
        vitem = ListItem(label=url, path=resolved)
        vitem.is_folder = False
        vitem.set_is_playable = True
        vitem.set_info(type='video', info_labels={'Title': url})
        vitem.add_stream_info(stream_type='video', stream_values={})
        plugin.set_resolved_url(resolved)
        return plugin.play_video(vitem)
    except:
        vitem = {'path': url, 'is_playable': True}
    #return plugin.set_resolved_url(vitem)


if __name__ == '__main__':
    plugin.run()
