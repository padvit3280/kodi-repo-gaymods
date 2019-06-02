# -*- coding: utf-8 -*-
import os, sys, ssl, time, datetime, json, re
from kodiswift import Plugin, ListItem, xbmc
from resources.lib import getoauth, TUMBLRAUTH, TumblrRestClient
from collections import namedtuple
from urllib import quote_plus
from operator import itemgetter

tclient = TumblrRestClient
viewmode = 20
APIOK = False
plugin = Plugin(name="TumblrV", addon_id="plugin.video.tumblrv", plugin_file="addon.py", info_type="video")
__addondir__ = xbmc.translatePath(plugin.addon.getAddonInfo('path'))
__resdir__ = os.path.join(__addondir__, 'resources')
__imgdir__ = os.path.join(__resdir__, 'images')
__imgsearch__ = os.path.join(__imgdir__, 'search.png')
__imgnext__ = os.path.join(__imgdir__, 'next.png')
__imgback__ = os.path.join(__imgdir__, 'back.png')
__imgtumblr__ = os.path.join(__imgdir__, 'tumblr.png')
tagpath = os.path.join(xbmc.translatePath('special://profile/addon_data/'), 'plugin.video.tumblrv', 'tagslist.json')
weekdelta = datetime.timedelta(days=7)
updatedelta = datetime.timedelta(minutes=10)
try:
    import web_pdb
except:
    web_pdb = None


@plugin.route('/')
def index():
    # setview_list()
    litems = []
    itemdashvids = {}
    itemliked = {}
    itemfollowing = {}
    itemtagbrowse = {}
    itemtagged = {}
    itemsearch = {}
    tstamp = str(time.mktime((datetime.datetime.now() - weekdelta).timetuple())).split('.', 1)[0]
    info = {"name": "Not logged in", "likes": 1, "following": 1}
    tinfo = namedtuple("tumblr_info", field_names=info.keys())(*info.values())
    try:
        userinforesp = tclient.info()
        if isinstance(userinforesp, dict):
            info = userinforesp.get("user", {})
            tinfo = namedtuple('tumblr_info', info.keys(), rename=True)(*info.values())
    except:
        plugin.notify("ERROR: Tumblr needs this addon to be authorized.")
    try:
        dashimg = 'http://api.tumblr.com/v2/blog/{0}/avatar/128'.format(tinfo.name)
        setlastup = plugin.get_setting('lastupdate', converter=str)
        setlastupdash = plugin.get_setting('lastupdatedash', converter=str)
        lastdashdate = datetime.datetime.utcfromtimestamp(float(setlastupdash))
        lastfoldate = datetime.datetime.utcfromtimestamp(float(setlastup))
        lbldash = "[COLOR red]Tumblr Dashboard:[/COLOR] [COLOR white][B]{0}[/B][/COLOR] [I](Posts Since {1} {2})[/I]".format(
            tinfo.name, lastdashdate.date().isoformat(), lastdashdate.time().isoformat().rpartition(':')[0])
        lblfoldate = "Updated {0} {1}".format(lastfoldate.date().isoformat(),
                                              lastfoldate.time().isoformat().rpartition(':')[0])
        lblfol = "[COLOR orange]Following:[/COLOR] [COLOR white][B]{0}[/B][/COLOR] [I]({1})[/I]".format(
            str(tinfo.following), lblfoldate)
        lbllike = "[COLOR pink]Liked:[/COLOR] [COLOR white][B]{0}[/B][/COLOR]".format(str(tinfo.likes))
        itemdash = ListItem(label=lbldash, icon=dashimg, thumbnail=dashimg,
                            path=plugin.url_for(dashboard, offset=0))  # , offset=0))
        itemfollowing = ListItem(label=lblfol, icon=__imgtumblr__, thumbnail=__imgtumblr__,
                                 path=plugin.url_for(blogs_following, offset=0))
        itemliked = ListItem(label=lbllike, icon="DefaultFolder.png", path=plugin.url_for(liked, offset=0))
        litems.append(itemdash)
        #litems.append(itemdashold)
        litems.append(itemfollowing)
        litems.append(itemliked)
        if doDebug():
            itemdebug = ListItem(label="Debug Tests", thumbnail="DefaultFolder.png", icon="DefaultTags.png",
                                 path=plugin.url_for(debugtest))
            litems.append(itemdebug)
    # itemargs = {'offset': 0, 'lastid':0}
    # itemdashvids = makeitem(name='Dashboard Videos', img=__imgtumblr__,  path='dashboard', kwargs=itemargs)
    # itemargs = {'offset':0}
    # itemliked = makeitem(name='Liked Videos', path='liked', kwargs=itemargs)
    # itemfollowing = makeitem(name='Following', path='blogs_following', kwargs=itemargs)
    # itemargs = {'timestamp': str(tstamp)}
    # itemtagbrowse = makeitem(name='Browse Tags', path='taglist', kwargs=itemargs) #dict(timestamp=str(tstamp)))
    # itemargs.update({'tagname': 0})
    # litems.append(itemdash)
    # litems.append(itemfollowing)
    # litems.append(itemliked)
    # litems.append(itemtagbrowse)
    except Exception as ex:
        outmsg = "{0}".format(str(ex))
        plugin.notify(msg=outmsg, delay=7000)
        print outmsg
    return litems


@plugin.route('/dashboard/<offset>')
def dashboard(offset=0):
    litems = []
    titems = []
    items = []
    lim = 20
    startat = 100
    off = 0
    newestid = 0
    nextoff = int(offset) + 100
    strpage = (nextoff / 100) + 1
    startid = 0
    try:
        startid = plugin.get_setting('lastid', converter=int)
        lim = 20
        for off in range(100, 0, (-1 * lim)):
            titems = tclient.dashboard(limit=lim, offset=off, type='video', since_id=startid).get("posts", [])
            # items = dashboard_items(tclient.dashboard(limit=lim, offset=off, type='video', since_id=startid).get("posts", []))
            # items = make_viditems(titems)
            items.extend(titems)
        newestiditem = items[0]
        newestid = newestiditem.get('timestamp', None)
        if newestiditem is not None:
            newestid = lbl2id(items[0].get('timestamp', startid))
            #newestid = newestiditem.get_property(key='id')
        litems = make_viditems(items)
        plugin.set_setting('lastid', newestid)
        pathnext = plugin.url_for(dashboard, offset=nextoff)
        nextitem = ListItem(label="[B]Next Page #{0}[/B] ->", icon=__imgnext__, thumbnail=__imgnext__, path=pathnext)
        litems.append(nextitem)
    except:
        pass
    try:
        if not doDebug():
            if newestid == 0:
                newestid = lbl2id(litems[-2].label2)  # .get_property(key='id')
            plugin.set_setting('lastid', newestid)
            stamp = str(time.mktime((datetime.datetime.now()).timetuple())).split('.', 1)[0]
            plugin.set_setting('lastupdatedash', stamp)
    except:
        pass
    return litems


