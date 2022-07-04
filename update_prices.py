from asyncio.windows_events import NULL
from selenium import webdriver
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import time
import sqlite3
from sqlite3 import Error
import backup
import start
db_name='pricing.db'

def manyvids_up():
    restore_in=input('1)Restore Previous Pricing\n2)Bulk Set New Price (same price for all videos)\n')
    try:
        conn =sqlite3.connect(db_name)
        print(sqlite3.version)
        c = conn.cursor()
    except Error as e:
        print(e)
    c.execute("SELECT price,link FROM pricing_data WHERE site_name='Manyvids';")
    rows = c.fetchall()
    data=[]
    if restore_in == '1':
        for row in rows:
            print(row)
            p=row[0]
            id=row[1]
            price=p.replace('$','')
            link='https://www.manyvids.com/Edit-vid/'+id
            data.append([price,link])
            #print(link,' ',price)
            print(len(rows), ' videos pulled from database')
    elif restore_in =='2':
        backedup=input('Have you backed up your current pricing? (y/n): ')
        if backedup =='y':
            price=input('What is the new price you would like to set?: ')
            for row in rows:
                id=row[1]
                link=link='https://www.manyvids.com/Edit-vid/'+id
                data.append([price,link])
        else:
            print('creating a backup of current pricing')
            backup.manyvids()
    username=input('Enter your manyvids username: ')
    password=input('Enter your manyvids passowrd: ')
    bot = uc.Chrome()
    bot.get('https://www.manyvids.com/Login/')
    time.sleep(3)
    bot.find_element(By.ID,'triggerUsername').send_keys(username)
    bot.find_element(By.ID,'triggerPassword').send_keys(password)
    bot.find_element(By.ID,'loginAccountSubmit').click()
    print('username and password entered')
    try:
        time.sleep(3)
        bot.find_element(By.CLASS_NAME,'two-way-authentication')
        print('2fa detected, please enter your 2fa code in the site and continue to log in, press any key to continue when logged in')
        input()
    except:
        pass
    time.sleep(3)
    while len(data) != 0:
        for l in data:
            link=l[1]
            price=l[0]
            bot.get(link)
            time.sleep(3)
            pin=bot.find_element(By.ID,'appendedPrependedInput')
            pin.clear()
            time.sleep(3)
            pin.send_keys(Keys.CONTROL+'a')
            pin.send_keys(Keys.DELETE)
            pin.send_keys(price)
            print('sent price of ',price)
            bot.find_element(By.ID,'saveVideo').click()
            data.remove(l)
            print(len(data), ' Videos left to change')
    print('all prices updated')
    bot.close()
    start.run()

def c4s_up():
    restore_in=input('1)Restore Previous Pricing\n2)Bulk Set New Price (same price for all videos)\n')
    try:
        conn =sqlite3.connect(db_name)
        print(sqlite3.version)
        c = conn.cursor()
    except Error as e:
        print(e)
    c.execute("SELECT price,link FROM pricing_data WHERE site_name='c4s';")
    rows = c.fetchall()
    data=[]
    if restore_in == '1':
        for row in rows:
            p=row[0]
            id_temp=row[1]
            price_temp=p.replace('$','')
            price=price_temp.replace(' USD','')
            id=id_temp.replace('ID: ','')
            link='https://admin.clips4sale.com/clips/show/'+id
            data.append([price,link])
            #print(link,' ',price)
        print(len(rows), ' videos pulled from database')
    elif restore_in =='2':
        backedup=input('Have you backed up your current pricing? (y/n): ')
        if backedup =='y':
            price=input('What is the new price you would like to set?: ')
            for row in rows:
                id_temp=row[1]
                id=id_temp.replace('ID: ','')
                link=link='https://admin.clips4sale.com/clips/show/'+id
                data.append([price,link])
        else:
            print('creating a backup of current pricing')
            backup.c4s()
    site_name='c4s'
    username=input('Enter your Clips4Sale username: ')
    password=input('Enter your Clips4Sale passowrd: ')
    bot = uc.Chrome()
    bot.get('https://admin.clips4sale.com/login/')
    user=bot.find_element(By.ID,'username')
    user.clear()
    user.send_keys(username)
    site_pass=bot.find_element(By.ID,'password')
    site_pass.clear()
    site_pass.send_keys(password)
    time.sleep(1)
    try: 
        bot.find_element(By.TAG_NAME,'iframe')
        print('re-capcha detected, please complete captcha and press any key to continue')
        input()
    except:
        bot.find_element(By.CLASS_NAME,'login_btn').click()
    time.sleep(3)
    while len(data) != 0:    
        for d in data:
            clip_url=d[1]
            price=d[0]
            bot.get(clip_url)
            time.sleep(3)
            bot.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
            time.sleep(3)
            pdd=Select(bot.find_element(By.ID,'clip_price'))
            pdd.select_by_visible_text(price)
            time.sleep(3)
            smb=bot.find_element(By.ID,'submitButton').click()
            time.sleep(4)
            print('Price updated for video id:', d[1])
            data.remove(d)
            print(len(data), ' left to change')
    print('All video prices updated, now closing browser session')
    bot.close()
    start.run()
