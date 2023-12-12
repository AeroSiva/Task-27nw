from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import datetime
import time
from Locators.locators import Zen_locators
from Data.data import Zen_Data
from Excel_Functions.excel_functions import Excel_Functions


class Login:
    def __init__(self):
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 20)
        self.action = ActionChains(self.driver)
        self.date = datetime.datetime.now()
        self.excel_func = Excel_Functions(Zen_Data().excel_file_name, Zen_Data().excel_sheet_name)
        self.row = self.excel_func.row_count()


    # Openiing url
    def access_url(self):
        try:
            self.driver.maximize_window()
            self.driver.get(Zen_Data().url)
        except Exception as e:
             print("Selenium Exception : ",e)


    # In this website it takes time to load the next page and hence a method is used to handle that for a time
    def wait_for_url_change(self, old_url, timeout=4):
        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.driver.current_url != old_url:
                return True
            time.sleep(0.5)
        return False
    
    '''
    This util will be used by a "test_login" method in pytest Test_login.py page 
    and it loates the respective element in the page and perform the reqwuired actions.
    while also writes the report tio the Excel file.
    '''
    def login_logout_util(self,username,password,row,exp_result):
        try: 
            user_box = self.wait.until(EC.visibility_of_element_located((By.NAME,Zen_locators.username_ip_box_name)))
            user_box.clear()
            user_box.send_keys(username) 
            password_box = self.wait.until(EC.visibility_of_element_located((By.NAME,Zen_locators.password_pw_box_name)))
            password_box.clear()
            password_box.send_keys(password)
            self.wait.until(EC.visibility_of_element_located((By.XPATH,Zen_locators.login_button_Xpath))).click()
            actual_result = ''

            # Wait for the next page to load (or for the URL to change) with a reduced timeout
            page_loaded = self.wait_for_url_change(Zen_Data().url) 
    
            # test PASS or FAIL
            if page_loaded:
                print("SUCCESS : Login success with \n username :{a} and password {b}".format(a=username, b=password))
                actual_result = 'Login'
                drop_down = self.wait.until(EC.element_to_be_clickable((By.XPATH, Zen_locators().drop_down_on_click_Xpath)))
                self.action.click(on_element=drop_down).perform()
                self.wait.until(EC.visibility_of_element_located((By.XPATH,Zen_locators().logout_button_Xpath))).click()

            elif(Zen_Data().url in self.driver.current_url):
                print("FAIL : Login failure with \n username :{a} and password {b}".format(a=username, b=password))
                actual_result = 'No Login'
                #self.driver.refresh()
            
            date = self.date.strftime("%x")
            self.excel_func.write_data(row, 4, date)
            time = self.date.strftime("%X")
            self.excel_func.write_data(row,5,time)
            self.excel_func.write_data(row, 9, actual_result)
            
            if actual_result == exp_result:
                self.excel_func.write_data(row, 11, "TEST PASS")
            else:
                self.excel_func.write_data(row, 11, "TEST FAIL")
            return actual_result

        except Exception as e:
            print("Selenium error",e)
            

    

'''lg = Login()
test_details =  lg.excel_func.read_excel_test_detail_util()
print(test_details)
lg.access_url()
for test_det in test_details:
    u_n,pw,ro,exp_re = test_det
    lg.login_logout_util(u_n,pw,ro,exp_re)'''