@plugin.route('/liked/<offset>')
def liked(offset=0):
    # setview_thumb()
    likes = {}
    alltags = []
    litems = []
    listlikes = []
    likeitems = []
    strpage = str(((int(offset) + 100) / 100))
    nextitem = ListItem(label="Next Page -> #{0}".format(int(strpage) + 1), label2="Liked Videos", icon=__imgnext__,
                        thumbnail=__imgnext__, path=plugin.url_for(liked, offset=int(100 + int(offset))))
    nextitem.set_art({'poster': __imgnext__, 'thumbnail': __imgnext__, 'fanart': __imgnext__})
    nextitem.is_folder = True
    # litems = [nextitem]
    for coffset in range(0, 100, 20):
        results = tclient.likes(limit=20, offset=int(coffset))
        if results is not None:
            if results.get('liked_posts', '') is not None:
                likeitems = results.get('liked_posts', '')
                listlikes.extend(likeitems) # = results.get('liked_posts', '')
            else:
                likeitems = results.get(results.keys()[-1])
                listlikes.extend(likeitems) # = results.get(results.keys()[-1])
    '''
    for item in listlikes:
        if item.get('type', '') == 'video':
            b = {}
            b.update(item)
            lbl = ""
            lbl2 = ""
            img = item.get('thumbnail_url', item.get('image_permalink', item.get('image_permalink', "")))
            alltags.extend(item.get('tags', []))
            if img == '':
                img = __imgtumblr__
            try:
                if len(b.get('slug', '')) > 0:
                    lbl = b.get('slug', '')
                elif len(b.get('title', '')) > 0:
                    lbl = b.get('title', '')
                elif len(b.get('caption', '')) > 0:
                    lbl = Strip(b.get('caption', ''))
                elif len(b.get('summary', '')) > 0:
                    lbl = b.get('summary', '')
                elif len(b.get('source_title', '')) > 0:
                    lbl = b.get('source_title', '')
                else:
                    lbl = b.get('short_url', '')
                if len(item.get('summary', '')) > 0:
                    lbl2 = item.get('summary', '')
                else:
                    lbl2 = item.get('blog_name', "") + " / " + item.get('source_title', '') + "(" + item.get(
                        'slug_name', '') + ")"
            except:
                lbl = b.get(b.keys()[0], "")
                lbl2 = b.get(b.keys()[-1], "")
            vidurl = item.get('video_url', "")
            if vidurl is not None and len(vidurl) > 10:
                litem = ListItem(label=lbl, label2=lbl2, icon=img, thumbnail=img, path=vidurl)
                litem.playable = True
                litem.is_folder = False
                if item.get('date', '') is not None:
                    rdate = str(item.get('date', '')).split(' ', 1)[0].strip()
                litem.set_info(info_type='video', info_labels={'Date': rdate})
                litem.set_art({'poster': img, 'thumbnail': img, 'fanart': img})
                pathdl = plugin.url_for(endpoint=download, urlvideo=vidurl)
                litem.add_context_menu_items([('Download', 'RunPlugin({0})'.format(pathdl)), ])
                litems.append(litem)
    savetags(alltags)
    '''
    litems = make_viditems(listlikes)
    litems.append(nextitem)
    return litems


def dashboard_items(results=[]):
    alltags = []
    litems = []
    c = 0
    newitems = []
    #newitems = make_viditems(results)
    print("** DASHBOARD ITEMS: {0}".format(len(results)))
    for item in results:
        c = c + 1
        vidurl = item.get('video_url', '')
        try:
            b = {}
            b.update(item)
            vidid = b.get('id', 0)
            ctxlist = []
            lbl = ""
            lbl2 = ""
            vidurl = item.get('video_url', '')
            if vidid != 0:
                pathaddlike = plugin.url_for(endpoint=addlike, id=vidid)
                citemlike = ('[B][COLOR red]Like[/COLOR][/B]', 'RunPlugin({0})'.format(pathaddlike))
                ctxlist.append(citemlike)
            postblogname = b.get('blog_name', None)
            if postblogname is not None:
                pathtoblog = plugin.url_for(endpoint=blogposts, blogname=postblogname, offset=0)
                citemblog = ('[B]{0}[/B] Blog'.format(postblogname), 'RunPlugin({0})'.format(pathtoblog))
                ctxlist.append(citemblog)
            pathdl = plugin.url_for(endpoint=download, urlvideo=vidurl)
            citemdl = ('Download', 'RunPlugin({0})'.format(pathdl))
            ctxlist.append(citemdl)
            img = item.get('thumbnail_url', item.get('image_permalink', __imgtumblr__))
            alltags.extend(item.get('tags', []))
            try:
                reblog = b.get('reblog', {}).get('tree_html', None)
                if reblog is None or b.get('summary', None) is not None:
                    lblt = b.get('summary', b.get('caption', b.get('source_title', b.get('slug', b.get('title', b.get('short_url', b.get('blog_name','')))))))
                    lbl = "{0} [I]({1})[/I]".format(Strip(lblt), postblogname)
                else:
                    lbl = "{0} [I]({1})[/I]".format(Strip(reblog)) #.split(':', 1)[-1], postblogname)
            except:
                lbl = Strip(str(b.values()))
            try:
                lbl2 = b.get('blog_name', '') + " " + str(vidid) + " " + b.get('short_url', '')
                if item.get('video_url', None) is None:
                    if vidurl.find('.mp4') == -1 and len(vidurl) > 0:
                        vidurl = "plugin://plugin.video.hubgay/playtumblr/" + quote_plus(vidurl)
                    else:
                        vidurl = "plugin://plugin.video.hubgay/playmovie/" + quote_plus(b.get('short_url', b.get('source_url', '')))
                postdate = item.get('date', datetime.datetime.fromtimestamp(item.get('timestamp', None)).isoformat(sep=' ').rpartition(':')[0])
                if postdate is not None:
                    lbl2 += postdate
                else:
                    postdate = datetime.datetime.fromtimestamp(item.get('timestamp', 1500000000)).isoformat(sep=' ').rpartition(':')[0]
                postdate = postdate.split(' ', 1)[0]
                if doDebug():
                    lbl = "{0}: {1} ({2})".format(str(c), lbl, vidid)
            except:
                err = "**Trouble converting post to ListItem: " + str(b.get("id", 0)) + "\n" + b.get("source_url", "")
                plugin.log.error(err)
            litem = ListItem(label=lbl, label2="{0}|{1}".format(str(vidid), lbl2), icon=img, thumbnail=img, path=vidurl)
            litem.playable = True
            litem.is_folder = False
            litem.set_info(info_type='video', info_labels={'Date': postdate, 'Genre': str(vidid)})
            litem.set_art({'poster': img, 'thumbnail': img, 'fanart': img})
            try:
                litem.set_property(key='id', value=str(vidid))
                litem.add_context_menu_items(ctxlist)
            except Exception as ex:
                err = "Problem adding date, or prop or context to item:\n" + str(ex)
                plugin.log.error(err)
                plugin.notify(err)
            litems.append(litem)
        except Exception as ex:
            plugin.log.error(msg=ex)
            #print ("**ERROR CREATING DASHBOARD ITEMS**\n**{0}**\n--{1}--".format(str(ex)), str(item.values()))
            plugin.notify(ex)
    #savetags(alltags)
    #return litems #, alltags
    print("** CREATED ITEMS: {0}".format(len(litems)))
    return litems
    #return newitems


