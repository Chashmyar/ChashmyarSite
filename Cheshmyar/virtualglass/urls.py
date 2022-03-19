from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='virtual-glass'),
    path('<str:glasses>/virtual-try-on', views.video, name='video'),
    path('<str:glasses>/virtual-try-on/video-stream', views.video_stream, name='video_stream'),
    path('<str:glasses>/color-filter', views.upload_files, name='upload_files'),
    path('<str:glasses>/color-filter/upload', views.upload_files, name='upload_files'),
    path('<str:glasses>/color-filter/choose', views.choose_pic, name="choose_pic")
]
