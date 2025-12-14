# SmartFlow Web Application

Hệ thống định tuyến giao thông thông minh với mô phỏng tắc nghẽn sử dụng mô hình BPR (Bureau of Public Roads).

## 🚀 Cài đặt

### 1. Cài đặt các thư viện cần thiết:

```powershell
pip install -r requirements.txt
```

### 2. Kiểm tra file dữ liệu:

Đảm bảo file `graph_with_congestion.gpickle` tồn tại trong thư mục `SmartFlow/`.

Nếu không có, ứng dụng sẽ tự động tải dữ liệu từ OpenStreetMap (Quận Tân Bình, TP.HCM) khi khởi động lần đầu.

## ▶️ Chạy ứng dụng

```powershell
python app.py
```

Ứng dụng sẽ khởi động tại: **http://localhost:5000**

## 📖 Hướng dẫn sử dụng

### 🔹 Chế độ "Tìm đường"

1. Click nút **"Tìm đường"** (màu xanh lá)
2. Click vào bản đồ để chọn **điểm A** (xuất phát) - đánh dấu xanh lá
3. Click vào bản đồ để chọn **điểm B** (đích đến) - đánh dấu đỏ
4. Hệ thống tự động tìm đường tối ưu và hiển thị:
   - Tuyến đường màu xanh dương
   - Khoảng cách (mét)
   - Thời gian di chuyển (phút)
   - Số đoạn đường

### 🔹 Chế độ "Thêm tắc đường"

1. Click nút **"Thêm tắc đường"** (màu xám)
2. Click vào bất kỳ đoạn đường nào trên bản đồ
3. Nhập số lượng xe (1-1000) để mô phỏng tắc nghẽn
4. Click **"Xác nhận"**
5. Đoạn đường tắc nghẽn sẽ được tô màu đỏ
6. Thử tìm đường lại - hệ thống sẽ tránh đoạn đường tắc nghẽn

### ⚙️ Tham số BPR

**Công thức BPR:** `We = We_base × [1 + α × (fe/Ce)^β]`

- **Alpha (α)**: Hệ số tắc nghẽn (0.1 - 5.0)
  - Giá trị nhỏ: ít bị tắc nghẽn
  - Giá trị lớn: tắc nghẽn nhiều hơn
  - **Mặc định: 1.5** (Strong BPR)

- **Beta (β)**: Độ phi tuyến (1 - 15)
  - Giá trị nhỏ: tăng dần
  - Giá trị lớn: tăng đột ngột khi quá tải
  - **Mặc định: 8** (Strong BPR)

- **Dung lượng**: Hệ số dung lượng (0.1 - 1.0)
  - 1.0 = 100% dung lượng
  - 0.4 = 40% dung lượng (giờ cao điểm)
  - **Mặc định: 0.4** (Strong BPR)

**Cách điều chỉnh:**
1. Nhập giá trị mới vào các ô
2. Click **"Cập nhật tham số"**
3. Hệ thống sẽ áp dụng tham số mới cho các tuyến đường tiếp theo

### 🔄 Các thao tác khác

- **Xóa tuyến đường**: Xóa các điểm A, B và tuyến đường hiện tại
- **Reset tắc đường**: Xóa tất cả các đoạn đường tắc nghẽn đã thêm

## 🎯 Tính năng chính

✅ **Tìm đường tối ưu** với thuật toán Dijkstra
✅ **Mô phỏng tắc nghẽn** theo công thức BPR
✅ **Điều chỉnh tham số** theo thời gian thực
✅ **Giao diện trực quan** với Leaflet.js
✅ **Dữ liệu thực tế** từ OpenStreetMap
✅ **Hỗ trợ hẻm nhỏ** - khác với Google Maps

## 📊 So sánh với Google Maps

| Tính năng | SmartFlow | Google Maps |
|-----------|-----------|-------------|
| Tìm đường hẻm | ✅ Có | ❌ Không |
| Mô phỏng tắc nghẽn | ✅ Có (BPR) | ⚠️ Chỉ hiển thị |
| Điều chỉnh tham số | ✅ Có | ❌ Không |
| Dữ liệu địa phương | ✅ OSM | ✅ Google |

