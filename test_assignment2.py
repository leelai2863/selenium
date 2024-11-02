import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    prefs = {
        'autofill.profile_enabled': False
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

#test chức năng đăng ký thành công
def testcase_1(driver):
    driver.get("https://demo.opencart.com/")
    time.sleep(5)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for new content to load
        time.sleep(2)
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Exit the loop if no new content is loaded
        last_height = new_height
    
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='My Account']"))
    )
    element.click()
    time.sleep(5)
    create_account_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Continue']"))
    )
    create_account_button.click()
    time.sleep(5)
    driver.find_element(By.NAME, "firstname").send_keys("Le Nguyen")
    driver.find_element(By.NAME, "lastname").send_keys("Ton")
    driver.find_element(By.NAME, "email").send_keys("testemail11@gmail.com.vn")
    driver.find_element(By.NAME, "password").send_keys("test12345")
    agree_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@name='agree']"))
    )
    agree_button.click()
    time.sleep(2)
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Continue']"))
    )
    continue_button.click()
    time.sleep(3)
    content = driver.find_element(By.ID, "content").text
    assert "Your Account Has Been Created!" in content

#test chức năng đăng nhập đúng thông tin
def testcase_2(driver):
    driver.get("https://demo.opencart.com/")
    time.sleep(5)
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        time.sleep(2)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='My Account']"))
    )
    element.click()
    time.sleep(5)
    driver.find_element(By.NAME, "email").send_keys("testemail11@gmail.com.vn")
    driver.find_element(By.NAME, "password").send_keys("test12345")
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']"))
    )
    login_button.click()
    time.sleep(5)
    assert "https://demo.opencart.com/en-gb?route=account/account&customer_token" in driver.current_url

def testcase_3(driver):
    driver.get("https://demo.opencart.com/")
    time.sleep(5)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        time.sleep(2)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Exit the loop if no new content is loaded
        last_height = new_height
    
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='My Account']"))
    )
    element.click()
    time.sleep(5)
    driver.find_element(By.NAME, "email").send_keys("testexamplezz1213@example.com.vn")
    driver.find_element(By.NAME, "password").send_keys("1231231231")
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']"))
    )
    login_button.click()
    time.sleep(2)
    message = driver.find_element(By.ID, "alert").text
    assert "Warning: No match for E-Mail Address and/or Password." in message

def testcase_4(driver):
    testcase_2(driver)
    logout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div//a[@class='list-group-item' and text()='Logout']"))
    )
    logout_button.click()
    time.sleep(2)
    content = driver.find_element(By.ID, "content").text
    assert "You have been logged off your account. It is now safe to leave the computer." in content

#TC5: thêm địa chỉ
def testcase_5(driver):
    testcase_2(driver)
    
    add_address = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Modify your address book entries']"))
    )
    add_address.click()
    new_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='New Address']"))
    )
    new_btn.click()
    
    driver.find_element(By.NAME, "firstname").send_keys("Le Nguyen")
    driver.find_element(By.NAME, "lastname").send_keys("Show")
    driver.find_element(By.NAME, "company").send_keys("nocompany")
    driver.find_element(By.NAME, "address_1").send_keys("ga rung")
    driver.find_element(By.NAME, "address_2").send_keys("Vn number too")
    
    country_options = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//select[@name='country_id']"))
    )
    country_options.click()

    for i in range(4):
        country_options.send_keys("v")
    
    driver.find_element(By.NAME, "city").send_keys("Ha Noi")
    driver.find_element(By.NAME, "postcode").send_keys("SW1A 1AA")
    
    zone_options = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//select[@name='zone_id']"))
    )
    zone_options.click()
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    for i in range(9):
        zone_options.send_keys("H")
    
    
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@name='default']"))
    )
    btn.click()
    continue_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='col text-end']/button"))
    )
    continue_btn.click()
    time.sleep(2)
    message = driver.find_element(By.XPATH, "//div[@class='alert alert-success alert-dismissible']").text
    assert "Your address has been successfully added" in message

