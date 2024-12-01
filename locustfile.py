from locust import HttpUser, task, between

class MultiPageUser(HttpUser):
    host = "https://www.n11.com"
    wait_time = between(1, 3)

    @task(3)  # This task will run more frequently
    def browse_homepage(self):
        self.client.get("/")
        print("Visited Homepage")

    @task(2)  # This task will run less frequently
    def search_product(self):
        query = {"q": "laptop"}
        response = self.client.get("/arama", params=query)
        print("Performed Product Search")
        if response.status_code == 200:
            # Navigate to product detail page
            product_id = self.extract_product_id(response.text)
            if product_id:
                self.client.get(f"/urun-detay/{product_id}")

    def extract_product_id(self, html):
        # Extract a product ID from the HTML response (sample method)
        # In complex scenarios, you can use BeautifulSoup or regex
        return "123456"

class AuthenticatedUser(HttpUser):
    host = "https://www.n11.com"
    wait_time = between(1, 3)

    def on_start(self):
        # The user logs in before the test starts
        self.login()

    def login(self):
        payload = {"username": "testuser", "password": "testpassword"}
        response = self.client.post("/giris", json=payload)
        if response.status_code == 200:
            print("Login successful!")
        else:
            print(f"Login failed: {response.status_code}")

    @task
    def add_to_cart(self):
        product_id = "123456"
        response = self.client.post(f"/sepet/ekle/{product_id}")
        if response.status_code == 200:
            print(f"Added product {product_id} to cart")
        else:
            print(f"Failed to add product {product_id} to cart: {response.status_code}")

    @task
    def view_cart(self):
        response = self.client.get("/sepetim")
        if response.status_code == 200:
            print("Viewed cart")
        else:
            print(f"Failed to view cart: {response.status_code}")


class StressTestUser(HttpUser):
    host = "https://www.n11.com"
    wait_time = lambda self: 0  # Sends requests without any waiting

    @task
    def rapid_requests(self):
        self.client.get("/")
        print("Rapidly sending requests to the homepage")


class SlowPageTest(HttpUser):
    host = "https://www.n11.com"
    wait_time = between(2, 5)  # Simulates a longer wait time between requests

    @task
    def slow_page(self):
        with self.client.get("/yavas-sayfa", catch_response=True) as response:
            if response.elapsed.total_seconds() > 3:
                response.failure(f"Page load too slow: {response.elapsed.total_seconds()} seconds")
            else:
                response.success()