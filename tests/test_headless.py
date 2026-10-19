from browser.driver import create_driver


def test_headless_browser():
    driver = create_driver(headless=True)

    try:
        driver.get("https://the-internet.herokuapp.com/login")

        assert "The Internet" in driver.title
        assert "/login" in driver.current_url

    finally:
        driver.quit()
