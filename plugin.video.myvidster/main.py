# -*- coding: utf-8 -*-
# Module: main
# Author: moedje
# Github: https://github.com/moedje/
# Updated on: June 23, 2019
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
import ssl, re, datetime, time
import sys, os
import base64
try:
    import xbmc, xbmcplugin
except:
    import Kodistubs.xbmc as xbmc
    import Kodistubs.xbmcplugin as xbmcplugin
GIF = False
#try:
#    import imageio
#except:
#    GIF = False
try:
     # Python 2.6-2.7
     from HTMLParser import HTMLParser
except ImportError:
     # Python 3
     from html.parser import HTMLParser
try:
     # Python 2.6-2.7
     import urllib
     urlretrieve = urllib.urlretrieve
except ImportError:
     # Python 3
     import urllib.request
     urlretrieve = urllib.request.urlretrieve
h = HTMLParser()
from resources import lib as Lib
try:
    import urllib, urllib2
except:
    import urllib3.util as urllib2
quote_plus = urllib.quote_plus
quote = urllib.quote
path = os.path
ssl._create_default_https_context = ssl._create_unverified_context


plugin = Lib.simpleplugin.Plugin()
__datadir__ = xbmc.translatePath('special://profile/addon_data/{0}/'.format(plugin.id))
__cookie__ = path.join(__datadir__, 'cookies.lwp')
__next__ = path.join(xbmc.translatePath('special://home/addons/plugin.video.myvidster/resources/'), 'next.png')
API = Lib.vidster.MyVidster(path_addon=__datadir__)

#e=sys.exit
def create_gif(images=[]):
    imagefiles = []
    tempfiles = []
    try:
        images.remove('')
    except:
        pass
    try:
        images.remove(u'')
    except:
        pass
    vidster_headers = {'referer': 'https://www.myvidster.com/',
                       'Cookie': '__cfduid=d913c54b56fe95616689ce1f1fc683a231559474798; sm_dapi_session=1; _gat=1; PHPSESSID=r1aptmhcmicd179f94v7o72id2; referral=myvidster.com; _ga=GA1.2.638511231.1559474803; _gid=GA1.2.142664491.1559474803; __atuvc=1%7C23; __atuvs=5cf3b2727692eeb9000; user_name=Skyler32UK; user_id=2219807; password=46c53b8a852c4ee94f458dc99786e23ebd666bd1; cc_data=2219807; auto_refresh=1'}
    gifname = images[0].replace('https://', '').replace('http://', '').partition('/')[-1].split('/',1)[0] + '.gif'
    output_dir = os.path.join(xbmc.translatePath("special://profile/addon_data/{0}/".format(plugin.id)),'thumbs/')
    output_file = os.path.join(output_dir, gifname)
    if path.exists(output_file):
        return output_file
    tempdir = os.path.join(output_dir,'temp/')
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
        os.mkdir(tempdir)
    if not os.path.isdir(tempdir):
        os.mkdir(tempdir)
    output_gif = Lib.gifmaker.from_urls(images, tempdir)
    '''
    for img in images:
        tempfilename = img.rpartition('/')[-1]
        tempfilenamefull = os.path.join(tempdir, tempfilename)
        tempfiles.append(tempfilenamefull)
        resp = Lib.urlquick.get(img, params={'headers': vidster_headers})
        output = open(tempfilenamefull, "wb")
        output.write(resp.raw.read())
        output.close()
        imagefiles.append(tempfilenamefull)
    #imageio.mimsave(output_file, imagefiles, duration=duration)
    #for img in tempfiles:
    #    os.remove(img)
    gifpath = Lib.gifmaker.make(output_file, imagefiles)
    plugin.log(message="GIF: "+output_file)
    return output_file
    '''
    return output_gif


