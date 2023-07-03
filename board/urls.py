from django.urls import path
from . import views
from .views import AnnouncementCreate, PostList, PostDetail, PostCategory, AnnouncementUpdate

app_name = 'board'

urlpatterns = [
    path('', PostList.as_view(), name='announcement_list'),
    path('<int:pk>/', PostDetail.as_view(), name='announcement_detail'),
    path('add/', AnnouncementCreate.as_view(), name='ann_create'),
    path('<int:pk>/update/', AnnouncementUpdate.as_view(), name='ann_update'),
    path('category/<int:pk>/', PostCategory.as_view(), name='category'),
]