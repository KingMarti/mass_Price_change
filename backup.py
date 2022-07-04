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
import start
db_name='pricing.db'

def manyvids():
    site_name='manyvids'
    username=input('Enter your manyvids username: ')
    password=input('Enter your manyvids passowrd: ')
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    bot = uc.Chrome(options=options)
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
    bot.get('https://manyvids.com/MV-Content-Manager/')
    print('loading content manager page')
    time.sleep(3)
    i=0
    videos=[]
    last_page='f'
    print('Getting video data')
    while last_page=='f':
        containers=bot.find_elements(By.CLASS_NAME,'manage-content__list-item')
        video_links=bot.find_elements(By.XPATH,'//a[contains(text(),"Edit")]')
        titles=bot.find_elements(By.CLASS_NAME,"manage-content__list-item__title")
        prices=bot.find_elements(By.CLASS_NAME,'manage-content__list-item__label--price')
        for item in containers:
            id_count=str(i+1)
            try:
                ids=bot.find_elements(By.XPATH,'//*[@id="content-items-sorting"]/li['+id_count+']')
            except:
                print('didnt find ids')
            try:
                res=NULL
                ftype=NULL
                insert_data=('Manyvids',titles[i].text,prices[i].text,ids[0].get_attribute('data-content-id'),res,ftype)
                if insert_data not in videos:
                    videos.append(insert_data)
                print(insert_data)
            except:
                print('failed insert data')
                exit()
            i+=1
        try:
            time.sleep(3)
            print('looking for next button')
            bot.find_element(By.XPATH,'/html/body/div[6]/div/div/ul/li[5]/a').click()
            print('loading next page')
            i=0
            time.sleep(5)            
        except:
            print('on last page')
            last_page='t'
            print('there are ',len(videos),' that were scanned')
            time.sleep(10)
    ############### DB Connect #############
    try:
        conn =sqlite3.connect(db_name)
        print(sqlite3.version)
        time.sleep(5)
        c = conn.cursor()
    except Error as e:
        print(e)
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS pricing_data ([id] INTEGER PRIMARY KEY,[site_name] TEXT NOT NULL,[vid_title] TEXT NOT NULL,[price] TEXT NOT NULL,[link] TEXT UNIQUE NOT NULL,[res] TEXT,[ftype] TEXT)''')
    except Error as e:
        print(e)
    try:
        for d in videos:
            sql = ''' INSERT INTO pricing_data(site_name,vid_title,price,link,res,ftype)
        VALUES(?,?,?,?,?,?) '''
            c.execute(sql, d)
            conn.commit()
        print('video written to db')
    except Error as e:
        print('Could not add data to database error: ',e)
    change_price=input('Do you want to bulk change the pricing? (y/n): ')
    if change_price =='n':
        print('All Pricing has been backed up')
        bot.close()
        start.run()
    elif change_price =='y':
        price=input('Enter the new price to apply across all videos: ')
        for l in videos:
            link='https://www.manyvids.com/Edit-vid/'+l[3]
            print(l[1],' ',link)
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
        print('all prices updated')
        bot.close()
    start.run()



def c4s():
    site_name='c4s'
    username=input('Enter your Clips4Sale username: ')
    password=input('Enter your Clips4Sale passowrd: ')
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    bot = uc.Chrome(options=options)
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
    
    bot.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
    time.sleep(1)
    try:
        bot.find_element(By.XPATH,'/html/body/div[2]/div[2]/form/input').click()
        time.sleep(2)
    except:
        pass
    vid_page=bot.get('https://admin.clips4sale.com/clips/list')
    time.sleep(3)
    video_ids=[]
    bot.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    clip_url='https://admin.clips4sale.com/clips/show/'
    data=[]
    c=0
    while c == 0:
        i=2
        t=0
        vids=bot.find_elements(By.CLASS_NAME,'item_id')
        titles=bot.find_elements(By.CLASS_NAME,'item_title')
        for v in vids:
            #print(v.text)
            price=bot.find_element(By.XPATH,'//*[@id="frm_list"]/table[1]/tbody/tr['+str(i)+']/td[3]/ul/li[3]/span[2]')
            res=bot.find_element(By.XPATH,'//*[@id="frm_list"]/table[1]/tbody/tr['+str(i)+']/td[3]/ul/li[7]/span[2]')
            ftype=bot.find_element(By.XPATH,'//*[@id="frm_list"]/table[1]/tbody/tr['+str(i)+']/td[3]/ul/li[6]/span[2]')
            v=v.text
            print(v,' ',titles[t].text,' ', price.text, ' ', res.text, ' ',ftype.text)
            data.append([site_name,titles[t].text,price.text,v,res.text,ftype.text])
            id=v.replace('ID: ','')
            video_ids.append(id)
            i+=1
            t+=1
        try:
            bot.find_element(By.CLASS_NAME,'pagination_next-page-button').click()
        except:
            c=1
    print(len(video_ids),' video ids found')
        ############### DB Connect #############
    try:
        conn =sqlite3.connect(db_name)
        print(sqlite3.version)
        time.sleep(5)
        c = conn.cursor()
    except Error as e:
        print(e)
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS pricing_data ([id] INTEGER PRIMARY KEY,[site_name] TEXT NOT NULL,[vid_title] TEXT NOT NULL,[price] TEXT NOT NULL,[link] TEXT UNIQUE NOT NULL,[res] TEXT,[ftype] TEXT)''')
    except Error as e:
        print(e)
    try:
        for d in data:
            sql = ''' INSERT INTO pricing_data(site_name,vid_title,price,link,res,ftype)
        VALUES(?,?,?,?,?,?) '''
            c.execute(sql, d)
            conn.commit()
        print('video written to db')
    except Error as e:
        print('Could not add data to database error: ',e)
    change_price=input('Do you want to chnage all video prices?(y/n): ')
    if change_price == 'n':
        print('All prices have been backed up')
        bot.close()
        start.run()
    elif change_price =='y':
        price=input('Enter the new price for the videos:\nNOTE: THE PRICE NEEDS TO BE AVALIBULE IN C4S DROPDOWN\n THESE ARE FROM $10.99 to $999.99 IN $1 INCREMENTS\n: ')
        while len(video_ids)!=0:
            for i in video_ids:
                bot.get(clip_url+i)
                time.sleep(3)
                bot.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
                time.sleep(3)
                pdd=Select(bot.find_element(By.ID,'clip_price'))
                pdd.select_by_visible_text(price)
                time.sleep(3)
                smb=bot.find_element(By.ID,'submitButton').click()
                time.sleep(4)
                print('Price updated for video id:',i)
                video_ids.remove(i)
                print(len(video_ids), ' left to change')
        print('All video prices updated, now closing browser session')
        bot.close()
        start.run()

