# -*- coding: utf-8 -*-
# https://docs.microsoft.com/en-us/rest/api/cognitiveservices/bing-web-api-v7-reference
from kodiswift import Plugin, xbmc
from urllib import quote_plus as Quote, unquote_plus as Unquote
import webutil
import sys, os, os.path as path
import json
plugin = Plugin()
APIKEY=plugin.get_setting('apikey')
tplWho = '( jovenes OR chavalo OR chavo OR amigo OR hombre OR hermano OR novinho OR chico OR chavalito )'
tplWhat = '( mecos OR masturbo OR masturbandose OR batendo OR paja OR follando OR cogiendo OR cojiendo OR sobarse OR punheta OR verga OR lefa )'
tplWhere = '( flagra OR flagrou OR trabajo OR publico OR biblioteca OR aula OR "en clase" OR escuela OR omnibus OR autobus OR viajandor )'
tplWank = '( wank OR wanking OR wanked OR stroke OR stroking OR jerk OR jack OR masturbate OR masturbating OR cumming OR cum OR jackoff OR jerkoff OR handjob )'
searchq = tplWhere + ' AND ' + tplWhat + ' ' + tplWho
cpath = path.join(xbmc.translatePath('special://userdata'), 'cookies.lwp')
dl = webutil.DemystifiedWebRequest(cookiePath=cpath)
__addondir__ = xbmc.translatePath(plugin.addon.getAddonInfo('path'))
__resdir__ = os.path.join(__addondir__, 'resources')
__imgdir__ = os.path.join(__resdir__, 'images')
__imgsearch__ = os.path.join(__imgdir__, 'search.png')
__imgnext__ = os.path.join(__imgdir__, 'next.png')
__imgback__ = os.path.join(__imgdir__, 'back.png')
__imgtumblr__ = os.path.join(__imgdir__, 'tumblr.png')

@plugin.route('/')
def index():
    itemnew = {
        'label': 'New Bing Video Search!',
        'icon': __imgsearch__, 'thumbnail': __imgsearch__,
        'path': plugin.url_for(endpoint=query, searchfor='NEW'),
        'is_playable': False
    }
    itemlast = {
        'label': 'Last Bing Video Search!',
        'icon': __imgsearch__, 'thumbnail': __imgsearch__,
        'path': plugin.url_for(endpoint=query, searchfor='LAST'),
        'is_playable': False
    }
    itemhistory = {
        'label': 'Search History',
        'icon': __imgsearch__, 'thumbnail': __imgsearch__,
        'path': plugin.url_for(endpoint=history),
        'is_playable': False
    }
    litems = [itemnew]
    litems.append(itemlast)
    litems.append(itemhistory)
    return litems

