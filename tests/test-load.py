from locust import HttpUser, between, task

class TaskUser(HttpUser):
    host = 'http://127.0.0.1:8000'
    wait_time = between(1, 5)
    @task
    def create_task(self):
        self.client.post('/task/', json={
        'title': 'load test task',
        'description': 'description',
        'status': 'ok',
        'priority': 0
    })
    @task
    def read_task(self):
        self.client.get('/task/')