def apc():
    site_name='apc'
    username=input('Enter your APClips email: ')
    password=input('Enter your APclips passowrd: ')
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    bot = uc.Chrome(options=options)
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
    video_ids=[]
    bot.get('https://apclips.com/model/video')
    time.sleep(3)
    tv=bot.find_element(By.XPATH,'//*[@id="library-tabs"]/li[1]/a/span').text
    print('tv is ',tv)
    tv=int(tv)
    btns=bot.find_elements(By.CLASS_NAME,'btn')
    data=[]
    res=NULL
    ftype=NULL
    i=0
    while len(video_ids) != tv:
        for b in btns:
            if  b.get_attribute('href'):
                if 'https://apclips.com/video/edit/' in b.get_attribute('href'):
                    video_ids.append(b.get_attribute('href'))
                    titles=bot.find_elements(By.CLASS_NAME,'video-title')
                    title=titles[i+1].text
                    print(title)
                    print('video id found', b.get_attribute('href'))
                    print (len(video_ids), 'videos currently in list')
                    temp_id='row'+b.get_attribute('href')
                    row_id=temp_id.replace('https://apclips.com/video/edit/','')
                    old_price=bot.find_element(By.XPATH,'//*[@id="'+row_id+'"]/div[2]/p[2]').text
                    old_price=old_price[-10:]
                    op=old_price.replace(' ','')
                    old_price=op.replace('Tokens','')
                    price=old_price
                    data.append([site_name,title,price,row_id,res,ftype])
                    i+=1
                            ############### DB Connect #############
    try:
        conn =sqlite3.connect(db_name)
        print(sqlite3.version)
        time.sleep(5)
        c = conn.cursor()
    except conn.Error as e:
        print(e)
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS pricing_data ([id] INTEGER PRIMARY KEY,[site_name] TEXT NOT NULL,[vid_title] TEXT NOT NULL,[price] TEXT NOT NULL,[link] TEXT UNIQUE NOT NULL,[res] TEXT,[ftype] TEXT)''')
    except Error as e:
        print(e)
        start.run()
    try:
        for d in data:
            sql = ''' INSERT INTO pricing_data(site_name,vid_title,price,link,res,ftype)
        VALUES(?,?,?,?,?,?) '''
            c.execute(sql, d)
            conn.commit()
        print('video written to db')
    except Error as e:
        print('Could not add data to database error: ',e)            
        if len(video_ids) != tv:
            bot.find_element(By.XPATH,'//*[@id="videos"]/div[2]/div[2]/ul/li[5]').click()
    change_price=input('Do you want to bulk change pricing?(y/n): ')
    if change_price=='n':
        print('all pricing backed up')
        bot.close()
        start.run()
    elif change_price=='y':
        price=input('please enter the new price for all videos: ')
        print('Updating video pricing, Please Wait...')
        while len(video_ids) != 0:
            for l in video_ids:
                bot.get(l)
                time.sleep(3)
                pin=bot.find_element(By.CLASS_NAME,'input-price')
                pin.clear()
                pin.send_keys(price)
                bot.find_element(By.XPATH,'//*[@id="video-form"]/div[3]/div[3]/button').click()
                time.sleep(4)
                print('Price updated for video link ',l )
                video_ids.remove(l)
                print(len(video_ids), ' left to update')
        bot.close()
        start.run()

def onlyfans():
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
    bot.get('https://onlyfans.com/')
    print('waiting 5 seconds for page to finish loading')
    time.sleep(10)
    data=[]
    sub_price=bot.find_element(By.XPATH,'//*[@id="content"]/div[1]/div[2]/div/div[1]/a/div[1]/div/span').text
    price=sub_price.replace('$','')
    res=NULL
    vid_title=0
    site_name='onlyfans'
    ftype=NULL
    link = 'https://onlyfans.com/my/settings/subscription'
    data.append([site_name,vid_title,price,link,res,ftype])
                                ############### DB Connect #############
    try:
        conn =sqlite3.connect(db_name)
        print(sqlite3.version)
        time.sleep(5)
        c = conn.cursor()
    except conn.Error as e:
        print(e)
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS pricing_data ([id] INTEGER PRIMARY KEY,[site_name] TEXT UNIQUE NOT NULL,[vid_title] TEXT NOT NULL,[price] TEXT NOT NULL,[link] TEXT NOT NULL,[res] TEXT,[ftype] TEXT)''')
    except Error as e:
        print(e)
    try:
        for d in data:
            sql = ''' INSERT INTO pricing_data(site_name,vid_title,price,link,res,ftype)
        VALUES(?,?,?,?,?,?) '''
            c.execute(sql, d)
            conn.commit()
        print('video written to db')
    except Error as e:
        print('Could not add data to database error: ',e)  
    change_price=input('Do you want to change the price now?(y/n): ')
    if change_price =='n':
        print('Price has been backed up')
        bot.close()
        start.run()  
    elif change_price =='y':        
        bot.get('https://onlyfans.com/my/settings/subscription')
        price=input('Enter Your New Subsciption Price (The max is $50)')
        subp=bot.find_element(By.ID,'priceInput_1')
        subp.send_keys(Keys.CONTROL+'a')
        subp.send_keys(Keys.DELETE)
        subp.send_keys(price)
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
    site_select=input('\nSelect the site that you want to update pricing on:\n1)Manyvids\n2)Clips4Sale\n3)APClips\n4)Onlyfans\n5)Exit\n')
    if site_select=='1':
        manyvids()
    elif site_select=='2':
        c4s()
    elif site_select=='3':
        apc()
    elif site_select=='4':
        onlyfans()
    elif site_select=='5':
        q=input('\n1)Return To Main Menu\n2)Quit Program')
        if q=='1':
            start.run()
        elif q=='2':
            exit()
if __name__=='__main__':
    main()