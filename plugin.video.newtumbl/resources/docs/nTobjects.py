
class AField(object):

    def __init__(self, **kwargs):
        """
        : attribute o_min : string
        : attribute o_max : string
        : attribute s_name : string
        : attribute s_type : string
        : attribute b_numeric : bool
        """
        self.oMin = kwargs.get('oMin', '')
        self.oMax = kwargs.get('oMax', '')
        self.sName = kwargs.get('sName', '')
        self.sType = kwargs.get('sType', '')
        self.bNumeric = kwargs.get('oMin', False)


class Results(dict):

    def __init__(self, **kwargs):
        super(Results, self).__init__(**kwargs)
        self.aResultSet = []
        self.nResult = kwargs.get('nResult', '0')


class AResultSet(object):

    def __init__(self, **kwargs):
        """
        : attribute a_field : array
        : attribute a_row : array
        : attribute n_total_rows : float
        """
        self.aField = kwargs.get('aField', [])
        self.aRow = kwargs.get('aRow', [])
        self.nTotalRows = len(self.aRow)


class Field(object):

    def __init__(self, min="", max="", name="", type="", numeric=False):
        """
        : attribute o_min : string
        : attribute o_max : string
        : attribute s_name : string
        : attribute s_type : string
        : attribute b_numeric : bool
        """
        self.o_min = min
        self.o_max = max
        self.s_name = name
        self.s_type = type
        self.b_numeric = numeric


class Fields(list):

    def __init__(self, afields=[]):
        super(Fields, self).__init__()
        for field in afields:
            assert isinstance(field, AField)
            self.append(AField(min=field.o_min, max=field.o_max, name=field.s_name, type=field.s_type, numeric=field.b_numeric))


class RowTag(object):

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


class RowBlog(object):

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
        : attribute ac_language : string
        : attribute b_rating_blog_links : float
        : attribute dw_user_ix : float
        : attribute n_birth_year : float
        : attribute qw_media_ix_background : float
        : attribute dw_admin : float
        : attribute qw_media_ix : float
        : attribute b_rating_blogs : float
        : attribute b_logged_in : float
        : attribute n_count_post_ask : float
        : attribute sz_name : string
        : attribute n_height : float
        : attribute n_count_post_flagged : float
        : attribute sz_body : string
        : attribute b_status : float
        : attribute b_hide : float
        : attribute dw_color_background : float
        : attribute b_terms : float
        : attribute ac_country : string
        : attribute b_minor : float
        : attribute n_count_post_out_of_range : float
        : attribute sz_location : string
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
        : attribute b_online : float
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
        self.ac_language = None
        self.b_rating_blog_links = None
        self.dw_user_ix = None
        self.n_birth_year = None
        self.qw_media_ix_background = None
        self.dw_admin = None
        self.qw_media_ix = None
        self.b_rating_blogs = None
        self.b_logged_in = None
        self.n_count_post_ask = None
        self.sz_name = None
        self.n_height = None
        self.n_count_post_flagged = None
        self.sz_body = None
        self.b_status = None
        self.b_hide = None
        self.dw_color_background = None
        self.b_terms = None
        self.ac_country = None
        self.b_minor = None
        self.n_count_post_out_of_range = None
        self.sz_location = None
        self.b_no_index = None
        self.sz_blog_id = None
        self.b_verified = None
        self.b_private = None
        self.b_active = None
        self.b_rating_ix = None
        self.n_count_post_submit = None
        self.b_primary = None
        self.b_age = None
        self.b_block = None
        self.dw_blog_ix = None
        self.b_gender = None
        self.b_online = None
        self.sz_description = None
        self.dw_color_foreground = None
        self.qw_media_ix_icon = None
        self.sz_sub = None
        self.n_size = None
        self.b_follow = None
        self.dw_i_p_address_ix = None
        self.b_t_o_s = None


class RowPost(object):

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


class RowBlogPost(object):

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


class RowFave(object):

    def __init__(self):
        """
        : attribute dt_favorite : string
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
        : attribute b_follow : float
        : attribute dt_modified : string
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


