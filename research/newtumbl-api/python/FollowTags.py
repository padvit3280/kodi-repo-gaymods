
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
        : attribute dt_created : string
        : attribute dt_origin : string
        : attribute n_count_tag_hide : float
        : attribute dw_tag_ix_dst : float
        : attribute n_count_blog_hide : float
        : attribute dw_user_ix : float
        : attribute n_count_blog_follow : float
        : attribute n_count_tag_follow : float
        : attribute sz_tag_id_dst : string
        """
        self.dt_created = None
        self.dt_origin = None
        self.n_count_tag_hide = None
        self.b_order = None
        self.dw_tag_ix_dst = None
        self.n_count_blog_hide = None
        self.dw_user_ix = None
        self.n_count_blog_follow = None
        self.n_count_tag_follow = None
        self.sz_tag_id = None
        self.dw_tag_ix = None
        self.sz_tag_id_dst = None


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

