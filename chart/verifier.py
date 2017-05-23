from database import *
import hashlib
import requests
import time

loop_time = 60

def make_url(account):
    userid = hashlib.md5(account.url.encode('utf-8')).hexdigest()
    return 'http://%s/secrets/%s' % (account.url, userid)

def make_flag(account):
    userid = hashlib.md5(account.url.encode('utf-8')).hexdigest()
    return "FLAG_%s" % userid

def has_flag(account):
    response = requests.get(make_url(account))
    return response.status_code == 200 and \
           make_flag(account) in str(response.content)

def put_flag(account):
    url = make_url(account)
    flag = make_flag(account)
    requests.post(url, data={'note': flag})
    print('uploaded flag: %s for url: %s' % (flag, url))



if __name__ == '__main__':
    while True:

        start_time = time.time()

        try:
            for account in Account.select():
                print(account.url, " ", end="")

                try:
                    is_up = has_flag(account)

                    if not is_up:
                        put_flag(account)
                        is_up = has_flag(account)

                except:
                    is_up = False

                account.is_up = is_up

                if is_up:
                    account.points += 10

                account.save()
                print("UP" if is_up else "DOWN")


            elapsed = time.time() - start_time
            time.sleep(loop_time - elapsed)

        except KeyboardInterrupt:
            break
