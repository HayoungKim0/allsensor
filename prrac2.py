import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import matplotlib.pyplot as plt
import scipy
import numpy as np
from scipy.interpolate import spline
import matplotlib.animation as animation
import threading

cred = credentials.Certificate('hkim-b7ce1-firebase-adminsdk-axn2j-4d2a78909a.json')  #download 받은 (새 비공개키 생성) 파일 path 경로
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {'databaseURL': 'https://hkim-b7ce1.firebaseio.com/'})

alldata = db.reference()
SensorData = alldata.child("SENSORS").child("자기장").get()

# 키와 쌍으로 이루어진 딕셔너리에서 values 값만 리스트로 가져오기.
value = list(SensorData.values())
length_value = len(value)

x = np.arange(1,length_value+1)    #array
#x = list(range(1,length_value+1))   #list
y = value



def raw_plt(x,y):
    #fig = plt.figure()
    plt.scatter(x,y,'.')
    plt.title("magnetic field")
    plt.xlabel("Number of measurement")
    plt.ylabel("y value")
    plt.show()

#raw_plt(x,y)

def curv_fit(x,y):

    plt.plot(x,y,'.r',label='raw data')
    #raw data plotting(red)
    plt.plot(x,y,'-b',label='raw data linear')
    #raw data 선 (blue)
    num = len(x)**2
    x_smooth = np.linspace(x.min(),x.max(),num)
    # x간격을 num개로 쪼갬 ex)x가 0~30이면 x= [0, 0.5, 1, 1.5 ... 29.5, 30]. num이 클수록 곡선처럼 보임
    y_smooth = scipy.interpolate.spline(x,y,x_smooth)
    #spline: 인접한 두 점에 대한 곡선 다항식
    #curve를 구할 기본 x,y 값. return 값 : x_smooth에 대한 spline y 값.
    plt.plot(x_smooth,y_smooth,'g',label='smoothing line')#(green)
    plt.legend(loc='best')
    plt.show()

curv_fit(x,y)

def update_data():
    up_data = db.reference()
    mag_data = up_data.child("SENSORS").child("자기장").get()
    value = list(mag_data.values())
    length_value = len(value)
    x = np.arange(1, length_value + 1)
    y = value

    #curv_fit(x,y)

    timer = threading.Timer(10,update_data)     #multithreading 10초마다 업데이트 함수 부르기
    timer.start()
    print(y)
    return x,y
update_data()

