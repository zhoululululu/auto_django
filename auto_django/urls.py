"""auto_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from auto_django.api import manage_user, manage_tracking_number, manage_check_sql
from rest_framework.schemas import get_schema_view
from auto_django.api.manage_tracking_number import GenerateTrackingNumberAPI, GetTrackingNumberAPI
from auto_django.api.manage_check_sql import DownloadTemplateAPI, NewCheckSqlAPI, UploadFileAPI, GetCheckSqlDataAPI, \
    DelCheckSqlAPI, DownloadResultAPI
from auto_django.api.manage_validation_data import GetValidationData, AddValidationData, EditValidationData, \
    DeleteValidationData
from auto_django.api.manage_validation import NewValidation, DeleteValidation, DownloadValidation, QueryValidation
from auto_django.api.Func import EditData
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', get_schema_view()),
    path('auth/', manage_user.login),
    path('create/', manage_user.create_user),
    path('getTrackingNumber', GenerateTrackingNumberAPI.as_view()),
    path('getAllTrackingNumber', GetTrackingNumberAPI.as_view()),
    path('getCheckSqlTemplate', DownloadTemplateAPI.as_view()),
    path('uploadCheckFile', UploadFileAPI.as_view()),
    path('getNewCheck', NewCheckSqlAPI.as_view()),
    path('getSqlResult', GetCheckSqlDataAPI.as_view()),
    path('deleteCheckResult', DelCheckSqlAPI.as_view()),
    path('downloadResult', DownloadResultAPI.as_view()),
    path('getValidationData', GetValidationData.as_view()),
    path('addNewValidationData', AddValidationData.as_view()),
    path('editNewValidationData', EditValidationData.as_view()),
    path('deleteNewValidationData', DeleteValidationData.as_view()),
    path('newValidation', NewValidation.as_view()),
    path('getValidation', QueryValidation.as_view()),
    path('deleteValidation', DeleteValidation.as_view()),
    path('downloadValidation', DownloadValidation.as_view()),
    path('updataya', EditData.as_view()),
]