def apc_up():
    restore_in=input('1)Restore Previous Pricing\n2)Bulk Set New Price (same price for all videos)\n')
    try:
        conn =sqlite3.connect(db_name)
        print(sqlite3.version)
        c = conn.cursor()
    except Error as e:
        print(e)
    c.execute("SELECT price,link FROM pricing_data WHERE site_name='apc';")
    rows = c.fetchall()
    data=[]
    if restore_in == '1':
        for row in rows:
            print(row)
            p=row[0]
            id_temp=row[1]
            id=id_temp.replace('row','')
            price=p.replace('$','')
            link='https://apclips.com/video/edit/'+id
            data.append([price,link])
            #print(link,' ',price)
            print(len(rows), ' videos pulled from database')
    elif restore_in =='2':
        backedup=input('Have you backed up your current pricing? (y/n): ')
        if backedup =='y':
            price=input('What is the new price you would like to set?: ')
            for row in rows:
                id_temp=row[1]
                id=id_temp.replace('row','')
                link=link='https://apclips.com/video/edit/'+id
                data.append([price,link])
        else:
            print('creating a backup of current pricing')
            backup.apc()
    site_name='apc'
    username=input('Enter your APClips email: ')
    password=input('Enter your APclips passowrd: ')
    bot = uc.Chrome()
    bot.get('https://APClips.com/login')
    time.sleep(3)
    try:
        bot.find_element(By.CLASS_NAME, "challenge-form")
        print('Re-capcha detected, please complete the re-capcha manually and press any key to continue')
        input()
    except:
        print('no cap')
        time.sleep(600)
    print('looking for login')
    try:
        em=bot.find_element(By.ID,'email')
        em.clear()
        em.send_keys(username)
        pw=bot.find_element(By.ID,'pass')
        pw.clear()
        pw.send_keys(password)
        bot.find_element(By.XPATH,'//*[@id="loginForm"]/div[4]/button').click()
    except:
        print('couldnt find login')
    time.sleep(3)
    try:
        if bot.current_url == 'https://apclips.com/model/twofactor':
            print('2fa detected, plase finish logging in and press any key to continue')
            input()
            time.sleep(3)

    except:
        print('fail')
    while len(data) !=0:
        for l in data:
                bot.get(l[1])
                time.sleep(3)
                pin=bot.find_element(By.CLASS_NAME,'input-price')
                pin.clear()
                pin.send_keys(l[0])
                bot.find_element(By.XPATH,'//*[@id="video-form"]/div[3]/div[3]/button').click()
                time.sleep(4)
                print('Price updated for video link ',l[1] )
                data.remove(l)
                print(len(data), ' left to update')
        bot.close()
        start.run()
    
