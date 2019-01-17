from django.conf.urls import url
from django.urls import path
from . import views


app_name = 'lango_content'
urlpatterns = [
    path(r'sentence_edit/<int:sid>', views.sentence_edit, name='sentence_edit'),
    # path(r'sentence_edit/<int:pk>', views.sentence_edit.as_view(), name='sentence'),
]

