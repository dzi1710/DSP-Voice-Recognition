\# 🎙️ Hệ thống Nhận diện Giọng nói Bật/Tắt Đèn



\## 📖 Giới thiệu

Đồ án này ứng dụng các kỹ thuật cốt lõi của Xử lý tín hiệu số (DSP) để xây dựng hệ thống nhận diện khẩu lệnh đơn giản. Hệ thống sẽ lắng nghe âm thanh từ Micro và tự động bật/tắt thiết bị điện (Relay) khi nghe đúng từ khóa.



\## 🎯 Mục tiêu dự án

1. Phân tích lý thuyết toán học (Autocorrelation \& Cross-correlation).
2. Viết code mô phỏng thuật toán trên Python.
3. Thu âm file mẫu (Templates) cho lệnh "Bật đèn" và "Tắt đèn".
4. Triển khai code C/C++ xuống vi điều khiển.
5. Lắp ráp phần cứng điều khiển bóng đèn 220V.



\## ⚙️ Nguyên lý hoạt động (Ý tưởng)

1\. \*\*Phát hiện giọng nói (VAD):\*\* Sử dụng \*\*Tự tương quan (Autocorrelation)\*\* để phân biệt tiếng ồn môi trường và giọng nói con người, giúp vi điều khiển tiết kiệm năng lượng tính toán.

2\. \*\*Nhận diện lệnh (Template Matching):\*\* Sử dụng \*\*Tương quan chéo (Cross-correlation)\*\* để quét và so sánh tín hiệu âm thanh thu được với các file âm thanh mẫu. Nếu hệ số tương quan vượt ngưỡng (Threshold), hệ thống ra quyết định đóng/ngắt Relay.



## 1\.Phân tích Lý thuyết Toán học

***a. Tự tương quan (Autocorrelation) - Ứng dụng làm VAD***

* Mục đích: Phát hiện xem có người đang nói hay không (Voice Activity Detection - VAD) để đánh thức hệ thống, loại bỏ tiếng ồn môi trường.
* Công thức toán học: Hàm tự tương quan của một tín hiệu rời rạc $x(n)$ tại độ trễ $l$ ($l = 0, \\pm1, \\pm2, \\dots$) được định nghĩa là:

&#x20; $$r\_{xx}(l) = \\sum\_{n=-\\infty}^{\\infty} x(n)x(n-l)$$



\-Ví dụ \& Ý nghĩa vật lý:Phép toán này lấy tín hiệu $x(n)$ trượt và nhân với chính nó. Tại độ trễ $l=0$, tín hiệu khớp hoàn toàn với chính nó, tạo ra đỉnh cực đại.Trong thực tế, giọng nói con người phát ra từ thanh quản có tính tuần hoàn, do đó $r\_{xx}(l)$ sẽ tạo ra các đỉnh lặp đi lặp lại. 

\-Ngược lại, tiếng ồn ngẫu nhiên (tiếng quạt, gió) không có tính tuần hoàn nên $r\_{xx}(l)$ sẽ suy giảm rất nhanh về $0$. Hệ thống dựa vào điểm này để nhận diện khi nào bạn bắt đầu cất tiếng.



***b. Tương quan chéo (Cross-correlation) - Ứng dụng Nhận diện từ khóa***

* Mục đích: Tìm kiếm sự xuất hiện của các từ khóa mẫu ("Bật", "Tắt") bên trong đoạn âm thanh mà Micro vừa thu được.
* Công thức toán học:Tương quan chéo của hai tín hiệu $x(n)$ và $y(n)$ là một chuỗi $r\_{xy}(l)$ với $l = 0, \\pm1, \\pm2, \\dots$, được tính bằng:

&#x20; $$r\_{xy}(l) = \\sum\_{n=-\\infty}^{\\infty} x(n)y(n-l)$$



Ví dụ minh họa:

Giả sử tín hiệu thu được là $x(n) = \\{0, 1, 3, 1, 0\\}$ và tín hiệu mẫu lệnh "Bật" là $y(n) = \\{0, 1, 3, 1, 0\\}$. Khi thực hiện trượt tương quan chéo, tại thời điểm độ trễ $l = -2$, ta đạt được giá trị lớn nhất $\\max(r\_{xy}(l)) = r\_{xy}(-2) = 11$. 

Tại điểm này, tín hiệu $y(n)$ giống với tín hiệu $x(n)$ nhất. Áp dụng vào thực tế nhận diện:

Trong môi trường thực, tín hiệu Micro thu được thường có dạng $y(n) = \\alpha x(n-D) + w(n)$, trong đó $\\alpha$ là hệ số suy hao (bạn nói to hay nhỏ), $D$ là độ trễ (thời điểm bạn ra lệnh), và $w(n)$ là nhiễu môi trường.  Để giải quyết vấn đề âm lượng nói to/nhỏ khác nhau làm sai lệch kết quả, hệ thống sẽ sử dụng Chuỗi tương quan chéo chuẩn hóa (Normalized crosscorrelation sequence):

&#x20; $$\\rho\_{xy}(l) = \\frac{r\_{xy}(l)}{\\sqrt{r\_{xx}(0)r\_{yy}(0)}}$$



Nhờ công thức này, giá trị luôn được giới hạn trong khoảng $|\\rho\_{xy}(l)| \[cite\_start]\\le 1$. Nếu $\\rho\_{xy}(l)$ vượt qua một ngưỡng (Threshold) định sẵn (ví dụ 0.8), hệ thống sẽ kết luận đã nhận diện thành công lệnh và xuất tín hiệu kích hoạt Relay.

