from uiApp.views import *
from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls import url

urlpatterns = [
    url(r'^project/$', ProjectListView.as_view()),
    url(r'^project/(?P<pk>\d+)/$', ProjectDetailView.as_view()),
    url(r'^case/$', CaseListView.as_view()),
    url(r'^case/(?P<pro_id>\d+)/$', CaseDetailView.as_view()),
    url(r'^case/uploadScript/(?P<pro_id>\d+)/$', CaseScriptView.as_view()),
    url(r'^case/excuse/(?P<case_id>\d+)/$', CaseExcuseView.as_view()),
    url(r'^user/$', UserListView.as_view()),
    url(r'^user/(?P<user_id>\d+)/$', UserDetailView.as_view()),
    url(r'^teamMember/$', ProjectMemberView.as_view()),
    url(r'^case/report/(?P<case_id>\d+)/$', CaseReportView.as_view()),
    url(r'^login/$', obtain_jwt_token)

]
