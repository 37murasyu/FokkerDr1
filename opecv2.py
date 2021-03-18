"""import time
import threading


def func1():
    a=1
    while True:
        print("func1")
        a=a+1
        print(a)
        time.sleep(2)


def func2():
    while True:
        print("func2")
        time.sleep(2)


if __name__ == "__main__":
    thread_1 = threading.Thread(target=func1)
    thread_2 = threading.Thread(target=func2)

    thread_1.start()
    time.sleep(1)
    thread_2.start()"""
degree=0
try:
    while True:
        print("(-90 ~ 90)の範囲で回転角度数を入力してください")
        degree = float(input())+degree
        dc = 2.5 + (12.0-2.5)/180*(degree+90)
        print('現在の角度'+str(degree))
except KeyboardInterrupt:
    print('!!FINISH!!')