@plugin.action()
@plugin.mem_cached(10)
def root():
    imgVidster = __next__.replace('next', 'myvidster')
    vidsterNameChan = 'GayPublic'
    lblTpl = '[COLOR green]{0}[/COLOR] ([COLOR white][I]{1}[/I][/COLOR])\n[COLOR yellow]{2}[/COLOR]'
    lblVidsterNew = lblTpl.format('MyVidster', 'Latest', vidsterNameChan)
    lblVidsterChan = lblTpl.format('MyVidster', 'View Channel', vidsterNameChan) #'[COLOR green]MyVidster[/COLOR] - [COLOR white][I]View Channel[/I][/COLOR]\n[COLOR yellow]{0}[/COLOR]'.format(vidsterNameChan)
    lblVidsterGetChan = lblTpl.format('MyVidster Channel', vidsterNameChan, '')
    lblWs = lblTpl.format("Watch Series", "Latest", "")
    lblWsAll = lblTpl.format("Watch Series", "Full List", "")
    rootmenu = {
        "Home": [
            {'label': lblVidsterGetChan, 'url': plugin.get_url(action='get_channel', id=1533786, page=1), 'thumb': imgVidster,
             'is_folder': True, 'is_playable': False},
            {'label': lblVidsterNew, 'url': plugin.get_url(action='home_myvidster', id=1533786), 'thumb': imgVidster,
             'is_folder': True, 'is_playable': False},             
            {'label': lblVidsterChan, 'url': plugin.get_url(action='list_vidster', id=1533786), 'thumb': imgVidster,
             'is_folder': True, 'is_playable': False},
            {'label': "Search MyVidster", 'url': plugin.get_url(action='search_vidster', query="public"), 'thumb': imgVidster,
             'is_folder': True, 'is_playable': False}]
    }
    return rootmenu["Home"]


@plugin.action()
def get_channel(params):
    items = []
    litems = []
    linext = {}
    chanid = "1533786"
    if params.id is not None:
        chanid = params.id
    page = 1
    if params.page is not None:
        page = params.page
    nextpage = int(page) + 1
    nextlbl = 'Next -> {0}'.format(nextpage.__str__())
    linext = {'label': nextlbl, 'url': plugin.get_url(action='get_channel', page=nextpage, id=chanid), 'thumb': __next__, 'icon': __next__, 'is_folder': True}
    items = API.get_channel(channel=chanid, page=page)
    for li in items:
        playpath = plugin.get_url(action='playvidster', video=li.get('url'))
        li.update({'url': playpath})
        litems.append(li)
    if len(litems) == 250:
        litems.append(linext)
    return litems


@plugin.action()
def home_myvidster(params):
    items = []
    litems = []
    cid = 1533786
    if params.id is not None:
        cid = params.id
    urlrss = 'https://www.myvidster.com/rss/channel/' + str(cid) # https://www.myvidster.com/user/manage.php?level=video&id=1533786&entries_per_page=300
    resp = Lib.urlquick.get(urlrss)
    for item in resp.xml().iter('item'):
        items.append(item)
    for item in items:
        litem = {'is_folder': False} #, 'is_playable': True}
        gif = ''
        for kid in item.getchildren():
            if kid.tag == 'link':
                vurl = kid.text
                vid = vurl.replace('/video/','').split('/',1)[0]
                pathdl = plugin.get_url(action='download', video=vurl)
                images = API.vidster_images(id=vid)
                gif = create_gif(images)
                litem.update({'url': plugin.get_url(action='play', video=vurl), 'art': {'AnimatedPoster': gif}, 'context_menu': [('Download', 'RunPlugin({0})'.format(pathdl)), ]})  # {'url': plugin.get_url(action=sources_ws, url=kid.text)})
                #{'context_menu': [('Download', 'RunPlugin({0})'.format(pathdl)), ]}
            elif kid.tag == 'title':
                name = kid.text.encode('latin', 'ignore')
                litem.update({'label': name.strip()})
            if kid.tag == '{http://search.yahoo.com/mrss/}thumbnail':
                    attr = kid.attrib
                    img = attr.get('url')
                    litem.update({'thumb': img, 'icon': img})
            elif kid.tag == 'description':
                lbl2 = kid.text.strip() + '\n' + litem.get('label2', '')
                litem.update({'label2': lbl2})
            elif kid.tag == 'pubdate':
                lbl2 = kid.text.strip() + '\n' + litem.get('label2', '')
                litem.update({'label2': lbl2})
        #if path.isfile(gif):
        #    img = gif
        #    litem.update({'thumb': img, 'icon': img})
        litems.append(litem)
    return litems


