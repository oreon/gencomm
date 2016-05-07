from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from rest_framework import serializers


        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group        


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User




# class UserSerializer(serializers.ModelSerializer):
# 
#     class Meta:
#         model = User
#         '''
#         fields = (
#             'id',
#             'username',
#             'password',
#             'email',
#             ...,
#         )
#         '''
#         extra_kwargs = {
#             'password': {'write_only': True},
#         }
# 
#     def create(self, validated_data):
#         user = get_user_model().objects.create_user(**validated_data)
#         return user
# 
#     def update(self, instance, validated_data):
#         if 'password' in validated_data:
#             password = validated_data.pop('password')
#             instance.set_password(password)
#         return super(UserSerializer, self).update(instance, validated_data)