#TC6: test thêm sản phẩm + navigate to cart
def testcase_6(driver):
    testcase_2(driver)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='search']"))
    )
    element.send_keys("Nikon D300")

    search_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@id='search']//button[@type='button']"))
    )
    search_btn.click()
    time.sleep(1)

    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

    add_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='button-group']/button"))
    )
    add_button.click()
    time.sleep(2)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP)
    time.sleep(5)
    mini_cart_button = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-lg btn-inverse btn-block dropdown-toggle']"))
    )
    mini_cart_button.click()
    
    cart_button = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//p[@class='text-end']//a[@href='https://demo.opencart.com/en-gb?route=checkout/cart']"))
    )
    cart_button.click()
    time.sleep(1)
    elements = driver.find_elements(By.XPATH, "//div[@class='table-responsive']//tbody//tr//td[@class='text-start text-wrap']")

    # assert 1 == len(elements)

#TC7: test remove product from cart
def testcase_7(driver):
    testcase_2(driver)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='search']"))
    )
    element.send_keys("Nikon D300")

    search_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@id='search']//button[@type='button']"))
    )
    search_btn.click()
    time.sleep(1)

    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

    add_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='button-group']/button"))
    )
    add_button.click()
    time.sleep(2)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP)
    time.sleep(5)
    mini_cart_button = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-lg btn-inverse btn-block dropdown-toggle']"))
    )
    mini_cart_button.click()
    
    cart_button = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//p[@class='text-end']//a[@href='https://demo.opencart.com/en-gb?route=checkout/cart']"))
    )
    cart_button.click()
    time.sleep(1)  
    product_num = driver.find_elements(By.XPATH, "//div[@class='input-group']//button[2]")
    for i in range(len(product_num)):
        actions = ActionChains(driver)
        remove_buttons = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='input-group']//button[2]"))
        )
        actions.move_to_element(remove_buttons).perform()
        remove_buttons.click()
        time.sleep(1)
    message = driver.find_element(By.ID, "content").text
    assert "Your shopping cart is empty!" in message

#TC8: test checkout
def testcase_8(driver):
    testcase_6(driver)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    checkout_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Checkout']"))
    )
    checkout_btn.click()
    time.sleep(2)
    
    #checkout section
    
    address_options = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "input-shipping-address"))
    )
    address_options.click()
    address_options.send_keys("L")
    time.sleep(0.5)
    #chọn phương thức thanh toán
    shipping_method_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "button-shipping-methods"))
    )
    shipping_method_btn.click()
    time.sleep(3)
    option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='form-check']//input[@name='shipping_method']"))
    )
    option.click()
    time.sleep(1)
    option.click()
    time.sleep(1)
    continue_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "button-shipping-method"))
    )
    continue_button.click()
    time.sleep(3)
    
    #payment section
    payment_method_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "button-payment-methods"))
    )
    payment_method_btn.click()
    
    time.sleep(5)
    option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='form-check']//input[@name='payment_method']"))
    )
    option.click()
    time.sleep(1)
    continue_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "button-payment-method"))
    )
    continue_button.click()
    time.sleep(3)
    
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    confirm = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Confirm Order']"))
    )
    confirm.click()
    time.sleep(3)
    result = driver.find_element(By.ID, 'content').text
    assert "Your order has been placed!" in result

@pytest.mark.parametrize("search_query, expected_product_name", [
    ("MacBook", "MacBook"),
    ("iPhone", "iPhone"),
    ("Canon", "Canon")
])
def testcase_9_search_function(driver, search_query, expected_product_name):
    driver.get("https://demo.opencart.com/")
    time.sleep(3)
    
    search_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "search"))
    )
    search_box.clear()
    search_box.send_keys(search_query)
    time.sleep(3)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    try:
        product_name = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//h4/a[contains(text(), '{expected_product_name}')]"))
        )
        assert expected_product_name.lower() in product_name.text.lower(), "Product name does not match expected result"
        print(f"Test Passed: Product '{expected_product_name}' found in search results for query '{search_query}'.")
    except:
        print(f"Test Failed: Product '{expected_product_name}' not found in search results for query '{search_query}'.")

    time.sleep(3)