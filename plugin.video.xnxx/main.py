# -*- coding: utf-8 -*-
# Module: default
# Author: moedje (Roman V. M. example plugin as template)
# Created on: 28.11.2014
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
import sys, json, os, re
from urllib import urlencode
from urlparse import parse_qsl
from simpleplugin import Plugin
import simpleutils
import xbmc, xbmcgui
plugin = Plugin()
# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])
__addondir__ = xbmc.translatePath(plugin.addon.getAddonInfo('path'))
__resources__ = os.path.join(__addondir__, 'resources/')
VIDEOS = json.load(file(os.path.join(__resources__, 'tags.json')))
urlorientation = 'straight'
urlsort = 'uploaddate'
urlorientation = plugin.get_setting('filterorientation')
urlsort = plugin.get_setting('sortby')

@plugin.action()
def root():
    """
    Root virtual folder

    This is mandatory item.
    """
    listitems = []
    for tagkey in VIDEOS.iterkeys():
        numtags = str(len(VIDEOS[tagkey]))
        label = "{0} [COLOR white][I]({1})[/I][/COLOR]".format(tagkey, numtags)
        tagpath = plugin.get_url(action='taglistforletter', tagkey=tagkey)
        listitems.append({'label': label, 'label2': numtags, 'url': tagpath})
    return plugin.create_listing(listitems, succeeded=True, update_listing=False, cache_to_disk=False, view_mode=50, content='movies')
    #return listitems


@plugin.action()
def taglistforletter(params):
    """Virtual subfolder"""
    # Create 1-item list with a link to a playable video.
    plugin.log(message=str("** Taglist: " + str(repr(params))), level=xbmc.LOGERROR)
    listitems = []
    for item in VIDEOS.get(params.tagkey, []):
        tagname = item.get('tagname', None)
        if tagname is not None:
            tagpath = plugin.get_url(action='videosfortag', tagname=tagname, page=1)
            litem = {'label': item.get('name', tagname), 'thumb': item.get('thumb', 'DefaultFolder.png'), 'url': tagpath}
            listitems.append(litem)
    #return listitems
    return plugin.create_listing(listitems, succeeded=True, update_listing=False, cache_to_disk=False, view_mode=51, content='movies')


@plugin.action()
def videosfortag(params):
    plugin.log(message=str("** videosfortag: " + str(repr(params))), level=xbmc.LOGERROR)
    webreq = simpleutils.CachedWebRequest(cookiePath=os.path.join(xbmc.translatePath('special://profile'),'addon_data/', plugin.id))
    revidparts = re.compile(ur'video_([\d]+).*? src="(.*?)".*?a href="(.*?)".*?title="(.*?)".*?"duration">[\(](.+?)[\)]</span',re.DOTALL)
    tagname = params.tagname
    pagenum = '1'
    doup = False
    if params.page is not None:
        pagenum = params.page
    tagurl = "http://www.xnxx.com/tags/{0}/{1}/t:{2}/s:{3}".format(tagname, str(pagenum), urlorientation, urlsort)
    pagenum = str(1 + int(pagenum))
    nexturl = "http://www.xnxx.com/tags/{0}/{1}/t:{2}/s:{3}".format(tagname, str(pagenum), urlorientation, urlsort)
    nextpagepath = plugin.get_url(action='videosfortag', tagname=tagname, page=pagenum)
    nextitem = {'label': 'Next -> #{0}'.format(pagenum), 'label2': nexturl, 'thumb': os.path.join(__resources__, 'next.png'), 'url': nextpagepath}
    try:
        resp = webreq.getSource(url=tagurl).encode('latin-1', 'ignore')
        html = resp.partition('div class="mozaique"')[-1].rpartition('class="no-page">Next</a>')[0]
    except:
        plugin.log('Error downloading page', xbmc.LOGERROR)
    try:
        resp = webreq.getSource(url=tagurl)
        html = simpleutils.try_coerce_native(resp).partition('div class="mozaique"')[-1].rpartition('class="no-page">Next</a>')[0]
    except:
        plugin.log('Error downloading page', xbmc.LOGERROR)
    #notifytxt = "Notification('{0} {1}', '{2}')".format(params.page, tagurl, html)
    #xbmc.executebuiltin(notifytxt)
    #plugin.log(notifytxt, xbmc.LOGNOTICE)
    matches = re.compile(ur'<div id="(video_.*?)</p></div>', re.DOTALL).findall(html)
    listitems = []
    for vidhtml in matches:
        vmatches = revidparts.findall(vidhtml)
        if vmatches is not None:
            for vidid, thumb, link, title, length in vmatches:
                linkfull = 'https://flashservice.xvideos.com/embedframe/' + vidid
                label = title + " [COLOR white][I][B]({0})[/B][/I][/COLOR]".format(length)
                label2 = linkfull
                itempath = plugin.get_url(action='play', url=linkfull)
                mitem = {'label': label, 'label2': label2, 'thumb': thumb.replace('THUMBNUM', '1'), 'url': itempath, 'is_playable': True}
                listitems.append(mitem)
    listitems.append(nextitem)
    if int(pagenum) > 1: doup = True
    return plugin.create_listing(listitems, succeeded=True, update_listing=doup, cache_to_disk=False, view_mode=500, content='movies')

