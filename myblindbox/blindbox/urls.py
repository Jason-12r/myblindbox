from django.urls import path
from . import views

app_name = 'blindbox'

urlpatterns = [
    path('create/', views.blindbox, name='blindbox'),  # 创建盲盒
    path('detail/<int:box_id>/', views.blindbox_detail, name='blindbox_detail'),  # 盲盒详情
    path('all/', views.all_blindboxes, name='all_blindboxes'),  # 所有盲盒
]
