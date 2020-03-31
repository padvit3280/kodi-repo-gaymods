
class AResultSet(object):

    def __init__(self):
        """
        : attribute a_field : array
        : attribute a_row : array
        : attribute n_total_rows : float
        """
        self.a_field = None
        self.a_row = None
        self.n_total_rows = None


class ARow(object):

    def __init__(self):
        """
        : attribute b_rating_blog_links : float
        : attribute n_birth_day : float
        : attribute b_gender : float
        : attribute n_birth_month : float
        : attribute sz_email_id : string
        : attribute b_verified : float
        : attribute n_birth_year : float
        : attribute b_rating_ix : float
        : attribute b_rating_blogs : float
        """
        self.b_rating_blog_links = None
        self.n_birth_day = None
        self.b_gender = None
        self.n_birth_month = None
        self.sz_email_id = None
        self.b_verified = None
        self.n_birth_year = None
        self.b_rating_ix = None
        self.b_rating_blogs = None


class AField(object):

    def __init__(self):
        """
        : attribute o_min : string
        : attribute o_max : string
        : attribute s_name : string
        : attribute s_type : string
        : attribute b_numeric : bool
        """
        self.o_min = None
        self.o_max = None
        self.s_name = None
        self.s_type = None
        self.b_numeric = None


class BaseClass(object):

    def __init__(self):
        """
        : attribute n_result : string
        : attribute a_result_set : array
        """
        self.n_result = None
        self.a_result_set = None

