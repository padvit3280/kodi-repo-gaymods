# -*- coding: utf-8 -*-
# Module: main
# Author: moedje
# Github: https://github.com/moedje/
# Updated on: June 23, 2019
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
import ssl, re, datetime, time
import sys, os
from resources import lib as Lib

path = os.path
handle = int(sys.argv[1])
ssl._create_default_https_context = ssl._create_unverified_context
urlresolver = None
try:
    import xbmc, xbmcplugin
except:
    import Kodistubs.xbmc as xbmc
    import Kodistubs.xbmcplugin as xbmcplugin
quote = Lib.urlquick.quote
unquote = Lib.urlquick.unquote
def quote_plus(text): return quote(text.replace(' ', '+'))
plugin = Lib.simpleplugin.Plugin()

__datadir__ = xbmc.translatePath('special://profile/addon_data/{0}/'.format(plugin.id))
__cookie__ = path.join(__datadir__, 'cookies.lwp')
__next__ = path.join(xbmc.translatePath('special://home/addons/{0}/resources/'.format(plugin.id)), 'next.png')
Tv = Lib.wsovf.wsOVF(cookiepath=__cookie__)
Tv.search.ICONSEARCH = __next__.replace('next', 'search')
Tv.search.AddonSearchPaths = plugin.path, plugin.get_url(action='show_searchbox'), plugin.get_url(action='show_search', query='-QUERY-')

@plugin.action()
@plugin.mem_cached(30)
def root():
    imgWs = __next__.replace('next', 'watchseries')
    lblTpl = '[COLOR green]{0}[/COLOR] ([COLOR white][I]{1}[/I][/COLOR])\n[COLOR yellow]{2}[/COLOR]'
    lblWs = lblTpl.format("Watch Series", "Newest", "")
    lblWsAll = lblTpl.format("Watch Series", "Full List", "")
    rootmenu = {
        "Home": [
            {'label': lblWs, 'url': plugin.get_url(action='home_ws'), 'thumb': imgWs,
             'is_folder': True, 'is_playable': False},
            {'label': lblWsAll, 'url': plugin.get_url(action='latest_ws', page=1), 'thumb': imgWs,
             'is_folder': True, 'is_playable': False},
            {'label': 'Search History (Broken)', 'url': plugin.get_url(action='show_searchfolder'), 'thumb': Tv.search.ICONSEARCH,
             'is_playable': False},
            {'label': 'Search', 'url': plugin.get_url(action='show_searchbox', site='ws'), 'thumb': __next__.replace('next', 'search'),
             'is_folder': True, 'is_playable': False}
        ]
    }
    return rootmenu["Home"]


@plugin.action()
@plugin.mem_cached(2)
def home_ws():
    items = []
    xitems = []
    urlrss = 'https://www1.swatchseries.to/rss/newest-episodes' #'https://watchseries.ovh/rss/newest-episodes'
    resp = Lib.urlquick.get(urlrss)
    for item in resp.xml().iter('item'):
        xitems.append(item)
    for item in xitems:
        litem = {'is_folder': True, 'is_playable': False}
        for kid in item.getchildren():
            if kid.tag == 'link':
                litem.update({'url': plugin.get_url(action='sources_ws', vurl=kid.text)}) #{'url': plugin.get_url(action=sources_ws, url=kid.text)})
            elif kid.tag == 'title':
                name = kid.text.encode('latin', 'ignore')
                epname, epdetails = name.split(',',1)
                litem.update({'label': "[COLOR white][B]{0}[/B][/COLOR] [I]{1}[/I]".format(epname.strip(), epdetails.strip())})
            elif kid.tag == 'description':
                img = kid.text.rpartition('src="')[-1].split('"')[0]
                lbl2 = kid.text.rpartition('/>')[-1].strip()
                litem.update({'thumb': img, 'icon': img, 'label2': lbl2})
        items.append(litem)
    return items


