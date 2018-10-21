from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.PollView.as_view(), name='poll_add'),
    path('<int:id>/edit/', views.PollView.as_view(), name='poll_edit'),
    path('<int:id>/delete/', views.PollView.as_view(), name='poll_delete'),
    path('', views.index, name='polls_list'),
    path('<int:id>/details', views.details, name='poll_details'),
    path('<int:id>/', views.vote_poll, name='poll_vote'),

]