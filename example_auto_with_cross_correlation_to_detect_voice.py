#Khai bao thu vien can thiet
import numpy as np
import matplotlib.pyplot as plt

#========================= 1. Chuan bi MICRO va am thanh cho moi truong ===========================#
fs = 100                                                #Tan so lay mau cho tin hieu
f_voice = 10                                          #Tan so ma con nguoi phat ra

#Ta can co mau cua chu -> vi du chu "BAT" (noi trong vong 0.5s va la song sin 10Hz)
n_template = np.arange(0, 0.5, 1/fs)    #Moi chu ky la 0.01s thi sau 0.5s lay duoc 50 mau
template_BAT = np.sin(2 * np.pi * f_voice * n_template)

#Ta chuan bi Micro thu am thuc te voi ngau nhien cac gia tri
n_total = np.arange(0, 3, 1/fs)             #Moi chu ky la 0.01 thi sau 3s lay duoc 300 mau
mic_stream = np.random.randn(len(n_total)) * 0.25                #Random trong khoang thoi gian lay 300 mau va giam 0.5 cac tin hieu nhieu moi truong

#Vi du tieng nguoi noi tu giay thu 1.2 -> giay thu 1.7 ta chuan bi khoang thoi gian noi do
start_idx = int(1.2 * fs)                         #1.2 * fs = 120, tai mau thu 120 voi chu ky la 0.01s thi xac dinh duoc tai 1.2s
end_idx = int(1.7 * fs)                           #1.7 * fs = 170, tai mau thu 170 voi chu ky la 0.01s thi xac dinh duoc tai 1.7s
mic_stream[start_idx : end_idx] += np.sin(2 * np.pi * f_voice * n_total[start_idx : end_idx])

#========================= 2. QUA TRINH AUTO_CORRELATION -> CROSS CORRELATION ===========================#
#Ta cung se chuan bi lay mau chu BAT de dem di truot tren mic_stream
window_size = int(0.5 * fs)                     #Moi lan truot 50 mau
step_size = int(0.1 * fs)                          #Tang 10 mau moi lan truot xong

vad_flag = np.zeros(len(n_total))           #Cho tat ca cac gia tri trong bien co nay cua mic_stream la = 0 -> KHAI BAO AUTOCORRELATION
cross_score = np.zeros(len(n_total))      #Cho tat ca gia tri khi so sanh mau chu Bat va tin hieu giong noi trong mic stream la 0 -> KHAI BAO CROSS_CORRELATION

vad_threshold = 25.0                              #Nguong VAD -> NGHE DUOC CON NGUOI NOI
cross_threshold = 15.0                           #Nguon cross-correlation -> NGHE DUOC CHU "BAT"

print("HỆ THỐNG ĐANG LẮNG NGHE...")

for i in range(0, len(n_total) - len(template_BAT), step_size):
    #---BUOC 1: TU TUONG QUAN - AUTO-CORRELATION---#
    frame_vad = mic_stream[i : i + window_size]                     #Moi frame tuong ung voi moi lan quet
    r_xx = np.sum(frame_vad ** 2)                                          #Tinh toan nang luong tong cua frame theo cong thuc tong binh phuong cac gia tri moi lan truot

    if(r_xx > vad_threshold):
        vad_flag[i : i + window_size] = 1                                   #Cho cac gia tri trong khoang duoc xac dinh co GIONG NOI len 1

        #---BUOC 2: KHI PHAT HIEN GIONG NOI CON NGUOI, TA CROSS NO VOI template_BAT XEM CO GIONG NHAU KHONG---#
        frame_cross = mic_stream[i : i + len(template_BAT)]     #Ta cat 0.5s cua micstream tai vi tri ma no quet duoc 50 mau co giong noi thi no lay 50 mau do di so sanh

        #Ham correlate va mode='valid' de chap 2 doan frame_cross -> giong noi ben ngoai, con template_BAT -> giong noi chuan bi san
        r_xy = np.correlate(frame_cross, template_BAT, mode='valid')

        score = np.max(r_xy)                            #Ghi nhan gia tri dinh sau khi tuong quan
        cross_score[i] = score                          #Ta luu gia tri dinh tai vi tri i

        # --- BƯỚC 3: RA QUYẾT ĐỊNH ---#
        if score > cross_threshold:
            print(f"[!] Kích hoạt lúc {i/fs:.2f}s: Đã nghe chữ BẬT! (Điểm: {score: .1f})")
            break # Thoát vòng lặp, đi bật đèn thôi!

# ================= 3. TRỰC QUAN HÓA =================
plt.figure(figsize=(12, 10))

# Đồ thị 1: Micro
plt.subplot(3, 1, 1)
plt.plot(n_total, mic_stream, color='gray')
plt.title('1. Tín hiệu thu từ Micro liên tục')
plt.ylabel('Biên độ')
plt.grid(True, linestyle='--', alpha=0.6)

# Đồ thị 2: VAD
plt.subplot(3, 1, 2)
plt.plot(n_total, vad_flag, color='C1', linewidth=2)
plt.fill_between(n_total, 0, vad_flag, color='C1', alpha=0.3)
plt.title('2. VAD (Tự tương quan) - Chỉ thức dậy khi r_xx(0) vượt ngưỡng')
plt.ylabel('Trạng thái')
plt.ylim(-0.2, 1.2)
plt.grid(True, linestyle='--', alpha=0.6)

# Đồ thị 3: Cross-correlation
plt.subplot(3, 1, 3)
plt.plot(n_total, cross_score, color='C2')
plt.axhline(cross_threshold, color='r', linestyle='--', label='Ngưỡng chốt lệnh')
plt.title('3. Điểm số Tương quan chéo r_xy - Nằm im, chỉ nhảy vọt khi VAD bật')
plt.xlabel('Thời gian t (s)')
plt.ylabel('Điểm khớp lệnh')
plt.legend(loc='upper right')
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()
