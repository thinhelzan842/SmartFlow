# 🎯 HƯỚNG DẪN DEMO NHANH

## ⚡ START NGAY

### 1. Mở Terminal
```powershell
cd d:\tdtt\SmartFlow
python app.py
```

### 2. Mở Browser
```
http://localhost:5000
```

### 3. Bắt đầu demo!

---

## 📍 DEMO SCENARIO 1: TÌM ĐƯỜNG CƠ BẢN

### Bước 1: Chọn điểm A (xuất phát)
- Click nút **"Tìm đường"** (xanh lá)
- Click vào bản đồ → marker xanh xuất hiện

### Bước 2: Chọn điểm B (đích đến)
- Click lần 2 vào bản đồ → marker đỏ xuất hiện
- Tuyến đường màu xanh dương tự động hiển thị

### Bước 3: Xem thông tin
- **Khoảng cách**: XXX m
- **Thời gian**: XX.X phút
- **Số đoạn**: XX

### Bước 4: Thử lại
- Click **"Xóa tuyến đường"**
- Chọn 2 điểm khác

---

## 🚦 DEMO SCENARIO 2: MÔ PHỎNG TẮC ĐƯỜNG

### Bước 1: Tìm đường trước
- Tìm đường như scenario 1
- Ghi nhớ thời gian (ví dụ: 5.3 phút)

### Bước 2: Thêm tắc đường
- Click nút **"Thêm tắc đường"** (xám)
- Click vào đoạn đường trên tuyến xanh
- Nhập: **50** xe
- Click **"Xác nhận"**
- Đoạn đường chuyển màu đỏ

### Bước 3: Tìm lại đường
- Click **"Xóa tuyến đường"**
- Chọn lại 2 điểm A và B như cũ
- Quan sát: Tuyến đường mới **TRÁNH** đoạn đỏ!
- Thời gian có thể khác (ví dụ: 6.1 phút)

### Highlight:
> "Hệ thống tự động tránh đường tắc và chọn tuyến tối ưu khác!"

---

## ⚙️ DEMO SCENARIO 3: ĐIỀU CHỈNH THAM SỐ

### Test 1: Giờ thấp điểm (ít tắc)
- Alpha: **0.15**
- Beta: **4**
- Capacity: **0.7**
- Click **"Cập nhật tham số"**
- Tìm đường → thời gian ngắn hơn

### Test 2: Giờ cao điểm (tắc nghẽn)
- Alpha: **1.5**
- Beta: **8**
- Capacity: **0.4**
- Click **"Cập nhật tham số"**
- Tìm đường → thời gian dài hơn

### Highlight:
> "Tham số BPR cho phép mô phỏng các điều kiện giao thông khác nhau!"

---

## 💡 ĐIỂM NÊU BẬT KHI DEMO

### 1. So sánh Google Maps
> "Google Maps KHÔNG đi vào hẻm vì chính sách an toàn. Nhưng tại TP.HCM, nhiều hẻm rộng rãi phù hợp xe máy. SmartFlow tận dụng điều này để tối ưu!"

### 2. Mô phỏng thực tế
> "Khi đường chính tắc, SmartFlow tự động tìm đường khác, kể cả qua hẻm - giống như tài xế taxi địa phương!"

### 3. Linh hoạt
> "Có thể điều chỉnh tham số cho từng khu vực, từng giờ - Quận 1 khác Tân Bình, giờ cao điểm khác giờ thấp điểm."

### 4. Công nghệ
> "Sử dụng thuật toán Dijkstra kết hợp mô hình BPR - tiêu chuẩn công nghiệp trong quy hoạch giao thông!"

---

## 🎬 KỊCh BẢN DEMO 5 PHÚT

### Phút 1: Giới thiệu
- Vấn đề: Google Maps không dùng hẻm
- Giải pháp: SmartFlow tận dụng hẻm

### Phút 2: Demo tìm đường cơ bản
- Click 2 điểm
- Hiển thị kết quả
- Giải thích tuyến đường

### Phút 3: Demo tắc đường
- Thêm tắc nghẽn
- Tìm lại đường
- So sánh trước/sau

### Phút 4: Demo tham số
- Điều chỉnh α, β
- Thấy sự khác biệt
- Giải thích ứng dụng

### Phút 5: Kết luận
- Tóm tắt ưu điểm
- Ứng dụng thực tế
- Q&A

---

## 🎯 TỌA ĐỘ DEMO GỢI Ý (Quận Tân Bình)

### Route 1: Ngắn (~2km)
- **A**: Click gần Cộng Hòa (10.8006, 106.6503)
- **B**: Click gần Trường Sơn (10.8050, 106.6550)

### Route 2: Trung bình (~3km)
- **A**: Click gần Tân Sơn Nhất (10.8080, 106.6600)
- **B**: Click gần Lũy Bán Bích (10.7950, 106.6450)

### Route 3: Dài (~4km)
- **A**: Phía Bắc Tân Bình (10.8150, 106.6550)
- **B**: Phía Nam Tân Bình (10.7850, 106.6400)

---

## 🔥 MẸO DEMO

### ✅ NÊN:
- Test trước khi demo thật
- Chuẩn bị 2-3 tuyến đường mẫu
- Giải thích từng bước rõ ràng
- Zoom bản đồ phù hợp (level 14-16)
- Có video backup nếu mạng lỗi

### ❌ TRÁNH:
- Chọn 2 điểm quá xa (không tìm được đường)
- Chọn 2 điểm quá gần (không thấy sự khác biệt)
- Demo khi chưa test
- Quên reset congestion giữa các demo
- Nói quá nhanh

---

## 📸 SCREENSHOTS CẦN CHỤP

1. ✅ Màn hình chính với bản đồ
2. ✅ Tuyến đường màu xanh với 2 markers
3. ✅ Thông tin route (khoảng cách, thời gian)
4. ✅ Đoạn đường tắc nghẽn màu đỏ
5. ✅ Panel tham số BPR
6. ✅ Tuyến đường trước/sau khi thêm tắc nghẽn

---

## 🆘 XỬ LÝ SỰ CỐ

### Lỗi: Không tìm được đường
➡️ **Giải pháp**: Chọn 2 điểm gần hơn trong Quận Tân Bình

### Lỗi: Bản đồ không load
➡️ **Giải pháp**: Reload trang (F5), kiểm tra internet

### Lỗi: Server không chạy
➡️ **Giải pháp**: 
```powershell
cd d:\tdtt\SmartFlow
python app.py
```

### Lỗi: API trả về lỗi
➡️ **Giải pháp**: Kiểm tra console (F12), reset congestion

---

## ✨ CLOSING STATEMENT

> "SmartFlow không chỉ là công cụ tìm đường, mà là giải pháp tận dụng tối đa cơ sở hạ tầng hiện có - đặc biệt là các con hẻm ở TP.HCM. Điều mà các ứng dụng lớn như Google Maps chưa làm được vì chính sách an toàn toàn cầu của họ. SmartFlow được thiết kế riêng cho bối cảnh giao thông Việt Nam!"

---

## 🎉 CHÚC DEMO THÀNH CÔNG!

**Tip cuối:** Tự tin, nói rõ ràng, và đừng sợ lỗi - có thể biến lỗi thành cơ hội giải thích thêm về hệ thống! 💪
