# http://django-filter.readthedocs.io/en/stable/
import django_filters


class MBooleanFilter(django_filters.Filter):

	def filter(self, qs, value):
		if value in [None, '']:
			return qs
		else:
			lc_value = value.lower()
			if lc_value in ["true", '1']:
				value = True
			elif lc_value in ["false", '0']:
				value = False
			return qs.filter(**{self.name: value})
		return qs