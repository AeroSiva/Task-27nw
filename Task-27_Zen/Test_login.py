'''
Using Data Driven Testing Framework (DDTF), Page Object Model (POM), Exlicit wait,Expected Conditions, Pytest kindly do the following task as mentioned below:-
1.create an Excel file which will comprise of Test Id, username, Password, Date, Time of Test, Name of rtester, Test result for login into zen portal.
2.Go to URl 
3. Login in to Zen portal using the username and password provided in the Excl files. Try to use Username and password.
4. If the login is suxccessfull your Pythion code willl write in the Excel file whether your Test passed or failed.
Do not use sleep() method.
'''


import pytest
from Login_page import Login
from Excel_Functions.excel_functions import Excel_Functions
from Data.data import Zen_Data


# usuing fixture to the test cases
@pytest.fixture(scope="session")
def zen_instance():
    login_logout = Login()
    login_logout.access_url()
    yield login_logout
    login_logout.driver.quit()


# By using parametrizing individual test details are passed into the test case 
# while writing the same in the excel file by using a method inside login_logout_util
@pytest.mark.parametrize("username, password, row, exp_result", Excel_Functions
                         (Zen_Data.excel_file_name,Zen_Data.excel_sheet_name).read_excel_test_detail_util())
def test_login(zen_instance, username, password, row, exp_result):
    act_res = zen_instance.login_logout_util(username, password, row, exp_result)
    assert act_res == exp_result