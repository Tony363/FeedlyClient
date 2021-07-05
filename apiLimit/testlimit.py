import requests,time

def main():
    t_end = time.time() + 60 * 15
    while time.time() < t_end:
        try:
            # r = requests.get('http://127.0.0.1:8000/tokenAlgo')
            # r = requests.get('http://127.0.0.1:8000/bucketAlgo/Hello_World')
            #r = requests.get('https://127.0.0.1:8000/detabase/Hello_World')
            # r = requests.get('https://u42jtn.deta.dev/tokenAlgo')
            # r = requests.get('https://u42jtn.deta.dev/bucketAlgo/Hello_World')
            r = requests.get('https://u42jtn.deta.dev/detabase/Hello_World')
            
            #r = requests.get('https://y399sm.deta.dev/leakyBucket')
            #r = requests.get('https://puuanx.deta.dev/tokenAlgo')
            #r = requests.get('http://127.0.0.1:8081/tokenAlgo')
            #r = requests.get('http://127.0.0.1:8081/leakyBucket')

            time.sleep(1)
            print(r.content)
        except KeyboardInterrupt as ki:
            exit(0)

if __name__ == '__main__':
    main()
    
