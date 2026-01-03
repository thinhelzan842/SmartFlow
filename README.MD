# 🚗 SmartFlow - Hệ thống định tuyến giao thông thông minh

> **Đồ án môn Tư duy tính toán - HCMUS 2025**  
> Hệ thống tìm đường tối ưu với mô phỏng tắc nghẽn giao thông  sử dụng thuật toán Dijkstra và mô hình BPR (Bureau of Public Roads).



---

## 📋 Mục lục
- [Giới thiệu](#-giới-thiệu)
- [Tính năng](#-tính-năng-chính)
- [Cài đặt](#-cài-đặt)
- [Sử dụng](#-hướng-dẫn-sử-dụng)
- [Đánh giá](#-evaluation)
- [Cấu trúc project](#-cấu-trúc-project)
- [API](#-api-endpoints)

---

## 🎓 Giới thiệu

**SmartFlow** là hệ thống định tuyến giao thông thông minh được phát triển như đồ án môn **Tư duy tính toán** tại Trường Đại học Khoa học Tự nhiên (HCMUS), năm học 2025-2026.

### 🎯 Mục tiêu
- Tìm đường tối ưu giữa 2 điểm trên bản đồ TP.HCM (Quận Tân Bình)
- Mô phỏng tác động của tắc nghẽn giao thông đến thời gian di chuyển
- Áp dụng mô hình BPR (Bureau of Public Roads, 1964) để tính toán độ trễ do congestion
- Cung cấp nhiều tuyến đường thay thế với độ đa dạng cao

### 🔬 Cơ sở khoa học
- **Thuật toán:** Dijkstra's Shortest Path (1959)
- **Mô hình congestion:** BPR Function - `t = t₀[1 + α(v/c)^β]`
- **Nguồn dữ liệu:** OpenStreetMap (OSM) - chuẩn quốc tế
- **Thư viện:** NetworkX, OSMnx, Flask, Leaflet.js

### 📊 Đánh giá hệ thống
- **30 test cases** với statistical validity (n=30, 95% CI, ±18% error)
- **Overall Score:** 85/100 (Grade A)
- **Route Diversity:** 0.416 (target >0.3) ✅
- **Response Time:** <1s average (Nielsen's excellent threshold) ✅
- **Comprehensive evaluation** với 11+ scientific references

---

## ✨ Tính năng chính

### 🔹 Core Features
✅ **Tìm đường thông minh** - Dijkstra + BPR model với 3 routes thay thế  
✅ **Mô phỏng tắc nghẽn** - Thêm congestion zones bằng click/path drawing  
✅ **Baseline comparison** - So sánh route hiện tại vs. shortest path không tắc  
✅ **Route diversity** - 1-2 tuyến đường khác biệt (Jaccard Distance >0.3)  
  

### 🔹 Technical Features
✅ **Dữ liệu thực tế** - OSM graph: 1,487 nodes, 3,420 edges (Tân Bình District)  
✅ **Hỗ trợ hẻm nhỏ** - Bao gồm residential roads (khác biệt với Google Maps)  
✅ **Adjustable parameters** - Thay đổi α, β, capacity real-time  
✅ **Graph caching** - Load nhanh với pickle serialization  
✅ **Responsive UI** - Leaflet.js interactive map  

---

## 🚀 Cài đặt

### 📦 Yêu cầu hệ thống
- **Python:** 3.11 hoặc cao hơn
- **Storage:** ~200MB cho dependencies + graph cache
- **OS:** Windows/Linux/macOS

### 1️⃣ Clone repository
```bash
git clone https://github.com/thinhelzan842/SmartFlow.git
cd SmartFlow
```

### 2️⃣ Tạo virtual environment (optional)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Cài đặt dependencies
```bash
pip install -r requirements.txt
```

**Dependencies chính:**
- `flask==3.0.0` - Web framework
- `networkx==3.4.2` - Graph algorithms
- `osmnx==2.0.0` - OpenStreetMap data
- `numpy`, `pandas` - Data processing

### 4️⃣ Chạy ứng dụng
```bash
python app.py
```

**Output mong đợi:**
```
============================================================
SmartFlow Traffic Routing System
============================================================

Initializing...
Loading graph from cache: graph_with_congestion.gpickle
Graph is not strongly connected, extracting largest component...
Using largest component: 1487 nodes, 3420 edges
Routing system initialized with α=1.5, β=8, capacity=0.4

✓ System ready!
============================================================

Starting web server...
Running in production mode on port 5000
 * Running on http://127.0.0.1:5000
```

### 5️⃣ Mở trình duyệt
Truy cập: **http://localhost:5000**

---

## 📖 Hướng dẫn sử dụng

### 🗺️ Chế độ "Tìm đường"
1. Click nút **"Chế độ tìm đường"** (màu xanh)
2. Click **điểm A** trên bản đồ (xuất phát) → marker xanh lá xuất hiện
3. Click **điểm B** trên bản đồ (đích đến) → marker đỏ xuất hiện
4. Hệ thống tự động hiển thị:
   - **Route 1** (màu xanh dương đậm) - Tuyến tối ưu nhất
   - **Route 2** (màu xanh lá) - Tuyến thay thế 1

5. Click vào marker để xem thông tin chi tiết (khoảng cách, thời gian)

### 🚧 Chế độ "Thêm tắc đường"
1. Click nút **"Thêm tắc đường"** (màu đỏ)

2. **Vẽ path:**
   - Click nhiều điểm liên tiếp để vẽ path
   - Tất cả segments trên path được đánh dấu tắc

### 🔄 Chế độ "Xóa tắc đường"
1. Click nút **"Xóa tắc đường"** (màu xanh nhạt)
2. Click vào đoạn đường màu đỏ để xóa congestion
3. Màu đỏ biến mất, route tự động recalculate

### ⚙️ Điều chỉnh tham số BPR

**Công thức BPR:** `t = t₀ × [1 + α × (v/c)^β]`

- **Alpha (α)**: 0.1 - 5.0 (mặc định: **1.5**)
  - Hệ số ảnh hưởng tuyến tính của congestion
  - Càng cao → tắc nghẽn ảnh hưởng càng mạnh
  
- **Beta (β)**: 1 - 15 (mặc định: **8**)
  - Hệ số phi tuyến (độ cong đường cong)
  - Chuẩn BPR 1964: β=4, Project này: β=8 (nhạy hơn)
  
- **Capacity (c)**: 0.1 - 1.0 (mặc định: **0.4**)
  - 0.4 = 40% capacity (mỗi đoạn đường chứa ~40 xe)
  - Thấp hơn → dễ bị tắc

**Cách thay đổi:**
1. Mở sidebar bên phải
2. Kéo slider hoặc nhập giá trị
3. Click "Cập nhật" → BPR weights recalculate toàn bộ graph

---

## 📊 Evaluation

### 🎯 Comprehensive Test Suite
- **30 test cases** với statistical validity
- Coverage: 10 short/10 medium/10 long distance
- Congestion patterns: 80+ unique segments
- Geographic: 10 north-south/10 east-west/10 diagonal

### 📈 Evaluation Results
| Metric | Score | Target | Status |
|--------|-------|--------|--------|
| **Overall** | **85/100** | ≥70 | ✅ **Grade A** |
| Routing Quality | 94.8/100 | ≥80 | ✅ |
| Performance | 100/100 | ≥75 | ✅ |
| BPR Accuracy | 65.0/100 | ≥60 | ✅ |
| UX Score | 90.3/100 | ≥70 | ✅ |

**Chi tiết:**
- **Route Diversity:** 0.416 (target >0.3)
- **Route Quality:** 0.985 (target >0.95)
- **Congestion Avoidance:** 0.880 (target >0.85)
- **Avg Response Time:** 0.15s (target <5s)

### 📚 Scientific References
Evaluation dựa trên 11+ published papers và tiêu chuẩn quốc tế:
- Dijkstra (1959), Jaccard (1901), Wardrop (1952)
- Bureau of Public Roads (1964), Nielsen (1993)
- ISO 9241-11:2018, Li et al. (2011), Bader et al. (2011)

👉 **Chi tiết:** Xem `evaluation.ipynb` và `EVALUATION_REFERENCES.md`

---

## 🏗️ Cấu trúc project

```
SmartFlow/
├── 📄 app.py                            # Flask web server
├── 📄 routing_logic.py                  # Core routing logic (BPR + Dijkstra)
├── 📊 evaluation.ipynb                  # Comprehensive evaluation notebook
├── 📋 test_cases_comprehensive.json     # 30 test cases
├── 📄 evaluation_report.json            # Evaluation results
├── 🖼️ evaluation_results.png            # Visualization charts
│
├── 📦 graph_with_congestion.gpickle     # Cached OSM graph (1487 nodes, 3420 edges)
│
├── 📁 templates/
│   └── index.html                       # Web UI
├── 📁 static/
│   ├── style.css                        # Styling
│   └── app.js                           # Frontend logic (Leaflet.js)
│
├── 📄 requirements.txt                  # Python dependencies
├── 📄 .gitignore                        # Git ignore rules
├── 📄 Procfile                          # Heroku deployment
├── 📄 runtime.txt                       # Python version for deployment
│
├── 📚 README.MD                         # 👈 Bạn đang đọc file này
├── 📚 README_DEPLOY.md                  # Deployment guide
├── 📚 EVALUATION_REFERENCES.md          # Scientific references
└── 📚 CAU_TRA_LOI_DANH_GIA.md          # Q&A for evaluation
```

**Key files:**
- `routing_logic.py` - 28KB, chứa SmartRoutingSystem class
- `evaluation.ipynb` - 528KB, 16+ cells với comprehensive evaluation
- `graph_with_congestion.gpickle` - 1MB, OSM graph cache

---

## 🔧 API Endpoints

### `POST /api/find_route`
Tìm đường giữa 2 điểm

**Request:**
```json
{
    "start_lat": 10.8006,
    "start_lon": 106.6503,
    "end_lat": 10.8050,
    "end_lon": 106.6550,
    "num_search": 20,
    "num_display": 3
}
```

**Response:**
```json
{
    "success": true,
    "routes": [
        {
            "distance": 1250.5,
            "time": 180.2,
            "path": [...],
            "geometry": [[[lat, lon], ...]]
        }
    ],
    "baseline_distance": 1100.0,
    "baseline_geometry": [[lat, lon], ...]
}
```

### `POST /api/add_congestion_path`
Thêm tắc nghẽn theo path (nhiều điểm)

**Request:**
```json
{
    "points": [
        [10.8006, 106.6503],
        [10.8020, 106.6520],
        [10.8035, 106.6540]
    ],
    "vehicle_count": 100
}
```

### `POST /api/remove_congestion`
Xóa tắc nghẽn tại 1 điểm

**Request:**
```json
{
    "lat": 10.8006,
    "lon": 106.6503
}
```

### `POST /api/reset_congestion`
Reset toàn bộ tắc nghẽn về 0

### `POST /api/update_parameters`
Cập nhật tham số BPR

**Request:**
```json
{
    "alpha": 1.5,
    "beta": 8,
    "capacity_factor": 0.4
}
```

---

## 🛠️ Troubleshooting

### ❌ Lỗi: Module not found
```bash
pip install -r requirements.txt
```

### ❌ Lỗi: Graph file not found
- Xóa cache cũ: `rm graph_with_congestion.gpickle`
- Chạy lại: `python app.py` (sẽ tự động download từ OSM)

### ❌ Lỗi: Port 5000 already in use
```bash
# Windows: Tìm và kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### ❌ Lỗi: Cannot find route between points
- Kiểm tra 2 điểm có cùng connected component không
- Thử điểm khác gần trung tâm quận Tân Bình

---

## 🚀 Deployment

### Railway Deployment

---

## 📝 License & Credits

### 👨‍💻 Tác giả
- **Sinh viên:** 
20127552 – Vương Huỳnh Tấn Lộc
21127738 – Trần Bảo Ngọc
23127465 – Nguyễn Hồ Anh Quốc
23127518 – Trần Quốc Việt
24127244 – Phạm Tấn Nhật Thịnh
- **Lớp:** 24C6
- **Môn học:** Tư duy tính toán
- **Giảng viên:** 
thầy Bùi Duy Đăng
thầy Huỳnh Lâm Hải Đăng
thầy Nguyễn Thanh Tình
- **Trường:** Đại học Khoa học Tự nhiên (HCMUS) - ĐHQG TP.HCM
- **Năm học:** 2025-2026 HK1

### 📚 References
1. **Dijkstra, E. W.** (1959). "A note on two problems in connexion with graphs"
2. **Bureau of Public Roads** (1964). "Traffic Assignment Manual"
3. **Jaccard, P.** (1901). "Étude comparative de la distribution florale"
4. **Wardrop, J.** (1952). "Road Traffic Research"
5. **Nielsen, J.** (1993). "Usability Engineering"
6. **ISO 9241-11:2018** - Ergonomics of human-system interaction
7. **Boeing, G.** (2017). "OSMnx: New methods for acquiring street networks"

### 🙏 Acknowledgments
- **OpenStreetMap** contributors for map data
- **NetworkX** team for graph algorithms library
- **OSMnx** team for OpenStreetMap Python library
- **Flask** team for web framework
- **Leaflet.js** team for interactive maps

---

## 📞 Contact & Support

- **GitHub:** https://github.com/thinhelzan842/SmartFlow
- **Issues:** https://github.com/thinhelzan842/SmartFlow/issues
- **Email:** thinhelzan842@gmail.com

---

## 📌 Changelog

### v2.0 (Jan 2026) - Clean & Optimized
- 🧹 Removed 12 dead functions from routing_logic.py
- 🗑️ Deleted ~100 unused files (old demos, CSV, cache)
- 📊 Added comprehensive evaluation (30 test cases)
- 📚 Added scientific references document
- 🎯 Overall score: 85/100 (Grade A)

### v1.0 (Dec 2025) - Initial Release
- ✅ Basic routing with Dijkstra + BPR
- ✅ Interactive map with Leaflet.js
- ✅ Congestion simulation
- ✅ Parameter adjustment

---

**⭐ Nếu project này hữu ích, hãy để lại 1 star trên GitHub!**

---

<div align="center">
  <strong>Made with ❤️ for HCMUS Computational Thinking Course</strong>
  <br>
  <sub>© 2025-2026 SmartFlow Project</sub>
</div>

