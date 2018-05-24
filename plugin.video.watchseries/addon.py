from kodiswift import Plugin, xbmc, ListItem, download_page, clean_dict, SortMethod
from resources.lib.addontools import WsolUtils, utils as WebUtils
import ssl, os.path as path, json, re
import webutil as WebUtilsLib
import web_pdb

ssl._create_default_https_context = ssl._create_unverified_context
plugin = Plugin()
ws = WsolUtils(kodiplugin=plugin)
DL = ws.DL
__imgsearch__ = ws.imgsearch  # 'https://watchseries-online.pl'


@plugin.route('/')
def index():
    litems = []
    plugin.set_content('episodes')
    itemlatest = {'label': 'Latest Episodes', 'icon': 'DefaultFolder.png', 'thumbnail': 'DefaultFolder.png',
                  'path': plugin.url_for(category, name='last-350-episodes', url='last-350-episodes')}
    itemlatest2 = {'label': 'Other Shows', 'icon': 'DefaultFolder.png', 'thumbnail': 'DefaultFolder.png',
                   'path': plugin.url_for(category, name="category/", url="not-in-homepage")}
    itemsaved = {'label': 'Saved Shows', 'path': plugin.url_for(saved), 'icon': 'DefaultFolder.png',
                 'thumbnail': 'DefaultFolder.png'}
    itemplay = {'label': 'Resolve URL and Play (URLresolver required)',
                'path': plugin.url_for(endpoint=resolveurl),
                'icon': 'DefaultFolder.png', 'thumbnail': 'DefaultFolder.png'}
    itemsearch = {'label': 'Search', 'icon': __imgsearch__, 'thumbnail': __imgsearch__,
                  'path': plugin.url_for(search)}
    litems.append(itemlatest)
    litems.append(itemlatest2)
    litems.append(itemsaved)
    litems.append(itemsearch)
    litems.append(itemplay)
    return litems


def category_episodemake(episodename, episodelink, dateadded=None):
    '''
    Will return a ListItem for the given link to an episode and it's full linked name.
    Name will be sent to format show to attempt to parse out a date or season from the title.
    Infolabels are populated with any details that can be parsed from the title as well.
    Should be used anytime an item needs to be created that is an item for one specific episode of a show.
    Latest 350, Saved Show, Category (Show listing of all episodes for that series) would all use this.
    '''
    infolbl = {}
    spath = plugin.url_for(episode, name=episodename, url=episodelink)
    if plugin.get_setting('playold', converter=bool):
        spath = spath.replace("plugin.video.watchseries/", "plugin.video.wsonline/")
    img = "DefaultVideoFolder.png"
    seasonstr = ''
    try:
        eptitle, epdate, epnum = ws.formatshow(episodename)
        eplbl = ws.formatlabel(eptitle, epdate, epnum)
        plotstr = "{0} ({1}): {2} {3}".format(epdate, epnum, eptitle, episodelink)
        infolbl = {'EpisodeName': epdate, 'Title': eptitle, 'Plot': plotstr}
        if len(epnum) > 0:
            showS, showE = ws.findepseason(epnum)
            snum = int(showS)
            epnum = int(showE)
            infolbl.update({'Episode': showE, 'Season': showS})
            if snum > 0 and epnum > 0:
                epdate = "S{0}e{1}".format(snum, epnum)
                infolbl.update({'PlotOutline': epdate})
        if dateadded is not None:
            dateout = str(dateadded.replace(' ', '-')).strip()
            infolbl.update({"Date": dateout})
        item = {'label': eplbl, 'label2': epdate, 'icon': img, 'thumbnail': img, 'path': spath}
        item.setdefault(item.keys()[0])
        li = ListItem.from_dict(**item)
        li.set_is_playable(is_playable=True)
        li.is_folder = True
        li.set_info(type='video', info_labels=infolbl)
        li.add_context_menu_items(
            [('Autoplay', 'RunPlugin("{0}")'.format(plugin.url_for(endpoint=ws.func_autoplay, url=episodelink)),)])
    except:
        li = ListItem(label=episodename, label2=episodelink, icon=img, thumbnail=img, path=spath)
    return li


