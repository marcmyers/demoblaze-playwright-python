import pytest
from playwright.sync_api import Page, APIRequestContext, expect
from faker import Faker
import base64

@pytest.mark.usefixtures("handle_dialog")
class TestLogin:
    @pytest.fixture(scope="class")
    def api_context(self, playwright):
        api_context = playwright.request.new_context(base_url="https://api.demoblaze.com")
        yield api_context
        api_context.dispose()

    @pytest.fixture(scope="class")
    def create_user(self, api_context: APIRequestContext):
        # Initialize Faker
        faker = Faker()
        raw_password = "P@ssw0rd!"
        encoded_password = base64.b64encode(raw_password.encode()).decode()
        
        user_data = {
            "username": faker.email(),
            "password": encoded_password,  # Send encoded password to API
        }

        response = api_context.post("/signup", data=user_data)
        assert response.ok, f"User creation failed: {response.status} {response.json()}"

        if response.status == 200:
            print(f"User created successfully with email {user_data['username']}.")
        elif response.status == 409:
            print("User already exists.")
        else:
            pytest.fail(f"Unexpected response: {response.status} - {response.json()}")

        return {
            "username": user_data["username"],
            "password": raw_password,  # Return raw password for UI testing
            "encoded_password": encoded_password  # Keep encoded password if needed
        }

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page
        self.page.goto("https://www.demoblaze.com/")

    def test_successful_login(self, create_user):
        self.page.click("#login2")
        self.page.wait_for_selector("#logInModal")
        self.page.fill("#loginusername", create_user["username"])
        self.page.fill("#loginpassword", create_user["password"])
        self.page.click('button:has-text("Log in")')

        # Assert
        self.page.wait_for_selector("#logout2")
        assert self.page.is_visible("#logout2"), "Logout button not visible, login may have failed."

    def test_wrong_password_login(self):
        self.page.click("#login2")
        self.page.wait_for_selector("#logInModal")

        self.page.fill("#loginusername", "invalid_user")
        self.page.fill("#loginpassword", "wrong_password")
        
        self.page.click('button:has-text("Log in")')
        self.page.wait_for_event("dialog")
        
        # Assert
        assert self.dialog_message == "Wrong password.", f"Unexpected dialog message: {self.dialog_message}"

    def test_empty_login_fields(self):
        self.page.click("#login2")
        self.page.wait_for_selector("#logInModal")
        self.page.click('button:has-text("Log in")')
        
        # Assert
        assert self.dialog_message == "Please fill out Username and Password.", f"Unexpected dialog message: {self.dialog_message}"
