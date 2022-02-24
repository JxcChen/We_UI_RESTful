from django.urls import re_path

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
    url(r'^case/concurrent/$', ConcurrentExcuseCaseView.as_view()),
    url(r'case/reportsummary/(?P<pro_id>\d+)/$', CaseReportSummaryView.as_view()),
    re_path(r'case/downloadclient/(?P<project_id>\d+)/', download),
    re_path(r'case/openMonitor/(?P<project_id>\d+)/', MonitorView.as_view()),
    url(r'^case/uploadUtils/(?P<pro_id>\d+)/$', UploadUtilsView.as_view()),
    url(r'^notice/$', NoticeListView.as_view()),
    url(r'^notice/(?P<project_id>\d+)/$', NoticeDetailView.as_view()),
    url(r'^page/$', PageListView.as_view()),
    url(r'^page/(?P<page_id>\d+)/$', PageDetailView.as_view()),
    url(r'^element/$', ElementListView.as_view()),
    url(r'^element/(?P<element_id>\d+)/$', ElementDetailView.as_view()),
    url(r'^login/$', obtain_jwt_token)

]
