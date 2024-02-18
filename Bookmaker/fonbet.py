import undetected_chromedriver as uc
import time
import datetime
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains as AC
from selenium.common.exceptions import *
from bs4 import BeautifulSoup
import re
import os
from PIL import Image

def get_selen_F():
    directory = 'C:\\Users\Professional\prct\Bookmaker\Scrin'
    driver=uc.Chrome()
    driver.get('https://www.fon.bet/sports/football/?dateInterval=6') # 6 - день
    time.sleep(35)
    dv_ish = driver.find_elements(By.XPATH,'//span[@class="caption--4XueAn"]')
    try:
        dv_ish[1].click()
    except Exception as ex:
        driver.refresh()
        print(ex)
    try:
        driver.find_element(By.XPATH,'//div[@class="table-component-market-combo__popup--2YGxBV"]').click()
    except Exception as ex:
        driver.refresh()
        print(ex)
    soup_1=BeautifulSoup(driver.page_source,'lxml')
    usl_1=""
    count=0
    dm=datetime.date.today().day
    driver.minimize_window()
    while True:
        if count<10:
            item = f'scr_{dm}_0{count}.png'  # названия файлов скринов
        else:
            item = f'scr_{dm}_{count}.png'
        patch = os.path.join(directory, item)  # путь к скринам
        try:
            driver.save_screenshot(patch)
        except Exception as ex:
            print(ex)
        usl = driver.find_elements(By.XPATH, '//div[@class="tournament-competition-section__caption--2ARlku"]')
        if len(usl)>0:
            print(len(usl))
 #           break
        try:
            dfe=driver.find_element(By.XPATH,'//div[@class="sport-base-event__main__caption--11Epy3 _clickable--3VqjxU _inline--4pgDR3"]').text
        except Exception as ex:
            print(ex)
            break
        if usl_1!=dfe:
            usl_1= dfe
        else:
            break
        a=driver.find_elements(By.XPATH,'//div[@class="scrollbar--SQKjxm custom-scrollbar-area__scrollbar--63fqKB _vertical--4rxDxV _vertical--6Cdhjn"]')
        action= AC(a[0])
        try:
            a[0].send_keys((Keys.PAGE_DOWN))
            time.sleep(randint(10, 15))
        except Exception.TimeoutException as ex:
            print (ex)
            break
        soup_2=BeautifulSoup(driver.page_source,'lxml')
        with open(f"index.html", "w", encoding="utf-8") as file:
            file.write(soup_1.prettify())
        for el in soup_2.body:
            soup_1.body.append(el)
        count+=1
        print(count)
    driver.close()
    driver.quit()
    with open(f"index.html", "w", encoding="utf-8") as file:
        file.write(soup_1.prettify())