@plugin.route('/search/<query>/<offset>')
def search(query='', offset=0):
    litems = []
    filterterms = '-chica -novinha'
    replacestr = ' -site:youtube.com -site:dailymotion.com {0}'.format(filterterms)
    origquery = query
    query += replacestr
    burl = 'https://api.cognitive.microsoft.com/bing/v7.0/videos/search?count=50&offset={0}&safeSearch=Off&subscription-key=a2bbbe20b19543b9ab6dee3bac81d3da&q={1}'.format(offset, Quote(query))
    freshon = plugin.get_setting('freshon', bool)    
    if freshon:
        burl = 'https://api.cognitive.microsoft.com/bing/v7.0/videos/search?freshness=Month&count=50&offset={0}&safeSearch=Off&subscription-key=a2bbbe20b19543b9ab6dee3bac81d3da&q={1}'.format(offset, Quote(query))
    jresults = dl.getSource(url=burl)
    results = json.JSONDecoder(encoding='utf-8').decode(jresults)
    nextoff = results.get('nextOffset', 0)
    totalresults = results.get('totalEstimatedMatches', 0)
    for v in results.get('value', []):
        ctxlist = []
        img = v.get('thumbnailUrl', 'defaultvideo.png')
        durat = v.get('duration', '')
        lbl2 = v.get('description', v.get('hostPageUrl', v.get('contentUrl', '')))
        lbl = v.get('name', '')
        if len(durat) > 0:
            durationstr = durat[2:-1].replace('M', ':').replace('H', ':')
            durparts = durationstr.split(':')
            if len(durparts) < 3:
                if len(durparts) < 2:
                    durparts.insert(0, "00")
                durparts.insert(0, "00")
            dstr = ''
            dp = []
            for p in durparts:
                if len(p) < 2: p = "0"+p
                dp.append(p)
            durparts = dp
            durationstr = "{0}:{1}:{2}".format(dp[0], dp[1], dp[2])
            lbl += " [COLOR yellow]({0})[/COLOR]".format(durationstr)
        #playpath = plugin.url_for(endpoint=play, vurl=v.get('contentUrl', v.get('hostPageUrl', '')))
        vidhostedurl = v.get('contentUrl', v.get('hostPageUrl', ''))
        lbl2 += vidhostedurl
        #playpath = "plugin://plugin.video.wsonline/play/" + Quote(vidhostedurl)
        playpath = plugin.url_for(endpoint=play, vtitle=v.get('name', '').encode('latin'), vurl=vidhostedurl)
        item = {'label': lbl, 'label2': lbl2, 'thumbnail': img, 'icon': img, 'path': playpath, 'is_folder': False, 'is_playable': True}
        pathdl = plugin.url_for(endpoint=download, vurl=vidhostedurl)
        citem = ('Download', 'RunPlugin({0})'.format(pathdl),)
        ctxlist.append(citem)
        xitem = plugin._listitemify(item)
        xitem.add_context_menu_items(items=ctxlist, replace_items=False)
        xitem.playable = True
        xitem.is_folder = False
        xitem.set_info(info_type='video', info_labels={'Title': lbl, 'Plot': lbl2, 'Duration': durationstr, 'Premiered': v.get('datePublished', '')})
        xitem.thumbnail = img
        xitem.icon = img
        idvid = v.get('videoId', 0)
        if idvid is not 0:
            xitem.set_property(key='videoId', value=idvid)
            xitem.set_info(info_type='video', info_labels={'VideoID': idvid})
        #for vkey, vval in v.items():
        #    xitem.set_property(key=vkey, value=str(repr(vval)))
        #litems.append(item)
        litems.append(xitem)
    if  totalresults > int(offset)+50 or nextoff > int(offset)+50:
        nextlbl = "Next -> {0}-{1} of {2}".format(nextoff, str(nextoff+50), totalresults)
        nextitem = {'label': nextlbl, 'is_folder': True, 'icon': __imgnext__, 'thumbnail': __imgnext__, 'path': plugin.url_for(endpoint=search, query=origquery, offset=nextoff)}
        litems.append(plugin._listitemify(nextitem))
    return litems


@plugin.route('/query/<searchfor>')
def query(searchfor='LAST'):
    if searchfor == 'LAST':
        searchtxt = plugin.get_setting('lastsearch')        
    else:
        searchtxt = ""
    res = []
    def gettext(textdefault=''):
        searchtxt = plugin.keyboard(textdefault, 'Bing Video Search', False)
        if len(searchtxt) > 1:
            if searchtxt.find("[") != -1:
                searchtxt = searchtxt.replace("[who]", tplWho)
                searchtxt = searchtxt.replace("[what]", tplWhat)
                searchtxt = searchtxt.replace("[where]", tplWhere)
                searchtxt = searchtxt.replace("[wank]", tplWank)
                searchtxt = gettext(searchtxt)
        return searchtxt
    searchtxt = gettext(textdefault=searchtxt)
    if len(searchtxt) > 1:
        plugin.set_setting(key='lastsearch', val=searchtxt)
        history_add(query=searchtxt)
        res = search(searchtxt, 0)
    return res


@plugin.route('/history')
def history():
    item = {
        'label': '1: ',
        'icon': __imgsearch__, 'thumbnail': __imgsearch__,
        'path': plugin.url_for(endpoint=search, query='', offset=0),
        'is_playable': False
    }
    litems = []
    litems = history_load()
    xitems = []
    for item in litems:
        ctxlist = []
        snum = item.get('label', '0: ').split(':', 1)[0]
        pathdel = plugin.url_for(endpoint=history_del, num=int(snum))
        citem = ('DELETE', 'RunPlugin({0})'.format(pathdel),)
        ctxlist.append(citem)
        xitem = plugin._listitemify(item)
        xitem.add_context_menu_items(items=ctxlist, replace_items=False)
        xitems.append(xitem)
    return xitems


def history_load():
    litems = []
    histpath = os.path.join(plugin.storage_path, 'history.json')
    if not os.path.exists(histpath) or not os.path.isfile(histpath):
        histfile = file(histpath, mode='w')
        json.dump(litems,fp=histfile)
        histfile.close()
    histfile = file(histpath, mode='r')
    litems = json.load(fp=histfile)
    histfile.close()
    return litems


