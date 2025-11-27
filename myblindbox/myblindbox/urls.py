from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('blindbox/', include('blindbox.urls')),  # 包含到/blindbox/前缀下
]
