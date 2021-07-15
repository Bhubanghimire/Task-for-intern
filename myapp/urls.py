from django.urls.conf import path
from .views import  CreateUserAPIView, UserRetrieveUpdateAPIView, login,TaskAPIView,TaskIdAPIView,TaskUserAPIView,TaskStatusAPIView,TaskCreateAPIView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path('register/', CreateUserAPIView.as_view(),name="register"),
    path('login/', login,name="login"),

    path('alltask/',csrf_exempt(TaskAPIView.as_view()),name="alltask"),
    path('taskid/',TaskIdAPIView.as_view(),name="task_by_id"),
    path('tasktouser/',TaskUserAPIView.as_view(),name='task_to_user'),
    path('taskstatus/',TaskStatusAPIView.as_view(),name='task_by_status'),
    path('newtask/',TaskCreateAPIView.as_view(),name="new_task"),


]