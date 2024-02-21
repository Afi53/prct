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
from inspect import currentframe, getframeinfo
import match
from xl import load_l_turn,load_matches

l_match=[]
def lig_or_match(mt,tur):
    try:
        c = mt.find_element(By.XPATH, "./following-sibling::div[1]")
        tag = c.get_attribute('class')
        if tag == 'sport-competition--Xt2wb _clickable--QLum2 _compact--wuzr7':
            return
        elif tag == 'sport-event-separator--xZ16g _sub-event--Edkan':
            b = c.find_element(By.XPATH, "./following-sibling::div[1]")
            st_match(b,tur)
            return
        elif tag == 'sport-event-separator--xZ16g':
            b = c.find_element(By.XPATH, "./following-sibling::div[1]")
            st_match(b,tur)
            return
        else:
            print (f'ошибка {mt.tag_name, mt.text}')
    except Exception as ex:
        print(getframeinfo(currentframe()).lineno)
        print (mt.tag_name, mt.text)

def st_match(mt,tur):
    try:
        if mt.text=='':
            lig_or_match(mt,tur)
            return
        kom = mt.text.splitlines()[0]
    except Exception as ex:
        print(getframeinfo(currentframe()).lineno)
        print(ex)
        print(mt.get_attribute('class'))
        lig_or_match(mt,tur)
        return
    try:
        if (not  ' — ' in kom) or ('матч' in kom):
            try:
                lig_or_match(mt,tur)
                return
            except Exception as ex:
                print(getframeinfo(currentframe()).lineno)
                print(f'ошибка {kom}')
                lig_or_match(mt, tur)
        else:
            try:
                date = mt.text.splitlines()[1].split(' ')[0].strip()
                if date=='Матч':
                    date = mt.text.splitlines()[2].split(' ')[0].strip()
                elif date.find(':')!=-1 or date=='Не':
                    date='Сегодня'
                data = match.transform_date(date)
            except Exception as ex:
                print(getframeinfo(currentframe()))
                data = f'ошибка даты'
            k_1 = kom.split(' — ')[0]
            try:
                k_2 = kom.split(' — ')[1]
            except Exception as ex:
                print(f'нет второй команды {k_1}')
            try:
                match_1 = mt.find_elements(By.XPATH,'./div[@class="factor-value--zrkpK _normal--LfrKg _value--XNfOo _interactive--xaSFF table-component-factor-value_single--TOTnW _compact--K5sVc"]')
            except Exception as ex:
                print(getframeinfo(currentframe()).lineno)
                print(f'ошибка {kom}')
            l_st=[]
            for i in range(6):
                try:
                    st = float(match_1[i].text)
                except Exception as ex:
                    st = None
                l_st.append(st)
            rq = match.Match(tur, data, k_1, k_2, l_st[0], l_st[1], l_st[2], l_st[3], l_st[4], l_st[5])
            print(vars(rq).values())
            l_match.append(rq)
            lig_or_match(mt,tur)
            return
    except Exception as ex:
        print(getframeinfo(currentframe()).lineno)
        print(f'ошибка {kom}')
        lig_or_match(mt, tur)

def get_selen_F():
    directory = 'C:\\Users\Professional\prct\Bookmaker\Scrin'
    dm=datetime.date.today().day
    fp = 'C:\\Users\Professional\prct\Bookmaker\WR.xlsx'
    sh = 'Лист2'
    d_ligs=match.d_liges()  # словарь лиг
    k = 1
    driver = uc.Chrome()
    driver.get('https://www.fon.bet/sports/football/?dateInterval=6')  # 6 - день
    time.sleep(randint(40, 50))

    c=driver.find_elements(By.XPATH,'//div[@class="row--jpv3h _clickable--vp1EO"]')[1]
    c.click()   # открываем список Исходы, тоталы, форы двойные шансы
    try:
        f=driver.find_element(By.XPATH,'//div[@data-source="portal"]')
    except Exception as ex:
        print(ex)
    try:
        g = f.find_elements(By.XPATH, './/div/div/div')[3].click() # выбор двойные шансы
    except Exception as ex:
        print(ex)
    d=True
    l_turs = []
    while True:
        if d==False:
            break
        if k < 10:
            item = f'scr_{dm}_0{k}.png'  # названия файлов скринов
        else:
            item = f'scr_{dm}_{k}.png'
        patch = os.path.join(directory, item)  # путь к скринам
        try:
            driver.save_screenshot(patch)
        except Exception as ex:
            print(ex)
        liges = driver.find_elements(By.XPATH,'//div[@class="sport-competition--Xt2wb _clickable--QLum2 _compact--wuzr7"]')  # список лиг на странице
        if k==1:
            liges = liges[1:]  # а на 1-ой странице обрезаем первую строку
        for lig in liges:
            try:
                tur = lig.text.splitlines()[0].title().strip()
            except:
                print(getframeinfo(currentframe()).lineno)
                tur = lig.text.strip()
            if 'Жен' in tur or 'Fc' in tur:
                d=False
                break
            if ('До ' in tur)  or ('Кубок' in tur) or ('Хозяева' in tur):
                continue
            elif tur=='Босния И Герцеговина. Премьер-Лига':
                tur='Босния и Герцеговина. Премьер-Лига'
            else:
                tur = ' '.join(tur.split()[:3])  # названия лиг 3 слова
            print(tur)
            if not tur in d_ligs.values():  # поиск в значениях словаря лиг
                try:
                    tur= d_ligs[tur]  # поиск по ключам
                except KeyError:
                    if tur!=l_turs[:-1]:
                        l_turs.append(tur) # добавляем в список лиг без словаря
                        print(getframeinfo(currentframe()).lineno)
                        print(f'{tur} ошибка словаря')
                    continue
            try:
                mt = lig.find_element(By.XPATH, "./following-sibling::div[1]")  # переход к тегу с матчем
                tag = mt.get_attribute('class')
            except Exception as ex:
                print(getframeinfo(currentframe()).lineno, tag)
#                print(ex)
                continue
            st_match(mt,tur)

        try:                                  # поиск элемента для скроллинга
            a = driver.find_elements(By.XPATH, '//div[@class="scrollbar--y_qLI scroll-area__scrollbar--L_UN7 _vertical--GdKOZ _vertical--aYpNv"]')  # /span
        except Exception as ex:
            print(getframeinfo(currentframe()))
            break
        action = AC(a[1])
        try:
            a[1].send_keys(Keys.PAGE_DOWN)  # страница вниз
            time.sleep(20)
            a[1].send_keys(Keys.ARROW_UP)   # две строки вверх
            time.sleep(15)
            k += 1  # кол-во страниц
            print(k)
            if k == 50:
                break
        except Exception as ex:
            print(getframeinfo(currentframe()).lineno)
            print(ex)
    driver.close()
    driver.quit()
    try:
        load_l_turn(l_turs) # список лиг, которых нет в словаре
    except Exception as ex:
        print(ex)
    return l_match,fp,sh


# l_matches,fp,sh=get_selen_F()
# load_matches(l_matches,fp,sh)



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
        try:
            soup.body.append(tag)
        except Exception as ex:
            print(ex)
    with open(f"index_M.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())
    driver.close()
    driver.quit()



