from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from random import randint

category_quantity = 4
productlist = [2,3,4,2]
recepie_num = 4
faq_num = 4

Youtub_link = "https://www.youtube-nocookie.com/embed/qtlhdIfojmc?controls=0"
lorem = "Lorem ipsum, dolor sit, amet, consectetur, adipiscing elit, sed do eiusmod ,tempor " \
        "incididunt ut, labore et dolore, magna aliqua. Ut enim ad, minim veniam, quis nostrud exercitation ,ullamco laboris" \
        " nisi ut aliquip, ex ea commodo, consequat. Duis aute irure, dolor in reprehenderit, in voluptate velit esse, cillum " \
        "dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, " \
        "sunt in, culpa qui officia ,deserunt mollit ,anim id est laborum."

PATH = "C:/Program Files (x86)/chromedriver.exe"
option = Options()
option.add_argument("start-maximized")
option.add_experimental_option("useAutomationExtension", False)
option.add_experimental_option("excludeSwitches",["enable-automation"])
# prefs = {"credentials_enable_service", False}
# prefs = {"profile.password_manager_enabled" : False}
# prefs = {"profile.default_content_setting_values.notifications": 2}

prefs = {"credentials_enable_service": False,
         "profile.password_manager_enabled": False,
         "profile.default_content_setting_values.notifications": 2
         }
option.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(PATH,options=option)
driver.get("http://127.0.0.1:8000/admin/")

def checkpageload(driv, xpath):
    try:
        messenger = WebDriverWait(driv, 50).until(EC.presence_of_element_located((By.XPATH
                                            , xpath))
        )
        return messenger
    except Exception as e:
        print("couldn't find xpath")
def login(driver):
    username = driver.find_element_by_id("id_username").send_keys("admin")
    password = driver.find_element_by_id("id_password").send_keys("admin")
    login = driver.find_element_by_xpath("//*[@id='login-form']/div[3]/input").click()

def add_category(driv,quantity):
    driv.get("http://127.0.0.1:8000/admin/home/category/add/")
    for i in range(1,quantity+1):
        checkpageload(driv,"//*[@id='id_product_category']").send_keys("category_" + str(i))
        checkpageload(driv,"//*[@id='id_product_category_image']").send_keys(r"C:\Users\User\Desktop\AnjalSaps\projects\collegehtmlprojects\opera\assets\img\cake1.jpg")
        checkpageload(driv,"//*[@id='category_form']/div/div/input[2]").click()
def add_product(driv,quantity,lorem):
    driv.get("http://127.0.0.1:8000/admin/home/product/add/")
    for index, i in enumerate(quantity, start=1):
        for j in range(1, i+1):
            category = Select(checkpageload(driv,"//*[@id='id_product_category']"))
            category.select_by_index(index)
            product_name = checkpageload(driv,"//*[@id='id_product_name']").send_keys(f"C{index}_Product_{j}")
            product_price = checkpageload(driv,"//*[@id='id_product_price']").send_keys(randint(999,7000))
            product_short_description = checkpageload(driv, "//*[@id='id_product_short_description']").send_keys(lorem)
            product_long_description = checkpageload(driv, "//*[@id='id_product_long_description']").send_keys(lorem)
            image1 = checkpageload(driv, "//*[@id='id_image1']").send_keys(r"C:\Users\User\Desktop\AnjalSaps\projects\collegehtmlprojects\opera\assets\img\cake1.jpg")
            image2 = checkpageload(driv, "//*[@id='id_image2']").send_keys(r"C:\Users\User\Desktop\AnjalSaps\projects\collegehtmlprojects\opera\assets\img\cake1.jpg")
            image3 = checkpageload(driv, "//*[@id='id_image3']").send_keys(r"C:\Users\User\Desktop\AnjalSaps\projects\collegehtmlprojects\opera\assets\img\cake1.jpg")
            add_another = checkpageload(driv,"//*[@id='product_form']/div/div/input[2]").click()
def youtube_link(driv,link):
    ylinkadd = driv.get("http://127.0.0.1:8000/admin/home/youtube_link/add/")
    youlink = checkpageload(driv,"//*[@id='id_Youtube_Link']").send_keys(link)
    addyoulink = checkpageload(driv,"//*[@id='youtube_link_form']/div/div/input[1]").click()
def recepie(driv,num,lorem):
    rece = driv.get("http://127.0.0.1:8000/admin/home/recepie/add/")
    for i in range(1,num+1):
        recepie_name = checkpageload(driv, "//*[@id='id_recepie_name']").send_keys(f"Recepie_{i}")
        recepie_description = checkpageload(driv, "//*[@id='id_recepie_description']").send_keys(lorem)
        recepie_ingredient = checkpageload(driv, "//*[@id='id_recepie_ingredients']").send_keys(lorem)
        recepie_direction = checkpageload(driv, "//*[@id='id_recepie_direction']").send_keys(lorem)
        final_image = checkpageload(driv, "//*[@id='id_final_image']").send_keys(r"C:\Users\User\Desktop\AnjalSaps\projects\collegehtmlprojects\opera\assets\img\cake1.jpg")
        saverece = checkpageload(driv,"//*[@id='recepie_form']/div/div/input[2]").click()
def faq(driv,faqnum,lorem):
    faq = driv.get("http://127.0.0.1:8000/admin/home/faq/add/")
    for i in range(1,faqnum+1):
        question = checkpageload(driv,"//*[@id='id_question']").send_keys(lorem[:80] + " ?")
        answer = checkpageload(driv,"//*[@id='id_answer']").send_keys(lorem)
        savefaq = checkpageload(driv,"//*[@id='faq_form']/div/div/input[2]").click()
def fp_month(driv):
    fpm=driv.get("http://127.0.0.1:8000/admin/home/featured_product_of_month/add/")
    fpofmoth = Select(checkpageload(driv, "//*[@id='id_product_of_month']"))
    fpofmoth.select_by_index(1)
    save_fp_month = checkpageload(driv,"//*[@id='featured_product_of_month_form']/div/div/input[1]").click()
def fp_today(driv):
    driv.get("http://127.0.0.1:8000/admin/home/today_special/add/")
    fp1 = Select(checkpageload(driv, "//*[@id='id_product_1']"))
    fp1.select_by_index(1)
    fp2 = Select(checkpageload(driv, "//*[@id='id_product_2']"))
    fp2.select_by_index(2)
    fp3 = Select(checkpageload(driv, "//*[@id='id_product_3']"))
    fp3.select_by_index(3)
    fp_today_save = checkpageload(driv,"//*[@id='today_special_form']/div/div/input[1]").click()
login(driver)
add_category(driver,category_quantity)
add_product(driver,productlist,lorem)
youtube_link(driver,Youtub_link)
recepie(driver,recepie_num,lorem)
faq(driver,faq_num,lorem)
fp_month(driver)
fp_today(driver)
