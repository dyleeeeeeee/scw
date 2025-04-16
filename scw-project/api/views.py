

# Create your views here.
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TaskSerializer
from .models import TaskModel
from .tasks import sample_task

# View for the specific /api/process POST endpoint
class ProcessTaskView(APIView):
    """
    Handles POST requests to /api/process to create a new task.
    """
    permission_classes = [permissions.IsAuthenticated] # Or permissions.IsAuthenticated

    def post(self, request, *args, **kwargs):
        # Simulated DB operation.
        result = sample_task.delay(request.data)
        serializer = TaskSerializer(result)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskViewSet(viewsets.ReadOnlyModelViewSet): # ReadOnly to only read resource
    """
    Handles retrieving Task status.
    """
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.AllowAny]

    # Action to get status for a specific task
    # endpoint like /api/tasks/{pk}
    @action(detail=True, methods=['get'], url_path='status')
    def status(self, request, pk=None):
        if not pk:
            task = self.get_object() # Gets the task instance
            serializer = self.get_serializer(task)
            return Response(serializer.data)
        else:
            task = TaskModel.objects.get(id=pk)
            serializer = self.get_serializer(task)
            return Response(serializer.data)


from .serializers import RegisterSerializer
from django.contrib.auth.models import User

class RegisterView(APIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)