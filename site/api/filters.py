# http://django-filter.readthedocs.io/en/stable/
import django_filters

def ToBoolean(value):
	if type(value) is bool:
		return value
	value = value.lower()
	if value in ['true', '1']:
		return True
	if value in ['false', '0']:
		return False
	return None


class MBooleanFilter(django_filters.Filter):

	def filter(self, qs, value):
		if value in [None, '']:
			return qs
		else:
			return qs.filter(**{self.name: ToBoolean(value)})
		return qs