@plugin.action()
def latest_ws(params):
    items = []
    page = 1
    if params.page is not None:
        page = params.page
    url_base = 'https://www1.swatchseries.to/latest/' #'https://watchseries.ovh/latest/'
    nextpagenum = int(page) + 1
    nextpagename = str(nextpagenum)
    startoffset = ((int(page) - 1) * 10) + 1
    endoffset = startoffset + 10
    nextlbl = 'Next ({0} to {1}) -> {2}'.format(str(endoffset), str(endoffset+10), nextpagename)
    nextitem = {'label': nextlbl, 'url': plugin.get_url(action='latest_ws', page=nextpagenum), 'thumb': __next__,
             'icon': __next__, 'is_folder': True, 'is_playable': False}
    for p in range(startoffset, endoffset):
        url = url_base + str(p)
        items.extend(get_episodelists(url))
    items.append(nextitem)
    return items


def get_episodelists(url):
    epname = ""
    epseason = ""
    resp = Lib.urlquick.get(url)
    src = resp.content
    html = src.rpartition('<ul class="listings">')[-1].split('<ul class="pagination">')[0]
    litems = []
    results = re.compile('<li.+?href="(.+?)" title="(.+?)".+?epnum">(.+?)</span>').findall(html)
    for link,title,date in results:
        sepchar = '-'
        if title.find('-') == -1:
            sepchar = ','
        epname, epseason = title.split(sepchar,1)
        lbl = "{0} {1} {2}".format(epname.strip(), epseason.strip(), date)
        item = {'label': title, 'label2': date,'is_folder': True, 'is_playable': False, 'url': plugin.get_url(action='sources_ws', vurl=link)}
        litems.append(item)
    return litems


def get_seriesepisodelists(url):
    epname = ""
    epseason = ""
    resp = Lib.urlquick.get(url)
    src = resp.content
    html = src.rpartition('<ul class="listings')[-1].split('<ul class="pagination">')[0]
    litems = []
    results = re.findall(r'href="(.+?)".+?"name" >(.+?)</.+?"datepublished">(.+?)</', string=html, flags=re.MULTILINE)
    for link,title,date in results:
        try:
            char = u'&nbsp;'
            epname = title.replace(char, ' ')
            lbl = "{0} [COLOR yellow]{1}[/COLOR]".format(epname.strip(), date)
            item = {'label': epname, 'label2': date,'is_folder': True, 'is_playable': False, 'url': plugin.get_url(action='sources_ws', vurl=link)}
            litems.append(item)
        except:
            try:
                p1,p2 = title.split(' ', 1)
                epname = p1 + ' ' + p2[0]
            except:
                epname = url.rpartition('/')[-1].replace('_', ' ').title()
            lbl = "{0} [COLOR yellow]{1}[/COLOR]".format(epname.strip(), date)
            item = {'label': epname, 'label2': date,'is_folder': True, 'is_playable': False, 'url': plugin.get_url(action='sources_ws', vurl=link)}
            litems.append(item)
    return litems


@plugin.action()
def sources_ws(params):
    items = []
    vurl = "https://www1.swatchseries.to/episode/"
    epurl = ""
    if params.vurl is not None:
        epurl = params.vurl
    items = get_sourceslist(epurl)
    alphaitems = sorted(items,reverse=True)
    alphaitems.append({'label': '[COLOR red]--UNSORTED--[/COLOR]', 'url': plugin.get_url(action='root')})
    alphaitems.extend(items)
    return alphaitems


