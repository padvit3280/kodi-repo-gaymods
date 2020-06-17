import json
import os.path as Path

class kodiSearch(list):

    def __init__(self, history_file='history.json', path=None, addonpath=None, urlnewsearch=None, urldosearch=None, items=[]):
        self.FILEHISTORY = None
        self.ICONFOLDER = 'DefaultFolder.png'
        self.ICONSEARCH = '../search.png'
        self.ADDONPATH = addonpath
        self.URLNEWSEARCHACTION = urlnewsearch
        self.URLDOSEARCHACTION = urldosearch
        self.litem_search = {}
        self.litem_clear = {}
        if path is None:
            self.FILEHISTORY = history_file
            if not Path.exists(history_file):
                self.FILEHISTORY = Path.join(Path.realpath(Path.curdir), history_file)
        else:
            self.FILEHISTORY = Path.join(Path.realpath(path), history_file)
        if not Path.isfile(self.FILEHISTORY):
            if not Path.exists(Path.dirname(self.FILEHISTORY)):
                self.FILEHISTORY = Path.join(Path.realpath(Path.curdir), 'history.json')
        historyitems = self.gethistory()
        if len(items) > 0:
            allitems = list(set(items.extend(historyitems)))
        else:
            allitems = historyitems
        super(kodiSearch, self).__init__(allitems)

    def save(self):
        try:
            json.dump(self, fp=open(self.FILEHISTORY, mode='wb'))
        except:
            print("Error Saving Search History List to {0}".format(self.FILEHISTORY))

    def append(self, listitem):
        litem = {'label': '', 'label2': '', 'icon': self.ICONFOLDER, 'thumb': self.ICONFOLDER, 'is_folder': True, 'is_playable': False, 'path': ''}
        litem.update(listitem)
        super(kodiSearch, self).append(litem)
        self.save()

    def add(self, query=''):
        safequery = query.replace(' ', '+')
        pluginpath = self.URLDOSEARCHACTION.replace('-QUERY-', safequery)
        litem = {'label': query, 'label2': 'Search for {0}'.format(query), 'icon': self.ICONFOLDER, 'thumb': self.ICONFOLDER,
                 'is_playable': False, 'path': pluginpath}
        self.append(litem)
        return litem

    def load(self):
        return self.extend(self.gethistory())

    def search(self, func_getinput=None):
        item = {}
        if func_getinput is not None:
            query = func_getinput.__call__()
            item = self.add(query)
        return item

    def clear(self):
        super(kodiSearch, self).clear()
        self.save()

    def gethistory(self):
        items = []
        if Path.exists(self.FILEHISTORY) and Path.isfile(self.FILEHISTORY):
            items = json.load(fp=open(self.FILEHISTORY, mode='rb'), strict=False)
        if isinstance(items, list):
            return items
        else:
            super(kodiSearch, self).__init__([])
            self.save()
            return []

    @property
    def ListItemNewSearch(self):
        self.litem_search = {'label': '[B]New Search[/B]', 'label2': 'New Search', 'icon': self.ICONSEARCH,
                             'thumb': self.ICONSEARCH, 'is_folder': True, 'is_playable': False,
                             'path': self.URLNEWSEARCHACTION}
        return self.litem_search

    @property
    def ListItemClear(self):
        self.litem_clear = {'label': 'Clear History', 'label 2': 'Clear Search History', 'icon': 'DefaultFolder.png', 'path': self.URLDOSEARCHACTION.replace('action=show_search', 'action=search_clear')}
        return self.litem_clear

    @property
    def AddonSearchPaths(self):
        return self.ADDONPATH, self.URLNEWSEARCHACTION, self.URLDOSEARCHACTION

    @AddonSearchPaths.setter
    def AddonSearchPaths(self, addonpath='', urlnewsearch='', urldosearch=''):
        self.ADDONPATH = addonpath
        self.URLNEWSEARCHACTION = urlnewsearch
        self.URLDOSEARCHACTION = urldosearch
