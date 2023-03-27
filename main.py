import random
import struct
import threading

import serial
import time
import string
import binascii

import tkinter as tk

# import tk as tk


run_flag: bool = False
glb_x: int = 0
glb_y: int = 0


def float_to_hex(f):
    return str(hex(struct.unpack('<I', struct.pack('<f', f))[0]))


def random_send():
    list_32 = ['dc', 'ff', '05', '04', 00, 00, 00, 00, '14', 00, 00, 00, 00, '24', '11', '22', '33', '44', '34', '44',
               '22',
               '33', '44', '48', '31', '30', '30', '31', '30', '30', '30', '31']
    str_com = user_text.get()
    dev = serial.Serial(str_com, 115200)
    if dev.is_open:
        print("port open success")
    while run_flag:

        x = random.randint(0, 360)
        global glb_x
        glb_x = x
        list_0_360 = []
        a = float_to_hex(x)
        for i_1 in range(2, 9, 2):
            b = a[i_1:i_1 + 2]
            # print('b:  ',b)
            list_0_360.append(b)  # 分割成了四位
        list_32[4:8] = list_0_360

        y = random.randint(-90, 90)
        global glb_y
        glb_y = y
        list_90_90 = []
        c = float_to_hex(y)
        for i_2 in range(2, 9, 2):
            d = c[i_2:i_2 + 2]
            # print('d:  ', d)
            list_90_90.append(d)
        list_32[9:13] = list_90_90

        for i_3 in range(0, 32):
            if list_32[i_3] == '' or list_32[i_3] == '0':
                list_32[i_3] = '00'

                # dev.write(list_32.encode())
            xxxx = ''
            for i_4 in range(len(list_32)):
                xxxx += list_32[i_4]
                xxxx += ' '

        # print("buf is " + xxxx)
        print("x is " + str(x) + " y is " + str(y))
        dev.write(bytes.fromhex(xxxx))  # 发送命令
        time.sleep(3)  # 延时


# random_send()
def start_udp_thread():
    udp_thread = threading.Thread(target=random_send, name='aa')
    udp_thread.setDaemon(True)
    udp_thread.start()
    get_flow_id()
    global run_flag
    run_flag = True


def stop_udp():
    global run_flag
    run_flag = False


def get_flow_id():
    string = '当前坐标： x =' + str(glb_x) + " y =" + str(glb_y)
    dstr.set(string)
    root.after(100, get_flow_id)


root = tk.Tk()
root.geometry("400x300")
root.title("ptz随机坐标测试")

tk.Label(root, text="请输入当前串口：").pack()
user_text = tk.Entry()
user_text.pack()

tk.Button(root, text="开始运行", width=15, height=3, command=start_udp_thread).pack()
tk.Button(root, text="停止运行", width=15, height=3, command=stop_udp).pack()

dstr = tk.StringVar()
lb = tk.Label(root, textvariable=dstr)
lb.pack()

root.mainloop()
