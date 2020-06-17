
class BaseClass(object):

    def __init__(self):
        """
        : attribute user_session : UserSession
        """
        self.user_session = None


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
        : attribute n_width : float
        : attribute sz_title : string
        : attribute b_icon_shape : float
        : attribute qw_media_ix_banner : float
        : attribute dt_created : string
        : attribute b_media_type_ix : float
        : attribute n_count_blog_message : float
        : attribute dt_origin : string
        : attribute b_rating_blog_links : float
        : attribute dw_user_ix : float
        : attribute n_birth_year : float
        : attribute qw_media_ix_background : float
        : attribute dw_admin : float
        : attribute qw_media_ix : float
        : attribute b_rating_blogs : float
        : attribute b_logged_in : float
        : attribute n_count_post_ask : float
        : attribute n_height : float
        : attribute n_count_post_flagged : float
        : attribute sz_body : string
        : attribute b_status : float
        : attribute b_hide : float
        : attribute dw_color_background : float
        : attribute b_terms : float
        : attribute b_minor : float
        : attribute n_count_post_out_of_range : float
        : attribute b_no_index : float
        : attribute sz_blog_id : string
        : attribute b_verified : float
        : attribute b_private : float
        : attribute b_active : float
        : attribute b_rating_ix : float
        : attribute n_count_post_submit : float
        : attribute b_primary : float
        : attribute b_block : float
        : attribute dw_blog_ix : float
        : attribute sz_description : string
        : attribute dw_color_foreground : float
        : attribute qw_media_ix_icon : float
        : attribute sz_sub : string
        : attribute n_size : float
        : attribute b_follow : float
        : attribute dw_i_p_address_ix : float
        : attribute b_t_o_s : float
        """
        self.n_width = None
        self.sz_title = None
        self.b_icon_shape = None
        self.qw_media_ix_banner = None
        self.dt_created = None
        self.b_media_type_ix = None
        self.n_count_blog_message = None
        self.dt_origin = None
        self.b_rating_blog_links = None
        self.dw_user_ix = None
        self.n_birth_year = None
        self.qw_media_ix_background = None
        self.dw_admin = None
        self.qw_media_ix = None
        self.b_rating_blogs = None
        self.b_logged_in = None
        self.n_count_post_ask = None
        self.n_height = None
        self.n_count_post_flagged = None
        self.sz_body = None
        self.b_status = None
        self.b_hide = None
        self.dw_color_background = None
        self.b_terms = None
        self.b_minor = None
        self.n_count_post_out_of_range = None
        self.b_no_index = None
        self.sz_blog_id = None
        self.b_verified = None
        self.b_private = None
        self.b_active = None
        self.b_rating_ix = None
        self.n_count_post_submit = None
        self.b_primary = None
        self.b_block = None
        self.dw_blog_ix = None
        self.sz_description = None
        self.dw_color_foreground = None
        self.qw_media_ix_icon = None
        self.sz_sub = None
        self.n_size = None
        self.b_follow = None
        self.dw_i_p_address_ix = None
        self.b_t_o_s = None


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


class UserSession(object):

    def __init__(self):
        """
        : attribute n_result : string
        : attribute a_result_set : array
        """
        self.n_result = None
        self.a_result_set = None

