from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('history/', views.reading_history, name='reading_history'),
    path('history/clear/', views.clear_history, name='clear_history'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('refresh/<str:secret>/', views.refresh_articles, name='refresh_articles'),
]