@plugin.action()
def search_vidster(params):
    if params.query is not None:
        query = params.query
    urlthumb = 'http://www.myvidster.com/user/api.php?action=fetch&password=46c53b8a852c4ee94f458dc99786e23ebd666bd1&email=alljer@gmail.com&video_id='
    surl = 'https://www.myvidster.com/search/?password=46c53b8a852c4ee94f458dc99786e23ebd666bd1&email=alljer@gmail.com&filter_by=myvidster&sortby=utc_posted&cfilter_by=gay&q='+query.replace(' ', '+')
    resp = Lib.urlquick.get(surl, params={'user_id': 2219807, 'email': 'alljer@gmail.com', 'password': '46c53b8a852c4ee94f458dc99786e23ebd666bd1', 'adult_filter': 0})
    src = resp.content
    litems = []
    items = []
    matches = []
    vidster_headers = {'Cookie': '__cfduid=d913c54b56fe95616689ce1f1fc683a231559474798; sm_dapi_session=1; _gat=1; PHPSESSID=r1aptmhcmicd179f94v7o72id2; referral=myvidster.com; _ga=GA1.2.638511231.1559474803; _gid=GA1.2.142664491.1559474803; __atuvc=1%7C23; __atuvs=5cf3b2727692eeb9000; user_name=Skyler32UK; user_id=2219807; password=46c53b8a852c4ee94f458dc99786e23ebd666bd1; cc_data=2219807; auto_refresh=1',
        'referer': 'https://www.myvidster.com/'}
    html = src.rpartition('id="search-content"')[-1].split('id="search-header"',1)[0]
    matches = re.compile('class="viddetails">\n.+?href="(.+?)">(.+?)</a>.+?\n.+?Bookmarked (.+?) ago').findall(html)
    for link, vid_title, posted in matches:
        vurl = "https://www.myvidster.com" + link
        vid = link.replace('/video/','').split('/',1)[0]
        resp = Lib.urlquick.get(urlthumb+vid)
        img = resp.content.partition('<thumbnail_url1>')[-1].split('</thumbnail_url1>')[0].strip()
        #img = images[0]
        #if len(images) > 1:
        #    img = images[1]
        lbl = '[COLOR yellow][B]{0}[/B][/COLOR] [I]{1}[/I]'.format(vid_title.title(), posted) 
        lbl2 = "{0}\n{1}\n{2}".format(vurl, posted, img)
        pathdl = plugin.get_url(action='download', video=vurl)
        playpath = plugin.get_url(action='play', video=vurl)
        images = API.vidster_images(vid)
        gif = create_gif(images)
        item = {'label': lbl, 'label2': lbl2, 'thumb': img, 'icon': img, 'art': {'AnimatedPoster': gif}, 'is_folder': False, 'url': plugin.get_url(action='play', video=vurl), 'info': {'video': {}}, 'context_menu': [('Play', 'RunPlugin({0})'.format(playpath)), ('Download', 'RunPlugin({0})'.format(pathdl)), ]}
        #if GIF:
        #    resp = Lib.urlquick.get(urlgetimg+vid, params={'headers': vidster_headers})
        #    images = resp.json()
        #    gifimage = create_gif(images)
        #    item.update(art={'AnimatedPoster': gifimage, 'AnimatedFanart': gifimage})
        litems.append(item)
    return litems

@plugin.action()
def list_vidster(params):
    items = []
    matches = []
    litems = []
    urlthumb = 'http://www.myvidster.com/user/api.php?action=fetch&password=46c53b8a852c4ee94f458dc99786e23ebd666bd1&email=alljer@gmail.com&video_id='
    #urlgetimg = 'https://www.myvidster.com/fetch_preview.php?action=fetch_preview&video_id='
    vidster_headers = {'referer': 'https://www.myvidster.com/', 'Cookie': '__cfduid=d913c54b56fe95616689ce1f1fc683a231559474798; sm_dapi_session=1; _gat=1; PHPSESSID=r1aptmhcmicd179f94v7o72id2; referral=myvidster.com; _ga=GA1.2.638511231.1559474803; _gid=GA1.2.142664491.1559474803; __atuvc=1%7C23; __atuvs=5cf3b2727692eeb9000; user_name=Skyler32UK; user_id=2219807; password=46c53b8a852c4ee94f458dc99786e23ebd666bd1; cc_data=2219807; auto_refresh=1'}
    cid = 1533786
    if params.id is not None:
        cid = params.id
    BASEURL = 'https://www.myvidster.com/processor.php?action=display_channel&channel_id={0}&page=1&thumb_num=300'
    url = BASEURL.format(str(cid))
    url_adult = "https://www.myvidster.com/disable_filter.php" #user/index.php?action=log_in&save_login=on" #&adult_filter=0" 'password': '46c53b8a852c4ee94f458dc99786e23ebd666bd1'
    presp = Lib.urlquick.post(url_adult, params={'user_id': 2219807, 'email': 'alljer@gmail.com', 'password': '46c53b8a852c4ee94f458dc99786e23ebd666bd1', 'adult_filter': 0}) #vidster_headers)
    resp = Lib.urlquick.get(url, params={}, cookies=presp.cookies) #vidster_headers.update(presp.headers)
    src = resp.content
    html = src.rpartition('<ul class="slides clearfix">')[-1].split('</ul>')[0]
    results = re.compile('src="(.+?)".+?\n.+?\n.+?href="(/video.+?)" title="(.+?)"').findall(html)
    for img, link, vid_title in results:
        vurl = "https://www.myvidster.com" + link
        vid = link.replace('/video/','').split('/',1)[0]
        images = vidster_images(vid)
        gif = create_gif(images)
        resp = Lib.urlquick.get(urlthumb+vid)
        img = resp.content.partition('<thumbnail_url1>')[-1].split('</thumbnail_url1>')[0].strip()        
        lbl = '[COLOR yellow][B]{0}[/B][/COLOR] [I]{1}[/I]'.format(vid_title.title(), "") 
        lbl2 = "{0}\n{1}".format(vurl, img)
        pathdl = plugin.get_url(action='download', video=vurl)
        playpath = plugin.get_url(action='play', video=vurl)
        item = {'label': lbl, 'label2': lbl2, 'thumb': img, 'icon': img, 'art': {'AnimatedPoster': gif}, 'is_folder': False, 'url': plugin.get_url(action='play', video=vurl), 'info': {'video': {}}, 'context_menu': [('Play', 'RunPlugin({0})'.format(playpath)), ('Download', 'RunPlugin({0})'.format(pathdl)), ]}
        #if len(images) > 1:
        #    item = item.update({'art': {'Posters': images}})
        litems.append(item)
    return litems