def dashboard_getitems(startoffset, max=60):
    offset = int(startoffset)
    item = {}
    litems = []
    postslist = []
    startid = plugin.get_setting('lastid', converter=int)
    startat = int(offset) + 100
    for offnum in range(startat, 0, -20):
        litems.extend(dashboard_items(
            tclient.dashboard(limit=20, offset=offnum, type='video', since_id=startid).get("posts", [])))
    
    nextoff = int(60 + int(offset))
    strpage = str(nextoff / 60)
    pathnext = plugin.url_for(dashboard, offset=nextoff)
    nextitem = ListItem(label="[B]Page #{0}[/B] ->".format(str(int(strpage) + 1)), label2=pathnext, icon=__imgnext__,
                        thumbnail=__imgnext__, path=pathnext)
    nextitem.set_art({'poster': __imgnext__, 'thumbnail': __imgnext__, 'fanart': __imgnext__})
    nextitem.is_folder = True
    litems.append(nextitem)
    if not doDebug():
        try:
            id1 = lbl2id(litems[0].label2)  # .get_property('id'))
            id2 = lbl2id(litems[-1].label2)  # .get_property('id'))
            plugin.notify("{0} {1}".format(str(id1), str(id2)))
            if id1 > id2:
                plugin.set_setting('lastid', str(id1).encode('utf-8', 'ignore'))
            else:
                plugin.set_setting('lastid', str(id2).encode('utf-8', 'ignore'))
        except:
            pass
    return litems


def make_viditems(listlikes=[]):
    litems = []
    alltags = []
    for item in listlikes:
        if item.get('type', '') == 'video':
            b = {}
            b.update(item)
            lbl = ""
            lbl2 = ""
            img = item.get('thumbnail_url', item.get('image_permalink', item.get('image_permalink', "")))
            alltags.extend(item.get('tags', []))
            if img == '':
                img = __imgtumblr__
            try:
                if len(b.get('slug', '')) > 0:
                    lbl = b.get('slug', '')
                elif len(b.get('title', '')) > 0:
                    lbl = b.get('title', '')
                elif len(b.get('caption', '')) > 0:
                    lbl = Strip(b.get('caption', ''))
                elif len(b.get('summary', '')) > 0:
                    lbl = b.get('summary', '')
                elif len(b.get('source_title', '')) > 0:
                    lbl = b.get('source_title', '')
                else:
                    lbl = b.get('short_url', '')
                if len(item.get('summary', '')) > 0:
                    lbl2 = item.get('summary', '')
                else:
                    lbl2 = item.get('blog_name', "") + " / " + item.get('source_title', '') + "(" + item.get(
                        'slug_name', '') + ")"
            except:
                lbl = b.get(b.keys()[0], "")
                lbl2 = b.get(b.keys()[-1], "")
            vidurl = item.get('video_url', "")
            if vidurl is not None and len(vidurl) > 10:
                litem = ListItem(label=lbl, label2=lbl2, icon=img, thumbnail=img, path=vidurl)
                litem.playable = True
                litem.is_folder = False
                if item.get('date', '') is not None:
                    rdate = str(item.get('date', '')).split(' ', 1)[0].strip()
                litem.set_info(info_type='video', info_labels={'Date': rdate})
                litem.set_art({'poster': img, 'thumbnail': img, 'fanart': img})
                pathdl = plugin.url_for(endpoint=download, urlvideo=vidurl)
                litem.add_context_menu_items([('Download', 'RunPlugin({0})'.format(pathdl)), ])
                litems.append(litem)
                #litems.append(makeitem(lbl, img, pathdl, True))
    # savetags(alltags)
    # litems.append(nextitem)
    return litems


@plugin.route('/addlike/<id>')
def addlike(id=0):
    try:
        tclient.like(None, id)
        plugin.notify(msg="LIKED: {0}".format(str(id)))
    except:
        plugin.notify(msg="Failed to add like: {0}".format(str(id)))


@plugin.route('/download/<urlvideo>')
def download(urlvideo):
    try:
        from YDStreamExtractor import getVideoInfo
        from YDStreamExtractor import handleDownload
        info = getVideoInfo(urlvideo, resolve_redirects=True)
        dlpath = plugin.get_setting('downloadpath')
        if not os.path.exists(dlpath):
            dlpath = xbmc.translatePath("home://")
        handleDownload(info, bg=True, path=dlpath)
    except:
        plugin.notify(urlvideo, "Download Failed")


@plugin.route('/blogposts/<blogname>/<offset>')
def blogposts(blogname, offset=0):
    listposts = []
    lbl = ''
    lbl2 = ''
    vidurl = ''
    results = []
    alltags = []
    litems = []
    if blogname.find('.') != -1:
        shortname = blogname.split('.', 1)[-1]
        if shortname.find('.') != -1:
            blogname = shortname.lsplit('.')[0]
    strpage = str((20 + int(offset)) / 20)
    nextitem = ListItem(label="Next Page -> #{0}".format(strpage), label2=blogname, icon=__imgnext__,
                        thumbnail=__imgnext__,
                        path=plugin.url_for(blogposts, blogname=blogname, offset=int(20 + int(offset))))
    nextitem.set_art({'poster': __imgnext__, 'thumbnail': __imgnext__, 'fanart': __imgnext__})
    nextitem.is_folder = True
    # litems = [nextitem]
    if blogname is not None:
        results = tclient.posts(blogname=blogname, limit=20, offset=int(offset), type='video')
        items = results.get('posts', [])
        for item in items:
            litems.append(makeitem(name=item.get('slug', blogname), img=item.get('thumbnail_url', 'DefaultVideo.png'),
                                   path=item.get('video_url'), playable=True, **item))
    else:
        results = tclient.posts(blogname=blogname, limit=20, offset=int(offset), type='video')
        if results is not None:
            if len(results.get('posts', '')) > 1:
                results = results.get('posts', '')
            for post in results:
                lbl2 = post.get('blog_name', '')
                lbl = post.get('slug', '').replace('-', ' ')
                img = post.get('thumbnail_url', post.get('image_permalink', __imgtumblr__))
                img2 = post.get('image_permalink', post.get('thumbnail_url', __imgtumblr__))
                alltags.extend(post.get('tags', []))
                try:
                    if post.get('slug', '') is not None:
                        lbl = post.get('slug', '').replace('-', ' ')
                    if len(post.get('caption', '')) > 0:
                        lbl = Strip(post.get('caption', ''))
                    elif len(post.get('summary', '')) > 0:
                        lbl = post.get('summary', '')
                    elif len(post.get('source_title', '')) > 0:
                        lbl = post.get('source_title', '')
                    else:
                        lbl = post.get('short_url', '')
                    if post.get('video_url', '') is not None:
                        vidurl = post.get('video_url', '')
                except:
                    plugin.notify(str(repr(post)))
                litem = ListItem(label=lbl, label2=lbl2, icon=img2, thumbnail=img, path=vidurl)
                litem.playable = True
                litem.is_folder = False
                if len(post.get('date', '')) > 0:
                    rdate = str(post.get('date', '')).split(' ', 1)[0].strip()
                litem.set_info(info_type='video', info_labels={'Date': rdate, 'Duration': post.get('duration', '')})
                litem.set_art({'poster': img2, 'thumbnail': img, 'fanart': img2})
                pathdl = plugin.url_for(endpoint=download, urlvideo=vidurl)
                pathaddlike = plugin.url_for(endpoint=addlike, id=post.get('id', ''))
                litem.add_context_menu_items(
                    [('Download', 'RunPlugin({0})'.format(pathdl)), ('Like', 'RunPlugin({0})'.format(pathaddlike)), ])
                litems.append(litem)
        else:
            litems = []
            backurl = ''
            if offset == 0:
                backurl = plugin.url_for(endpoint=blogs_following, offset=0)
            else:
                backurl = plugin.url_for(blogposts, blogname=blogname, offset=(int(offset) - 20))
            nextitem = ListItem(label="No Results - GO BACK".format(strpage), label2=blogname, icon=__imgtumblr__,
                                thumbnail=__imgtumblr__, path=backurl)
            nextitem.set_art({'poster': __imgtumblr__, 'thumbnail': __imgtumblr__, 'fanart': __imgtumblr__})
            nextitem.is_folder = True
            litems = [nextitem]
        savetags(alltags)
    litems.append(nextitem)
    return litems


