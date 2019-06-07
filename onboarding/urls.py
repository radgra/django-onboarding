from django.urls import path
from . import views

app_name = 'onboarding'
urlpatterns = [
    path('',views.onboarding_list,name='onboarding_list'),
    path('<int:pk_onboard>/tasks/<int:pk_task>',views.task_detail,name='task_detail'),
    path('<int:pk_onboard>/tasks/<int:pk_task>/update',views.update_task_detail,name='task_detail_update'),
    path('<int:pk>',views.onboarding_detail,name='onboarding_detail'),
    path('<int:pk>/delete',views.onboarding_delete,name='onboarding_delete'),
    path('<int:pk>/update',views.onboarding_update,name='onboarding_update'),
    path('create/',views.onboarding_create,name='onboarding_create'),
    path('tasks/',views.task_list,name='task_list'),


]