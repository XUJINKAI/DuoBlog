from django.core.exceptions import ValidationError

def validate_abosolute_url(value):
	if not value.startswith('http') or not value.endswith('/'):
		raise ValidationError('Url must start with http(s):// and end with slash /', params={'value': value})