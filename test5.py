import time, threading



def to():
    print(threading.current_thread().name)
# 新线程执行的代码:
def loop():

    n = 0
    while n < 5:
        n = n + 1
        # print('thread %s >>> %s' % (threading.current_thread().name, n))
        t = threading.Thread(target=to,args=())
        t.start()
        # time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

print('thread %s is running...' % threading.current_thread().name)
# t = threading.Thread(target=loop)
# t.start()
# t.join()
print('thread %s ended.' % threading.current_thread().name)

if __name__ == '__main__':
    while True:
        input("a or b\n")
        print("dsfsad\n")
        input("c or d\n")