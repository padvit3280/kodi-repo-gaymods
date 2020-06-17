from django.db import models

class ARow(models.Model):
	b_gender = models.FloatField(blank=True)
	n_birth_day = models.FloatField(blank=True)
	b_rating_blog_links = models.FloatField(blank=True)
	n_birth_month = models.FloatField(blank=True)
	b_rating_blogs = models.FloatField(blank=True)
	sz_email_id = models.CharField(max_length=255, blank=True)
	b_verified = models.FloatField(blank=True)
	n_birth_year = models.FloatField(blank=True)
	b_rating_ix = models.FloatField(blank=True)
	a_result_set = models.ForeignKey("AResultSet", blank=True)


class AField(models.Model):
	o_min = models.CharField(max_length=255, blank=True)
	o_max = models.CharField(max_length=255, blank=True)
	s_name = models.CharField(max_length=255, blank=True)
	s_type = models.CharField(max_length=255, blank=True)
	b_numeric = models.BooleanField(blank=True, null=True)
	a_result_set = models.ForeignKey("AResultSet", blank=True)


class UserSettings(models.Model):
	n_result = models.CharField(max_length=255, blank=True)


class AResultSet(models.Model):
	user_settings = models.ForeignKey("UserSettings", blank=True)
	n_total_rows = models.FloatField(blank=True)

