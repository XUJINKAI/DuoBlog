from rest_framework import serializers

from accounts import models as account_models



class UserListSerializer(serializers.ModelSerializer):

	class Meta:
		model = account_models.User
		fields = '__all__'
