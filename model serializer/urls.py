from uiApp.views import *
# from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls import url
urlpatterns = [
    url(r'^project/$',ProjectListView.as_view()),
    url(r'^project/(?P<pro_id>\d+)/$',ProjectDetailView.as_view())

]
