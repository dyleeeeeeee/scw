from django.urls import include, path
from rest_framework import routers

from .views import TaskViewSet, ProcessTaskView, RegisterView

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    # POST endpoint
    path('api/process/', ProcessTaskView.as_view(), name='task-process'),

    # Include the router-generated URLs (e.g., /api/tasks/, /api/tasks/{pk}/status/)
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]