@plugin.route('/posts/<blogname>/<offset>')
def posts(blogname, offset=0):
    postdata = tclient.posts(blogname=blogname, type='text', filter='video', offset=offset)
    postdata = postdata.get('response', {})
    postdata = postdata.get('posts', {"posts": [{"__type__": "Post"}]})
    listdata = json2obj(postdata)
    assert isinstance(listdata, namedtuple)


@plugin.route('/search')
def search():
    # plugin.log.debug(TUMBLRAUTH)
    # client = TumblrRestClient(**TUMBLRAUTH)
    # info = client.info()
    litems = []
    searchtxt = ''
    searchquery = ''
    offsetnum = 0
    searchtxt = plugin.get_setting('lastsearch')
    searchtxt = plugin.keyboard(searchtxt, 'Search All Sites', False)
    searchquery = searchtxt.replace(' ', '+')
    plugin.set_setting(key='lastsearch', val=searchtxt)
    results = following_list(offset=offsetnum)
    listmatch = []
    max = 20
    # if len(results) < 20:
    #    max = len(results) - 1
    for blog in results:
        name = blog.get('name', '')
        posts = tclient.posts(name, type='video')
        for post in posts.get('posts', []):
            for k, v in post.items():
                try:
                    if searchquery.lower() in str(v.encode('latin-1', 'ignore')).lower():
                        listmatch.append(post)
                        break
                except:
                    pass
    plugin.notify(msg="Matches: {0}".format(str(len(listmatch))))
    alltags = []
    for post in listmatch:
        lbl2 = post.get('blog_name', '')
        lbl = post.get('slug', '').replace('-', ' ')
        img = post.get('thumbnail_url', post.get('image_permalink', __imgtumblr__))
        img2 = post.get('image_permalink', post.get('thumbnail_url', __imgtumblr__))
        alltags.extend(post.get('tags', []))
        try:
            if post.get('slug', '') is not None:
                lbl = post.get('slug', '').replace('-', ' ')
            if len(post.get('caption', '')) > 0:
                lbl = Strip(post.get('caption', ''))
            elif len(post.get('summary', '')) > 0:
                lbl = post.get('summary', '')
            elif len(post.get('source_title', '')) > 0:
                lbl = post.get('source_title', '')
            else:
                lbl = post.get('short_url', '')
            if post.get('video_url', '') is not None:
                vidurl = post.get('video_url', '')
        except:
            plugin.notify(str(repr(post)))
        litem = ListItem(label=lbl, label2=lbl2, icon=img2, thumbnail=img, path=vidurl)
        litem.playable = True
        litem.is_folder = False
        if len(post.get('date', '')) > 0:
            rdate = str(post.get('date', '')).split(' ', 1)[0].strip()
        litem.set_info(info_type='video', info_labels={'Date': rdate, 'Duration': post.get('duration', '')})
        litem.set_art({'poster': img2, 'thumbnail': img, 'fanart': img2})
        pathdl = plugin.url_for(endpoint=download, urlvideo=vidurl)
        pathaddlike = plugin.url_for(endpoint=addlike, id=post.get('id', ''))
        litem.add_context_menu_items(
            [('Download', 'RunPlugin({0})'.format(pathdl)), ('Like', 'RunPlugin({0})'.format(pathaddlike)), ])
        litems.append(litem)
    savetags(alltags)
    return litems


def makeitem(name=None, img=None, path='blogposts', playable=False, **kwargs):
    # if doDebug():
    xitem = None
    try:
        if not path.startswith('plugin://'):
            itempath = plugin.url_for(endpoint=path, items=kwargs)
        else:
            itempath = path
        lbl2 = str(
            kwargs.get("label2", "") + Strip(kwargs.get('caption', itempath.partition('plugin.video.tumblrv/')[-1])))
        if img is None:
            img = kwargs.get('thumbnail_url', None)
            if img is None:
                img = "https://api.tumblr.com/v2/blog/{0}/avatar/64".format(name)
        xitem = ListItem(label=name, label2=lbl2, icon=img, thumbnail=img, path=itempath)
        xitem.playable = playable
        xitem.poster = img
        # litem = {'label': name, 'thumbnail': img, 'icon': img, 'is_playable': playable, 'path': itempath)}
        try:
            if plugin.request.path.find('following/') != -1 or plugin.request.path.find(
                    'liked/') != -1 or plugin.request.path.find('dashboard/') != -1:
                blogname = kwargs.get('blog_name', name)
                ctxaction = "RunPlugin({0})".format(plugin.url_for(endpoint=blogposts, blogname=blogname))
                cname = "[COLOR green]GOTO:[/COLOR] {0}".format(blogname)
                citem = (cname, ctxaction,)
                ctxlist.append(citem)
                vidurl = kwargs.get("vidurl", None)
                pathtoblog = plugin.url_for(blogposts, blogname=blogname, offset=0)
                citemblog = ('View Blog', 'RunPlugin({0})'.format(pathtoblog),)
                ctxlist.append(citemblog)
                if vidurl is not None:
                    pathdl = plugin.url_for(endpoint=download, urlvideo=vidurl)
                    citem = ('Download', 'RunPlugin({0})'.format(pathdl),)
                    ctxlist.append(citem)
                vidid = kwargs.get('id', None)
                if vidid is not None:
                    pathaddlike = plugin.url_for(endpoint=addlike, id=vidid)
                    citem = ('Like', 'RunPlugin({0})'.format(pathaddlike),)
                    ctxlist.append(citem)
            xitem.add_context_menu_items(items=ctxlist, replace_items=False)
        except:
            plugin.log.error("Failed to add context item to " + name)
    except Exception as ex:
        outmsg = "Error: {0}\n{1}\n{2}\n".format(str(ex), str(ex.message), str(ex.args))
        plugin.notify(msg=outmsg, delay=6000)
        print outmsg
    return xitem


