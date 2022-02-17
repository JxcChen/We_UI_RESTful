from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
import urllib


class LoginRequiredView(LoginRequiredMixin, View):
    login_url = r"http://localhost:8080/"
    redirect_field_name = 'redirect_to'  # 记录从哪个页面来的(忽略)
