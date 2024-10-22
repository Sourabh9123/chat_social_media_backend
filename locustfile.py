from locust import HttpUser, task, between
import json
class LoadTestUser(HttpUser):
    wait_time = between(1, 3)  # Wait between 1 to 5 seconds
   

    @task
    def post_request(self):
        # Sample data you want to send with the POST request
        payload =   {
                        "title": "load testing from locust ",
                      
                    }
        token =  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4ODcyMzM5LCJpYXQiOjE3Mjg4MTgzMzksImp0aSI6IjhjYTY0MTc0NTA1NTQzYjk5YTFmMzkyNmFiZWI4NjY4IiwidXNlcl9pZCI6IjQzNWZjYzI5LWUwN2YtNDg4Zi1iOTlkLTYxMWY2MGRjZmMwOSJ9.uWy5V7F0wMA6S794rHFJkNYTzC6gIPNbsn_EPazpxOI"
        # Making the POST request to the specified endpoint
        response = self.client.post("post/", json=payload , headers={"Authorization": f"Bearer {token}"})

        # http://localhost:8000/
        # Optional: Print response status or data to debug
        if response.status_code == 201:  # Successful creation
            print(response.json(), "actual res")
            print("POST request successful")
        

        else:
            print(f"Failed with status code: {response.status_code}")


# locust -f locustfile.py