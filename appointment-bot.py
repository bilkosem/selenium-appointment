from logging import exception
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import webbrowser
import pyautogui
credentials = {
    'title':'',
    'name':'',
    'surname':'',
    'phone':'',
    'mail':'',
}

def sleep_for_a_while():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print("Current Time:", current_time)
    print('Going to sleep for 10 minutes...\n\n')
    time.sleep(60*10) # retry after 10 minutes

def button_next_month():
    driver.find_element_by_css_selector("[title='Go to the next month']").click()


def button_prev_month():
    driver.find_element_by_css_selector("[title='Go to the previous month']").click()


def button_submit():
    driver.find_element_by_id('plhMain_btnSubmit').click()


def button_back():
    driver.find_element_by_id('plhMain_btnBack').click()


def select_box(id, text):
    select = Select(driver.find_element_by_id(id))
    select.select_by_visible_text(text)


def credential_page():
    # Enter credentials
    select = Select(driver.find_element_by_id('plhMain_repAppVisaDetails_cboTitle_0'))
    select.select_by_visible_text(credentials['title'])

    name = driver.find_element_by_id('plhMain_repAppVisaDetails_tbxFName_0')
    name.send_keys(credentials['name'])

    surname = driver.find_element_by_id('plhMain_repAppVisaDetails_tbxLName_0')
    surname.send_keys(credentials['surname'])

    phone = driver.find_element_by_id('plhMain_repAppVisaDetails_tbxContactNumber_0')
    phone.send_keys(credentials['phone'])

    mail = driver.find_element_by_id('plhMain_repAppVisaDetails_tbxEmailAddress_0')
    mail.send_keys(credentials['mail'])

    select_box('plhMain_cboConfirmation', 'I confirm the above statement')
    button_submit()


def calendar_page():
    '''
        If current month is May:
            if greenday exists click
            else click next
        elif current month is June
            if greenda exist click
            else click prev
        elif current month is July
            click prev
    '''
    month_list = ['May 2022', 'June 2022', 'July 2022']
    count_next_click, count_prev_click = 0, 0
    is_success = False
    while(True):
        current_month_name = driver.find_element_by_xpath('//*[@id="plhMain_cldAppointment"]/tbody/tr[1]/td/table/tbody/tr/td[2]').text
        print("Current Month:", current_month_name)

        message = str(driver.find_element_by_id('plhMain_lblMsg').text)
        print("Message:", message)
        if 'No date' in message:
            break

        if 'Error' in message:
            if count_next_click == 1 and count_prev_click == 1:
                button_back()
                break

            if count_next_click == 0 and current_month_name in month_list[0:1]:
                count_next_click += 1
                button_next_month()
            elif count_prev_click == 0 and current_month_name in month_list[1:2]:
                count_prev_click += 1
                button_prev_month()
            pass
        else:
            green_cell = driver.find_elements_by_class_name("OpenDateAllocated")
            print("Available appointment found in ",  green_cell[0].text, "of", current_month_name)
            if current_month_name == month_list[0] or (current_month_name == month_list[1] and int(green_cell[0].text)<14): # May or earlier then 14 of June
                print("Clicked the new appointment found in ",  green_cell[0].text, "of", current_month_name)
                green_cell[0].click() # Click the first item
                webbrowser.open('D:\\Downloads\\alarm-sound-effects-modern-alarm-1.mp3')
                slot = driver.find_element_by_id('plhMain_gvSlot_lnkTimeSlot_0')
                slot.click()
                print("Slot:",slot.text)
                driver.switch_to.window(driver.window_handles[-1])
                driver.switch_to.alert.accept()
                
                myScreenshot = pyautogui.screenshot()
                myScreenshot.save(f'D:\\Downloads\\appointment_{slot.text}_{green_cell[0].text}_{current_month_name}.png')
                is_success = True
            break
        pass

    return is_success

if __name__ == '__main__':
    driver = webdriver.Chrome("D:\Downloads\chromedriver_win32 (1)\chromedriver.exe")

    while(True):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print("Current Time:", current_time)

        driver.get('https://www.netherlandsworldwide.nl/countries/turkey/travel/applying-for-a-long-stay-visa-mvv')
        link = driver.find_elements_by_class_name("external")[9].get_attribute('href')
        driver.get(link)

        # 1 Schedule Page
        driver.find_element_by_id('plhMain_lnkSchApp').click()

        # 2 Embassy Page
        select = Select(driver.find_element_by_id('plhMain_cboVAC'))
        select.select_by_visible_text('Istanbul CG')
        button_submit()

        # 3 Visa Category Page
        select = Select(driver.find_element_by_id('plhMain_cboVisaCategory'))
        select.select_by_visible_text('MVV ??? visa for long stay (>90 days)')
        button_submit()

        try:
            message = str(driver.find_element_by_id('plhMain_lblMsg').text)
            no_date_error = 'No date(s) available for appointment.'
            if message == no_date_error:
                sleep_for_a_while()
                continue
        except:
            sleep_for_a_while()
            continue

        # 4 Credential Page
        credential_page()

        # 5 Credential Page
        is_success = calendar_page()
        
        print(is_success)
        if is_success:
            print(is_success)
            break
        else:
            sleep_for_a_while()
    pass