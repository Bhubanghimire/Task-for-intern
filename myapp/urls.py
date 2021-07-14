from django.urls.conf import path
from .views import  CreateUserAPIView, UserRetrieveUpdateAPIView, login,TaskAPIView,TaskIdAPIView,TaskUserAPIView,TaskStatusAPIView,TaskCreateAPIView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path('register/', CreateUserAPIView.as_view()),
    path('update/', UserRetrieveUpdateAPIView.as_view()),
    path('login/', login),

    path('alltask/',csrf_exempt(TaskAPIView.as_view())),
    path('taskid/',TaskIdAPIView.as_view()),
    path('tasktouser/',TaskUserAPIView.as_view()),
    path('taskstatus/',TaskStatusAPIView.as_view()),
    path('newtask/',TaskCreateAPIView.as_view())


]