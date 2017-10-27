from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^problems/$', views.problems, name='problems'),
    url(r'^active_problem/$', views.active_problem, name='active_problem'),
    url(r'^add_row/$', views.add_row, name='add_row'),
    url(r'^receive_protocol/$', views.receive_protocol, name='receive_protocol'),
    url(r'^problem/(?P<problem_id>\d+)/$', views.problem, name='problem'),
    url(r'^view/(?P<submit_id>\d+)/$', views.view_submit, name='view_submit'),
    url(r'^add_row_info/(?P<user_id>\d+)/$', views.add_row_info, name='add_row_info'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
]
