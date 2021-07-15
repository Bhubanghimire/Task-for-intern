from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.signals import user_logged_in
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework_jwt.utils import jwt_payload_handler


from .serializers import TaskSerializer, UserSerializer
from django.conf import settings
from .models import Task, User
import jwt


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def login(request):

    try:
        email = request.data['email']
        password = request.data['password']
        

        user = User.objects.filter(email=email, password=password)
        print(user)
        if user:
            user = User.objects.get(email=email, password=password)
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['name'] = "%s %s" % (
                    user.first_name, user.last_name)
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)



class TaskAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

   


class TaskIdAPIView(APIView):
    serializer_class = TaskSerializer

    def post(self, request):

        user = request.user.id
        if not user:
            res={'error':"Current user is not authorized.Please provide authorization key."}
            return Response(res)

        task_id = request.data.get("task_id",None)
        if not task_id:
            res={'error':"You dont provide id."}
            return Response(res)

        task=Task.objects.filter(id=task_id)
        serializers = TaskSerializer(task,many=True)
        return Response(serializers.data)


class TaskUserAPIView(APIView):
    serializer_class = TaskSerializer

    def get(self, request):
        user = request.user.id
        if not user:
            res={'error':"Current user is not authorized.Please provide authorization key."}
            return Response(res)

        task=Task.objects.filter(assigned=user)
        serializers = TaskSerializer(task,many=True)
        return Response(serializers.data)


class TaskStatusAPIView(APIView):
    serializer_class = TaskSerializer

    def post(self, request):

        user = request.user.id
        if not user:
            res={'error':"Current user is not authorized.Please provide authorization key."}
            return Response(res)

        task_status = request.data.get("task_status",None)

        if not task_status:
            res={'error':"Please provide task status.Your choices:incomplete,complete"}
            return Response(res)

        task=Task.objects.filter(status=task_status)
        serializers = TaskSerializer(task,many=True)
        return Response(serializers.data)


class TaskCreateAPIView(APIView):
    serializer_class = TaskSerializer

    def post(self,request):
        user = request.user.id
        if not user:
            res={'error':"Current user is not authorized.Please provide authorization key."}
            return Response(res)

        title = request.data.get('title',None)
        description = request.data.get('description',None)
        assigned = request.data.get('assigned',0)

        if (title and description and assigned):
            user = User.objects.filter(id=assigned)
            if user:
                user = User.objects.get(id=assigned)
                task = Task.objects.create(title=title,description=description,assigned=user)
                task.save()
                res = {'status': 'Successfully created and assigned the task'}
            else:
                res = {'error': 'User does not exists.'}
        
        elif (title and description):
            user = request.user
            print(user)
            assigned = User.objects.get(email=user)
            task = Task.objects.create(title=title,description=description,assigned=assigned)
            task.save()
            res = {'status': 'task created for you'}
        
        else:
            res = {'error': 'please provide complete data'}
        return Response(res)
            