def get_sourceslist(url):
    litems = []
    name = ""
    link = ""
    img = "https://static.swatchseries.to/templates/default/images/favicons/{0}.png)"
    name = url.rpartition('/')[-1]
    epfullname = name.replace('_', ' ').split('.htm', 1)[0].title()
    showname = re.split(" S\d+ E\d+", epfullname, 1)[0]
    epnum = epfullname.replace(showname, '').strip()
    noepnum = False
    m = re.findall("S\d+ E\d+", epnum)
    if len(epnum) < 2 or len(m) < 1:
        epnum = ''
        showname = epfullname
    resp = Lib.urlquick.get(url)
    src = resp.content
    resrc = re.compile("Delete link (http.+?)'")
    matches = resrc.findall(src)
    for link in matches:
        srcname = link.split('//',1)[-1].split('/',1)[0]
        host = unicode(srcname).capitalize()
        vurl = link
        thumb = img.format(srcname)
        id = vurl.rpartition('/')[-1]
        if id.find('.') != -1:
            id = id.rpartition('.')[0]
        if len(id) > 14:
            if id.find('.') != -1:
                if str(id).count('.') > 2:
                    newid = ''
                    for idx, p in enumerate(id.split('.')):
                        if idx < len(id.split('.')) - 2:
                            newid += '.' + p
                    id = newid.strip('.')
                id = id.rpartition('.')[0].rpartition('.')[0]
            if id.find('-') != -1:
                id = id.rpartition('-')[0]
            id = id[0:10].strip() + '...' + id[-15:].strip()
        num = epnum
        if len(epnum) == 0:
            num = id
        playtitle = "{0} @ {1} ({2})".format(epfullname, host, id)
        lbl = "{0} ({1})\n{2} {3}".format(host, id, showname, epnum)
        lbl2 = "[B]{0}[/B] [I]({1})[/I]\nURL: {2} Video Link: {3}".format(showname, num, url, vurl)
        playpath = 'plugin://plugin.video.resolveurl-tester/?action=play&url={0}&title={1}'.format(quote(vurl), quote(playtitle))
        item = {'label': lbl, 'label2': lbl2, 'thumb': thumb, 'icon': thumb, 'is_folder': False, 'is_playable': True, 'url': playpath, 'info': {'video': {'plot': lbl2}}}
        litems.append(item)
    return litems


@plugin.action()
def play(params):
    stream_url = None
    if params.video is not None:
        urlvid = params.video
    else:
        return None
    #xbmc.log(msg="Play: {0}".format(urlvid))
    xbmc.executebuiltin('Notification("{0}","{1}")'.format("Play", urlvid))
    url = 'plugin://plugin.video.resolveurl-tester/?action=play&url={0}'.format(quote(urlvid))
    return plugin.resolve_url(url)


def showMessage(header='', msg=''):
    try:
        header = str(header.encode('utf-8', 'ignore'))
        msg = str(msg.encode('utf-8', 'ignore'))
        xbmc.executebuiltin('Notification({0},{1})'.format(header, msg))
    except:
        print(header + '\n' + msg)


@plugin.action()
def show_latest():
    return list_latest()


def search_ws(query):
    items = []
    url = "https://www1.swatchseries.to/serie/" + query.replace(' ', '_')
    items = get_seriesepisodelists(url)
    return items


@plugin.action()
def show_searchbox(params):
    site = params.site
    searchtxt = ''
    searchtxt = plugin.get_setting('lastsearch')
    item = Tv.search.search(func_getinput=get_input(searchtxt))
    litem = plugin.create_list_item(item)
    querytext = litem.getLabel()
    plugin.set_setting('lastsearch', querytext)
    return search_ws(query=querytext)

@plugin.action()
def show_searchfolder(params):
    litems = []
    items = []
    items = Tv.search.gethistory()
    newitem = plugin.create_list_item(Tv.search.ListItemNewSearch)
    clearitem = plugin.create_list_item(Tv.search.ListItemClear)
    litems.append(newitem)
    for item in items:
        litems.append(plugin.create_list_item(item))
    litems.append(clearitem)
    return litems
    #return list_searchepisodes(query=params.searchterm)

@plugin.action()
def show_search(params):
    return list_searchepisodes(query=params.query)

@plugin.action()
def search_clear(params):
    Tv.search.clear()
    return plugin.create_listing([plugin.create_list_item(Tv.search.ListItemNewSearch)])

@plugin.action()
def show_sources(params):
    return list_sources(episode=params.episode)

@plugin.action()
def show_category():
    searchtxt = ''
    searchtxt = plugin.get_setting('lastsearch')
    searchtxt = get_input(searchtxt)
    querytext = searchtxt.replace(' ', '+')
    plugin.set_setting('lastsearch', searchtxt)
    return list_category(category=searchtxt)


def list_latest():
    litems = []
    latestshows = Tv.latest()
    for show in latestshows:
        showname = show.get('name', '')
        showlink = show.get('video', '')
        showpath = plugin.get_url(action='show_sources', episode=showlink)
        item = {
            'label': showname,
            'label2': showlink,
            'is_folder': True,
            'thumb': "DefaultVideo.png",
            'url': showpath
        }
        litems.append(item)
    return litems


