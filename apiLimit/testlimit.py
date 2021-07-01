import requests,time

def main():
    t_end = time.time() + 60 * 15
    while time.time() < t_end:
        try:
            r = requests.get('http://127.0.0.1:8000/')
            time.sleep(1)
            print(r.content)
        except KeyboardInterrupt as ki:
            print(ki.message)

if __name__ == '__main__':
    main()
    