# An action can take an optional argument that contain
# plugin call parameters parsed into a dict-like object.
# The params object allows to access parameters by key or by attribute
@plugin.action()
def play(params):
    """Play video"""
    # Return a string containing a playable video URL
    plugin.log(message=str("** play: " + str(repr(params))), level=xbmc.LOGINFO)
    vidurl = params.url
    webreq = simpleutils.CachedWebRequest(cookiePath=os.path.join(xbmc.translatePath('special://profile'), 'addon_data/', plugin.id))
    resp = simpleutils.to_unicode(webreq.getSource(vidurl))
    movurl = resp.split("html5player.setVideoUrlHigh('",1)[-1].split("'",1)[0]
    if not movurl.startswith('http'):
        matches = re.compile(ur"html5player.setVideoUrlHigh\('(.*?)'").findall(resp)
        if matches is not None:
            if isinstance(matches, list):
                movurl = matches.pop()
            else:
                moveurl = matches
    plugin.log(message="Video url: " + movurl, level=xbmc.LOGINFO)
    return movurl


def get_categories(ITEMS):
    """
    Get the list of video categories.

    Here you can insert some parsing code that retrieves
    the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    from some site or server.

    .. note:: Consider using `generator functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :return: The list of video categories
    :rtype: list
    """
    if isinstance(ITEMS, list):
        keys = []
        for ITEM in ITEMS:
            keys.append(ITEM.iterkeys())
        return keys
    else:
        return ITEMS.iterkeys()

def get_videos(category):
    """
    Get the list of videofiles/streams.

    Here you can insert some parsing code that retrieves
    the list of video streams in the given category from some site or server.

    .. note:: Consider using `generators functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :param category: Category name
    :type category: str
    :return: the list of videos in the category
    :rtype: list
    """
    return VIDEOS[category]

def list_tags(ITEMS):
    list_items = []
    for ITEM in ITEMS:
        thumbimg = ITEM.get('thumb', 'DefaultFolder.png')
        name = ITEM.get('name', '')
        tagname = ITEM.get('tagname', '')
        genre = ITEM.get('genre', '')
        list_item = xbmcgui.ListItem(label=name, label2=genre)
        list_item.setArt({'thumb': thumbimg, 'icon': thumbimg, 'fanart': thumbimg})
        list_item.setInfo('video', {'title': name, 'genre': tagname})
        url = get_url(action='list_videos', tagname=tagname)
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)

def get_tag(tagname):
    xurl = 'http://www.xnxx.com/tags/{0}/t:gay/s:uploaddate'.format(tagname)

def list_categories(ITEMS=VIDEOS):
    """
    Create the list of video categories in the Kodi interface.
    """
    # Get video categories
    #categories = get_categories(ITEMS)
    # Iterate through categories
    for category in VIDEOS.iterkeys():
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category)
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        thumbimg = ITEMS.get(category, [{'thumb': 'DefaultFolder.png'}])[0].get('thumb', 'DefaultVideo.png')
        list_item.setArt({'thumb': thumbimg,
                          'icon': thumbimg,
                          'fanart': thumbimg})
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        list_item.setInfo('video', {'title': category, 'genre': category})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='listing', category=category)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)

def list_videos(category, **kwargs):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: Category name
    :type category: str
    """
    # Get the list of videos in the category.
    if isinstance(kwargs, list):
        videos = kwargs
    else:
        videos = get_videos(category)
    # Iterate through videos.
    for video in videos:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=video['name'])
        # Set additional info for the list item.
        list_item.setInfo('video', {'title': video['name'], 'genre': video['genre']})
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(action='play', video=video['video'])
        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)

if __name__ == '__main__':
    plugin.run()  # Start plugin
    #viewmodeid = plugin.get_setting('viewmode')


'''
def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'list_videos':
            tagname = params['tagname']
            ITEMS = get_tag(tagname)
            list_videos(tagname, ITEMS)
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            ITEMS = VIDEOS.get(params['category'], None)
            if ITEMS is not None:
                list_tags(ITEMS)
            else:
                list_videos(params['category'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_categories(VIDEOS)


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])

'''
