from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase #  for DRF testing
from .models import TaskModel
# If your serializer is needed for comparison, import it too
# from .serializers import TaskSerializer

class TaskAPITests(APITestCase):

    def setUp(self):
        """
        Set up data needed for tests that retrieve or modify existing objects.
        This method runs before each test method.
        """
        # sample task for GET tests
        self.sample_task = TaskModel.objects.create(email="test@task.com", message="Test Message")

    # Test the POST /api/process/ endpoint
    def test_create_task_via_process_endpoint(self):
        """
        Ensure we can create a new task using the /api/process/ endpoint.
        """
        url = reverse('task-process') # Use the name defined in your urls.py
        data = {'email': 'test@task.com', 'message': 'New Task via Process'} # Adjust fields based on your serializer/model
        
        # Use self.client provided by APITestCase
        response = self.client.post(url, data, format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskModel.objects.count(), 2) # One from setUp, one created now
        
        # Check the response data (optional but recommended)
        # created_task = TaskModel.objects.get(email='test@task.com')
        self.assertEqual(response.data['message'], 'New Task via Process')
        # self.assertEqual(response.data['id'], str(created_task.id)) # Compare string representation of UUID
        # self.assertEqual(response.data['status'], 'PENDING') # Check default status

    def test_create_task_via_process_invalid_data(self):
        """
        Ensure creating a task with invalid data fails correctly.
        """
        url = reverse('task-process')
        # Assuming 'name' is required by your serializer
        invalid_data = {'wrong_field': 'Some Value'}
        response = self.client.post(url, invalid_data, format='json')

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TaskModel.objects.count(), 1) # No new task should be created
        self.assertIn('message', response.data)

    # def test_get_task_status_not_found(self):
    #     """
    #     Ensure retrieving status for a non-existent task returns 404.
    #     """
    #     import uuid
    #     non_existent_pk = uuid.uuid4() # Generate a random UUID
    #     # url = reverse('task-status', kwargs={'pk': non_existent_pk})

    #     response = self.client.get(url, format='json')

    #     # Assertions
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_retrieve_task(self):
        """
        Ensure we can retrieve a specific task (if the endpoint /api/tasks/{pk}/ exists).
        """
        # URL name is typically '<basename>-detail'
        url = reverse('task-detail', kwargs={'pk': self.sample_task.pk})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], self.sample_task.message)