def onlyfans_up():
    restore_in=input('1)Restore Previous Pricing\n2)Bulk Set New Price (same price for all videos)\n')
    try:
        conn =sqlite3.connect(db_name)
        print(sqlite3.version)
        c = conn.cursor()
    except Error as e:
        print(e)
    c.execute("SELECT price,link FROM pricing_data WHERE site_name='onlyfans';")
    rows = c.fetchall()
    data=[]
    if restore_in == '1':
        for row in rows:
            print(row)
            price=row[0]
            link=row[1]
            data.append([price,link])
            #print(link,' ',price)
            print(len(rows), ' videos pulled from database')
    elif restore_in =='2':
        backedup=input('Have you backed up your current pricing? (y/n): ')
        if backedup =='y':
            price=input('What is the new price you would like to set?: ')
            for row in rows:
                link=row[1]
                data.append([price,link])
        else:
            print('creating a backup of current pricing')
            backup.onlyfans()
    username=input('Enter your OnlyFans email: ')
    password=input('Enter your OnlyFans passowrd: ')
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    bot = uc.Chrome(options=options)
    url=bot.get('https://onlyfans.com/')
    time.sleep(5)
    login_user=bot.find_element(By.XPATH,'//*[@id="input-20"]').send_keys(username)
    login_password=bot.find_element(By.XPATH,'//*[@id="input-23"]').send_keys(password)
    time.sleep(1)
    login_btn=bot.find_element(By.XPATH,'/html/body/div/div[2]/div/div/div[2]/div/form/button[1]').click()
    time.sleep(4)
    bot.get('https://onlyfans.com/my/vault')
    time.sleep(5)
    if bot.current_url != 'https://onlyfans.com/my/vault':
        print('Unable to login with onlyfans credentals, please provide your twitter details to log in via twitter instead')
        tw_username=input('Please enter your twitter username: ')
        tw_pass=input('Please enter your twitter password: ')
        tw_btn=bot.find_element(By.XPATH,'/html/body/div/div[2]/div/div/div[2]/div/form/a[1]').click()
        time.sleep(3)
        twitter_login_user=bot.find_element(By.XPATH,'//*[@id="username_or_email"]')
        twitter_login_user.clear()
        twitter_login_user.send_keys(tw_username)
        twitter_login_password=bot.find_element(By.XPATH,'//*[@id="password"]')
        twitter_login_password.clear()
        twitter_login_password.send_keys(tw_pass)
        twitter_login_btn=bot.find_element(By.XPATH,'//*[@id="allow"]').click()
        time.sleep(5)
        bot.get('https://onlyfans.com/my/vault')
        time.sleep(5)
        if bot.current_url != 'https://onlyfans.com/my/vault':
            print('Unable to log in via onlyfans or twitter, please try again later')
        bot.get('https://onlyfans.com/my/settings/subscription')
        for d in data:
            subp=bot.find_element(By.ID,'priceInput_1')
            subp.send_keys(Keys.CONTROL+'a')
            subp.send_keys(Keys.DELETE)
            subp.send_keys(d[0])
            change=bot.find_element(By.XPATH,'//*[@id="content"]/div[1]/div[2]/div/div/form/div[2]/button[2]')
            sure=input('Changeing your subscription will turn off all re-bills, are you sure you want to continue?(y/n)')
            if sure =='n':
                print('price not updated, returning to main menu')
                start.run()
            change.click()
        print('Price updated to ',price)
        bot.close()
        start.run()

def main():
    site_select=input('\nWhich site would you like to update prices on?\n1)manyvids\n2)clips4sale\n3)apc\n4)onlyfans\n5)exit\n')
    if site_select == '1':
        manyvids_up()
    elif site_select =='2':
        c4s_up()
    elif site_select =='3':
        apc_up()
    elif site_select =='4':
        onlyfans_up()
    elif site_select=='5':
        q=input('\n1)Return To Main Menu\n2)Quit Program')
        if q=='1':
            start.run()
        elif q=='2':
            exit()
if __name__=="__main__":
    main()