@plugin.route('/debugtest')
def debugtest():
    allfollowedblogs = []
    if doDebug():
        web_pdb.set_trace()
        with web_pdb.catch_post_mortem():
            # allfollowedblogs = refresh_following()
            # save_following(allblogs=allfollowedblogs)
            allfollowedblogs = blogs_following(offset=0)
    else:
        # allfollowedblogs = refresh_following()
        # save_following(allblogs=allfollowedblogs)
        allfollowedblogs = blogs_following(offset=0)
    plugin.log.info(str(allfollowedblogs))
    return allfollowedblogs


@plugin.route('/indexold')
def indexold():
    curid, previd = get_postids()
    dashoffset = int(curid) - int(previd) * -1
    itemdashvids = {
        'label': 'Dashboard Videos',
        'thumbnail': __imgtumblr__,
        'path': plugin.url_for(endpoint=dashboard, offset=0, lastid=0),
        'is_playable': False}
    itemliked = {
        'label': 'Liked Videos',
        'thumbnail': __imgtumblr__,
        'path': plugin.url_for(endpoint=liked, offset=0),
        'is_playable': False}
    itemfollowing = {
        'label': 'Following',
        'thumbnail': __imgtumblr__,
        'path': plugin.url_for(endpoint=blogs_following, offset=0),
        'is_playable': False}
    itemtagbrowse = {
        'label': 'Browse Tags',
        'thumbnail': __imgtumblr__,
        'path': plugin.url_for(endpoint=taglist, timestamp=str(tstamp)),
        'is_playable': False}
    itemtagged = {
        'label': 'Search Tags',
        'thumbnail': __imgtumblr__,
        'path': plugin.url_for(endpoint=tags, tagname='0', timestamp=str(tstamp)),
        'is_playable': False}
    itemsearch = {
        'label': 'Search Tumblr',
        'thumbnail': __imgsearch__,
        'path': plugin.url_for(endpoint=search),
        'is_playable': False}


@plugin.route('/setup')
def setup():
    litems = []
    itemappkey = {
        'label': "Consumer KEY: {0}".format(TUMBLRAUTH['consumer_key']),
        'path': plugin.keyboard(default=TUMBLRAUTH['consumer_key'], heading=TUMBLRAUTH['consumer_key'])}
    itemappsecret = {
        'label': "Consumer SECRET: {0}".format(TUMBLRAUTH['consumer_secret']),
        'path': plugin.keyboard(default=TUMBLRAUTH['consumer_secret'], heading=TUMBLRAUTH['consumer_secret'])
    }
    itemurl = {
        'label': 'Visit: https://api.tumblr.com/console/calls/user/info\nenter Key and Secret from this screen',
        'path': plugin.url_for(endpoint=setup)
    }
    litems.append(itemurl)
    litems.append(itemappkey)
    litems.append(itemappsecret)
    return litems


@plugin.route('/taglist/<timestamp>')
def taglist(timestamp=0):
    # setview_list()
    if not os.path.exists(tagpath):
        json.dump([], fp=open(tagpath, mode='w'))
    litems = []
    alltags = json.load(open(tagpath))
    for tag in alltags:
        turl = plugin.url_for(tags, tagname=tag, timestamp=str(timestamp))
        li = ListItem(label=tag, label2=tag, icon=__imgtumblr__, thumbnail=__imgtumblr__, path=turl)
        li.is_folder = True
        litems.append(li)
    return litems


@plugin.route('/tags/<tagname>/<timestamp>')
def tags(tagname='', timestamp=0):
    atags = {}
    taglist = []
    litems = []
    if tagname == '0':
        tagname = plugin.keyboard(plugin.get_setting('lastsearch'), 'Search for tags')
        plugin.set_setting('lastsearch', tagname)
    nextstamp = time.mktime((datetime.datetime.fromtimestamp(float(timestamp)) - weekdelta).timetuple())
    nstamp = str(nextstamp).split('.', 1)[0]
    nextitem = ListItem(label="Next -> {0}".format(time.ctime(nextstamp)), label2="Tagged Videos", icon=__imgnext__,
                        thumbnail=__imgnext__, path=plugin.url_for(tags, tagname=tagname, timestamp=nstamp))
    nextitem.set_art({'poster': __imgnext__, 'thumbnail': __imgnext__, 'fanart': __imgnext__})
    nextitem.is_folder = True
    # litems = [nextitem]
    if tagname is not None and len(tagname) > 0:
        results = tclient.tagged(tagname, filter='text')  # ), before=float(timestamp))
        if results is not None:
            for res in results:
                if res.get('type', '') == 'video': taglist.append(res)
        for item in taglist:
            b = {}
            b.update(item)
            lbl = ""
            lbl2 = ""
            img = __imgtumblr__
            if 'thumb' in str(item.keys()[:]):
                if item.get('thumbnail_url', '') is not None:
                    img = item.get('thumbnail_url', '')  # .replace('https', 'http') #item.get('thumbnail_url','')
            elif 'image' in str(item.keys()[:]):
                if item.get('image_permalink', ""):
                    img = item.get('image_permalink', "")
            try:
                plugin.log.debug(msg=item.get('thumbnail_url', ''))
                if len(b.get('slug', '')) > 0:
                    lbl = b.get('slug', '')
                elif len(b.get('title', '')) > 0:
                    lbl = b.get('title', '')
                elif len(b.get('caption', '')) > 0:
                    lbl = Strip(b.get('caption', ''))
                elif len(b.get('summary', '')) > 0:
                    lbl = b.get('summary', '')
                elif len(b.get('source_title', '')) > 0:
                    lbl = b.get('source_title', '')
                else:
                    lbl = b.get('short_url', '')
                if len(item.get('summary', '')) > 0:
                    lbl2 = item.get('summary', '')
                else:
                    lbl2 = item.get('blog_name', "") + " / " + item.get('source_title', '') + "(" + item.get(
                        'slug_name', '') + ")"
            except:
                lbl = b.get(b.keys()[0], "")
                lbl2 = b.get(b.keys()[-1], "")
            vidurl = item.get('video_url', "")
            if vidurl is not None and len(vidurl) > 10:
                litem = ListItem(label=lbl, label2=lbl2, icon=img, thumbnail=img, path=vidurl)
                litem.playable = True
                litem.is_folder = False
                if item.get('date', '') is not None:
                    rdate = str(item.get('date', '')).split(' ', 1)[0].strip()
                litem.set_info(info_type='video', info_labels={'Date': rdate})
                litem.set_art({'poster': img, 'thumbnail': img, 'fanart': img})
                litems.append(litem)
    litems = [nextitem]
    return litems


@plugin.route('/setup/get')
def setup_get():
    token = plugin.keyboard(heading="OAUTH TOKEN")
    secret = plugin.keyboard(heading="OAUTH SECRET")
    plugin.set_setting('oauth_token', token)
    plugin.set_setting('oauth_secret', secret)
    TUMBLRAUTH['oauth_secret'] = secret
    TUMBLRAUTH['oauth_token'] = token
    try:
        client = TumblrRestClient(**TUMBLRAUTH)
        APIOK = True
    except:
        plugin.notify("Problem with the Tumblr OAUTH details", "Tumblr Login Failed")


