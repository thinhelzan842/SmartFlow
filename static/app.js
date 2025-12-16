// SmartFlow Application JavaScript

// Global variables
let map;
let routeLayer;
let markersLayer;
let congestionLayer;
let currentMode = 'route'; // 'route' or 'congestion'
let startPoint = null;
let endPoint = null;
let congestionPoints = []; // Array để lưu nhiều điểm

// Initialize map
function initMap() {
    // Create map centered on Tan Binh District, HCMC
    map = L.map('map').setView([10.8006, 106.6503], 14);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
    
    // Create layers
    routeLayer = L.layerGroup().addTo(map);
    markersLayer = L.layerGroup().addTo(map);
    congestionLayer = L.layerGroup().addTo(map);
    
    // Add click handler
    map.on('click', handleMapClick);
    
    updateStatus('Bản đồ đã sẵn sàng');
}

// Handle map click
function handleMapClick(e) {
    const lat = e.latlng.lat;
    const lon = e.latlng.lng;
    
    if (currentMode === 'route') {
        handleRouteClick(lat, lon);
    } else if (currentMode === 'congestion') {
        handleCongestionClick(lat, lon);
    }
}

// Handle route mode click
function handleRouteClick(lat, lon) {
    if (!startPoint) {
        // Set start point
        startPoint = { lat, lon };
        
        // Add green marker
        const marker = L.marker([lat, lon], {
            icon: L.icon({
                iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
                shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowSize: [41, 41]
            })
        }).addTo(markersLayer);
        
        marker.bindPopup('<b>Điểm xuất phát (A)</b>').openPopup();
        
        updateStatus('Đã chọn điểm A. Click chọn điểm B...');
        
    } else if (!endPoint) {
        // Set end point
        endPoint = { lat, lon };
        
        // Add red marker
        const marker = L.marker([lat, lon], {
            icon: L.icon({
                iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
                shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowSize: [41, 41]
            })
        }).addTo(markersLayer);
        
        marker.bindPopup('<b>Điểm đích (B)</b>').openPopup();
        
        updateStatus('Đang tìm đường...');
        
        // Find route
        findRoute();
    } else {
        // Already have both points, clear and start over
        clearRoute();
        handleRouteClick(lat, lon);
    }
}

