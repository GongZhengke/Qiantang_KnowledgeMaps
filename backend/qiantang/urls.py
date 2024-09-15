
from django.urls import path

# python3 manage.py runserver 0.0.0.0:8000


from api import views
from graph.views import search

urlpatterns = [
    path('api/getToken', views.getToken),
    path('api/user/login', views.userLogin),
    path('api/user/logout', views.clearSession),
    path('api/user/info', views.userStatues),
    path('api/user/reg', views.userReg),
    path('api/admin/user/list', views.adminUserlist),
    path('api/search', search),
    path('api/search', search),
    path('api/user/updep', views.updateEphone),
    path('api/chat/qs', views.getAnswer),
]
