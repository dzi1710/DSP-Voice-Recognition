#Khai bao thu vien
import numpy as np
import matplotlib.pyplot as plt

#============================= 1. Tao moi truong am thanh random ===============================#
#Cai mot micro ao de lay tan so lay mau cho la 100Hz va thu am lien tuc trong vong 3 giay
fs = 100                    #Tan so lay mau
n = np.arange(0, 3, 1/fs)   #So mau trong vong 3 giay voi chu ky 1/fs => 1s lay duoc 100 mau

#Am thanh tu ben ngoai moi truong (am thanh khong mong muon -> quat, gio, xi xam), gia su tieng on nay bi giam xuong doi chut cho nho nho
mic_stream = np.random.randn(len(n)) * 0.25              #Cho tin hieu ngau nhien qua 300 mau, nhan 0.25 de giam 1/4 do lon tin hieu nhieu

#Vi du: Nguoi dung cat tieng noi tu giay 1.2 -> 1.7 (dai 0.5s) thi he thong se nhan dien the nao??
start_idx = int(1.2 * fs)           #Tai mau so 120 -> troi qua 1.2s
end_idx = int(1.7 * fs)             #Tai mau so 170 -> troi qua 1.7s
mic_stream[start_idx : end_idx] += np.sin(2 * np.pi * 10 * n[start_idx : end_idx])
#Luc nay ta nhet mot giong noi gia lap tu giay 1.2 -> 1.7 la mot song sin tuan hoan co tan so 10Hz, phep += la ta chong tieng noi len am thanh moi truong


#============================== 2. Xay dung thuat toan VAD (Tu tuong quan) ============================#
#Y tuong: Ta cho mot cua so chay voi kich thuoc nao do
#Sau do ta cho cua so dich qua mot doan co dinh nao do de quet het cai khoang thu am cua micro xem tu tuong quan
window_size = int(0.5 * fs)         #Kich thuoc cua so truot la chiem 50 mau moi lan truot
step_size = int(0.1 * fs)           #Moi lan cua so se truot tang len 10 mau
#Vd:            0       10      20      30      40      50      60      70      80      90      100 ------------->t
#step = 0       <---------------window_size--------------->
#step = 1               <---------------window_size--------------->
#step = 2                       <---------------window_size--------------->
#step = 3                                       <---------------window_size--------------->
#... cu moi lan truot no se tang len 10 mau de xet lien tiep 50 trong window

#VAD - VOICE ACTIVITY DETECTION - HANH DONG NHAN DIEN GIONG NOI 

vad_flag = np.zeros(len(n))         #Khoi tao bien co cho nhan dien tu tuong quan voi 0 -> TAT, 1-> BAT
vad_threshold = 25.0                #Muc nang luong de kich hoat bien co flag len 1

#Bat dau truot window
for i in range(0, len(n) - window_size, step_size):
    #Moi lan quet ta trich xuat cai frame -> tuc la khung am thanh do ra de xet
    frame = mic_stream[i : i + window_size]                 #Vi du tu 0 -> 50, 10 -> 60, 20 -> 70, 30 -> 80, ....
    #Ta biet tai l = 0, khi nay tu tuong quan la cao nhat vi tin hieu la giong nhau hoan toan
    rxx_0 = np.sum(frame ** 2)                              #Tong nang luong binh phuong -> Sieu lon neu giong nhau / Sieu nho neu khac nhau 
    #Ra quyet dinh rang co tieng nguoi hay la chi la tieng moi truong !! Neu nang luong > nguong => Co tieng nguoi
    if rxx_0 > vad_threshold:
        vad_flag[i : i + window_size] = 1                   #Boi vi tieng nguoi co tan so va chu ky vi the nen tu tuong quan se cao khi co tieng nguoi noi

#================================== 3. Truc quan hoa =================================#
plt.figure(figsize=(10, 6))

#Ta chia ra hai hinh, mot hinh la tin hieu dau vao, va mot hinh se la tin hieu tu tuong quan thu duoc
#Tin hieu thu duoc tu dau vao
plt.subplot(2, 1, 1)
plt.plot(n, mic_stream, color='red')
plt.title('1. Tin hieu thu tu Micro')
plt.ylabel('Bien do')
plt.xlabel('n (mau)')
plt.grid(True, linestyle='--', alpha = 0.6)

#Ket qua cua VAD (Tu tuong quan)
plt.subplot(2, 1, 2)
plt.plot(n, vad_flag, color='C1', linewidth = 2)
plt.fill_between(n, 0, vad_flag, color='C1', alpha = 0.3)   #Ham nay de cho nao ma vad_flag nho len 1 thi se duoc to dam, vi no loc di nhung so la 0 trong 300 mau
plt.title('2. Tin hieu tu tuong tu (VAD)')
plt.xlabel('n (mau)')
plt.ylabel('Trang thai nhan dien co tieng nguoi 0 -> Tat / 1 -> Bat')
plt.ylim(-0.2, 1.2)
plt.grid(True, linestyle='--', alpha = 0.6)

plt.tight_layout()
plt.show()
