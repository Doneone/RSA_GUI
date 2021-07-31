# -*- coding: UTF-8 -*-
from tkinter import *
import tkinter.filedialog
from tkinter.messagebox import *
from tkinter import scrolledtext,messagebox 
import time
import rsa
import binascii
import base64
import os 

path_d=""
path_e=""
class TKMain():
    xin = Tk()
    pathe = StringVar()
    pathd = StringVar()
    #路径赋值
    def selectPathD(self):
        #获取用户选择文件路径
        global path_d
        path_d = tkinter.filedialog.askopenfilename()
        self.pathd.set(path_d)

    def selectPathE(self):
        #获取用户选择文件路径
        global path_e
        path_e = tkinter.filedialog.askopenfilename()
        self.pathe.set(path_e)

    def views(self):
        self.xin.title('RSA 加解密')
        # 占位
        Label(self.xin, text="").grid(row=1, column=0)
        #设置按钮并绑定事件
        Button(self.xin, text="　生成新的密钥对　", command=self.create_rsa).grid(row=2, column=1, sticky=E)
        
        # 占位
        Label(self.xin, text="").grid(row=3, column=0)
        Label(self.xin, text="文件").grid(row=4, column=0, sticky=E)
        #设置entry组建用于记录文件路径
        self.xls_path = tkinter.StringVar()
        self.xls_path_public = tkinter.Entry(self.xin,stat="readonly")
        self.xls_path_public["textvariable"] = self.pathe
        self.xls_path_public.grid(row=4, column=1, sticky=E)
        Button(self.xin, text="　选择公钥　", command=self.selectPathE).grid(row=4, column=2, sticky=E)

        Label(self.xin, text="").grid(row=5, column=0)
        Label(self.xin, text="文件").grid(row=6, column=0, sticky=E)
        #设置entry组建用于记录文件路径
        self.xls_path = tkinter.StringVar()
        self.xls_path_private = tkinter.Entry(self.xin,stat="readonly")
        self.xls_path_private["textvariable"] = self.pathd
        self.xls_path_private.grid(row=6, column=1, sticky=E)
        Button(self.xin, text="　选择私钥　", command=self.selectPathD).grid(row=6, column=2, sticky=E)

        # 占位
        Label(self.xin, text="").grid(row=7, column=0)
        #设置按钮并绑定事件
        Button(self.xin, text="　加密　", command=self.rsa_encode).grid(row=8, column=1, sticky=E)
        # 占位
        #Label(self.xin, text="").grid(row=12, column=0)
        #设置按钮并绑定事件
        Button(self.xin, text="　解密　", command=self.rsa_decode).grid(row=8, column=2, sticky=E)

        # 占位
        Label(self.xin, text="").grid(row=14, column=0)
        # 滚动文本框-输入文本
        scrolW = 50  # 设置文本框的长度
        scrolH = 18  # 设置文本框的高度
        self.text_code = scrolledtext.ScrolledText(self.xin, width=scrolW, height=scrolH, wrap=tkinter.WORD)
        self.text_code.grid(row=17, columnspan=8, sticky=tkinter.E)
        #self.text.see(END)  # 一直查看文本的最后位置~
        self.text_code.insert('end', "请输入加解密内容!!!")
        self.text_code.update()#一直更新输出

        # 占位
        Label(self.xin, text="").grid(row=18, column=0)
        # 滚动文本框-输入文本
        scrolW = 50  # 设置文本框的长度
        scrolH = 18  # 设置文本框的高度
        self.text_result = scrolledtext.ScrolledText(self.xin, width=scrolW, height=scrolH, wrap=tkinter.WORD)
        self.text_result.grid(row=21, columnspan=8, sticky=tkinter.E)
        #self.text.see(END)  # 一直查看文本的最后位置~
        #self.text.insert('end', "请输入加解密内容!!!")
        #self.text_decode.update()#一直更新输出

    def create_rsa(self):
        if os.path.exists('private.pem') or os.path.exists('public.pem'):
            messagebox.showinfo(title='Error', message='当前目录下已存在密钥对')
        else:
            f, e = rsa.newkeys(1024)  # 生成公钥、私钥
            e = e.save_pkcs1() # 保存为 .pem 格式

            with open("private.pem", "wb") as x: # 保存私钥
                x.write(e)
            f = f.save_pkcs1() # 保存为 .pem 格式
            with open("public.pem", "wb") as x: # 保存公钥
                x.write(f)
            messagebox.showinfo(title='success', message='private.pem，public.pem已保存')
    def rsa_encode(self):
        global path_e
        if path_e=="":
            messagebox.showinfo(title='Error', message='请选择公钥文件路径')
        encode_string=self.text_code.get('1.0', 'end-1c')
        print(encode_string)
        with open(path_e, "rb") as x:
        #f = x.read()
        #print(f)
            f_key = rsa.PublicKey.load_pkcs1(x.read())
        cipher_text = rsa.encrypt(encode_string.encode("utf-8"), f_key) # 使用公钥加密
        self.text_result.insert('end', base64.b64encode(cipher_text)) 
        self.text_result.update()
    def rsa_decode(self):
        global path_d
        if path_d=="":
            messagebox.showinfo(title='Error', message='请选择公钥文件路径')
        with open(path_d, "rb") as x:
            e = x.read()
        decode_string=self.text_code.get('1.0', 'end-1c')
        e = rsa.PrivateKey.load_pkcs1(e)  # load 私钥
        text = rsa.decrypt(base64.b64decode(decode_string), e)  # 使用私钥解密
        self.text_result.delete(1.0, END)
        self.text_result.insert('end',text.decode("utf-8")) 
        self.text_result.update()
    #启动
    def app(self):
        self.views()
        mainloop()

def main():
    TKMain().app()

if __name__ == "__main__":
    main()