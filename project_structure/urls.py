from django.urls import path
from project_structure.views import *

urlpatterns = [
    path(r'<int:project>/meeting/add/<int:pageId>', MeetingCreate.as_view(), name='meeting-add'),
    path(r'<int:project>/meeting/<int:pk>/', MeetingUpdate.as_view(), name='meeting-update'),
    path(r'<int:project>/meeting/<int:pk>/delete/', MeetingDelete.as_view(), name='meeting-delete'),
    path(r'<int:project>/meeting/<int:pk>/', MeetingDetail.as_view(), name='meeting-detail'),
    path(r'<int:project>/meetings/', MeetingList.as_view(), name='meeting-list'),
    path(r'researcher/add/', ResearcherCreate.as_view(), name='researcher-add'),
    path(r'researcher/<int:pk>/', ResearcherUpdate.as_view(), name='researcher-update'),
    path(r'researcher/<int:pk>/delete/', ResearcherDelete.as_view(), name='researcher-delete'),
    path(r'researcher/<int:pk>/', ResearcherDetail.as_view(), name='researcher-detail'),
    path(r'researchers/', ResearcherList.as_view(), name='researcher-list'),
    path(r'add/<int:pageId>', ProjectCreate.as_view(), name='project-add'),
    path(r'<int:pk>/', ProjectUpdate.as_view(), name='project-update'),
    path(r'<int:pk>/delete/', ProjectDelete.as_view(), name='project-delete'),
    path(r'<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
    path(r'', ProjectList.as_view(), name='project-list'),
]