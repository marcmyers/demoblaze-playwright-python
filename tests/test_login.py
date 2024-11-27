import pytest
from playwright.sync_api import Page, APIRequestContext, expect
from faker import Faker
import base64

@pytest.mark.usefixtures("handle_dialog")
class TestLogin:
    @pytest.fixture(scope="class")
    def api_context(self, playwright):
        # Set up APIRequestContext
        api_context = playwright.request.new_context(base_url="https://api.demoblaze.com")
        yield api_context
        api_context.dispose()

    @pytest.fixture(scope="class")
    def create_user(self, api_context: APIRequestContext):
        # Initialize Faker
        faker = Faker()

        # Generate user data with both raw and encoded password
        raw_password = "P@ssw0rd!"
        encoded_password = base64.b64encode(raw_password.encode()).decode()
        
        user_data = {
            "username": faker.email(),
            "password": encoded_password,  # Send encoded password to API
        }

        # Make an API request to create the user
        response = api_context.post("/signup", data=user_data)
        assert response.ok, f"User creation failed: {response.status} {response.json()}"

        # Check if user creation was successful or if the user already exists
        if response.status == 200:
            print(f"User created successfully with email {user_data['username']}.")
        elif response.status == 409:
            print("User already exists.")
        else:
            pytest.fail(f"Unexpected response: {response.status} - {response.json()}")

        # Return user credentials with both passwords
        return {
            "username": user_data["username"],
            "password": raw_password,  # Return raw password for UI testing
            "encoded_password": encoded_password  # Keep encoded password if needed
        }

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        # Navigate to the Demoblaze homepage
        self.page = page
        self.page.goto("https://www.demoblaze.com/")

    def test_successful_login(self, create_user):
        # Click the login link
        self.page.click("#login2")

        # Wait for the login modal to appear
        self.page.wait_for_selector("#logInModal")

        # Enter valid credentials
        self.page.fill("#loginusername", create_user["username"])
        self.page.fill("#loginpassword", create_user["password"])

        # Click the login button
        self.page.click('button:has-text("Log in")')

        # Verify successful login by checking the presence of the logout button
        self.page.wait_for_selector("#logout2")
        assert self.page.is_visible("#logout2"), "Logout button not visible, login may have failed."

    def test_wrong_password_login(self):
        # Click the login link
        self.page.click("#login2")
        
        # Wait for the login modal to appear
        self.page.wait_for_selector("#logInModal")
        
        # Enter invalid credentials
        self.page.fill("#loginusername", "invalid_user")
        self.page.fill("#loginpassword", "wrong_password")
        
        # Click the login button
        self.page.click('button:has-text("Log in")')
        
        # Wait for the dialog to appear
        self.page.wait_for_event("dialog")
        
        # Verify error alert message
        assert self.dialog_message == "Wrong password.", f"Unexpected dialog message: {self.dialog_message}"

    def test_empty_login_fields(self):
        # Click the login link
        self.page.click("#login2")
        
        # Wait for the login modal to appear
        self.page.wait_for_selector("#logInModal")
        
        # Leave the username and password fields empty and click login
        self.page.click('button:has-text("Log in")')
        
        # Verify error alert message
        assert self.dialog_message == "Please fill out Username and Password.", f"Unexpected dialog message: {self.dialog_message}"
