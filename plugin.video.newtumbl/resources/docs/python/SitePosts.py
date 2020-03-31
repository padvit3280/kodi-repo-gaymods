
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
        : attribute b_flag : float
        : attribute b_part_type_ix : float
        : attribute dw_blog_ix : float
        : attribute qw_media_ix_background : float
        : attribute b_primary : float
        : attribute b_status : float
        : attribute sz_u_r_l : string
        : attribute dw_color_foreground : float
        : attribute b_tier : float
        : attribute b_order : float
        : attribute qw_media_ix : float
        : attribute b_state : float
        : attribute b_favorite : float
        : attribute dw_user_ix : float
        : attribute sz_tag_id_dst : string
        : attribute b_follow : float
        : attribute dt_created : string
        : attribute qw_post_ix_from : float
        : attribute b_block : float
        : attribute b_like : float
        : attribute qw_post_ix : float
        : attribute b_post_type_ix : float
        : attribute qw_post_ix_orig : float
        : attribute n_part_iz : float
        : attribute sz_sub : string
        : attribute b_private : float
        : attribute sz_title : string
        : attribute b_media_type_ix : float
        : attribute dw_i_p_address_ix : float
        : attribute sz_tag : string
        : attribute dt_active : string
        : attribute sz_body : string
        : attribute dw_blog_ix_submit : float
        : attribute b_rating_ix : float
        : attribute sz_description : string
        : attribute n_height : float
        : attribute b_icon_shape : float
        : attribute sz_external : string
        : attribute dw_blog_ix_from : float
        : attribute n_count_post : float
        : attribute n_size : float
        : attribute dw_blog_ix_orig : float
        : attribute dt_scheduled : string
        : attribute n_count_like : float
        : attribute dw_checksum : float
        : attribute b_no_index : float
        : attribute sz_source : string
        : attribute n_width : float
        : attribute qw_media_ix_banner : float
        : attribute b_hide : float
        : attribute n_count_comment : float
        : attribute qw_media_ix_icon : float
        : attribute sz_blog_id : string
        : attribute dt_origin : string
        : attribute dw_color_background : float
        """
        self.dt_favorite = None
        self.b_flag = None
        self.b_part_type_ix = None
        self.dw_blog_ix = None
        self.qw_media_ix_background = None
        self.b_primary = None
        self.b_status = None
        self.sz_u_r_l = None
        self.dt_deleted = None
        self.dw_color_foreground = None
        self.b_tier = None
        self.b_order = None
        self.qw_media_ix = None
        self.b_state = None
        self.b_favorite = None
        self.dw_user_ix = None
        self.dt_like = None
        self.sz_tag_id_dst = None
        self.b_follow = None
        self.dt_modified = None
        self.dt_created = None
        self.qw_post_ix_from = None
        self.b_block = None
        self.b_like = None
        self.qw_post_ix = None
        self.b_post_type_ix = None
        self.qw_post_ix_orig = None
        self.n_part_iz = None
        self.sz_sub = None
        self.b_private = None
        self.sz_title = None
        self.b_media_type_ix = None
        self.dw_i_p_address_ix = None
        self.sz_tag = None
        self.dt_active = None
        self.sz_body = None
        self.dw_blog_ix_submit = None
        self.sz_tag_id = None
        self.b_rating_ix = None
        self.sz_description = None
        self.n_height = None
        self.b_icon_shape = None
        self.sz_external = None
        self.dw_blog_ix_from = None
        self.n_count_post = None
        self.n_size = None
        self.dw_blog_ix_orig = None
        self.dt_scheduled = None
        self.n_count_like = None
        self.dw_checksum = None
        self.b_no_index = None
        self.sz_source = None
        self.n_width = None
        self.qw_media_ix_banner = None
        self.b_hide = None
        self.n_count_comment = None
        self.qw_media_ix_icon = None
        self.sz_blog_id = None
        self.dt_flag = None
        self.dt_origin = None
        self.dw_color_background = None


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

