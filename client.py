import numpy as np
import queue
import cv2, threading, time
from socket import *

q = queue.Queue(100000)  # 全局队列，获取图像的线程负责往队列里插入图片，另一个线程负责取图片发送，在socket建立后就启动


def send_img():
    while True:
        if not q.empty():   # 判断队列是否为空
            s.sendto(q.get(), addr)    # 向服务器发送数据
            # print(f'已发送{img.size}Bytes的数据')


# addr = ('192.168.43.106', 8080)
addr = ('localhost', 8080)          # 127.0.0.1表示本机的IP，相当于我和“自己”的关系
cap = cv2.VideoCapture(0)
s = socket(AF_INET, SOCK_DGRAM)  # 以utp的方式传输
th = threading.Thread(target=send_img)  # 创建一个线程
# th.setDaemon(True)
th.start()
while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    _, send_data = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 50])
    # 这里后面要加上while
    while True:
        if not q.full():
            q.put(send_data)   # 压缩之后的图像入队列
        break
    cv2.putText(img, "client", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('client_frame', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

s.close()  # 关闭连接
cv2.destroyAllWindows()