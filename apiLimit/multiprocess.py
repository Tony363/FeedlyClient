import time
from multiprocessing import Process,Manager,Value

class test:
    def __init__(self):
        self.manager = Manager()
        # self.cache = self.manager.list()
        self.token = self.manager.Value('i',0)
        self.s_time = time.time()

    def func1(self):
        while True:
            self.token.value += 1
            if self.token.value >= 10:
                # print("too many requests received")
                pass
            else:
                print("hello world")
                

    def func2(self):
        while True:
            if time.time() - self.s_time >= 5:
                print("TIME: ",time.time() - self.s_time >= 5)
                # self.cache[:] = []
                self.token.value = 0
                print(self.token.value)
                self.s_time = time.time()

if __name__ == '__main__':
    Test = test()
    
    p2 = Process(target=Test.func1)
    p2.start()
    p1 = Process(target=Test.func2)
    p1.start()

    p2.join()
    p1.join()