@plugin.route('/category2/<name>/<url>')
def category2(name='', url=''):
    DEBUGON = plugin.get_setting('debugon', converter=bool)
    if DEBUGON: web_pdb.set_trace()
    #url = ws.BASEURL + '/' + urlpath
    fullhtml = ws.DL(url)
    html = fullhtml.partition("</nav>")[-1].split("</ul>", 1)[0]
    strDate = ur"<li class='listEpisode'>(\d+ \d+ \d+) : "
    strUrl = ur'<a.+?href="([^"]*?)">'
    strName = ur'</span>([^<]*?)</a>'
    #regexstr = "{0}{1}.+?{2}".format(strDate, strUrl, strName)
    regexstr = "<li class=.listEpisode.>.+?{0}.+?{1}".format(strUrl, strName)
    matches = re.compile(regexstr).findall(html)
    litems = []
    eptitle = ''
    ws.Episode = episode
    if DEBUGON:
        def debugitems():
            with web_pdb.catch_post_mortem():
                litems = []
                for eplink, epname in matches:
                    item = category_episodemake(epname, eplink, dateadded=None)
                    itempath = plugin.url_for(endpoint=episode, name=epname, url=eplink)
                    #dateout = epdate.replace(' ', '-').strip()
                    #item.label += " [I][B][COLOR orange]{0}[/COLOR][/B][/I]".format(dateout)
                    litems.append(item)
                return litems
        items = debugitems()
        return items
    try:
        for eplink, epname in matches:
            item = category_episodemake(epname, eplink, dateadded=None)
            # itempath = plugin.url_for(endpoint=episode, name=epname, url=eplink)
            #dateout = epdate.replace(' ', '-').strip()
            #item.label += " [I][B][COLOR orange]{0}[/COLOR][/B][/I]".format(dateout)
            litems.append(item)
    except Exception as ex:
        print('ADDON ERROR: {0}'.format(str(repr(ex.message))))
        print(str(repr(ex)))
    return litems


@plugin.route('/category/<name>/<url>')
def category(name='', url=''):
    html = u''
    litems = []
    NODATE = False
    banner = 'DefaultVideoFolder.png'
    strDate = ur'<li class="listEpisode">(\d+ \d+ \d+) : '
    strUrl = ur'<a.+?href="([^"]*?)">'
    strName = ur'</span>([^<]*?)</a>'
    regexstr = "{0}{1}.+?{2}".format(strDate, strUrl, strName)
    DEBUGON = plugin.get_setting('debugon', converter=bool)
    if name.endswith('/'):
        regexstr = "{0}.+?{1}".format(strUrl, strName)
        NODATE = True
        url = name + url
    if not str(url).startswith('http') and len(url) > 8: url = ws.BASEURL + '/' + url
    fullhtml = DL(url)
    html = fullhtml.partition("</nav>")[-1].split("</ul>", 1)[0]
    try:
        banner = str(html.split('id="banner_single"', 1)[0].rpartition('src="')[2].split('"', 1)[0])
        if not banner.startswith('http') and banner != 'DefaultVideoFolder.png': banner = ws.BASEURL + banner
    except:
        banner = 'DefaultVideoFolder.png'
    if DEBUGON: web_pdb.set_trace()
    matches = re.compile(regexstr).findall(html)
    if len(matches) > 500: matches = matches[0:500]
    ws.Episode = episode
    if DEBUGON:
        def debugitems():
            with web_pdb.catch_post_mortem():
                if NODATE:
                    for eplink, epname in matches:
                        item = category_episodemake(epname, eplink)
                        item.thumbnail = banner
                        litems.append(item)
                else:
                    for epdate, eplink, epname in matches:
                        item = category_episodemake(epname, eplink)  # epname, eplink, epdate)
                        # itempath = plugin.url_for(endpoint=episode, name=epname, url=eplink)
                        dateout = epdate.replace(' ', '-').strip()
                        item.label += " [I][B][COLOR orange]{0}[/COLOR][/B][/I]".format(dateout)
                        item.thumbnail = banner
                        litems.append(item)
                return litems

        return debugitems()
    else:
        try:
            if NODATE:
                for eplink, epname in matches:
                    item = category_episodemake(epname, eplink)
                    item.thumbnail = banner
                    litems.append(item)
            else:
                for epdate, eplink, epname in matches:
                    item = category_episodemake(epname, eplink, epdate)
                    # itempath = plugin.url_for(endpoint=episode, name=epname, url=eplink)
                    dateout = epdate.replace(' ', '-').strip()
                    item.label += " [I][B][COLOR orange]{0}[/COLOR][/B][/I]".format(dateout)
                    item.thumbnail = banner
                    litems.append(item)
        except Exception as ex:
            print('ADDON ERROR: {0}'.format(str(repr(ex.message))))
            print(str(repr(ex)))
    # return litems
    # for eplink, epname in matches:
    #    item = category_episodemake(epname, eplink)
    #    item.path = plugin.url_for(episode, name=epname, url=eplink)
    #    litems.append(item)
    # if plugin.get_setting('sortalpha', converter=bool):
    #    litems.sort(key=lambda litems: litems.label, reverse=True)
    return litems