def list_sources(episode=''):
    litems = []
    videos = Tv.get_sources(episode)
    for video in videos:
        item = {
            'label': video['name'],
            'label2': "{0}: {1}".format(video['hoster'], video['videoid']),
            'thumb': 'defaultfolder.png',
            'url': plugin.get_url(action='play', video=video['video']),
            'is_folder': False }
        litems.append(item)
    return litems


def list_searchepisodes(query=''):
    litems = []
    eplist = Tv.dosearch(url="http://tvseries4u.com/?s="+query)
    for show in eplist:        
        showlink = show.get('video', '')
        showname = show.get('name', '')
        showthumb = show.get('thumb', 'DefaultVideo.png')
        showpath = plugin.get_url(action='show_sources', episode=showlink)
        item = {
            'label': showname,
            'thumb': showthumb,
            'url': showpath,
            'is_folder': True
        }
        litems.append(item)
    return litems


def list_category(category=''):
    VIDEOS = Tv.get_catepisodes(category)
    litems = []
    for show in VIDEOS:        
        showlink = show.get('video', '')
        showname = show.get('name', '')
        showthumb = 'DefaultVideo.png'
        showpath = plugin.get_url(action='show_sources', episode=showlink)
        item = {
            'label': showname,
            'thumb': showthumb,
            'url': showpath,
            'is_folder': True
        }
        litems.append(item)
    return litems


def add_ContextDL(item):
    ctxlist = []
    ctxlist = item.get('context_menu', [])
    name = item.get('label', item.get('label2', ''))
    hurl = item.get('url', '')
    if item.has_key('properties'):
        itemp = item.get('properties', {})
        if itemp.has_key("videourl"):
            hurl = unquote(itemp.get('videourl', ''))
    else:
        if hurl.find('&video=') != -1:
            uq = hurl.split('&video=',1)[-1]
        else:
            uq = hurl.split('&url=',1)[-1]
        hurl = unquote(uq.split('&', 1)[0])
    playpath = plugin.get_url(action='play', video=hurl)
    plugin.log_debug(message=playpath)
    ctx = ("[COLOR green]Play[/COLOR]", 'RunPlugin("{0}")'.format(playpath),)
    ctxlist.append(ctx)
    playpath = "plugin://plugin.video.resolveurl-tester/?action=play&url={0}".format(quote_plus(hurl))
    ctx = ("[COLOR orange]Resolver Play[/COLOR]", 'RunPlugin("{0}")'.format(playpath),)
    ctxlist.append(ctx)
    ctx = ("[COLOR yellow]Download[/COLOR]", 'RunPlugin("{0}")'.format(plugin.get_url(action="download", video=hurl)),)
    ctxlist.append(ctx)
    item.update({"context_menu": ctxlist})
    return item


@plugin.action()
def download(params):
    vurl = ''
    allok = False
    if params.video is not None:
        vurl = params.video
    else:
        return None
    try:
        from YDStreamExtractor import getVideoInfo
        from YDStreamExtractor import handleDownload
        info = getVideoInfo(vurl, resolve_redirects=True)
        dlpath = plugin.get_setting('downloadpath')
        if not path.exists(dlpath):
            dlpath = xbmc.translatePath("home://")
        handleDownload(info, bg=True, path=dlpath)
        allok = True
    except:
        allok = False
        xbmc.executebuiltin('Notification({0},{1})'.format("FAILED to Download", vurl))
    if allok:
        xbmc.executebuiltin('Notification({0},{1})'.format("OK! Download Started", vurl))


def get_input(default=''):
    kb = xbmc.Keyboard(default, 'Search WatchSeries.OVF')
    kb.setDefault(default)
    kb.setHeading('WatchSeries.OVF Search')
    kb.setHiddenInput(False)
    kb.doModal()
    if (kb.isConfirmed()):
        search_term = kb.getText()
        return(search_term)
    else:
        return None


if __name__ == '__main__':
    # Run our plugin
    plugin.run()
    xbmcplugin.setContent(handle, 'tvshows')