def get_decomp():
    with open("index.html","r",encoding='utf-8') as file:
        data=file.read()
    soup=BeautifulSoup(data,'lxml')
    l_ff=[['div',{'style': re.compile(r'^height')}],['div',{'id':'footerContainer'}],
          ['div',{'class':'how2play__inner--2Xl3kD'}],['div',{'class':'slider--26rfFe _type_compact--7G3qLf'}],
          ['div',{'class':'header__inner _theme_red _lang_ru _sports'}],
          ['div',{'class':'session-dialog'}],
          ['div',{'class':'table-component-market-combo--7HIt0I _clickable--1jPpDa sport-section__market--1b352g'}],
          ['div',{'class':'horizontal-panel__items--2pfRES'}],
          ['div',{'class':'session-dialog__container'}],
          ['div',{'class':'banner-template__inner--437Y9N'}],
          ['div',{'class':'live-tex-chat-button--17qAzv fonG-live-tex-chat-button'}],
          ['div',{'class':'sport-table-sticky--6eD2U2'}],
          ['div',{'id':'headerContainer'}],
          ['div',{'style':'visibility: hidden; overflow: scroll; position: absolute; left: -100px; top: -100px; width: 50px; height: 50px;'}]]
    for i in range(len(l_ff)):
        st=soup.find_all(l_ff[i][0],attrs=l_ff[i][1])
        n=len(st)
        for k in st:
            k.decompose()
    with open(f"index_1.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())
    file_save = f'index_{datetime.date.today().month}_{datetime.date.today().day}.html'
    directory=f'C:\\Users\Professional\prct\Bookmaker\Scrin'
    with open(os.path.join(directory,file_save), "w", encoding="utf-8") as file:
        file.write(soup.prettify())

def get_png():
    directory=f'C:\\Users\Professional\prct\Bookmaker\Scrin'
    l_png=[]
    for item in os.listdir(directory):
        if item.endswith('.png'):
            l_png.append(item)
    l_image=[]
    image1 = Image.open(os.path.join(directory,l_png[0]))
    im1 = image1.convert('RGB')
    l_image.append(im1)
    for i, pn in enumerate(l_png[1:],start=2):
        file_name=f'image{i}'
        file_conv=f'(im{i}'
        path=os.path.join(directory,pn)
        file_name=Image.open(path)
        file_conv=file_name.convert('RGB')
        l_image.append(file_conv)
    scr_pdf=f'{datetime.date.today().month}_{datetime.date.today().day}.pdf'
    im1.save(os.path.join(directory,scr_pdf),save_all=True,append_images=l_image)
    for item in os.listdir(directory):
        if item.endswith('.png'):
            os.remove(os.path.join(directory,item))

def get_selen_LS(l_turn):
    with open('soup.html', "r", encoding='utf-8') as f:
        data = f.read()
    soup = BeautifulSoup(data, 'lxml')
    for lig in l_turn:
        driver = uc.Chrome()
        print(lig[0])
        try:
            if lig[3] is None:
                driver.close()
                continue
            driver.get(lig[3])
            time.sleep(randint(5, 15))
        except Exception.TimeoutException:
            print(lig[3])
            driver.refresh()
        try:
            title=driver.find_element(By.XPATH,'//div[@id="content"]').find_element(By.TAG_NAME,'h1').text
        except Exception:
            driver.refresh()
            title = driver.find_element(By.XPATH, '//div[@id="content"]').find_element(By.TAG_NAME, 'h1').text
        driver.minimize_window()
        if title=='Главные события':
            driver.close()
            continue
        try:
            foot=driver.find_element(By.XPATH,'//div[@class="bui-events-lazy-bar__buttons-3fe77d"]')
            button = foot.find_elements(By.XPATH, 'button[@class="bui-events-lazy-bar__button-a683cb"]')
            n = len(button)
            if n>0:
                driver.execute_script("arguments[0].click();", button[n - 1])
                time.sleep(randint(5, 15))
        except Exception as ex:       #      Exception: #: # as ex:
            pass
 #           print(f'{title} нет элемента')
        soup_1 = BeautifulSoup(driver.page_source, 'lxml')

#        tag = soup_1.find("div", id='content')
        tag=soup_1.find('div',class_="content__inner-wrapper-c1fc01")
        soup.body.append(tag)
        driver.close()
    st=soup.find_all('svg',class_='stat bui-event-row-widget__statistics-47424e')
    n=len(st)
    for k in st:
        k.decompose()
    with open(f"index_LS.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())
    file_back=f'{datetime.date.today().month}_{datetime.date.today().day}_LS.html'
    directory=f'C:\\Users\Professional\prct\Bookmaker\Scrin'
    with open(os.path.join(directory,file_back), "w", encoding="utf-8") as file:
        file.write(soup.prettify())

    get_selen_BS(l_turn)
    get_selen_Marafon(l_turn)
    driver.quit()

def get_selen_BS(l_turn):                    #(l_turn):
    with open('soup.html', "r", encoding='utf-8') as f:
        data = f.read()
    soup=BeautifulSoup(data,'lxml')
    driver = uc.Chrome()
    for lig in l_turn:
        if lig[6] is None:
            print(f'BS {lig[0]} нет URL')
            continue
        try:
            driver.get(lig[6])
            time.sleep(randint(5, 15))
        except Exception.TimeoutException:
            driver.refresh()
        try:
            driver.find_element(By.XPATH, '//div[@class="line-champ__header-toggle"]').click()
            time.sleep(randint(5, 15))
        except Exception as ex:
            print(ex)
            print(f'{lig}нет элемента')
            continue
        soup_1 = BeautifulSoup(driver.page_source, 'lxml')
        ud=soup_1.find_all('div',{'data-id-template': re.compile(r"\d{3}")}) #\d{3}
        if len(ud)==0:
            continue
        for u in ud:
            u.decompose()
        ud=soup_1.find_all('div',{'data-id-template': re.compile(r"[1-6]|[8-9]")}) #\d{3}
        l_ff =[['div', {'data-id-template': re.compile(r"\d{3}")}],['div', {'class':'footer-row footer-row_border'}],
               ['div', {'class': 'ps__rail-y'}],['div', {'data-id-template': '71'}]]
        for i in range(len(l_ff)):
            st=soup_1.find_all(l_ff[i][0],attrs=l_ff[i][1])
            for k in st:
                k.decompose()
        tag = soup_1.find("div", class_='container')
        soup.body.append(tag)
    with open(f"index_BS.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())
    file_back=f'{datetime.date.today().month}_{datetime.date.today().day}_BS.html'
    directory=f'C:\\Users\Professional\prct\Bookmaker\Scrin'
    with open(os.path.join(directory,file_back), "w", encoding="utf-8") as file:
        file.write(soup.prettify())
    driver.close()
#    driver.quit()


def get_selen_Marafon(l_turn):                      #  (l_turn):
    with open('soup.html', "r", encoding='utf-8') as f:
        data = f.read()
    soup = BeautifulSoup(data, 'lxml')
    driver = uc.Chrome()
    for lig in l_turn:
        if lig[8] is None:
            continue
        driver.get(lig[8])
        time.sleep(15)
        soup_1 = BeautifulSoup(driver.page_source, 'lxml')
        tag=soup_1.find('div',class_='events-container')
        soup.body.append(tag)
    with open(f"index_M.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())
    driver.close()
    driver.quit()

# get_selen_Marafon()

