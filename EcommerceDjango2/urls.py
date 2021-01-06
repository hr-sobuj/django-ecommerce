from django.contrib import admin
from django.urls import path,re_path
from django.urls import include
from django.contrib.staticfiles.urls import static,staticfiles_urlpatterns
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/',include('App_Login.urls')),
    path('ordered/',include('App_Order.urls')),
    path('payment/',include('App_Payment.urls')),
    path('',include('App_Shop.urls')),
]

# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_DIR,document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
