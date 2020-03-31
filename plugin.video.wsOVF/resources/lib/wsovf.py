from . import urlquick
import os.path as Path
import re, sys
try:
    import simpleplugin
except:
    simpleplugin = None

class wsOVF:

    def __init__(self, cookiepath=None):
        self.plug = None
        self.BASEURL = "https://www1.swatchseries.to"
        self.HOST = self.BASEURL.split('//', 1)[-1]
        self.URL_latest = "/lastest"
        self.URL_category = "/serie/{0}"
        self.PATH = Path.realpath(Path.curdir)
        if cookiepath is not None:
            self.COOKIES = cookiepath
        else:
            self.COOKIES = Path.join(self.PATH, 'cookies.dat')
        self.getWeb = urlquick.get

    def getsource(self, url):
        resp = self.getWeb(url)
        rawhtml = resp.content
        html = rawhtml.decode('utf8')
        return html.split('<body', 1)[-1]

    def setup(self, path='.', plugin=None):
        self.PATH = Path.realpath(path)
        self.COOKIES = Path.join(self.PATH, 'cookies.dat')
        self.getWeb = urlquick.get
        try:
            import simpleplugin
            assert isinstance(self.plug, simpleplugin.Plugin)
        except:
            self.plug = simpleplugin.Plugin('plugin.video.wsOVF')
            assert isinstance(self.plug, simpleplugin.Plugin)

    def get_sources(self, url_episode=""):
        litems = []
        catitem = None
        src = self.getsource(url_episode)
        html = src.split('class="filmicerik linkcontent"', 1)[-1]
        shtml = html.split('</div>', 1)[0]
        reSources = re.compile('href="(.+?)"')
        matches = reSources.findall(shtml)
        count = 1
        if matches is not None and len(matches) > 0:
            for vidurl in matches:
                uparts = vidurl.partition('//')[-1].split('/', 1)
                hoster = uparts[0]
                vkey = uparts[-1].replace('/', ' ').replace('.html', '').replace('.htm', '').strip()
                sourcename = "#{0}: {1} ({2})".format(str(count), hoster, vkey)
                item = {'name': sourcename, 'video': vidurl, 'hoster': hoster, 'videoid': vkey}
                litems.append(item)
                count += 1
        if catitem is not None:
            litems.append(catitem)
        return litems

    def get_catepisodes(self, category=""):
        url = self.BASEURL + self.URL_category.format(category.replace(' ', '_'))
        litems = []
        src = self.getsource(url)
        html = src.split('class="wt-cat"', 1)[-1]
        matches = re.compile('href="(.+?)">(.+?)</a>').findall(html)
        if matches is not None and len(matches) > 0:
            for eplink, epname in matches:
                item = {'name': epname, 'video': eplink}
                litems.append(item)
        return litems

    def get_url(self, **kwargs):
        if self.plug is not None:
            return self.plug.get_url(**kwargs)
        else:
            plugurl = 'plugin://plugin.video.wsOVF/?'
            return plugurl + urlquick.urlencode(kwargs)

    def latest(self):
        litems = []
        url = self.BASEURL + self.URL_latest
        src = self.getsource(url)
        html = src.split('class="wt-cat"', 1)[-1]
        matches = re.compile('href="(.+?)">(.+?)</a>').findall(html)
        if matches is not None and len(matches) > 0:
            for eplink, epname in matches:
                item = {'name': epname, 'video': eplink}
                litems.append(item)
        return litems

    def get_latest(self):
        litems = []
        url = self.BASEURL + self.URL_latest
        src = self.getsource(url)
        html = src.split('class="lcp_catlist" id="lcp_instance_0">', 1)[-1]
        reLatest = re.compile('<li.+?<a href="({0}/.+?)" title="(.+?)".+?</li>'.format(self.BASEURL))
        matches = reLatest.findall(html)
        if matches is not None and len(matches) > 0:
            maxlen = 100
            if len(matches) < 100:
                maxlen = len(matches)
            for showlink, showname in matches[:maxlen]:
                item = {'name': showname, 'url': showlink, 'video': showlink}
                litems.append(item)
        return litems

    def get_searchresults(self, query=''):
        litems = []
        item = {}
        showthumb = 'DefaultVideo.png'
        url = self.BASEURL + self.URL_category.format(query.replace(' ', '_'))
        litems = self.dosearch(url)
        return litems

    def dosearch(self, url):
        litems = []
        try:
            src = self.getsource(url)
        except:
            src = urlquick.get(url).content
        html = src.split('="filmcontent"', 1)[-1]
        html = html.rpartition("<span class='pages'")[0]
        reEpisode = re.compile(
            'href="(https://www1.swatchseries.to/.+?)">.+?<img src="(.+?)" alt="(.+?)"')  # , re.DOTALL)
        matches = reEpisode.findall(html)
        for showlink, showThumb, showname in matches:
            item = {'name': showname, 'video': showlink, 'thumb': showThumb}
            litems.append(item)
        return litems
