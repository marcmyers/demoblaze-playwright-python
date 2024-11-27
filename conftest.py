import pytest

@pytest.fixture
def handle_dialog(page, request):
    """Global fixture to handle dialogs and store messages."""
    # Initialize dialog_message attribute on the test class
    request.instance.dialog_message = None
    
    def handle_dialog_fn(dialog):
        # Store dialog message in the test class instance
        request.instance.dialog_message = dialog.message
        dialog.accept()
    
    # Register the dialog handler
    page.on("dialog", handle_dialog_fn)
    
    # Clean up after the test
    yield
    
    # Reset dialog message
    if hasattr(request.instance, 'dialog_message'):
        request.instance.dialog_message = None
