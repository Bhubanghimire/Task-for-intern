from rest_framework import serializers
from .models import User,Task


class UserSerializer(serializers.ModelSerializer):

    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class TaskSerializer(serializers.ModelSerializer):
    assigned = UserSerializer(read_only=True)


    class Meta(object):
        model = Task
        fields =('id','title','description','status','assigned')