@plugin.route('/episode/<name>/<url>')
def episode(name=None, url=None):
    if plugin.get_setting('debugon', converter=bool): web_pdb.set_trace()

    waserror = False
    linklist = []
    litems = []
    if len(url) == '':
        waserror = True
    else:
        html = DL(url)
        linklist = ws.findvidlinks(html)
        itemparent = None
    if len(linklist) > 0:
        for name, link in linklist:
            itempath = plugin.url_for(play, url=link)
            item = dict(label=name, label2=link, icon='DefaultFolder.png', thumbnail='DefaultFolder.png', path=itempath)
            item.setdefault(item.keys()[0])
            litems.append(item)
        vitems = ws.sortSourceItems(litems)
        litems = []
        for li in vitems:
            item = ListItem.from_dict(**li)
            item.set_is_playable(True)
            item.set_info(info_type='video', info_labels={'Title': item.label, 'Plot': item.label2})
            item.add_stream_info(stream_type='video', stream_values={})
            litems.append(item)
    else:
        waserror = True
    if waserror:
        plugin.notify(title="ERROR No links: {0}".format(name), msg=url)
        return []
    return litems


@plugin.route('/latest/<offset>/<urlpath>')
def latest(offset=0, urlpath='last-350-episodes'):
    DEBUGON = plugin.get_setting('debugon', converter=bool)
    if DEBUGON: web_pdb.set_trace()
    url = ws.BASEURL + '/' + urlpath
    fullhtml = ws.DL(url)
    html = fullhtml.partition("</nav>")[-1].split("</ul>", 1)[0]
    strDate = ur"<li class='listEpisode'>(\d+ \d+ \d+) : "
    strUrl = ur'<a.+?href="([^"]*?)">'
    strName = ur'</span>([^<]*?)</a>'
    regexstr = "{0}{1}.+?{2}".format(strDate, strUrl, strName)
    matches = re.compile(regexstr).findall(html)
    litems = []
    epdate = ''
    eptitle = ''
    filtertxt = plugin.get_setting('filtertext')
    itemnext = {'label': 'Next ->', 'icon': 'DefaultFolder.png', 'thumbnail': 'DefaultFolder.png',
                'path': plugin.url_for(latest, offset=int(offset) + 400, urlpath=urlpath)}
    if len(matches) > 500:
        matches = matches[0:500]
    ws.Episode = episode
    if DEBUGON:
        def debugitems():
            with web_pdb.catch_post_mortem():
                for epdate, eplink, epname in matches:
                    item = category_episodemake(epname, eplink, epdate)
                    # itempath = plugin.url_for(endpoint=episode, name=epname, url=eplink)
                    dateout = epdate.replace(' ', '-').strip()
                    item.label += " [I][B][COLOR orange]{0}[/COLOR][/B][/I]".format(dateout)
                    litems.append(item)
                litems.append(itemnext)

        items = debugitems()
        return items
    try:
        for epdate, eplink, epname in matches:
            item = category_episodemake(epname, eplink, epdate)
            # itempath = plugin.url_for(endpoint=episode, name=epname, url=eplink)
            dateout = epdate.replace(' ', '-').strip()
            item.label += " [I][B][COLOR orange]{0}[/COLOR][/B][/I]".format(dateout)
            litems.append(item)
        litems.append(itemnext)
    except Exception as ex:
        print('ADDON ERROR: {0}'.format(str(repr(ex.message))))
        print(str(repr(ex)))
    return litems


