import requests,time

def main():
    t_end = time.time() + 60 * 15
    while time.time() < t_end:
        try:
            # r = requests.get('http://127.0.0.1:8000/')
            # r = requests.get('https://gm2mkz.deta.dev/hello_world') # leaky bucket,
            # r = requests.get('https://gm2mkz.deta.dev/') # token algorithm
            r = requests.get('https://zxkiws.deta.dev/')
            time.sleep(1)
            print(r.content)
        except KeyboardInterrupt as ki:
            print(ki.message)

if __name__ == '__main__':
    main()
    