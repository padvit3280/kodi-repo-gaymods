# -*- coding: utf-8 -*-
import json, urlparse, urllib, os.path as path
from resources.jsonpron import Result, PronApi, Metatags, Hosterurls,  Filedata
from urllib import urlencode, quote_plus, quote, unquote_plus, unquote
from xbmcswift2 import Plugin, xbmc, xbmcaddon, ListItem, download_page
from base64 import decodestring
HTML = None
try:
    from HTMLParser import HTMLParser
    HTML = HTMLParser()
except:
    HTML = None

APIKEY = "be4548a385c354cc02ca6135ae57b65f"
COUNT = 50
VIEWMODE = 500
urlsearch = "http://pron.tv/api/search/stream/?apikey={0}&count={1}&from=0&getmeta=1&query=".format(APIKEY, COUNT)
urlimages = "http://pron.tv/api/thumbnail/{0}?apikey=" + APIKEY
plugin = Plugin()
__addondir__ = xbmc.translatePath(plugin.addon.getAddonInfo('path'))
__resdir__ = path.join(__addondir__, 'resources')
__imgsearch__ = path.join(__resdir__, 'search.png')
__imgnext__ = __imgsearch__.replace('search.png', 'next.png')

def DL(url):
    return urllib.urlopen(url).read().decode('utf-8')

def searchstreams(query='gay', offset=0):
    vids = []
    img = 'DefaultVideo.png'
    fhosts = plugin.get_setting(key='filterhosts')
    fwords = plugin.get_setting(key='filterwords')
    fnames = plugin.get_setting(key='filternames')
    newlinks = plugin.get_setting(key='newlinkson', converter=bool)
    addqs = ""
    if len(fnames) > 0:
        addqs += "name:{0} ".format(fnames)
    if len(fhosts) > 0:
        addqs += "host:{0} ".format(fhosts)
    if len(fwords) > 0:
        addqs += fwords + " "
    if newlinks:
        addqs += "#newlinks "
    apiurl = urlsearch.replace("from=0", "from={0}".format(offset))
    apiurl += quote_plus(query + " " + addqs.strip())
    results = DL(apiurl)
    res = json.loads(results, encoding='utf-8')
    pornresults = PronApi(**res)
    if isinstance(res, dict) and res.get('result'):
        items = res.get('result')
        for item in items:
            mov = Result()
            hoster = Hosterurls()
            filedata = Filedata()
            if item.get('metatags'):
                meta = Metatags(**item.get('metatags'))
            if item.get('hosterurls'):
                hoster = Hosterurls(**item.get('hosterurls')[0])
            if item.get('hosterurls')[0].get('filedata'):
                filedata = Filedata(**item.get('hosterurls')[0].get('filedata'))
                filedatalist = []
                img = ''
                for fdata in item.get('hosterurls')[0].get('filedata').get('filedata'):
                    filedataitem = Filedata(**fdata)
                    if filedataitem.name == 'pic':
                        img = filedataitem.value
                    filedatalist.append(filedataitem)
                filedata.filedata = filedatalist
                hoster.filedata = filedata
            mov = Result(**item)
            mov.hosterurls = hoster
            mov.metatags = meta

            datemod = mov.modified
            title = unquote(HTML.unescape(mov.title))
            filename = mov.sourcetitle
            if filename:
                filename = unquote(filename)
            else:
                filename = ""
            url = mov.hosterurls.url
            hostname = mov.hosterurls.filedata.hosterurl
            lbl = "[COLOR white]" + filename + "[/COLOR]\n" + title
            if len(hostname) > 0 and len(fhosts) < 2:
                hostparts = urlparse.urlparse(hostname)
                hostname = hostparts.hostname.replace("www.","")
                if len(filename) > 20:
                    filename = filename[:20].strip() + ".."
                lbl = "[COLOR white]" + filename + "[/COLOR] ([COLOR yellow]" + hostname + ")[/COLOR]\n" + title
            imgid = mov.imageid
            #if len(img) < 1 and len(imgid) > 0:
            #    img = get_thumb(imgid)
            playpath = plugin.url_for(endpoint=play, url=url)
            litem = ListItem(label=lbl, label2=filename, icon=img, thumbnail=img, path=playpath)
            litem.set_info(type='video', info_labels={'Date': datemod, 'Title': title, 'Plot': mov.sourcetitle, 'Genre': hostname})
            litem.set_property('genre', str(repr(mov.hosterurls)))
            litem.set_property('date', datemod)
            litem.set_property('genre', hostname)
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
    datapath = xbmc.translatePath('special://profile/addon_data/plugin.video.prontv/')
    imagename = "{0}.png".format(imageid)
    imagefile = path.join(datapath, imagename)
    print "**GET THUMB: ImgID={0} Path={1} Imagefilename={2}".format(plugin.id, datapath, imagefile)
    if path.exists(imagefile) and path.isfile(imagefile):
        return imagefile
    else:
        try:
            results = DL(url).decode("utf-8")
            res = json.loads(results)
            plugin.log.debug(res)
            imagedata = res.get('result').get("thumbnail_base64").decode('base64')
            plugin.log.info("**IMAGE DATA**\n"+results + "\n*** LEN=" + str(len(imagedata)))
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
    searchterm = unquote_plus(plugin.get_setting(key='lastsearch'))
    kb = plugin.keyboard(default=searchterm, heading="Search Pron.TV")
    if kb is not None:
        searchterm = quote_plus(kb)
        plugin.set_setting(key='lastsearch', val=searchterm)
        items = searchstreams(query=searchterm)
        return items
    else:
        return []


@plugin.route('/play/<url>')
def play(url):
    url = url.decode('utf-8','ignore')
    resolved = u''
    try:
        import urlresolver
        resolved = urlresolver.HostedMediaFile(url).resolve()
        vitem = ListItem(label=url, path=resolved)
        vitem.is_folder = False
        vitem.set_is_playable = True
        vitem.set_info(type='video', info_labels={'Title': url})
        vitem.add_stream_info(stream_type='video', stream_values={})
        plugin.set_resolved_url(resolved)
        return plugin.play_video(vitem)
    except:
        plugin.notify(msg="Failed to resolve {0} to a playable video.".format(url))
    try:
        if resolved is None or len(resolved) < 5:
            import YoutubeDLWrapper
            ytdl = YoutubeDLWrapper._getYTDL()
            ytdl.clearDownloadParams()
            resolved = ytdl.extract_info(url, download=False)
            vitem = ListItem(label=url, path=resolved)
            vitem.is_folder = False
            vitem.set_is_playable = True
            vitem.set_info(type='video', info_labels={'Title': url})
            vitem.add_stream_info(stream_type='video', stream_values={})
            plugin.set_resolved_url(resolved)
            return plugin.play_video(vitem)
    except:
        plugin.notify(msg="Failed to resolve {0} to a playable video.".format(url))
    return None

if __name__ == '__main__':
    plugin.run()
    mode = int(plugin.get_setting(key='viewmode'))
    if mode is not None and mode >= 0:
        VIEWMODE = mode
    plugin.set_view_mode(view_mode_id=VIEWMODE)
    plugin.set_content('movies')
