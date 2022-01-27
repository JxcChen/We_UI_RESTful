from django.urls import path,re_path
from uiApp.views import *
# from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls import url
urlpatterns = [
    url(r'^authorizations/$',UserView.as_view),
    path('project/', ProjectInfoView.as_view()),
    re_path(r'project/(?P<pro_id>\d+)/', ProjectInfoView.as_view()),
    re_path(r'case/(?P<pk>\d+)',CaseInfoView.as_view()),
    re_path(r'case/uploadScript/(?P<pro_id>\d+)',CaseScriptView.as_view()),

]
