import os.path as path
import json
import re
import urllib
import urllib2
import ssl
from kodiswift import Plugin, xbmc, ListItem, download_page, clean_dict, SortMethod
#from xbmcswift2 import Plugin, xbmc, ListItem, download_page, clean_dict, SortMethod

ssl._create_default_https_context = ssl._create_unverified_context
plugin = Plugin()
__addondir__ = xbmc.translatePath(plugin.addon.getAddonInfo('path'))
__resdir__ = path.join(__addondir__, 'resources')
__imgsearch__ = path.join(__resdir__, 'search.png')
__savedjson__ = path.join(xbmc.translatePath(plugin.addon.getAddonInfo('profile')), 'savedshows.json')
__BASEURL__ = 'http://watchseries-online.nl'


@plugin.route('/')
def index():
    itemsearch = {'label': 'Search', 'path': plugin.url_for(search), 'icon': __imgsearch__,
                  'thumbnail': __imgsearch__}
    itemlatest = {'label': 'Latest Episodes',
        'icon': 'DefaultFolder.png',
        'path': plugin.url_for(latest)}
    itemsaved = {'label': 'Saved Shows', 'path': plugin.url_for(saved), 'icon': 'DefaultFolder.png', 'thumbnail': 'DefaultFolder.png'}
    itemplay = {'label': 'Play URL (Only URLresolver: vodlocker/openload/thevideo...)', 'path': plugin.url_for(playurl), 'icon': 'DefaultFolder.png', 'thumbnail': 'DefaultFolder.png'}
    litems = []
    litems.append(itemlatest)
    litems.append(itemsearch)
    litems.append(itemsaved)
    litems.append(itemplay)
    plugin.set_content('movies')
    return litems


def loadsaved():
    sitems = []
    litems = []
    items = []
    jsonin = plugin.addon.getSetting('savedshows') # file(__savedjson__, mode='r').read()
    if len(jsonin) < 1:
        items = []
        plugin.addon.setSetting('savedshows', json.dumps(items))
    else:
        items = json.loads(jsonin)
    return items


def makecatitem(name, link, removelink=False):
    item = {}
    ctxitem = {}
    itempath = plugin.url_for(category, name=name, url=link)
    item = {'label': name, 'label2': link, 'icon': 'DefaultFolder.png', 'thumbnail': 'DefaultFolder.png', 'path': itempath}
    item.setdefault(item.keys()[0])
    litem = ListItem(label=name, label2=link, icon='DefaultFolder.png', thumbnail='DefaultFolder.png', path=itempath)
    if removelink:
        litem.add_context_menu_items([('Remove Saved Show', 'RunPlugin("{0}")'.format(plugin.url_for(removeshow, name=name, link=link)),)])
    else:
        litem.add_context_menu_items([('Save Show', 'RunPlugin("{0}")'.format(plugin.url_for(saveshow, name=name, link=link)),)])
    return litem


@plugin.route('/playurl')
def playurl():
    url = ''
    url = plugin.keyboard(default='', heading='Video Page URL')
    if url != '' and len(url) > 0:
        play(url)
    else:
        return index()


@plugin.route('/saved')
def saved():
    litems = []
    sitems = []
    sitems = loadsaved()
    noitem = {'label': "No Saved Shows", 'icon': 'DefaultFolder.png', 'path': plugin.url_for('index')}
    if len(sitems) < 1:
        return [noitem]
    else:
        return sitems


@plugin.route('/saveshow/<name>/<link>')
def saveshow(name='', link=''):
    sitems = []
    litems = []
    try:
        sitems = loadsaved()
        item = makecatitem(name, link, True)
        if len(sitems) > 1:
            sitems.append(item)
        else:
            sitems = [item]
        jsout = json.dumps(sitems)
        plugin.addon.setSetting('savedshows', jsout)
        plugin.notify(msg='#{0}: {1} Saved link: {2}'.format(str(len(sitems)), name, link), title='Saved {0}'.format(name))
    except:
        plugin.notify(msg='Error saving {0}'.format(link), title='Save failed {0}'.format(name))
    return None


@plugin.route('/removeshow/<name>/<link>')
def removeshow(name='', link=''):
    sitems = []
    litems = []
    sitems = loadsaved()
    for item in sitems:
        if item.get('name') == name or item.get('link') == link:
            plugin.notify(title='Removed {0}'.format(name), msg='Removed "{0}": {1}'.format(name, link))
        else:
            litems.append(item)
    jsout = json.dumps(litems)
    plugin.addon.setSetting('savedshows', jsout)
    plugin.notify(title='Removed {0}'.format(name), msg='{0} Removed Show link: {1}'.format(name, link))


@plugin.route('/latest')
def latest():
    url = __BASEURL__ + '/last-350-episodes'
    headers = {}
    headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'})
    headers.update({'Accept': 'application/json,text/x-json,text/x-javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8;charset=utf-8'})
    headers.update({'Accept-Language': 'en-US,en;q=0.5'})
    req = urllib2.Request(url=url, data=None, headers=headers)
    html = str(urllib2.urlopen(req).read())
    matches = re.compile(ur'href="(http...watchseries-online.[a-z][a-z].episode.+?[^"])".+?</span>(.+?[^<])</a>', re.DOTALL + re.S + re.U).findall(html)
    litems = []
    for eplink, epname in matches:
        epname = epname.replace('&#8211;', '-')
        spath = plugin.url_for(episode, name=epname, url=eplink)
        item = {'label' : epname, 'icon':'DefaultVideoFolder.png', 'path':spath}
        item.setdefault(item.keys()[0])
        litems.append(item)
    return litems


