\# 🎙️ Hệ thống Nhận diện Giọng nói Bật/Tắt Đèn



\## 📖 Giới thiệu

Đồ án này ứng dụng các kỹ thuật cốt lõi của Xử lý tín hiệu số (DSP) để xây dựng hệ thống nhận diện khẩu lệnh đơn giản. Hệ thống sẽ lắng nghe âm thanh từ Micro và tự động bật/tắt thiết bị điện (Relay) khi nghe đúng từ khóa.



\## 🎯 Mục tiêu dự án

\- \[x] Phân tích lý thuyết toán học (Autocorrelation \& Cross-correlation).

\- \[ ] Viết code mô phỏng thuật toán trên Python.

\- \[ ] Thu âm file mẫu (Templates) cho lệnh "Bật đèn" và "Tắt đèn".

\- \[ ] Triển khai code C/C++ xuống vi điều khiển.

\- \[ ] Lắp ráp phần cứng điều khiển bóng đèn 220V.



\## ⚙️ Nguyên lý hoạt động (Ý tưởng)

1\. \*\*Phát hiện giọng nói (VAD):\*\* Sử dụng \*\*Tự tương quan (Autocorrelation)\*\* để phân biệt tiếng ồn môi trường và giọng nói con người, giúp vi điều khiển tiết kiệm năng lượng tính toán.

2\. \*\*Nhận diện lệnh (Template Matching):\*\* Sử dụng \*\*Tương quan chéo (Cross-correlation)\*\* để quét và so sánh tín hiệu âm thanh thu được với các file âm thanh mẫu. Nếu hệ số tương quan vượt ngưỡng (Threshold), hệ thống ra quyết định đóng/ngắt Relay.



\## 💻 Hướng dẫn sử dụng

\*(Phần này sẽ được cập nhật sau khi hoàn thành code)\*

