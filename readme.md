
# Playwright Test Automation for Demoblaze

This project uses **Playwright** with **Python** to automate testing for the [Demoblaze](https://www.demoblaze.com/) website. It covers various aspects of the site, including user signup and login functionality.

## Requirements

- **Python 3.7+**
- **Playwright**
- **pytest** for test management
- **Faker** (for generating test data)

## Setup Instructions

Follow the steps below to set up the project in a Python virtual environment and run the tests.

### 1. Clone the Repository

Clone the repository to your local machine.

```bash
git clone https://github.com/marcmyers/playwright-demoblaze-python.git
cd playwright-demoblaze-python
```

### 2. Create a Python Virtual Environment

It’s recommended to use a virtual environment to isolate project dependencies.

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

#### On Windows:

```bash
venv\Scripts\activate
```

#### On macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

Once the virtual environment is activated, install the necessary packages from `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 5. Install Playwright Browsers

Playwright requires you to install the necessary browsers. Run the following command to install them:

```bash
python -m playwright install
```

This will download the required browsers for testing (Chromium, Firefox, and WebKit).

### 6. Run the Tests

Once everything is set up, you can run the tests using `pytest`.

```bash
pytest test_login.py --headed
```

This will run the test suite with a visible browser window. Use the `--headless` flag if you prefer to run the tests without opening a browser window.

### 7. Customizing the Tests

You can modify the test data, such as the username and password, by editing the test scripts. The `Faker` library is used to generate unique test data, such as random usernames and emails, for each run.

---

## Test Examples

### 1. `test_signup.py`

Tests user signup functionality on the Demoblaze site.

### 2. `test_login.py`

Tests user login functionality, ensuring that users can log in with valid credentials.

---

## Troubleshooting

### 1. Playwright Installation Issues

If you face issues with installing Playwright or the browsers, try updating Playwright:

```bash
pip install --upgrade playwright
python -m playwright install
```

### 2. Browser Issues

If tests fail due to browser rendering issues, make sure that your system meets the necessary hardware and software requirements for running Playwright browsers.

---

## Contributing

Feel free to open issues or submit pull requests for improvements.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