@plugin.route('/search')
def search():
    searchtxt = ''
    searchtxt = plugin.get_setting('lastsearch')
    searchtxt = plugin.keyboard(searchtxt, 'Search All Sites', False)
    searchquery = searchtxt.replace(' ', '+')
    plugin.set_setting(key='lastsearch', val=searchtxt)
    urlsearch = __BASEURL__ + '/?s={0}&search='.format(searchquery)
    headers = {}
    headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'})
    headers.update({'Accept': 'application/json,text/x-json,text/x-javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8;charset=utf-8'})
    headers.update({'Accept-Language': 'en-US,en;q=0.5'})
    req = urllib2.Request(url=urlsearch, data=None, headers=headers)
    html = unicode(urllib2.urlopen(req).read())
    htmlres = unicode(html.partition('<div class="ddmcc">')[2]).split('</div>',1)[0]
    matches = re.compile(ur'href="(http...watchseries-online.[a-z][a-z].category.+?[^"])".+?[^>]>(.+?[^<])<.a>', re.DOTALL + re.S + re.U).findall(unicode(htmlres))
    litems = []
    for slink, sname in matches:
        litems.append(makecatitem(sname, slink))
    return litems


@plugin.route('/category/<name>/<url>')
def category(name, url):
    headers = {}
    headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'})
    headers.update({'Accept': 'application/json,text/x-json,text/x-javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8;charset=utf-8'})
    headers.update({'Accept-Language': 'en-US,en;q=0.5'})
    req = urllib2.Request(url=url, data=None, headers=headers)
    html = str(urllib2.urlopen(req).read())
    banner = None
    try:
        banner = str(html.split('id="banner_single"', 1)[0].rpartition('src="')[2].split('"',1)[0])
        if banner.startswith('/'): banner = __BASEURL__ + banner
    except:
        pass
    if banner is None: banner = 'DefaultVideoFolder.png'
    matches = re.compile(ur"href='(http...watchseries-online.[a-z][a-z].episode.+?[^'])'.+?</span>(.+?[^<])</a>", re.DOTALL + re.S + re.U).findall(html)
    litems =[]
    for eplink, epname in matches:
        epname = epname.replace('&#8211;', '-')
        epath = plugin.url_for(episode, name=epname, url=eplink)
        item = {'label' : epname, 'icon' : banner, 'thumbnail' : banner, 'path' : epath}
        item.setdefault(item.keys()[0])
        litems.append(item)
    litems.sort(key=lambda litems : litems['label'])
    return litems


def findvidlinks(html=''):
    matches = re.compile(ur'<div class="play-btn">.*?</div>', re.DOTALL).findall(html)
    vids = []
    for link in matches:
        url = re.compile(ur'href="(.+)">', re.DOTALL+re.S).findall(str(link))[0]
        if url is not None:
            host = str(url.lower().split('://', 1)[-1])
            host = host.replace('www.', '')
            host = str(host.split('.', 1)[0]).title()
            label = "{0} [COLOR green]({1})[/COLOR]".format(host, url.rpartition('/')[-1])
            vids.append((label, url,))
    return vids


@plugin.route('/episode/<name>/<url>')
def episode(name, url):
    headers = {}
    headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'})
    headers.update({'Accept': 'application/json,text/x-json,text/x-javascript,text/javascript,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8;charset=utf-8'})
    headers.update({'Accept-Language': 'en-US,en;q=0.5'})
    req = urllib2.Request(url=url, data=None, headers=headers)
    html = str(urllib2.urlopen(req).read())
    litems = []
    linklist = findvidlinks(html)
    if len(linklist) > 0:
        for name, link in linklist:
            itempath = plugin.url_for(play, url=link)
            item = ListItem(label=name, label2=link, icon='DefaultFolder.png', thumbnail='DefaultFolder.png', path=itempath)
            #item.set_info(type='video', info_labels={'Title': name})
            #item.set_is_playable(True)
            litems.append(item)
        litems.sort(key=lambda litems: litems.label, reverse=True)
    else:
        plugin.notify(msg="Failed to find vid links", title="Len {0}".format(str(len(linklist))))
    return litems


@plugin.route('/play/<url>')
def play(url):
    plugin.set_view_mode(0)
    plugurl = 'plugin://plugin.video.hubgay/playmovie/{0}'.format(urllib.quote_plus(url))
    plugin.play_video(plugurl)
    return plugin.end_of_directory()
    #xbmc.executebuiltin('RunPlugin(plugin://plugin.video.hubgay/playmovie/%s)' % urllib.quote_plus(url))
    #return [plugin.set_resolved_url(url)]


if __name__ == '__main__':
    plugin.run()
    plugin.set_content('movies')
    plugin.set_view_mode(0)

