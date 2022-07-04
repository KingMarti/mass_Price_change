import update_prices
import backup

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