from django.db import models

class ARow(models.Model):
	a_row = models.CharField(max_length=255, blank=True)
	dt_created = models.CharField(max_length=255, blank=True)
	dw_tag_ix_dst = models.FloatField(blank=True)
	dw_user_ix = models.FloatField(blank=True)
	n_count_tag_follow = models.FloatField(blank=True)
	n_count_tag_hide = models.FloatField(blank=True)
	dt_origin = models.CharField(max_length=255, blank=True)
	n_count_blog_follow = models.FloatField(blank=True)
	n_count_blog_hide = models.FloatField(blank=True)
	sz_tag_id_dst = models.CharField(max_length=255, blank=True)
	a_result_set = models.ForeignKey("AResultSet", blank=True)


class AField(models.Model):
	o_min = models.CharField(max_length=255, blank=True)
	o_max = models.CharField(max_length=255, blank=True)
	s_name = models.CharField(max_length=255, blank=True)
	s_type = models.CharField(max_length=255, blank=True)
	b_numeric = models.BooleanField(blank=True, null=True)
	a_result_set = models.ForeignKey("AResultSet", blank=True)


class TagsFollow(models.Model):
	n_result = models.CharField(max_length=255, blank=True)


class AResultSet(models.Model):
	tags_follow = models.ForeignKey("TagsFollow", blank=True)
	n_total_rows = models.FloatField(blank=True)

