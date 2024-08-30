from django.urls import path, include
from client.views import *

urlpatterns=[
  path('login/',NormalLogin,name='login'),
  path('signup/',signup),
  path('home/',home),
  path('createevent/',CreateEvenet.as_view()),
  path('eventcategorie/<str:categorie>/', Filter_by_categorie.as_view(), name='filter-by-categorie'),
  path('eventdetail/<int:id>',EventDetail.as_view(), name='eventdetail'),
  path('filter_wilaya/',FilterWilaya.as_view()),
  path('filter_type/',FilterType.as_view()),
  path('reset/', ResetPassword.as_view(), name='reset_password'),
  path('new_password/', NewPassword.as_view(), name='new_password'),
  path('category/',Filter_by_categorie2.as_view())
]
    # urls.py