// Handle congestion mode click
function handleCongestionClick(lat, lon) {
    // THÊM ĐIỂM VÀO MẢNG
    congestionPoints.push({ lat, lon });
    
    const pointIndex = congestionPoints.length;
    
    // Chọn màu marker theo thứ tự
    let markerColor = 'orange';
    if (pointIndex === 1) markerColor = 'orange';
    else if (pointIndex === 2) markerColor = 'violet';
    else if (pointIndex === 3) markerColor = 'blue';
    else if (pointIndex === 4) markerColor = 'yellow';
    else markerColor = 'grey';
    
    // Thêm marker
    const marker = L.marker([lat, lon], {
        icon: L.icon({
            iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${markerColor}.png`,
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        })
    }).addTo(markersLayer);
    
    marker.bindPopup(`<b>Điểm ${pointIndex}</b>`).openPopup();
    
    // Vẽ đường nối giữa các điểm
    if (congestionPoints.length > 1) {
        const lastPoint = congestionPoints[congestionPoints.length - 2];
        const currentPoint = congestionPoints[congestionPoints.length - 1];
        
        L.polyline(
            [[lastPoint.lat, lastPoint.lon], [currentPoint.lat, currentPoint.lon]],
            {
                color: '#FFA500',
                weight: 3,
                opacity: 0.7,
                dashArray: '5, 5'
            }
        ).addTo(markersLayer);
    }
    
    updateStatus(`Đã chọn ${congestionPoints.length} điểm. Click tiếp hoặc nhấn Enter để xác nhận, Esc để hủy`);
}

// Clear congestion points
function clearCongestionPoints() {
    congestionPoints = [];
    markersLayer.clearLayers();
    updateStatus('Đã xóa các điểm tắc đường');
}

// Confirm congestion path
function confirmCongestionPath() {
    if (congestionPoints.length < 2) {
        alert('Vui lòng chọn ít nhất 2 điểm!');
        return;
    }
    
    // Show modal to input vehicle count
    document.getElementById('congestionModal').classList.add('active');
    document.getElementById('vehicleCount').focus();
}



// Find route
async function findRoute() {
    try {
        // ✅ LẤY GIÁ TRỊ ĐỘ LỆCH TỪ INPUT
        const maxDetourMetersInput = document.getElementById('maxDetourMeters');
        const maxDetourMeters = maxDetourMetersInput ? parseFloat(maxDetourMetersInput.value) : 500;
        
        if (isNaN(maxDetourMeters) || maxDetourMeters < 0) {
            alert('Vui lòng nhập độ lệch hợp lệ (>= 0)');
            return;
        }
        
        updateStatus(`Đang tìm lộ trình (độ lệch tối đa: ${maxDetourMeters.toFixed(0)}m)...`);
        
        const response = await fetch('/api/find_route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                start_lat: startPoint.lat,
                start_lon: startPoint.lon,
                end_lat: endPoint.lat,
                end_lon: endPoint.lon,
                num_search: 20,
                num_display: 3,
                max_detour_meters: maxDetourMeters
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Hiển thị 2-3 routes tốt nhất
            drawMultipleRoutes(data.routes);
            
            // Update info with first route
            if (data.routes && data.routes.length > 0) {
                updateRouteInfo(data.routes[0]);
                
                const baselineInfo = `Thông thoáng: ${data.baseline_distance.toFixed(0)}m`;
                const routeDescriptions = data.routes.map((r, i) => {
                    const detour = r.distance - data.baseline_distance;
                    return `${r.recommendation}: ${r.distance.toFixed(0)}m (+${detour.toFixed(0)}m), ${(r.time/60).toFixed(1)}p`;
                }).join(' | ');
                
                updateStatus(`✓ ${baselineInfo} | ${routeDescriptions}`);
            }
        } else {
            updateStatus('Không tìm được lộ trình: ' + data.message);
            alert(data.message || 'Không tìm được lộ trình thỏa mãn độ lệch!');
        }
    } catch (error) {
        console.error('Error finding route:', error);
        updateStatus('Lỗi: ' + error.message);
        alert('Lỗi khi tìm đường: ' + error.message);
    }
}

// Draw multiple routes on map
function drawMultipleRoutes(routes) {
    // Clear previous routes
    routeLayer.clearLayers();
    
    // Colors: Đường 1 (xanh đậm), Đường 2 (xanh lá), Đường 3 (cam)
    const colors = ['#1976D2', '#388E3C', '#FF9800'];
    const weights = [7, 6, 5];
    const opacities = [0.85, 0.75, 0.7];
    
    routes.forEach((route, routeIndex) => {
        const color = colors[routeIndex] || '#9C27B0';
        const weight = weights[routeIndex] || 5;
        const opacity = opacities[routeIndex] || 0.7;
        const label = route.recommendation || `Đường ${routeIndex + 1}`;
        
        // Draw each segment of this route
        route.geometries.forEach((coords) => {
            if (coords.length > 0) {
                const polyline = L.polyline(coords, {
                    color: color,
                    weight: weight,
                    opacity: opacity
                }).addTo(routeLayer);
                
                // Add popup
                polyline.bindPopup(`
                    <b>🚗 ${label}</b><br>
                    Khoảng cách: ${route.distance.toFixed(0)}m<br>
                    Thời gian: ${(route.time/60).toFixed(1)} phút<br>
                    Số đoạn: ${route.segments}
                `);
            }
        });
    });
    
    // Fit map to all routes
    if (routes.length > 0 && routes[0].geometries.length > 0) {
        const allCoords = routes[0].geometries.flat();
        if (allCoords.length > 0) {
            const bounds = L.latLngBounds(allCoords);
            map.fitBounds(bounds, { padding: [50, 50] });
        }
    }
}

// Update route info
function updateRouteInfo(data) {
    document.getElementById('infoDistance').textContent = `${data.distance.toFixed(0)} m`;
    document.getElementById('infoTime').textContent = `${(data.time / 60).toFixed(1)} phút`;
    document.getElementById('infoSegments').textContent = data.segments;
}

// Add congestion
async function addCongestion(vehicleCount) {
    try {
        if (congestionPoints.length < 2) {
            alert('Cần ít nhất 2 điểm!');
            return;
        }
        
        updateStatus('Đang xử lý đoạn đường kẹt...');
        
        const response = await fetch('/api/add_congestion_path', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                points: congestionPoints,
                vehicle_count: vehicleCount
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Draw congested paths in red
            if (data.geometries && data.geometries.length > 0) {
                data.geometries.forEach((coords) => {
                    if (coords.length > 0) {
                        const polyline = L.polyline(coords, {
                            color: '#FF0000',
                            weight: 7,
                            opacity: 0.85
                        }).addTo(congestionLayer);
                        
                        polyline.bindPopup(`
                            <b>🚦 Đoạn đường tắc nghẽn</b><br>
                            Số xe thêm: ${vehicleCount}<br>
                            Số đoạn: ${data.num_segments}<br>
                            Khoảng cách: ${data.distance.toFixed(0)}m
                        `);
                    }
                });
            }
            
            updateStatus(`✓ Đã thêm tắc đường: +${vehicleCount} xe trên ${data.num_segments} đoạn (${data.distance.toFixed(0)}m)`);
            
            // Clear congestion points after adding
            clearCongestionPoints();
        } else {
            updateStatus('Lỗi: ' + data.message);
            alert('Không thể thêm tắc đường: ' + data.message);
        }
    } catch (error) {
        console.error('Error adding congestion:', error);
        updateStatus('Lỗi: ' + error.message);
        alert('Lỗi khi thêm tắc đường: ' + error.message);
    }
}

// Update BPR parameters
async function updateParameters() {
    try {
        const alpha = parseFloat(document.getElementById('alphaInput').value);
        const beta = parseFloat(document.getElementById('betaInput').value);
        const capacity = parseFloat(document.getElementById('capacityInput').value);
        
        updateStatus('Đang cập nhật tham số...');
        
        const response = await fetch('/api/update_parameters', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                alpha: alpha,
                beta: beta,
                capacity_factor: capacity
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            updateStatus('Đã cập nhật tham số BPR');
            alert('Tham số đã được cập nhật!\n\n' +
                  `Alpha: ${data.parameters.alpha}\n` +
                  `Beta: ${data.parameters.beta}\n` +
                  `Capacity: ${(data.parameters.capacity_factor * 100).toFixed(0)}%`);
        } else {
            updateStatus('Lỗi: ' + data.message);
            alert('Không thể cập nhật tham số: ' + data.message);
        }
    } catch (error) {
        console.error('Error updating parameters:', error);
        updateStatus('Lỗi: ' + error.message);
        alert('Lỗi khi cập nhật tham số: ' + error.message);
    }
}

// Reset congestion
async function resetCongestion() {
    try {
        updateStatus('Đang reset tắc đường...');
        
        const response = await fetch('/api/reset_congestion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            congestionLayer.clearLayers();
            updateStatus('Đã reset tất cả tắc đường');
        } else {
            updateStatus('Lỗi: ' + data.message);
            alert('Không thể reset tắc đường: ' + data.message);
        }
    } catch (error) {
        console.error('Error resetting congestion:', error);
        updateStatus('Lỗi: ' + error.message);
        alert('Lỗi khi reset tắc đường: ' + error.message);
    }
}

// Clear route
function clearRoute() {
    startPoint = null;
    endPoint = null;
    
    markersLayer.clearLayers();
    routeLayer.clearLayers();
    
    // Clear info
    document.getElementById('infoDistance').textContent = '-';
    document.getElementById('infoTime').textContent = '-';
    document.getElementById('infoSegments').textContent = '-';
    
    updateStatus('Đã xóa tuyến đường');
}

// Update status
function updateStatus(message) {
    document.getElementById('statusText').textContent = message;
    console.log('Status:', message);
}

// Update mode hint
function updateModeHint() {
    const hint = document.getElementById('modeHint');
    if (currentMode === 'route') {
        hint.textContent = 'Click 2 điểm trên bản đồ để tìm đường';
    } else {
        hint.textContent = 'Click nhiều điểm để tạo đường kẹt (Enter xác nhận, Esc hủy)';
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Initialize map
    initMap();
    
    // Mode buttons
    document.getElementById('modeRoute').addEventListener('click', function() {
        currentMode = 'route';
        document.getElementById('modeRoute').classList.add('active');
        document.getElementById('modeCongestion').classList.remove('active');
        updateModeHint();
        updateStatus('Chế độ: Tìm đường');
    });
    
    document.getElementById('modeCongestion').addEventListener('click', function() {
        currentMode = 'congestion';
        document.getElementById('modeCongestion').classList.add('active');
        document.getElementById('modeRoute').classList.remove('active');
        updateModeHint();
        updateStatus('Chế độ: Thêm tắc đường');
    });
    
    // Parameter inputs - update display
    document.getElementById('maxDetourMeters').addEventListener('input', function() {
        document.getElementById('maxDetourMetersValue').textContent = this.value + 'm';
    });
    
    document.getElementById('alphaInput').addEventListener('input', function() {
        document.getElementById('alphaValue').textContent = this.value;
    });
    
    document.getElementById('betaInput').addEventListener('input', function() {
        document.getElementById('betaValue').textContent = this.value;
    });
    
    document.getElementById('capacityInput').addEventListener('input', function() {
        document.getElementById('capacityValue').textContent = (this.value * 100).toFixed(0) + '%';
    });
    
    // Control buttons
    document.getElementById('updateParams').addEventListener('click', updateParameters);
    document.getElementById('clearRoute').addEventListener('click', clearRoute);
    document.getElementById('resetCongestion').addEventListener('click', resetCongestion);
    
    // Modal buttons
    document.getElementById('confirmCongestion').addEventListener('click', function() {
        const vehicleCount = parseInt(document.getElementById('vehicleCount').value);
        if (vehicleCount > 0) {
            addCongestion(vehicleCount);
        }
        document.getElementById('congestionModal').classList.remove('active');
    });
    
    document.getElementById('cancelCongestion').addEventListener('click', function() {
        document.getElementById('congestionModal').classList.remove('active');
        clearCongestionPoints();
    });
    
    // Allow Enter key to submit congestion
    document.getElementById('vehicleCount').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            document.getElementById('confirmCongestion').click();
        }
    });
    
    // KEYBOARD SHORTCUTS cho chế độ congestion
    document.addEventListener('keydown', function(e) {
        if (currentMode === 'congestion') {
            if (e.key === 'Enter' && congestionPoints.length >= 2) {
                confirmCongestionPath();
            } else if (e.key === 'Escape') {
                clearCongestionPoints();
                updateStatus('Đã hủy chọn điểm');
            }
        }
    });
});
