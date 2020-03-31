from collections import  namedtuple
from nT import AField, RowField


class BlogResultSet(object):

    def __init__(self, **kwargs):
        """
        : attribute aField : array
        : attribute aRow : array
        : attribute nTotalRows : float
        """
        self.aField = []
        self.aRow = []
        self.nTotalRows = '0' #kwargs.get('nTotalRows', len(kwargs))
        for afield in kwargs.get('aField', []):
            newfield = AField(afield)
            self.aField.append(newfield)
        for row in kwargs.get('aRow', []):
            newrow = BlogRow(row)
            self.aRow.append(newrow)


class BlogRow(dict):


    def __init__(self, **kwargs):
        """
        : attribute nWidth : float
        : attribute szTitle : string
        : attribute bIconShape : float
        : attribute qwMediaIxBanner : float
        : attribute dtCreated : string
        : attribute bMediaTypeIx : float
        : attribute nCountBlogMessage : float
        : attribute dtOrigin : string
        : attribute acLanguage : string
        : attribute bRatingBlogLinks : float
        : attribute dwUserIx : float
        : attribute nBirthYear : float
        : attribute qwMediaIxBackground : float
        : attribute dwAdmin : float
        : attribute qwMediaIx : float
        : attribute bRatingBlogs : float
        : attribute bLoggedIn : float
        : attribute nCountPostAsk : float
        : attribute szName : string
        : attribute nHeight : float
        : attribute nCountPostFlagged : float
        : attribute szBody : string
        : attribute bStatus : float
        : attribute bHide : float
        : attribute dwColorBackground : float
        : attribute bTerms : float
        : attribute acCountry : string
        : attribute bMinor : float
        : attribute nCountPostOutOfRange : float
        : attribute szLocation : string
        : attribute bNoIndex : float
        : attribute szBlogId : string
        : attribute bVerified : float
        : attribute bPrivate : float
        : attribute bActive : float
        : attribute bRatingIx : float
        : attribute nCountPostSubmit : float
        : attribute bPrimary : float
        : attribute bBlock : float
        : attribute dwBlogIx : float
        : attribute bOnline : float
        : attribute szDescription : string
        : attribute dwColorForeground : float
        : attribute qwMediaIxIcon : float
        : attribute szSub : string
        : attribute nSize : float
        : attribute bFollow : float
        : attribute dwIPAddressIx : float
        : attribute bTOS : float
        """
        super(BlogRow, self).__init__(**kwargs)
        self.nWidth = None
        self.szTitle = None
        self.bIconShape = None
        self.qwMediaIxBanner = None
        self.dtCreated = None
        self.bMediaTypeIx = None
        self.nCountBlogMessage = None
        self.dtOrigin = None
        self.acLanguage = None
        self.bRatingBlogLinks = None
        self.dwUserIx = None
        self.nBirthYear = None
        self.qwMediaIxBackground = None
        self.dwAdmin = None
        self.qwMediaIx = None
        self.bRatingBlogs = None
        self.bLoggedIn = None
        self.nCountPostAsk = None
        self.szName = None
        self.nHeight = None
        self.nCountPostFlagged = None
        self.szBody = None
        self.bStatus = None
        self.bHide = None
        self.dwColorBackground = None
        self.bTerms = None
        self.acCountry = None
        self.bMinor = None
        self.nCountPostOutOfRange = None
        self.szLocation = None
        self.bNoIndex = None
        self.szBlogId = None
        self.bVerified = None
        self.bPrivate = None
        self.bActive = None
        self.bRatingIx = None
        self.nCountPostSubmit = None
        self.bPrimary = None
        self.bAge = None
        self.bBlock = None
        self.dwBlogIx = None
        self.bGender = None
        self.bOnline = None
        self.szDescription = None
        self.dwColorForeground = None
        self.qwMediaIxIcon = None
        self.szSub = None
        self.nSize = None
        self.bFollow = None
        self.dwIPAddressIx = None
        self.bTOS = None
        for k, v in kwargs.iteritems():
            super.__setattr__(self, k, v)


class ntBlog(object):

    @property
    def Blog(self):
        return self.result

    def __init__(self, aResultSet=[], **kwargs):
        """
        : attribute nResult : string
        : attribute aResultSet : BlogResultSet
        """
        self.nResult = kwargs.get('nResult', '0')
        self.aResultSet = aResultSet
        self.result = BlogRow(aResultSet[2].get('aRow',{}))

        #for resultitem in self.aResultSet:
        #    assert isinstance(resultitem, dict)
        #    if resultitem.has_key('aRow'):
        #        self.results.append(BlogRow(resultitem['aRow']))
        #try:
        #    self.aResultSet = BlogResultSet(aResultSet)
        #except:
        #    print("Failed to Init Blog result with passed variable: " + str(aResultSet.items()))
        #    self.aResultSet = BlogResultSet({})