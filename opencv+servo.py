# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 18:46:05 2021

@author: villa
"""
import time
import threading

import cv2
import numpy as np

#GPIOの初期設定 
import RPi.GPIO as GPIO
center_x=320

GPIO.setmode(GPIO.BCM)
#GPIO4を出力端子設定 
GPIO.setup(4, GPIO.OUT)
#GPIO4をPWM設定、周波数は50Hz 
p = GPIO.PWM(4, 50)
        

def func1():
    while True:
        def red_detect(img):
            # HSV色空間に変換
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # 赤色のHSVの値域1
            hsv_min = np.array([0,70,0])
            hsv_max = np.array([5,255,255])
            mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

            # 赤色のHSVの値域2
            hsv_min = np.array([135,70,0])
            hsv_max = np.array([179,255,255])
            mask2 = cv2.inRange(hsv, hsv_min, hsv_max)
            
            return mask1 + mask2
        try:
            def analysis_blob(binary_img):
                #2値画像のラベリング処理
                label=cv2.connectedComponentsWithStats(binary_img)
                
                #ブロブ情報を項目別に抽出
                n=label[0]-1
                data=np.delete(label[2],0,0)
                center=np.delete(label[3],0,0)
                
                #ブロブ面積最大のインデックス
                max_index=np.argmax(data[:,4])
                
                #面積最大ブロブの情報格納用
                maxblob={}
                
                #面積最大ブロブの各種情報
                maxblob["upper_left"]=(data[:,0][max_index],data[:,1][max_index])
                maxblob["width"]=data[:,2][max_index]
                maxblob["height"]=data[:,3][max_index]
                maxblob["area"]=data[:,4][max_index]
                maxblob["center"]=center[max_index]
                
                return maxblob
            
            
            def main():
            # カメラのキャプチャ
                cap = cv2.VideoCapture(0)
            
                while(True):
                # フレームを取得
                    ret, frame = cap.read()
                # 赤色検出
                    mask = red_detect(frame)
                # マスク画像をブロブ解析    
                    target=analysis_blob(mask)
                    
                # 面積最大のブロブの中心座標
                    center_x=int(target["center"][0])
                    center_y=int(target["center"][1])
                # ブロブの中心に緑円の描画
                    cv2.circle(frame,(center_x,center_y),7,(0,200,0),thickness=2,lineType=cv2.LINE_AA)

                # 結果表示
                    cv2.imshow("Frame", frame)
                    """cv2.imshow("Mask", mask)"""

                # qキーが押されたら途中終了
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break

                cap.release()
                cv2.destroyAllWindows()


            if __name__ == '__main__':
                main()
        except:
            import sys
            print("Error:",sys.exc_info()[0])
            print(sys.exc_info()[1])
            import traceback
            print(traceback.format_tb(sys.exc_info()[2]))
        time.sleep(1)


def func2():
    while True:
        if center_x>319:
            
            #Duty Cycle 0% 
            p.start(0.0)
            time.sleep(1.0)
            #GPIO4を出力端子設定 
            """GPIO.setup(5, GPIO.OUT)
            #GPIO4をPWM設定、周波数は50Hz 
            q = GPIO.PWM(5, 50)
            #Duty Cycle 0% 
            q.start(0.0)
            #-90°の位置へ移動 
            q.ChangeDutyCycle(2.5)"""
            time.sleep(1.0)

            #少しずつ回転
            dc = 2.5 + (12.0-2.5)/180*(degree+90)
            for degree in range(dc, -90,-1):
                p.ChangeDutyCycle(dc)
                """q.ChangeDutyCycle(dc/2)"""
                time.sleep(0.03)
                p.ChangeDutyCycle(0.0)#一旦DutyCycle0%にする
                """q.ChangeDutyCycle(0.0)#一旦DutyCycle0%にする"""
        time.sleep(1)
def func3():
    while True:
        
            for degree in range(dc, -90,-1):
                p.ChangeDutyCycle(dc)
                time.sleep(0.03)
                p.ChangeDutyCycle(0.0)#一旦DutyCycle0%にする

            time.sleep(1)

if __name__ == "__main__":
    thread_1 = threading.Thread(target=func1)
    thread_2 = threading.Thread(target=func2)
    
    thread_1.start()
    thread_2.start()