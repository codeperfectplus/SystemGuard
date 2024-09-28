import os

from locust import HttpUser, TaskSet, task, between
from locust.exception import StopUser

from src.logger import logger


class UserBehavior(TaskSet):

    def on_start(self):
        """ Called when a Locust user starts running """
        self.login()

    def login(self):
        """ Simulate a user logging in """
        response = self.client.post("/login", {
            "username": "admin",
            "password": "adminpassword"
        })
        if response.status_code == 200 and "Invalid username or password" not in response.text:
            logger.info("Login successful")
        else:
            logger.info("Login failed")
            raise StopUser("Login failed")

    @task(1)
    def view_dashboard(self):
        """ Simulate viewing the dashboard """
        self.client.get("/")

    @task(2)
    def view_cpu_usage(self):
        """ Simulate viewing CPU usage """
        self.client.get("/cpu_usage")

    @task(1)
    def view_disk_usage(self):
        """ Simulate viewing disk usage """
        self.client.get("/disk_usage")

    @task(1)
    def view_memory_usage(self):
        """ Simulate viewing memory usage """
        self.client.get("/memory_usage")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Time to wait between tasks

if __name__ == "__main__":
    os.system("locust -f locustfile.py --host=http://localhost:5000")