## 🛠️ Cấu trúc project

```
SmartFlow/
├── app.py                          # Flask backend
├── routing_logic.py                # Logic tìm đường (BPR + Dijkstra)
├── requirements.txt                # Dependencies
├── graph_with_congestion.gpickle   # Dữ liệu bản đồ (cache)
├── templates/
│   └── index.html                  # Giao diện web
└── static/
    ├── style.css                   # CSS
    └── app.js                      # JavaScript frontend
```

## 🔧 API Endpoints

### POST /api/find_route
Tìm đường giữa 2 điểm

**Request:**
```json
{
    "start_lat": 10.8006,
    "start_lon": 106.6503,
    "end_lat": 10.8050,
    "end_lon": 106.6550
}
```

**Response:**
```json
{
    "success": true,
    "path": [123, 456, 789, ...],
    "geometries": [[[10.8006, 106.6503], ...]],
    "distance": 1500.0,
    "time": 180.5,
    "segments": 25
}
```

### POST /api/add_congestion
Thêm tắc đường vào một cạnh

**Request:**
```json
{
    "lat": 10.8006,
    "lon": 106.6503,
    "vehicle_count": 10
}
```

### POST /api/update_parameters
Cập nhật tham số BPR

**Request:**
```json
{
    "alpha": 1.5,
    "beta": 8,
    "capacity_factor": 0.4
}
```

### POST /api/reset_congestion
Reset tất cả tắc đường

### GET /api/status
Kiểm tra trạng thái hệ thống

## 📝 Lưu ý

1. **Lần chạy đầu tiên** sẽ mất 2-3 phút để tải dữ liệu từ OpenStreetMap
2. **Dữ liệu được cache** trong file `graph_with_congestion.gpickle`
3. **Xóa file cache** nếu muốn tải lại dữ liệu mới
4. **Tham số Strong BPR** (α=1.5, β=8, capacity=0.4) phù hợp cho giờ cao điểm tại TP.HCM

## 🎓 Ứng dụng cho bài thuyết trình

### Kịch bản Demo:

1. **Giới thiệu vấn đề:**
   - Google Maps không chỉ đường hẻm
   - TP.HCM có nhiều hẻm rộng phù hợp xe máy
   - Giờ cao điểm: đường lớn tắc, hẻm thông thoáng

2. **Demo SmartFlow:**
   - Chọn 2 điểm: từ đường lớn này sang đường lớn kia
   - SmartFlow tìm đường qua hẻm → nhanh hơn
   - Thêm tắc nghẽn vào đường chính
   - Tìm lại → SmartFlow chọn hẻm khác

3. **So sánh kết quả:**
   - Google Maps: chỉ đường lớn (bị tắc)
   - SmartFlow: kết hợp hẻm (tối ưu hơn)

4. **Điều chỉnh tham số:**
   - α, β nhỏ → ít tắc nghẽn (giờ thấp điểm)
   - α, β lớn → nhiều tắc nghẽn (giờ cao điểm)
   - Capacity thấp → mô phỏng đường hẹp

## 🐛 Troubleshooting

**Lỗi: "Module not found"**
```powershell
pip install -r requirements.txt
```

**Lỗi: "Cannot connect to server"**
- Kiểm tra xem port 5000 có bị chiếm không
- Thử đổi port trong `app.py`: `app.run(port=5001)`

**Bản đồ không load:**
- Kiểm tra kết nối internet
- Xóa cache trình duyệt
- Thử trình duyệt khác

**Không tìm được đường:**
- 2 điểm quá xa nhau hoặc không kết nối
- Thử chọn 2 điểm gần hơn trong khu vực Quận Tân Bình

## 📧 Liên hệ

Nếu gặp vấn đề, hãy kiểm tra console log trong trình duyệt (F12) và terminal.

---

**Chúc bạn demo thành công! 🎉**
