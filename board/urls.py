from django.urls import path
from . import views
from .views import BoardCategory

app_name = 'board'

urlpatterns = [
    path('category/<slug:cat_slug>/', BoardCategory.as_view(),
         name='category'),
    path('<int:year>/<int:month>/<int:day>/<slug:announcement>/', views.Announcement_detail,
         name='announcement_detail'),
    path('', views.AnnouncementList,
         name='announcement_list'),
]