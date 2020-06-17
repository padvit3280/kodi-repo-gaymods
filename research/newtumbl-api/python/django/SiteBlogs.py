from django.db import models

class ARow(models.Model):
	n_size = models.FloatField(blank=True)
	b_primary = models.FloatField(blank=True)
	dw_blog_ix = models.FloatField(blank=True)
	a_row = models.CharField(max_length=255, blank=True)
	a_result_set = models.ForeignKey("AResultSet", blank=True)
	qw_media_ix_banner = models.FloatField(blank=True)
	dw_color_foreground = models.FloatField(blank=True)
	b_media_type_ix = models.FloatField(blank=True)
	n_width = models.FloatField(blank=True)
	sz_sub = models.CharField(max_length=255, blank=True)
	sz_body = models.CharField(max_length=255, blank=True)
	b_status = models.FloatField(blank=True)
	b_hide = models.FloatField(blank=True)
	b_private = models.FloatField(blank=True)
	b_rating_ix = models.FloatField(blank=True)
	b_follow = models.FloatField(blank=True)
	sz_title = models.CharField(max_length=255, blank=True)
	qw_media_ix = models.FloatField(blank=True)
	sz_blog_id = models.CharField(max_length=255, blank=True)
	dw_color_background = models.FloatField(blank=True)
	sz_description = models.CharField(max_length=255, blank=True)
	b_icon_shape = models.FloatField(blank=True)
	qw_media_ix_icon = models.FloatField(blank=True)
	b_block = models.FloatField(blank=True)
	dw_user_ix = models.FloatField(blank=True)
	dt_created = models.CharField(max_length=255, blank=True)
	n_height = models.FloatField(blank=True)
	qw_media_ix_background = models.FloatField(blank=True)
	dw_i_p_address_ix = models.FloatField(blank=True)
	dt_origin = models.CharField(max_length=255, blank=True)
	b_no_index = models.FloatField(blank=True)


class AField(models.Model):
	o_min = models.CharField(max_length=255, blank=True)
	o_max = models.CharField(max_length=255, blank=True)
	s_name = models.CharField(max_length=255, blank=True)
	s_type = models.CharField(max_length=255, blank=True)
	b_numeric = models.BooleanField(blank=True, null=True)
	a_result_set = models.ForeignKey("AResultSet", blank=True)


class AResultSet(models.Model):
	site_blogs = models.ForeignKey("SiteBlogs", blank=True)
	n_total_rows = models.FloatField(blank=True)


class SiteBlogs(models.Model):
	n_result = models.CharField(max_length=255, blank=True)

