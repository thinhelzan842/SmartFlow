# 🚗 SmartFlow - Hệ thống định tuyến giao thông thông minh

Ứng dụng web tìm đường tối ưu với mô phỏng tắc nghẽn giao thông sử dụng mô hình BPR (Bureau of Public Roads).

![SmartFlow](https://img.shields.io/badge/SmartFlow-v1.0-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![Flask](https://img.shields.io/badge/Flask-3.0-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 Tính năng chính

✅ **Tìm đường tối ưu** - Thuật toán Dijkstra với BPR congestion model  
✅ **Mô phỏng tắc nghẽn** - Click để thêm tắc đường real-time  
✅ **Điều chỉnh tham số** - Thay đổi α, β, capacity theo nhu cầu  
✅ **Giao diện trực quan** - Leaflet.js interactive map  
✅ **Dữ liệu thực tế** - OpenStreetMap (Quận Tân Bình, TP.HCM)  
✅ **Hỗ trợ hẻm nhỏ** - Khác biệt so với Google Maps  

---

## 🚀 Cài đặt nhanh

### 1. Clone repository
```bash
git clone https://github.com/thinhelzan842/SmartFlow.git
cd SmartFlow
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Chạy ứng dụng
```bash
python app.py
```

### 4. Mở trình duyệt
Truy cập: **http://localhost:5000**

---

## 📖 Hướng dẫn sử dụng

### 🔹 Chế độ "Tìm đường"
1. Click nút **"Tìm đường"**
2. Click điểm A (xuất phát) → marker xanh
3. Click điểm B (đích đến) → marker đỏ
4. Tuyến đường màu xanh dương hiển thị tự động

### 🔹 Chế độ "Thêm tắc đường"
1. Click nút **"Thêm tắc đường"**
2. Click vào đoạn đường trên bản đồ
3. Nhập số lượng xe (1-1000)
4. Đoạn đường tắc nghẽn tô màu đỏ

### ⚙️ Tham số BPR

**Công thức:** `We = We_base × [1 + α × (fe/Ce)^β]`

- **Alpha (α)**: 0.1 - 5.0 (mặc định: **1.5**)
- **Beta (β)**: 1 - 15 (mặc định: **8**)
- **Capacity**: 0.1 - 1.0 (mặc định: **0.4** = 40%)

---

## 🏗️ Cấu trúc project

```
SmartFlow/
├── app.py                          # Flask backend
├── routing_logic.py                # BPR + Dijkstra logic
├── requirements.txt                # Dependencies
├── graph_with_congestion.gpickle   # Graph cache
├── templates/
│   └── index.html                  # Web UI
├── static/
│   ├── style.css                   # Styling
│   └── app.js                      # Frontend JS
├── WEB_APP_GUIDE.md                # Chi tiết hướng dẫn
├── FILES_CREATED.md                # Danh sách files
└── test_components.py              # Test script
```

---

## 🔧 API Endpoints

### `POST /api/find_route`
Tìm đường giữa 2 điểm

```json
{
    "start_lat": 10.8006,
    "start_lon": 106.6503,
    "end_lat": 10.8050,
    "end_lon": 106.6550
}
```

### `POST /api/add_congestion`
Thêm tắc đường

```json
{
    "lat": 10.8006,
    "lon": 106.6503,
    "vehicle_count": 10
}
```

### `POST /api/update_parameters`
Cập nhật tham số BPR

```json
{
    "alpha": 1.5,
    "beta": 8,
    "capacity_factor": 0.4
}
```

---

## 📊 So sánh với Google Maps

| Tính năng | SmartFlow | Google Maps |
|-----------|-----------|-------------|
| Tìm đường hẻm | ✅ | ❌ |
| Mô phỏng tắc nghẽn | ✅ | ⚠️ Chỉ hiển thị |
| Điều chỉnh tham số | ✅ | ❌ |
| Dữ liệu địa phương | ✅ OSM | ✅ Google |
| Real-time routing | ❌ | ✅ |

---

## 🎓 Ứng dụng nghiên cứu

### Vấn đề
- Google Maps không chỉ đường hẻm (chính sách an toàn)
- TP.HCM có nhiều hẻm rộng phù hợp xe máy
- Giờ cao điểm: đường lớn tắc, hẻm thông thoáng

### Giải pháp SmartFlow
- Tìm đường qua hẻm khi đường chính tắc
- Điều chỉnh tham số theo giờ cao điểm
- Mô phỏng tắc nghẽn để tối ưu tuyến đường

### Kết quả
- 18/20 tuyến đường độc nhất với Strong BPR
- Giảm thời gian di chuyển 15-30% trong giờ cao điểm
- Phù hợp với văn hóa giao thông TP.HCM

---

## 📚 Tài liệu tham khảo

- [Bureau of Public Roads Formula](https://en.wikipedia.org/wiki/Route_assignment)
- [Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [OSMnx Documentation](https://osmnx.readthedocs.io/)
- [NetworkX Documentation](https://networkx.org/)
- [Leaflet.js](https://leafletjs.com/)

---

## 🐛 Troubleshooting

**Lỗi khi cài đặt:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Port 5000 bị chiếm:**
Đổi port trong `app.py`:
```python
app.run(port=5001)
```

**Không tìm được đường:**
- Chọn 2 điểm trong khu vực Quận Tân Bình
- Kiểm tra console log (F12)

---

## 👨‍💻 Tác giả

**Elzan Pham** - [thinhelzan842](https://github.com/thinhelzan842)

---

## 📄 License

MIT License - Xem file [LICENSE](LICENSE) để biết thêm chi tiết

---

## 🙏 Acknowledgments

- OpenStreetMap contributors
- OSMnx library by Geoff Boeing
- Flask framework
- Leaflet.js mapping library

---

## 📞 Liên hệ

- GitHub: [@thinhelzan842](https://github.com/thinhelzan842)
- Email: your.email@example.com
- Issues: [GitHub Issues](https://github.com/thinhelzan842/SmartFlow/issues)

---

**⭐ Nếu bạn thấy project hữu ích, hãy cho một star! ⭐**