@plugin.route('/resolveurl')
def resolveurl():
    if plugin.get_setting('debugon', converter=bool): web_pdb.set_trace()

    url = plugin.keyboard(default='', heading='Video Page URL')
    if url is not None:
        name = url
        if len(url) > 0:
            item = ListItem(label=name, label2=url, icon='DefaultVideo.png', thumbnail='DefaultVideo.png',
                            path=plugin.url_for(endpoint=play, url=url))
            item.playable = True
            item.set_info(type='video', info_labels={'Title': url, 'Plot': url})
            item.add_stream_info(stream_type='video', stream_values={})
            playable = play(url)
            plugin.notify(msg=playable.path, title="Playing..")
            plugin.play_video(playable)
    plugin.clear_added_items()
    plugin.end_of_directory()


@plugin.route('/saved')
def saved():
    if plugin.get_setting('debugon', converter=bool): web_pdb.set_trace()

    litems = []
    sitems = []
    sitems = ws.loadsaved()
    noitem = {'label': "No Saved Shows", 'icon': 'DefaultFolder.png', 'path': plugin.url_for('index')}
    if len(sitems) < 1:
        return [noitem]
    else:
        return sitems


@plugin.route('/search/')
def search():
    if plugin.get_setting('debugon', converter=bool): web_pdb.set_trace()

    searchtxt = plugin.get_setting('lastsearch')
    searchtxt = plugin.keyboard(searchtxt, 'Search Watchseries-Online', False)
    if len(searchtxt) > 1:
        plugin.set_setting(key='lastsearch', val=searchtxt)
        return ws.query(searchquery=searchtxt)
    else:
        return []


@plugin.route('/saveshow/<name>/<link>')
def saveshow(name='', link=''):
    if plugin.get_setting('debugon', converter=bool): web_pdb.set_trace()
    ws.Category = category
    sitems = []
    litems = []
    try:
        savedpath = path.join(ws.datadir, "saved.json")
        if path.exists(savedpath):
            fpin = file(savedpath)
            rawjson = fpin.read()
            sitems = json.loads(rawjson)
            fpin.close()
        saveitem = ws.makecatitem(name, link)
        # saveitem = {'label': name, 'path': plugin.url_for(endpoint=category, name=name, url=link)}
        # saveitem.setdefault(saveitem.keys()[0])
        sitems.append(saveitem)
        fpout = file(savedpath, mode='w')
        json.dump(sitems, fpout)
        fpout.close()
        plugin.notify(msg="SAVED {0}".format(name), title=link)
    except:
        plugin.notify(msg="ERROR save failed for {0}".format(name), title=link)


@plugin.route('/removeshow/<name>/<link>')
def removeshow(name='', link=''):
    if plugin.get_setting('debugon', converter=bool): web_pdb.set_trace()

    sitems = []
    litems = []
    sitems = ws.loadsaved()
    for item in sitems:
        if item.get('name') == name or item.get('link') == link:
            plugin.notify(title='Removed {0}'.format(name), msg='Removed "{0}": {1}'.format(name, link))
        else:
            litems.append(item)
    jsout = json.dumps(litems)
    plugin.addon.setSetting('savedshows', jsout)
    plugin.notify(title='Removed {0}'.format(name), msg='{0} Removed Show link: {1}'.format(name, link))


@plugin.route('/playfirst/<url>')
def autoplay(url=''):
    if plugin.get_setting('debugon', converter=bool): web_pdb.set_trace()

    if len(url) < 1:
        return None
    sourceslist = []
    litems = []
    idx = 0
    prefhost = ''
    html = ws.DL(url)
    selItem = None
    outtxt = "Not Found"
    thispath = plugin.url_for(endpoint=play, url=url)
    stext = plugin.get_setting('topSources')
    if len(stext) < 1:
        prefhost = 'thevideo'
    else:
        sourceslist = stext.split(',')
        prefhost = sourceslist[0]
    try:
        for fitem in plugin.added_items:
            if fitem.selected == True or fitem.path.find(thispath) != -1:
                try:
                    plugin.set_resolved_url(fitem)
                    fitem.is_playable(True)
                    fitem.played(True)
                except:
                    pass
                selItem = fitem
                plugin.notify(msg=selItem.label, title="Found item")
                break
    except:
        selItem = None
    if selItem is not None:
        try:
            selItem.set_is_playable(True)
            selItem.set_played(was_played=True)
            outtxt = selItem.label + " " + selItem.label2
        except:
            outtxt = str(repr(selItem))
    linklist = ws.findvidlinks(html, findhost=prefhost)
    if len(linklist) > 0:
        name, link = linklist[0]
        itempath = plugin.url_for(play, url=link)
        sitem = dict(label=name, label2=link, icon='DefaultFolder.png', thumbnail='DefaultFolder.png', path=itempath)
        sitem.setdefault(sitem.keys()[0])
        item = ListItem.from_dict(**sitem)
        item.set_is_playable(True)
        item.set_info(type='video', info_labels={'Title': item.label, 'Plot': item.label2})
        item.add_stream_info(stream_type='video', stream_values={})
        plugin.notify(msg=link, title=name)
        item.set_played(was_played=True)
        plugin.play_video(item)
        return [plugin.set_resolved_url(item)]


