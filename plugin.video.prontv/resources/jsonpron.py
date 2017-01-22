
class Metatags(object):

    def __init__(self, **kwargs):
        """
        : attribute lang : string
        : attribute sourceurl : string
        : attribute metatags : array
        : attribute sourcetitle : string
        : attribute value : string
        : attribute sourcename : string
        : attribute name : string
        """
        self.lang = None
        self.sourceurl = None
        self.metatags = None
        self.sourcetitle = None
        self.value = None
        self.sourcename = None
        self.name = None
        if len(kwargs) > 0:
            self.__fromdict__(**kwargs)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __fromdict__(self, **kwargs):
        for k, v in kwargs.items():
            self[k] = v

class Result(object):

    def __init__(self, **kwargs):
        """
        : attribute sourcename : string
        : attribute modified : string
        : attribute sourceurl : string
        : attribute sourcetitle : string
        : attribute hosterurls : array
        : attribute stream : bool
        : attribute metatags : Metatags
        : attribute title : string
        : attribute tags : string
        : attribute download : bool
        : attribute imageid : string
        : attribute created : string
        : attribute extension : string
        : attribute hostername : string
        : attribute lang : string
        : attribute sizeinternal : float
        : attribute checked : string
        """
        self.sourcename = None
        self.modified = None
        self.sourceurl = None
        self.sourcetitle = None
        self.hosterurls = None
        self.stream = None
        self.metatags = None
        self.title = None
        self.tags = None
        self.download = None
        self.imageid = None
        self.created = None
        self.extension = None
        self.hostername = None
        self.lang = None
        self.sizeinternal = None
        self.checked = None
        if len(kwargs) > 0:
            self.__fromdict__(**kwargs)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __fromdict__(self, **kwargs):
        for k,v in kwargs.items():
            self.__setattr__(k, v)


class Hosterurls(object):

    def __init__(self, **kwargs):
        """
        : attribute filedataid : string
        : attribute url : string
        : attribute filedata : Filedata
        : attribute part : float
        """
        self.filedataid = None
        self.url = None
        self.filedata = None
        self.part = None
        if len(kwargs) > 0:
            self.__fromdict__(**kwargs)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __fromdict__(self, **kwargs):
        for k,v in kwargs.items():
            self.__setattr__(k, v)


class Filedata(object):

    def __init__(self, **kwargs):
        """
        : attribute length : string
        : attribute filedata : array
        : attribute imageid : string
        : attribute sizeinternal : float
        : attribute value : string
        : attribute hosterurl : string
        : attribute name : string
        """
        self.length = None
        self.filedata = None
        self.imageid = None
        self.sizeinternal = None
        self.value = None
        self.hosterurl = None
        self.name = None
        if len(kwargs) > 0:
            self.__fromdict__(**kwargs)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __fromdict__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)


class PronApi(object):

    def __init__(self, **kwargs):
        """
        : attribute result : array
        : attribute message : string
        : attribute resultcount : float
        : attribute fetchedtoday : float
        : attribute status : string
        """
        self.result = None
        self.message = None
        self.resultcount = None
        self.fetchedtoday = None
        self.status = None
        if len(kwargs) > 0:
            self.__fromdict__(**kwargs)

    def __setitem__(self, key, value):
        if key == 'result' and isinstance(value, list):
            resultlist = []
            for res in value:
                resultitem = Result(**res)
                resultlist.append(resultitem)
            self.result = resultlist
        self.__setattr__(key, value)

    def __fromdict__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)
