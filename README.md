# QA Automation Framework

A UI test automation framework built with Python, Selenium WebDriver, and Pytest, following the Page Object Model (POM) design pattern.

The project focuses on automating web application login scenarios while promoting code reusability, maintainability, and reliable test execution.

## Technologies

- **Python** – Programming language.
- **Selenium WebDriver** – Browser automation.
- **Pytest** – Test execution, fixtures, and parametrization.
- **Page Object Model (POM)** – Test architecture and code organization.
- **WebDriver Manager** – ChromeDriver management.
- **Git & GitHub** – Version control.

## Project Structure

```text
qa-automation-framework/
│
├── browser/
│   └── driver.py
│
├── config/
│   └── config.py
│
├── docs/
│   └── PROJECT_TECHNICAL_GUIDE.md
│
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   └── dashboard_page.py
│
├── tests/
│   ├── test_login.py
│   └── test_headless.py
│
├── conftest.py
├── exceptions.py
├── requirements.txt
└── README.md
```

## Current Test Coverage

The framework currently includes:

- Successful login validation.
- Invalid password validation.
- Invalid username validation.
- Unexpected login result handling.
- Headless browser execution.

## Framework Features

- Page Object Model implementation.
- Reusable BasePage class.
- Explicit waits using WebDriverWait.
- Pytest fixtures for browser setup and teardown.
- Parametrized test scenarios.
- Custom exception handling.
- Browser automation using Chrome.

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/JoelPim182/qa-automation-framework.git
```

**2. Navigate to the project directory**

```bash
cd qa-automation-framework
```

**3. Create a virtual environment**

```bash
python -m venv .venv
```

**4. Activate the virtual environment (Windows)**

```bash
.venv\Scripts\activate
```

**5. Install dependencies**

```bash
pip install -r requirements.txt
```

## Running Tests

Execute the test suite using:

```bash
python -m pytest -v
```

## Application Under Test

The framework currently uses [The Internet](https://the-internet.herokuapp.com/login) as its application under test.

## Future Improvements

- Allure test reporting.
- GitHub Actions integration for CI/CD.
- Automated screenshots on test failures.
- Logging implementation.
- Additional UI test scenarios.
- API test automation.

## Contributors

- **Joel Pimentel Gomez** – [GitHub](https://github.com/JoelPim182)
- **Itzel Ambrosio Garcia** – [GitHub](https://github.com/itzel-ambrosiog)