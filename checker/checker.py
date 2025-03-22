import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

URL = "http://web:5000"
ATTACKER_PAGE = "http://evil:5005/login"

def check():
    print("Starting check...", flush=True)
    
    # Включим логирование браузера
    #capabilities = DesiredCapabilities.CHROME
    #capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')  # Без GUI
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    #options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    driver = webdriver.Chrome(options=options)
    
    try:
        # Открываем страницу логина
        print(f"Opening login page: {URL}/login", flush=True)
        driver.get(f"{URL}/login")
        
        # Ожидаем загрузку формы логина
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        
        # Вводим логин и пароль
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("admin123")
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        
        # Ожидаем редирект на /welcome
        WebDriverWait(driver, 10).until(EC.url_contains("/welcome"))
        print(f"Redirected to: {driver.current_url}", flush=True)

        # Проверяем, что вход выполнен успешно
        if "Welcome, admin!" not in driver.page_source:
            print("Failed to log in as admin", flush=True)
            driver.quit()
            return
        
        # Открываем вредоносную страницу
        print(f"Opening attacker page: {ATTACKER_PAGE}", flush=True)
        driver.get(ATTACKER_PAGE)
        
        # Ожидаем загрузку страницы
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("Page loaded successfully", flush=True)
        
        time.sleep(5)  # Даем время на выполнение CSRF-атаки
        
        # Пробуем снова войти в систему с новым паролем
        print(f"Re-opening login page: {URL}/login", flush=True)
        driver.get(f"{URL}/login")
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        
        driver.find_element(By.NAME, "username").send_keys("admin")
        driver.find_element(By.NAME, "password").send_keys("hacked123")
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        print("Login form submitted with new password", flush=True)
        
        time.sleep(2)
        
        # Проверяем, что вход выполнен успешно
        if "Welcome, admin!" in driver.page_source:
            print("CSRF exploit worked! ✅", flush=True)
        else:
            print("CSRF exploit failed! ❌", flush=True)
    
    except Exception as e:
        print(f"Error: {e}", flush=True)
    
    #finally:
        # Получаем логи браузера
        #logs = driver.get_log('browser')
        #for log in logs:
            #print(f"Browser log: {log}", flush=True)


print("Checker script started", flush=True)
while True:
    print("Checking...", flush=True)
    check()
    time.sleep(10)