from locust import HttpUser, task, between
import json

class MyUser(HttpUser):
    wait_time = between(1, 5)  # Wait between 1 and 5 seconds between each task

    def on_start(self):
        json_data = json.dumps({"username": "username", "password": "password"})

        # Perform authentication and obtain a JWT token
        response = self.client.post("create-user/", json=json_data)
        response = self.client.post("login/", json=json_data)
        json_str = response._content.decode('utf-8')
        data_dict = json.loads(json_str)
        # Extract the JWT token from the response
        token = data_dict.get("access")

        # Set the token in the user's session headers for subsequent requests
        self.client.headers.update({"Authorization": f"Bearer {token}"})

    @task
    def my_task(self):
        self.client.post(url="get-songs", json={'songsDescription': 'Give a song by Taylor Swift raja'})
