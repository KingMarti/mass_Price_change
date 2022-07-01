from selenium import webdriver
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import time

def manyvids():
    username=input('Enter your manyvids username: ')
    password=input('Enter your manyvids passowrd: ')
    price=input('Enter New Video Price: ')
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
    bot.get('https://manyvids.com/MV-Content-Manager/')
    print('loading content manager page')
    time.sleep(3)
    pages = bot.find_elements(By.CLASS_NAME,'page-link')
    print('Building Video Index, Please Wait')
    links=[]
    new_link_list=[]
    video_list =[]
    for page in pages:
        print('there are ',len(pages), 'pages of videos')
        drop_btn = bot.find_elements(By.XPATH,'//i[contains(@data-toggle,"dropdown")]')
        time.sleep(3)
        videos = bot.find_elements(By.CLASS_NAME,'manage-content__list-item')
        for vid in videos:
            video_links=bot.find_elements(By.XPATH,'//a[contains(@title,"Edit your content")]')
        for vid_link in video_links:
            links.append(vid_link.get_attribute('href'))
        print('Finished Indexing Videos On This Page')
        try:
            bot.find_element(By.CLASS_NAME,'next').click()
        except:
            print('unable to change page')
    for i in links:
        if i not in new_link_list:
            new_link_list.append(i)
    print('There are ', len(video_list), ' videos')
    for link in new_link_list:
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
    main()



def c4s():
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
    c=0
    while c == 0:
        vids=bot.find_elements(By.CLASS_NAME,'item_id')
        for v in vids:
            print(v.text)
            v=v.text
            id=v.replace('ID: ','')
            video_ids.append(id)
        time.sleep(4)
        try:
            bot.find_element(By.CLASS_NAME,'pagination_next-page-button').click()
        except:
            c=1
    print(len(video_ids),' video ids found')
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
    main()
def apc():
    username=input('Enter your APClips email: ')
    password=input('Enter your APclips passowrd: ')
    price=input('Enter the new token amount for the video: ')
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
        ptint('fail')
    video_ids=[]
    bot.get('https://apclips.com/model/video')
    time.sleep(3)
    tv=bot.find_element(By.XPATH,'//*[@id="library-tabs"]/li[1]/a/span').text
    print('tv is ',tv)
    tv=int(tv)
    btns=bot.find_elements(By.CLASS_NAME,'btn')
    while len(video_ids) != tv:
        for b in btns:
            if  b.get_attribute('href'):
                if 'https://apclips.com/video/edit/' in b.get_attribute('href'):
                    video_ids.append(b.get_attribute('href'))
                    print('video id found', b.get_attribute('href'))
                    print (len(video_ids), 'videos currently in list')
        if len(video_ids) != tv:
            bot.find_element(By.XPATH,'//*[@id="videos"]/div[2]/div[2]/ul/li[5]').click()
    for l in video_ids:
        bot.get(l)
        time.sleep(3)
        pin=bot.find_element(By.CLASS_NAME,'input-price')
        pin.clear()
        pin.send_keys(price)
        bot.find_element(By.XPATH,'//*[@id="video-form"]/div[3]/div[3]/button').click()
        time.sleep(4)
    main()

def onlyfans():
    username=input('Enter your OnlyFans email: ')
    password=input('Enter your OnlyFans passowrd: ')
    bot = uc.Chrome()
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
    price=input('Enter Your New Subsciption Price (The max is $50)')
    subp=bot.find_element(By.ID,'priceInput_1')
    subp.send_keys(Keys.CONTROL+'a')
    subp.send_keys(Keys.DELETE)
    subp.send_keys(price)
    bot.find_element(By.XPATH,'//*[@id="content"]/div[1]/div[2]/div/div/form/div[2]/button[2]').click()
    print('Price updated to ',price)
    bot.close()
    main()

def main():
    site_select=input('Select the site that you want to update pricing on:\n1)Manyvids\n2)Clips4Sale\n3)APClips\n4)Onlyfans\n5)Exit\n')
    if site_select=='1':
        manyvids()
    elif site_select=='2':
        c4s()
    elif site_select=='3':
        apc()
    elif site_select=='4':
        onlyfans()
    elif site_select=='5':
        exit()
if __name__=='__main__':
    main()