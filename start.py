im = 0
while im==0:
    try:
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
        import os
        import update_prices
        import backup
        im =1

    except ImportError:
        print('Installing Required Dependancies')
        import sys
        try:
            import subprocess
            print('Installing Python dependancies')
            packages=['selenium','undetected_chromedriver']
            for package in packages:
                try:
                    print('installing ',package)
                    subprocess.check_call([sys.executable, "-m", "pip", "install",package])
                except:
                    pip=subprocess.run(['curl', 'https://bootstrap.pypa.io/get-pip.py','-o get-pip.py'])
                    print(pip.stdout)
                    print('instralling pip package manager')
                    subprocess.run('get-pip.py')
                    os.remove('get-pip.py')
                    print('pip installed')
                    print('installing required dependancies')
                    subprocess.check_call([sys.executable, "-m", "pip", "install",package])

        except:
            print('failed to install dependancies')

def run():
    func=input('\n1)Create Backup Of Current Pricing\n2)Change / Restore Pricing\n3)Exit\n')
    if func=='1':
        backup.main()
    elif func=='2':
        update_prices.main()
    elif func =='3':
        exit()
if __name__=='__main__':
    run()