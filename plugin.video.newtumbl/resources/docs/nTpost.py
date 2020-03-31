class Post(object):

    def _init__(self, **kwargs):
        """
        : attribute szSource : string
        : attribute dwBlogIx : float
        : attribute dwBlogIxSubmit : float
        : attribute nCountComment : float
        : attribute dtActive : string
        : attribute dwBlogIxFrom : float
        : attribute dwBlogIxOrig : float
        : attribute bTier : float
        : attribute bStatus : float
        : attribute szExternal : string
        : attribute bRatingIx : float
        : attribute szURL : string
        : attribute bPostTypeIx : float
        : attribute dtLike : string
        : attribute qwPostIx : float
        : attribute nCountPost : float
        : attribute dwChecksum : float
        : attribute dtScheduled : string
        : attribute nCountLike : float
        : attribute qwPostIxFrom : float
        : attribute dtCreated : string
        : attribute dtFavorite : string
        : attribute nCountMark : float
        : attribute qwPostIxOrig : float
        : attribute bState : float
        : attribute tags : list PostTag
        """
        self.dtFlag = None
        self.szSource = None
        self.dwBlogIx = None
        self.dwBlogIxSubmit = None
        self.nCountComment = None
        self.dtActive = None
        self.dwBlogIxFrom = None
        self.dwBlogIxOrig = None
        self.bTier = None
        self.bStatus = None
        self.szExternal = None
        self.dtModified = None
        self.bRatingIx = None
        self.szURL = None
        self.bPostTypeIx = None
        self.dtLike = None
        self.qwPostIx = None
        self.nCountPost = None
        self.dwChecksum = None
        self.dtScheduled = None
        self.nCountLike = None
        self.qwPostIxFrom = None
        self.dtCreated = None
        self.dtFavorite = None
        self.nCountMark = None
        self.qwPostIxOrig = None
        self.bState = None
        self.dtDeleted = None
        self.tags = []
        self.PostIx = kwargs.get('qwPostIx', kwargs.get('qxPostIxFrom', kwargs.get('qwPostIxOrig','0')))
        self.BlogIx = kwargs.get('dwBlogIx', kwargs.get('dwBlogIxFrom', kwargs.get('dwBlogIxOrig', kwargs.get('dwBlogIxSubmit', '0'))))
        self.MediaIx = "{0}"
        self.mediapath = "/{0}/{1}/0/{2}/nT_".format(self.BlogIx, self.PostIx, self.MediaIx)
        self.thumb = ""
        self.movie = ""
        self.Media = PostMedia


    def setMedia(self, medialist=[]):
        for media in medialist:
            assert isinstance(media, PostMedia)
            if media.PostIx == self.PostIx:
                self.MediaIx = media.qwMediaIx
                self.Media = media
                self.thumb = media.Thumb()
                self.movie = media.Movie()
                break


    def setTags(self, taglist=[]):
        for tag in taglist:
            assert isinstance(tag, PostTag)
            if tag.qwPostIx == self.PostIx
            self.tags.append(tag)


    def getTagString(self):
        tagstring = ""
        for tag in self.tags:
            tagstring += "," + tag.Name
        tagstring = tagstring.strip(",")
        return tagstring



class PostMedia(object):

    def _init__(self, **kwargs):
        """
        : attribute bPartTypeIx : float
        : attribute bOrder : float
        : attribute nPartIz : float
        : attribute dtScheduled : string
        : attribute qwMediaIx : float
        : attribute qwPostIx : float
        : attribute dwBlogIxFrom : float
        : attribute qwPostIxFrom : float
        """
        self.bPartTypeIx = None
        self.bOrder = None
        self.nPartIz = None
        self.dtScheduled = None
        self.qwMediaIx = None
        self.qwPostIx = None
        self.dwBlogIxFrom = None
        self.qwPostIxFrom = None
        self.PostIx = kwargs.get('qwPostIx', kwargs.get('qwPostIxFrom', '0'))
        self.BlogIx = kwargs.get('dwBlogIxFrom', '0')
        self.MediaIx = kwargs.get('qwMediaIx', '0')
        self.thumbnail = ''
        self.movie = ''
        self.Thumb()


    def Thumb(self):
        if self.thumbnail == '':
            self.thumbnail = base32path(**self.__dict__)
            self.movie = self.thumbnail.replace('.jpg', '.mp4')
        return self.thumbnail


    def Movie(self):
        if self.movie == '':
            self.Thumb()
        return self.movie


class PostTag(object):

    def _init__(self, **kwargs):
        """
        : attribute szTag : string
        : attribute qwPostIx : float
        : attribute bOrder : float
        """
        self.szTag = kwargs.get('szTag', '')
        self.qwPostIx = kwargs.get('qwPostIx', '0')
        self.bOrder = kwargs.get('bOrder', 0)
        self.Name = self.szTag.title()
        self.PostIx = self.qwPostIx