def doDebug():
    return bool(plugin.get_setting(key='debugon', converter=bool))


def _json_object_hook(d):
    f = {}
    for k, v in enumerate(d):
        keyname = k.replace("_", "-")
        f.update({keyname: v})
    return namedtuple('tumblr', f.keys(), rename=True)(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)


def setview_list():
    plugin.notify(
        msg="{0} View: {1} / L{2} / T{3}".format(str(plugin.request.path), str(plugin.get_setting('viewmode')),
                                                 str(plugin.get_setting('viewmodelist')),
                                                 str(plugin.get_setting('viewmodethumb'))))
    try:
        if int(plugin.get_setting('viewmodelist')) == 0:
            viewselector = viewModes.Selector(20)
            viewmode = viewselector.currentMode
            plugin.set_setting('viewmodelist', viewmode)
    except:
        plugin.set_setting('viewmodelist', 20)
    plugin.notify(
        msg="{0} View: {1} / L{2} / T{3}".format(str(plugin.request.path), str(plugin.get_setting('viewmode')),
                                                 str(plugin.get_setting('viewmodelist')),
                                                 str(plugin.get_setting('viewmodethumb'))))


def setview_thumb():
    plugin.notify(
        msg="{0} View: {1} / L{2} / T{3}".format(str(plugin.request.path), str(plugin.get_setting('viewmode')),
                                                 str(plugin.get_setting('viewmodelist')),
                                                 str(plugin.get_setting('viewmodethumb'))))
    try:
        if int(plugin.get_setting('viewmodethumb')) == 0:
            viewselector = viewModes.Selector(500)
            viewmode = viewselector.currentMode
            plugin.set_setting('viewmodethumb', viewmode)
    except:
        plugin.set_setting('viewmodethumb', 500)
    plugin.notify(
        msg="{0} View: {1} / L{2} / T{3}".format(str(plugin.request.path), str(plugin.get_setting('viewmode')),
                                                 str(plugin.get_setting('viewmodelist')),
                                                 str(plugin.get_setting('viewmodethumb'))))

@ plugin.route('/blogsfollowing/<offset>')
def blogs_following(offset=0):
    blogs = {}
    litems = []
    blogres = []
    listblogs = []
    litems = []
    name = ''
    results = []
    updated = ''
    url = ''
    desc = ''
    strpage = (((int(offset) + 100) / 100)) + 1
    inforesp = tclient.info()
    totalfollow = int(inforesp.get('user', {}).get('following', 0))
    nextoff = int(offset) + 100
    nextoffmax = nextoff * 2
    try:
        if totalfollow != 0 and int(offset) > int(totalfollow):
            xbmc.executebuiltin('Action(Back)')
            return plugin.end_of_directory(succeeded=True, update_listing=False)
            # return plugin.redirect(plugin.url_for(endpoint=blogs_following, offset=int(offset)-100))
        if nextoffmax > int(totalfollow):
            nextoffmax = int(totalfollow)
        nextpath = plugin.url_for(blogs_following, offset=nextoff)
        nextlbl = "[COLOR white]{1} to {2} of [I]{3}[/I][/COLOR]\n  [COLOR yellow]Next ->[/COLOR] [COLOR orange]PG#{0}[/COLOR]   ".format(
            str(strpage), str(nextoff), str(nextoffmax), str(totalfollow))
        nextitem = ListItem(label=nextlbl, label2=str(nextoff), icon=__imgnext__, thumbnail=__imgnext__, path=nextpath)
        nextitem.set_art({'poster': __imgnext__, 'thumbnail': __imgnext__, 'fanart': __imgnext__})
        nextitem.is_folder = True
        if nextoff > int(totalfollow) and totalfollow != 0:
            nextitem.icon = __imgback__
            nextitem.thumbnail = __imgback__
        litems = [nextitem]
    except Exception as ex:
        print(str(ex))
        plugin.log.error(str(ex))
    lim = 20
    for offnum in range(int(offset), int(nextoff), lim):
        resp = tclient.following(offset=offnum, limit=lim)
        items = resp.get('blogs', None)
        if items is not None:
            results.extend(items)  # following_list(offset=offnum, max=20))  # max not working right now, max=50)
    for b in results:
        name = b.get('name', '')
        thumb = 'http://api.tumblr.com/v2/blog/{0}/avatar/64'.format(name)  # __imgtumblr__
        title = b.get('title', '')
        desc = Strip(b.get('description', ''))
        url = b.get('url', "http://{0}.tumblr.com".format(name))
        updated = b.get('updated', 0)
        updatetime = datetime.datetime.fromtimestamp(updated)
        updatetext = updatetime.isoformat()
        if len(thumb) < 46:  thumb = 'https://api.tumblr.com/v2/blog/{0}/avatar/64'.format(name)
        iurl = plugin.url_for(endpoint=blogposts, blogname=name, offset=0)
        try:
            lbl = "[COLOR yellow][B]{0}[/B][/COLOR] [COLOR green][B]{4}/{5}[/B][/COLOR]\n[COLOR white][I]{1}[/I][/COLOR] ({2}:{3})".format(
                name, title.encode('latin-1', 'ignore'), updatetime.time.hour, updatetime.time.minute,
                updatetime.date.day, updatetime.datetime.month)
            lbl2 = title + "\n" + desc.encode('latin-1', 'ignore')
            litem = ListItem(label=lbl, label2=str(updated), icon=thumb, thumbnail=thumb, path=iurl)
            litem.set_art({'poster': thumb, 'thumbnail': thumb, 'fanart': thumb})
            litem.is_folder = True
            # litem.playable = False
            litems.append(litem)
        except Exception as ex:
            print(ex)
            plugin.log.error(str(ex))
    return litems


def lbl2id(txt):
    try:
        id = int(txt.partition('|')[0])
    except:
        id = 0
    return id


def get_lastid():
    lastid = 0
    lastid = plugin.get_setting('lastid', int)
    if lastid == 0:
        lastid = 150000000000
    if lastid is None or lastid < 1000000:
        lastid = 150000000000
    return lastid


def get_postids(ForceUpdate=False):
    lastid = get_lastid()
    latestid = lastid
    if shouldUpdate() or ForceUpdate:
        results = tclient.dashboard(limit=1, type='video')
        apost = None
        posts = results.get('posts', None)
        if posts is None:
            posts = results.get('posts', results.get(results.keys()[-1], []))
        if not isinstance(posts, list):
            apost = posts.get(posts.keys()[-1], None)
        else:
            if len(posts) > 0:
                apost = posts.pop()
            else:
                apost = None
        if apost is not None:
            latestid = apost.get('id', lastid)
        if latestid != lastid:
            tstampnow = float(str(time.mktime((datetime.datetime.now()).timetuple())).split('.', 1)[0])
            plugin.set_setting('newid', latestid)
            plugin.set_setting('idupdate', str(tstampnow))
    else:
        latestid = plugin.get_setting('newid')
    return (latestid, lastid)