@plugin.action()
def download(params):
    vurl = ''
    vurl = params.video
    try:
        from YDStreamExtractor import getVideoInfo
        from YDStreamExtractor import handleDownload
        info = getVideoInfo(vurl, resolve_redirects=True)
        dlpath = plugin.get_setting('downloadpath')
        if not path.exists(dlpath):
            dlpath = xbmc.translatePath("home://")
        handleDownload(info, bg=True, path=dlpath)
    except:
        plugin.notify(vurl, "Download Failed")


@plugin.action()
def playvidster(params):
    urlvid = params.video
    resolvedurl = urlvid
    url = "plugin://plugin.video.wsonline/play/{0}".format(quote_plus(urlvid))
    try:
        xbmc.executebuiltin("Notification({0}, {1})".format("Trying To Play...", urlvid))
        resolvedurl = API.resolve(urlvid)
        plugin.log_notice(resolvedurl)
        xbmc.executebuiltin("Notification({0}, {1})".format(urlvid, resolvedurl))
    except:
        plugin.log_notice("ERROR RESOLVING " + url)
    item = {'label': urlvid, 'label2': resolvedurl, 'thumb': 'DefaultVideo.png', 'is_folder': False, 'is_playable': True, 'url': resolvedurl}
    plugin.resolve_url(resolvedurl, item)
    xbmc.Player().play(resolvedurl)
    return [item]


@plugin.action()
def play(params):
    urlvid = params.video
    resolvedurl = urlvid
    url = "plugin://plugin.video.wsonline/play/{0}".format(quote_plus(urlvid))
    try:
        xbmc.executebuiltin("Notification({0}, {1})".format("Trying To Play...", urlvid))
        resolvedurl = API.resolve(urlvid)
        plugin.log_notice(resolvedurl)
        xbmc.executebuiltin("Notification({0}, {1})".format(urlvid, resolvedurl))
    except:
        plugin.log_notice("ERROR RESOLVING " + url)
    item = {'label': urlvid, 'label2': resolvedurl, 'thumb': 'DefaultVideo.png', 'is_folder': False, 'is_playable': True, 'url': resolvedurl}
    plugin.resolve_url(resolvedurl, item)
    xbmc.Player().play(resolvedurl)
    return [item]


def showMessage(self, header='', msg=''):
    try:
        header = str(header.encode('utf-8', 'ignore'))
        msg = str(msg.encode('utf-8', 'ignore'))
        xbmc.executebuiltin('Notification({0},{1})'.format(header, msg))
    except:
        print(header + '\n' + msg)


def get_input(default=''):
    kb = xbmc.Keyboard(default, 'Search MyVidster')
    kb.setDefault(default)
    kb.setHeading('MyVidster Search')
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
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmc.executebuiltin('Skin.SetBool(SkinHelper.EnableAnimatedPosters)')
