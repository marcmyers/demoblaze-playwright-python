import pytest
from playwright.sync_api import Page, expect
import faker

fake = faker.Faker()

@pytest.mark.usefixtures("handle_dialog")
class TestSignup:
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page
        self.page.goto("/")

    def fill_signup_form(self, username: str, password: str):
        """Helper method to fill in the signup form."""
        self.page.fill("#sign-username", username)
        self.page.fill("#sign-password", password)

    def test_successful_signup(self):
        self.page.click("#signin2")
        unique_email = fake.email()
        self.fill_signup_form(unique_email, "P@ssw0rd!")
        self.page.click('button:has-text("Sign up")')

        # Assert
        self.page.wait_for_event("dialog")
        assert self.dialog_message == "Sign up successful.", f"Unexpected dialog message: {self.dialog_message}"

    def test_duplicate_username_signup(self):
        self.page.click("#signin2")
        self.fill_signup_form("existing_user", "Test123!")
        self.page.click('button:has-text("Sign up")')

        # Assert
        self.page.wait_for_event("dialog")
        assert self.dialog_message == "This user already exist.", f"Unexpected dialog message: {self.dialog_message}"