def shouldUpdate(checkDashboardId=True, checkFollowing=False):
    needsupdate = False
    needupdate = False
    lastup = None
    try:
        if checkFollowing:
            blogpath = tagpath.replace("tagslist.json", "following.json")
            if not os.path.exists(blogpath):
                return True
            lastupdated = plugin.get_setting('lastupdate', converter=str)
        else:
            lastupdated = plugin.get_setting('idupdate', converter=str)
        tstampnow = float(str(time.mktime((datetime.datetime.now()).timetuple())).split('.', 1)[0])
        if tstampnow - float(lastupdated) > 600:
            needsupdate = True
    except Exception as ex:
        errmsg = "**Failed to check whether an update is required. Update requested for**\n  Dashboard Posts: {0} Posts from Followed Blogs: {1}\n** {2} **".format(
            str(repr(checkDashboardId)), str(repr(checkDashboardId)), str(repr(ex)))
        plugin.log.error(msg=errmsg)
        needsupdate = True
    return True

def dashboard_broken(offset=0):
    # setview_thumb()
    likes = {}
    listlikes = []
    litems = []
    alltags = []
    nextoff = int(60 + int(offset))
    strpage = str(nextoff / 60)
    pathnext = plugin.url_for(dashboard, offset=nextoff)
    nextitem = ListItem(label="[B]Page #{0}[/B] ->".format(str(int(strpage) + 1)), label2=pathnext, icon=__imgnext__,
                        thumbnail=__imgnext__, path=pathnext)
    nextitem.set_art({'poster': __imgnext__, 'thumbnail': __imgnext__, 'fanart': __imgnext__})
    nextitem.is_folder = True
    litems = [nextitem]
    litems.append(dashboard_getitems(offset))
    return litems


def dashboard_old(listlikes, alltags, litems):
    for item in listlikes:
        if item.get('type', '') == 'video':
            b = item
            img = item.get("thumbnail_url", __imgtumblr__)
            img2 = item.get("image_permalink", __imgtumblr__)
            alltags.extend(item.get('tags', []))
            try:
                if len(b.get('slug', '')) > 0:
                    lbl = b.get('slug', '')
                elif len(b.get('title', '')) > 0:
                    lbl = b.get('title', '')
                elif len(b.get('caption', '')) > 0:
                    lbl = Strip(b.get('caption', ''))
                elif len(b.get('summary', '')) > 0:
                    lbl = b.get('summary', '')
                elif len(b.get('source_title', '')) > 0:
                    lbl = b.get('source_title', '')
                else:
                    lbl = b.get('short_url', '')
                if len(item.get('summary', '')) > 0:
                    lbl2 = item.get('summary', '')
                else:
                    lbl2 = item.get('blog_name', '') + " / " + item.get('source_title', '') + "(" + item.get(
                        'slug_name', '') + ")"
            except:
                lbl = b.get('blog_name', '')
                lbl2 = b.get('short_url', '')
            vidurl = item.get('video_url', '')
            img = item.get('thumbnail_url',
                           item.get('image_permalink', item.get('image_permalink', __imgtumblr__))).replace('https:',
                                                                                                            'http:')
            img2 = item.get('image_permalink',
                            item.get('thumbnail_url', item.get('thumbnail_url', __imgtumblr__))).replace('https:',
                                                                                                         'http:')
            if vidurl is not None and len(vidurl) > 10:
                if len(b.get('caption', '')) > 0:
                    lbl = Strip(b.get('caption', ''))
                litem = ListItem(label=lbl, label2=lbl2, icon=img2, thumbnail=img, path=vidurl)
                litem.playable = True
                litem.is_folder = False
                if item.get('date', '') is not None:
                    rdate = str(item.get('date', '')).split(' ', 1)[0].strip()
                litem.set_info(info_type='video', info_labels={'Date': rdate})
                litem.set_art({'poster': img2, 'thumbnail': img, 'fanart': img2})
                pathdl = plugin.url_for(endpoint=download, urlvideo=vidurl)
                pathaddlike = plugin.url_for(endpoint=addlike, id=item.get('id', ''))
                litem.add_context_menu_items(
                    [('Download', 'RunPlugin({0})'.format(pathdl)), ('Like', 'RunPlugin({0})'.format(pathaddlike)),
                     ('Show Image', 'ShowPicture({0})'.format(img)), ])
                litems.append(litem)
    item = listlikes[-1]
    plugin.set_setting('lastid', str(item.get('id', lastid)))
    savetags(alltags)
    # litems.append(nextitem)
    return litems


def refresh_following():
    # blogpath = tagpath.replace("tagslist.json", "following.json")
    # needsupdate = False
    # if not os.path.exists(blogpath):
    #    needsupdate = True
    # lastupdated = plugin.get_setting('lastupdate')
    # tstamp = str(time.mktime((datetime.datetime.now() - updatedelta).timetuple())).split('.', 1)[0]
    # tstampnow = float(str(time.mktime((datetime.datetime.now()).timetuple())).split('.', 1)[0])
    # if tstampnow - float(lastupdated) > 600:
    #    needsupdate = True
    # if not shouldUpdate(checkFollowing=True):
    #    allblogs = []
    #    allblogs_temp = []
    #    allblogs_temp = json.load(fp=open(tagpath.replace("tagslist.json", "following.json"), mode='r'))
    #    for blog in allblogs:
    #        newblog = dict(blog)
    #        newblog['description'] = Strip(blog['description'])
    #        allblogs.append(newblog)
    #    return allblogs
    litems = []
    allblogs = []
    blogs = []
    offset = 0
    total = 0
    resp = tclient.following(offset=0, limit=20)  # tclient.dashboard(type='videos')
    results = resp.get('blogs', {})
    total = len(results)  # int(results.get('total_blogs', 0))
    for offset in range(0, total, 20):
        resp = tclient.following(offset=offset, limit=20)
        # results = resp.get('response', {})
        blogs = resp.get('blogs', [])  # results.get('blogs', [])
        blogs.sort(key=itemgetter('updated'), reverse=True)
        for item in blogs:
            allblogs.append(item)
    allblogs.sort(key=itemgetter('updated'), reverse=True)
    save_following(allblogs)
    plugin.set_setting('lastupdate', str(time.mktime((datetime.datetime.now()).timetuple())).split('.', 1)[0])
    return allblogs


def save_following(allblogs=[]):
    blogpath = tagpath.replace("tagslist.json", "following.json")
    outlist = []
    for blog in allblogs:
        newblog = {}
        newblog.update(blog)
        newblog['thumb'] = u'http://api.tumblr.com/v2/blog/{0}/avatar/64'.format(blog.get('name', 'tumblr'))
        newblog['description'] = Strip(blog.get('description', ''))
        outlist.append(newblog)
    plugin.set_setting('lastupdate', str(time.mktime((datetime.datetime.now()).timetuple())).split('.', 1)[0])
    json.dump(outlist, fp=open(blogpath, mode='w'))