@plugin.route('/play/<url>')
def play(url):
    if plugin.get_setting('debugon', converter=bool): web_pdb.set_trace()

    resolved = ''
    stream_url = ''
    item = None
    try:
        import urlresolver
        resolved = urlresolver.HostedMediaFile(url).resolve()
        if not resolved or resolved == False or len(resolved) < 1:
            resolved = urlresolver.resolve(url)
            if resolved is None or len(resolved) < 1:
                resolved = urlresolver.resolve(WebUtils.unescape(url))
        if len(resolved) > 1:
            plugin.notify(msg="PLAY {0}".format(resolved.partition('.')[-1]), title="URLRESOLVER", delay=1000)
            plugin.set_resolved_url(resolved)
            item = ListItem.from_dict(path=resolved)
            item.add_stream_info('video', stream_values={})
            item.set_is_playable(True)
            return item
    except:
        resolved = ''
        plugin.notify(msg="FAILED {0}".format(url.partition('.')[-1]), title="URLRESOLVER", delay=1000)
    try:
        import YDStreamExtractor
        info = YDStreamExtractor.getVideoInfo(url, resolve_redirects=True)
        resolved = info.streamURL()
        for s in info.streams():
            try:
                stream_url = s['xbmc_url'].encode('utf-8', 'ignore')
                xbmc.log(msg="**YOUTUBE-DL Stream found: {0}".format(stream_url))
            except:
                pass
        if len(stream_url) > 1:
            resolved = stream_url
        if len(resolved) > 1:
            plugin.notify(msg="Playing: {0}".format(resolved.partition('.')[-1]), title="YOUTUBE-DL", delay=1000)
            plugin.set_resolved_url(resolved)
            item = ListItem.from_dict(path=resolved)
            item.add_stream_info('video', stream_values={})
            item.set_is_playable(True)
            return item
    except:
        plugin.notify(msg="Failed: {0}".format(resolved.partition('.')[-1]), title="YOUTUBE-DL", delay=1000)

    if len(resolved) > 1:
        plugin.set_resolved_url(resolved)
        item = ListItem.from_dict(path=resolved)
        return item
    else:
        plugin.set_resolved_url(url)  # url)
        return None


if __name__ == '__main__':
    # if plugin.get_setting('debugon', converter=bool): web_pdb.set_trace()
    viewmode = 0
    hostname = ''
    hostname = plugin.get_setting('setHostname')
    if len(hostname) > 1:
        hostname = hostname.strip()
        hostname = hostname.strip('/')
        if str(hostname).startswith('http'):
            __BASEURL__ = hostname
        else:
            __BASEURL__ = 'https://' + hostname
    ws.BASEURL = __BASEURL__
    ws.Plugin = plugin
    ws.Remove = removeshow
    ws.Episode = episode
    ws.Category = category
    ws.Save = saveshow
    ws.Autoplay = autoplay
    ws.Play = play
    # funcmaps = {'episode': episode, 'category': category, 'save': saveshow, 'autoplay': autoplay, 'play': play, 'remove': reemoveshow, 'search': search}
    # ws = WsolUtils(kodiplugin=plugin, **funcmaps)
    plugin.run()
    plugin.set_content('episodes')
    viewmode = plugin.get_setting('viewmode', converter=int)
    plugin.set_view_mode(view_mode_id=viewmode)
    # plugin.set_view_mode(plugin.get_setting('viewmode'))