def history_add(query=''):
    litems = []
    litems = history_load()
    searchnum = len(litems) + 1
    lbl = "{0}: {1}".format(str(searchnum), query)
    item = {
        'label': lbl,
        'icon': __imgsearch__, 'thumbnail': __imgsearch__,
        'path': plugin.url_for(endpoint=search, query=query, offset=0),
        'is_playable': False
    }
    litems.append(item)
    histpath = os.path.join(plugin.storage_path, 'history.json')
    histfile = file(histpath, mode='w')
    json.dump(litems, fp=histfile)
    histfile.close()


@plugin.route('/history/del/<num>')
def history_del(num=0):
    litems = []
    litems = list(history_load())
    delitem = None
    for item in litems:
        hnum = item.get('label', '0: ').split(':', 1)[0]
        if int(hnum) == int(num):
            delitem = item
            break
    if delitem is not None:
        litems.remove(delitem)
        count = 1
        items = []
        for item in litems:
            lbl = item.get('label', '0: ')
            vnum = lbl.split(':', 1)[0]
            lbl = lbl.split(':', 1)[-1].strip()
            newlbl = "{0}: {1}".format(count, lbl)
            item.update({'label': newlbl})
            count+=1
            items.append(item)
        litems = items
        histpath = os.path.join(plugin.storage_path, 'history.json')
        histfile = file(histpath, mode='w')
        json.dump(litems, fp=histfile)
        histfile.close()
        plugin.notify(msg="DELETED #{0}: {1}".format(str(num), delitem.get('label', '')))
    else:
        plugin.notify(msg="ERROR deleting search #{0}".format(str(num)))
    xbmc.executebuiltin("Container.Refresh")


@plugin.route('/play/<vtitle>/<vurl>')
def play(vtitle="", vurl=""):
    playurl = ''
    if vurl is None or vurl == "":
        return []
    if vurl.find("%20") != -1 or vurl.find("+") != -1:
        vurl = Unquote(vurl)
    plugin.notify(msg=vurl)
    try:
        from YDStreamExtractor import getVideoInfo
        from YDStreamExtractor import handleDownload
        info = getVideoInfo(vurl, resolve_redirects=True)
        playurl = info.streamURL()
        plugin.log.info(msg="** PLAY VIDEO AT {0} **".format(vurl))
        plugin.log.info(msg=playurl)
        plugin.log.info(msg=str(repr(info)))
    except:
        plugin.notify(vurl, "Play Failed")
    if len(playurl) < 2:
        try:
            import urlresolver
            resolved = urlresolver.HostedMediaFile(vurl).resolve()
            if not resolved or resolved == False or len(resolved) < 1:
                resolved = urlresolver.resolve(vurl)
                if resolved is None or len(resolved) < 1:
                    resolved = urlresolver.resolve(Unquote(vurl))
            if len(resolved) > 1:
                playurl = resolved
        except:
            plugin.log.error(msg="** URL Resolver also failed **")
        playurl = vurl
        msg = "** Failed to resolve video at {0} to playable stream. **".format(vurl)
        plugin.log.error(msg=msg)
        plugin.notify(msg=msg, title="Play Failed")
        playurl = "plugin://plugin.video.wsonline/play/" + Quote(vurl)
        plugin.set_resolved_url(None)
        return None
    pitem = plugin._listitemify(item={'label': vtitle, 'label2': vurl, 'path': playurl})
    pitem.playable = True
    pitem.set_info(info_labels={'Title': vtitle, 'Plot': vurl + playurl}, info_type='video')
    pitem.add_stream_info('video', stream_values={})
    pitem.is_folder = False
    plugin.set_resolved_url(item=pitem)
    return pitem


@plugin.route('/download/<vurl>')
def download(vurl=None):
    if vurl is None:
        return []
    if vurl.find("%20") != -1 or vurl.find("+") != -1:
        vurl = Unquote(vurl)
    try:
        from YDStreamExtractor import getVideoInfo
        from YDStreamExtractor import handleDownload
        info = getVideoInfo(vurl, resolve_redirects=True)
        playurl = info.streamURL
        dlpath = plugin.get_setting('downloadPath')
        if not os.path.exists(dlpath):
            dlpath = xbmc.translatePath("home://")
        handleDownload(info, bg=True, path=dlpath)
        plugin.log.info(msg="** DOWNLOAD VIDEO AT {0} **".format(vurl))
        plugin.log.info(msg=playurl)
        plugin.log.info(msg=str(repr(info)))
    except:
        plugin.notify(vurl, "Download Failed")



if __name__ == '__main__':
    plugin.run()
    plugin.set_content(content='episodes')
    viewmode = 500
    viewmode = int(plugin.get_setting('viewmode'))
    plugin.set_view_mode(viewmode)
