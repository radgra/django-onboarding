from django.urls import path
from users.views import login_view
from . import views

app_name = 'core'
urlpatterns = [
        path('',views.main_page,name='main_page'),
]