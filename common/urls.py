from django.urls import path
from django.contrib.auth import views as auth_views


app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'),
         name='login'),  # loginview 그대로 사용, registration 이 아닌 common 디렉터리에 템플릿을 생성
]
