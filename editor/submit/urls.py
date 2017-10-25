from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^problems/$', views.problems, name='problems'),
    url(r'^problem/(?P<problem_id>\d+)/$', views.problem, name='problem'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
]