def following_list(offset=0, max=0):
    litems = []
    xitems = []
    blogs = []
    offset = 0
    total = 0
    lim = 20
    about = ''
    resp = tclient.following(offset=offset, limit=1)  # .get('response', {'total_blogs': 0, 'blogs': []})
    totalblogs = resp.get('total_blogs', 0)
    blogs = resp.get('blogs', [])
    for offnum in range(20, totalblogs, lim):
        resp = tclient.following(offset=offnum, limit=lim)
        bloglist = resp.get('blogs', [])
        blogs.extend(bloglist)  # .get('blogs', []))
    if max > len(blogs) or max == 0:
        max = len(blogs) - offset
        blogs = blogs[offset:]
    else:
        blogs = blogs[offset:max]
    try:
        for blog in blogs:
            updatetext = datetime.datetime.fromtimestamp(blog.get('updated'), 0).isoformat(sep=' ')
            # updatetext = "[B]{0}:{1}[/B] [I]{2}/{3}[/I]".format(updatedate.time().hour, updatedate.time().minute, updatedate.day, updatedate.month)
            blogname = blog.get('name', '')
            thumb = "https://api.tumblr.com/v2/blog/{0}/avatar/64".format(blogname)
            description = Strip(blog.get('description', '').partition('\n')[0])
            try:
                if len(description) > len(blogname) * 2:
                    splitidx = description.find('.')
                    if splitidx != -1:
                        if splitidx < len(blogname):
                            splitidx + 10
                    else:
                        splitidx = description.find(',')
                        if splitidx == -1:
                            splitidx = len(blogname) + 10
                    if splitidx < len(blogname):
                        splitidx = len(blogname)
                    about = str(description[0:splitidx]).strip() + '..'
                else:
                    about = description.strip()
                    if about.find('>') != -1:
                        about = about.partition('>')[-1].strip()
                about = "{0}".format(about)
                if thumb == '':
                    thumb = "https://api.tumblr.com/v2/blog/{0}/avatar/64".format(blog.get('name', __imgtumblr__))
            except:
                pass
            newitem = {'name': blogname, 'thumb': thumb, 'updated': updatetext, 'description': about}
            litems.append(newitem)
            li = ListItem(label=blogname, label2=updatetext, icon=thumb, thumbnail=thumb,
                          path=plugin.url_for(endpoint=blogposts, blogname=blogname, offset=0))
            xitems.append(li)
    except Exception as ex:
        print str(repr(ex))
    try:
        litems.sort(key=itemgetter('updated'), reverse=True)
        xitems.sort(key=itemgetter('label2'), reverse=True)
        save_following(litems)
    except:
        plugin.log.error("Couldn't sort following list")
    return xitems


def savetags(taglist=[]):
    if not os.path.exists(tagpath):
        json.dump([], fp=open(tagpath, mode='w'))
    taglist.extend(json.load(open(tagpath, mode='r')))
    alltags = sorted(set(taglist))
    json.dump(alltags, fp=open(tagpath, mode='w'))


def Strip(text):
    notagre = re.compile(r'[<\[\'\"].+?[>\]\'\"]')
    return notagre.sub(' ', text).strip()


if __name__ == '__main__':
    TUMBLRAUTH = dict(consumer_key='5wEwFCF0rbiHXYZQQeQnNetuwZMmIyrUxIePLqUMcZlheVXwc4',
                      consumer_secret='GCLMI2LnMZqO2b5QheRvUSYY51Ujk7nWG2sYroqozW06x4hWch',
                      oauth_token='7OaJ7GOFwVxi4VnquAY7E7kcJ3LMX7B0WcIX1zakhQ2p46xxDj',
                      oauth_secret='RdF74sWaG0N6GXQo0P7iq1wLIutkYaHoSf05WX5rFYrMMmcXKk')
    try:
        tclient = TumblrRestClient(**TUMBLRAUTH)
        if tclient is not None:
            info = tclient.info()
            print info
            APIOK = True
    except:
        tclient = None
        APIOK = False
        print "Couldn't get TumblrRestClient object"
    try:
        if tclient is None and not APIOK:
            otoken = plugin.get_setting('oauth_token')
            osecret = plugin.get_setting('oauth_secret')
            TUMBLRAUTH.update({'oauth_token': otoken, 'oauth_secret': osecret})
            tclient = TumblrRestClient(**TUMBLRAUTH)
            info = tclient.info()
            if info is not None and 'user' in info.keys():
                APIOK = True
            else:
                APIOK = False
    except:
        APIOK = False
        try:
            TUMBLRAUTH = getoauth()
            tclient = TumblrRestClient(**TUMBLRAUTH)
            info = tclient.info()
            if info is not None and info.get('user', None) is not None:
                APIOK = True
            else:
                APIOK = False
        except:
            plugin.notify(
                msg="Required Tumblr OAUTH token missing..Backup plan!",
                title="Tumblr Login Failed", delay=10000)
            plugin.log.error(
                msg="Tumblr API OAuth settings invalid. This addon requires you to authorize this Addon in your Tumblr account and in turn in the settings you must provide the TOKEN and SECRET that Tumblr returns.\nhttps://api.tumblr.com/console/calls/user/info\n\tUse the Consumer Key and Secret from the addon settings to authorize this addon and the OAUTH Token and Secret the website returns must be put into the settings.")
            try:  # Try an old style API key from off github as a backup so some functionality is provided?
                TUMBLRAUTH = dict(consumer_key='5wEwFCF0rbiHXYZQQeQnNetuwZMmIyrUxIePLqUMcZlheVXwc4',
                                  consumer_secret='GCLMI2LnMZqO2b5QheRvUSYY51Ujk7nWG2sYroqozW06x4hWch',
                                  oauth_token='RBesLWIhoxC1StezFBQ5EZf7A9EkdHvvuQQWyLpyy8vdj8aqvU',
                                  oauth_secret='GQAEtLIJuPojQ8fojZrh0CFBzUbqQu8cFH5ejnChQBl4ljJB4a')
                TUMBLRAUTH.update({'api_key', '5wEwFCF0rbiHXYZQQeQnNetuwZMmIyrUxIePLqUMcZlheVXwc4'})
                tclient = TumblrRestClient(**TUMBLRAUTH)
            except:
                plugin.notify(msg="Read Settings for instructions", title="COULDN'T AUTH TO TUMBLR")
    viewmode = int(plugin.get_setting('viewmode'))
    plugin.run()
    ctxlist = []
    plugin.set_content(content='movies')
    viewmodel = 500
    viewmodet = 500
    viewmodel = int(plugin.get_setting('viewmodelist'))
    viewmodet = int(plugin.get_setting('viewmodethumb'))
    plugin.set_view_mode(viewmodel)
    if str(plugin.request.path).startswith('/taglist/') or str(plugin.request.path).find(
            '/dashboard/') != -1 or plugin.request.path == '/':  # or str(plugin.request.path).startswith('/blogsfollowing/')
        plugin.set_view_mode(viewmodel)
    else:
        plugin.set_view_mode(viewmodet)
    #    viewmodel = int(plugin.get_setting('viewmodelist'))
    #    if viewmodel == 0:
    #        viewmodel = 504
    #    plugin.set_view_mode(viewmodel)
    # else:
    #    viewmodet = int(plugin.get_setting('viewmodethumb'))
    #    if viewmodet == 0:
    #        viewmodet = 504
    #    plugin.set_view_mode(viewmodet)
