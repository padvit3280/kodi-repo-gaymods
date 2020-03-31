import re, sys, os
import os.path as Path
from collections import namedtuple
import urlquick

class MyVidster:
    list_sorts = ['new','popular', 'recent']
    list_orientations = ['gay', 'straight', 'all']
    list_searchs = ['myvidster', 'user', 'web', 'profiles', 'groups']
    SortBy = namedtuple('SortBy', list_sorts, rename=True)(*list_sorts)
    Orientation = namedtuple("Orient", list_orientations, rename=True)(*list_orientations)
    SearchOf = namedtuple("Search", list_searchs, rename=True)(*list_searchs)

    def __init__(self, path_addon='.'):
        self.PATH = self.path_setup(path=path_addon)
        urlquick.CACHE_LOCATION = Path.join(self.PATH, 'cache')
        if not Path.isdir(urlquick.CACHE_LOCATION):
            os.makedirs(urlquick.CACHE_LOCATION)
        self.BASEURL = "http://myvidster.com"
        self.HOST = self.BASEURL.split('//', 1)[-1]

        self.URL_SHUFFLE = '/video_shuffle/{0}/{1}'
        self.URL_LISTS = "/?list={0}&filter_by={1}"
        self.URL_SEARCH = "/search/?q={0}&filter_by={1}"
        self.URL_CHANNEL = "/processor.php?action=display_channel&channel_id={0}&page={1}&thumb_num=250"
        self.URL_GETVID = "/user/api.php?action=fetch&email=alljer@gmail.com&password=46c53b8a852c4ee94f458dc99786e23ebd666bd1&video_id={0}"
        self.FETCHVID = "http://www.myvidster.com/user/api.php?action=fetch&email=alljer@gmail.com&password=46c53b8a852c4ee94f458dc99786e23ebd666bd1&video_id="

        self.HOME = self.BASEURL + self.URL_LISTS.format(self.SortBy.new, self.Orientation.gay)
        self.SHUFFLE = self.BASEURL + self.URL_SHUFFLE.format(self.SortBy.popular, self.Orientation.gay)
        self.SEARCH = self.BASEURL + self.URL_SEARCH.format("{0}", self.SearchOf.myvidster)
        self.CHANNEL = self.BASEURL + self.URL_CHANNEL


    def path_setup(self, path):
        okpath = None
        if Path.isdir(path):
            okpath = path
        else:
            okpath = Path.join(Path.realpath(Path.expanduser("~")), ".kodi")
            if not Path.isdir(okpath):
                os.makedirs(okpath)
            okpath = Path.join(okpath, "temp")
            if not Path.isdir(okpath):
                os.makedirs(okpath)
        return okpath


    def get_channel(self, channel=1533786, page=1):
        litems = []
        url = self.CHANNEL.format(channel, page)
        resp = urlquick.get(url)
        src = resp.content
        htmlitems = src.split("<li")[1:]
        for viditem in htmlitems:
            vidid = ""
            vidname = ""
            desc = ""
            urlpart = viditem.split('href="',1)[-1].split('"')[0]
            vidid = urlpart.replace("/video/","").split('/',1)[0]
            vidurl = self.BASEURL + urlpart
            respfetch = urlquick.get(self.FETCHVID + vidid)
            vidxml = respfetch.content
            thumbparts = vidxml.split("<thumbnail_url1>", 1)[-1]
            thumb = thumbparts.partition('</')[0]
            imagename = thumb.rpartition('/')[-1]
            if Path.exists(Path.join(self.PATH,imagename)):
                thumb = Path.join(self.PATH,imagename)
            nameparts = vidxml.split("<title>",1)[-1]
            vidname = nameparts.partition('</')[0]
            descparts = vidxml.split("<description>",1)[-1]
            desc = descparts.partition('</')[0]
            li = {'label': vidname, 'label2': desc, 'thumb': thumb, 'icon': thumb, 'url': vidurl, 'is_folder': False, 'info': {'video': {}}}
            litems.append(li)
        return litems


    def video_thumb(self, id, vidxml=None):
        if vidxml is None:
            respfetch = urlquick.get(self.FETCHVID + id)
            vidxml = respfetch.content
        thumbparts = vidxml.split("<thumbnail_url1>", 1)[-1]
        thumb = thumbparts.partition('</')[0]



    def vidster_images(self, id=''):
        images = []
        urlgetimg = 'https://www.myvidster.com/fetch_preview.php?action=fetch_preview&video_id='+id
        resp = urlquick.get(urlgetimg)
        images = resp.json()
        try:
            images.remove(u'')
        except:
            pass
        try:
            images.remove('')
        except:
            pass
        return images


    def resolve(self, url):
        resolved = ''
        stream_url = ''
        item = None
        try:
            import urlresolver
            resolved = urlresolver.HostedMediaFile(url).resolve()
            if not resolved or resolved == False or len(resolved) < 1:
                resolved = urlresolver.resolve(url)
                if resolved is None or len(resolved) < 1:
                    resolved = urlresolver.resolve(urlquick.unquote(url))
            if len(resolved) > 1:
                return resolved
        except:
            resolved = ''
        try:
            import YDStreamExtractor
            info = YDStreamExtractor.getVideoInfo(url, resolve_redirects=True)
            resolved = info.streamURL()
            for s in info.streams():
                try:
                    stream_url = s['xbmc_url'].encode('utf-8', 'ignore')
                except:
                    pass
            if len(stream_url) > 1:
                resolved = stream_url
            if len(resolved) > 1:
                return resolved
        except:
            resolved = None
        return resolved