import pytest
from playwright.sync_api import Page, APIRequestContext, expect

class TestCart:
    @pytest.fixture(scope="class")
    def api_context(self, playwright):
        api_context = playwright.request.new_context(base_url="https://api.demoblaze.com")
        yield api_context
        api_context.dispose()

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page
        self.page.goto("https://www.demoblaze.com/")

    def test_add_to_cart(self):
        self.page.get_by_role("link", name="Samsung galaxy s6").click()
        self.page.once("dialog", lambda dialog: dialog.dismiss())
        self.page.get_by_role("link", name="Add to cart").click()
        self.page.get_by_role("link", name="Cart", exact=True).click()
        
        # Assert
        expect(self.page.locator("#tbodyid")).to_contain_text("Samsung galaxy s6")

    def test_delete_from_cart(self):
        self.page.get_by_role("link", name="Samsung galaxy s6").click()
        self.page.once("dialog", lambda dialog: dialog.dismiss())
        self.page.get_by_role("link", name="Add to cart").click()
        self.page.get_by_role("link", name="Cart", exact=True).click()
        with self.page.expect_request_finished(lambda request: "/deleteitem" in request.url):
            self.page.get_by_role("link", name="Delete").click()
        with self.page.expect_request_finished(lambda request: "/viewcart" in request.url):
            pass
        # self.page.wait_for_selector("#tbodyid")
        
        # Assert
        cart_items = self.page.locator("#tbodyid > tr")
        assert cart_items.count() == 0, "The cart is not empty!"