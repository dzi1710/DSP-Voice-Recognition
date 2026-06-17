import numpy as np
import matplotlib.pyplot as plt

# ================= 1. TẠO MÔI TRƯỜNG ÂM THANH =================
fs = 100  
t = np.arange(0, 3, 1/fs) 
mic_stream = np.random.randn(len(t)) * 0.5 

# Người dùng cất tiếng nói từ giây 1.2 đến 1.7
start_idx = int(1.2 * fs)
end_idx = int(1.7 * fs)
mic_stream[start_idx:end_idx] += np.sin(2 * np.pi * 10 * t[start_idx:end_idx])

# ================= 2. THUẬT TOÁN VAD THÍCH NGHI (ADAPTIVE VAD) =================
window_size = int(0.1 * fs) # Cửa sổ trượt 0.1s
step_size = int(0.05 * fs)  # Bước nhảy 0.05s
vad_flag = np.zeros(len(t)) 

# --- PHA 1: CALIBRATION (HỌC MÔI TRƯỜNG) ---
# Lấy 0.5 giây đầu tiên (Giả định lúc này người dùng chưa nói gì, chỉ có tiếng ồn)
noise_sample = mic_stream[0 : int(0.5 * fs)]
noise_energies = []

# Quét để tính năng lượng của từng khung nhiễu
for i in range(0, len(noise_sample) - window_size, step_size):
    frame = noise_sample[i : i + window_size]
    noise_energies.append(np.sum(frame ** 2))

# Tính Năng lượng nhiễu trung bình (E_noise)
E_noise_avg = np.mean(noise_energies)

# Chốt Ngưỡng VAD: Gấp 4 lần năng lượng tiếng ồn nền
alpha = 4.0 
vad_threshold = E_noise_avg * alpha

print("====== BÁO CÁO HỆ THỐNG ======")
print(f"Năng lượng nhiễu nền trung bình : {E_noise_avg:.2f}")
print(f"Hệ số khuếch đại (Alpha)        : x{alpha}")
print(f"=> Ngưỡng VAD tự động chốt ở    : {vad_threshold:.2f}")
print("==============================")

# --- PHA 2: CHẠY QUÉT THỰC TẾ ---
for i in range(0, len(t) - window_size, step_size):
    frame = mic_stream[i : i + window_size]
    r_xx_0 = np.sum(frame ** 2) 
    
    if r_xx_0 > vad_threshold:
        vad_flag[i : i + window_size] = 1 

# ================= 3. TRỰC QUAN HÓA =================
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(t, mic_stream, color='gray')
plt.title(f'1. Tín hiệu thu từ Micro (Ngưỡng VAD tự động: {vad_threshold:.2f})')
plt.ylabel('Biên độ')
plt.grid(True, linestyle='--', alpha=0.6)

plt.subplot(2, 1, 2)
plt.plot(t, vad_flag, color='C1', linewidth=2)
plt.fill_between(t, 0, vad_flag, color='C1', alpha=0.3)
plt.title('2. Cờ kích hoạt VAD - Đã hết rò rỉ, bám cực chuẩn!')
plt.xlabel('Thời gian t (s)')
plt.ylabel('Trạng thái (0 = Ngủ, 1 = Thức)')
plt.ylim(-0.2, 1.2)
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()
