
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
        : attribute n_size : float
        : attribute b_primary : float
        : attribute dw_blog_ix : float
        : attribute b_media_type_ix : float
        : attribute n_width : float
        : attribute sz_sub : string
        : attribute qw_media_ix_icon : float
        : attribute sz_body : string
        : attribute b_status : float
        : attribute qw_media_ix_background : float
        : attribute b_hide : float
        : attribute b_private : float
        : attribute b_rating_ix : float
        : attribute sz_title : string
        : attribute sz_blog_id : string
        : attribute qw_media_ix : float
        : attribute b_follow : float
        : attribute sz_description : string
        : attribute b_icon_shape : float
        : attribute qw_media_ix_banner : float
        : attribute dw_color_foreground : float
        : attribute dw_user_ix : float
        : attribute dt_created : string
        : attribute b_block : float
        : attribute n_height : float
        : attribute dw_i_p_address_ix : float
        : attribute dt_origin : string
        : attribute dw_color_background : float
        : attribute b_no_index : float
        """
        self.n_size = None
        self.b_primary = None
        self.dw_blog_ix = None
        self.b_media_type_ix = None
        self.n_width = None
        self.sz_sub = None
        self.qw_media_ix_icon = None
        self.sz_body = None
        self.b_status = None
        self.qw_media_ix_background = None
        self.b_hide = None
        self.b_private = None
        self.b_rating_ix = None
        self.sz_title = None
        self.sz_blog_id = None
        self.qw_media_ix = None
        self.b_follow = None
        self.sz_description = None
        self.b_icon_shape = None
        self.qw_media_ix_banner = None
        self.dw_color_foreground = None
        self.dw_user_ix = None
        self.dt_created = None
        self.b_block = None
        self.n_height = None
        self.dw_i_p_address_ix = None
        self.dt_origin = None
        self.dw_color_background = None
        self.b_no_index = None


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

