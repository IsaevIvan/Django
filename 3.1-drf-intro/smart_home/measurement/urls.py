from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('sensors/create/', views.SensorCreateView.as_view(), name='sensor-create'),
    path('sensors/<int:pk>/update/', views.SensorUpdateView.as_view(), name='sensor-update'),
    path('measurements/create/', views.MeasurementCreateView.as_view(), name='measurement-create'),
    path('sensors/', views.SensorListView.as_view(), name='sensor-list'),
    path('sensors/<int:pk>/', views.SensorDetailView.as_view(), name='sensor-detail'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)