"""
SmartFlow Routing Logic
Extracted from traffic_new.ipynb for web application use
"""

import osmnx as ox
import networkx as nx
import numpy as np
import heapq
import math
from typing import List, Tuple, Dict, Optional
import pickle
import os
import heapq
import math

# BPR Formula Constants (default to Strong BPR)
DEFAULT_ALPHA = 1.5
DEFAULT_BETA = 8
DEFAULT_CAPACITY_FACTOR = 0.4

# Configuration
PLACE_NAME = 'Tan Binh District, Ho Chi Minh City, Vietnam'
GRAPH_CACHE_FILE = 'graph_with_congestion.gpickle'


def calculate_bpr_weight(We_base: float, fe: float, Ce: float, alpha: float, beta: float) -> float:
    """
    Calculate dynamic travel cost using BPR (Bureau of Public Roads) formula.
    
    Formula: We = We_base * [1 + α * (fe / Ce)^β]
    """
    if Ce <= 0:
        return We_base * 100
    
    congestion_ratio = fe / Ce
    congestion_factor = 1 + alpha * (congestion_ratio ** beta)
    We = We_base * congestion_factor
    
    return We


def update_edge_weights(G: nx.MultiDiGraph, alpha: float, beta: float) -> None:
    """Update all edge weights in the graph using the BPR formula."""
    for u, v, k, data in G.edges(keys=True, data=True):
        We_base = data.get('We_base', 60)
        fe = data.get('fe', 0)
        Ce = data.get('Ce', 100)
        
        We = calculate_bpr_weight(We_base, fe, Ce, alpha, beta)
        data['weight'] = We


def heuristic_distance(G: nx.MultiDiGraph, node1: int, node2: int) -> float:
    """Tính khoảng cách Euclidean giữa 2 nodes (meters)."""
    lat1, lon1 = G.nodes[node1]['y'], G.nodes[node1]['x']
    lat2, lon2 = G.nodes[node2]['y'], G.nodes[node2]['x']
    
    # Haversine formula approximation
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    distance = 6371000 * c  # Earth radius in meters
    
    return distance


def astar_shortest_path_simple(G: nx.MultiDiGraph, source: int, target: int, 
                               use_weight: bool = False) -> Tuple[List[int], float]:
    """
    A* algorithm ĐƠN GIẢN - TÌM ĐƯỜNG NGẮN NHẤT.
    
    Parameters:
    - use_weight: False = dùng khoảng cách vật lý (cho đánh dấu kẹt)
                  True = dùng trọng số BPR (cho tìm đường tránh kẹt)
    """
    frontier = [(0, source)]
    came_from = {source: None}
    cost_so_far = {source: 0}
    
    while frontier:
        _, current = heapq.heappop(frontier)
        
        if current == target:
            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path, cost_so_far[target]
        
        for neighbor in G.neighbors(current):
            if not G.has_edge(current, neighbor):
                continue
            
            edge_keys = list(G[current][neighbor].keys())
            if not edge_keys:
                continue
            
            edge_data = G[current][neighbor][edge_keys[0]]
            
            # Chọn trọng số
            if use_weight:
                # Dùng trọng số BPR (đã tính tắc nghẽn)
                edge_cost = edge_data.get('weight', edge_data.get('We_base', 60))
            else:
                # Dùng khoảng cách vật lý
                edge_cost = edge_data.get('length', 100)
            
            new_cost = cost_so_far[current] + edge_cost
            
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                
                # Heuristic: khoảng cách thẳng
                h = heuristic_distance(G, neighbor, target)
                priority = new_cost + h
                
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current
    
    return [], float('inf')

def dijkstra_shortest_path(G: nx.MultiDiGraph, source: int, target: int) -> Tuple[List, float]:
    """Find shortest path using Dijkstra's algorithm with current weights."""
    try:
        path = nx.shortest_path(G, source, target, weight='weight')
        cost = nx.shortest_path_length(G, source, target, weight='weight')
        return path, cost
    except nx.NetworkXNoPath:
        return [], float('inf')


def euclidean_distance(G: nx.MultiDiGraph, node1: int, node2: int) -> float:
    """Calculate Euclidean distance between two nodes."""
    x1, y1 = G.nodes[node1]['x'], G.nodes[node1]['y']
    x2, y2 = G.nodes[node2]['x'], G.nodes[node2]['y']
    # Convert to meters approximately (1 degree ≈ 111km)
    dx = (x2 - x1) * 111000 * math.cos(math.radians((y1 + y2) / 2))
    dy = (y2 - y1) * 111000
    return math.sqrt(dx**2 + dy**2)


def astar_straight_path(G: nx.MultiDiGraph, source: int, target: int) -> Tuple[List, float]:
    """
    Find most direct path using A* algorithm.
    Prioritizes straight paths and major roads for congestion marking.
    
    This is used for finding congestion paths, not routing.
    It prefers straight, direct routes that are typically congested.
    """
    if source == target:
        return [source], 0.0
    
    if source not in G or target not in G:
        return [], float('inf')
    
    # Priority queue: (f_score, node, g_score, path)
    open_set = [(0, source, 0, [source])]
    visited = set()
    
    target_x = G.nodes[target]['x']
    target_y = G.nodes[target]['y']
    
    while open_set:
        f_score, current, g_score, path = heapq.heappop(open_set)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        if current == target:
            return path, g_score
        
        current_x = G.nodes[current]['x']
        current_y = G.nodes[current]['y']
        
        # Explore neighbors
        for neighbor in G.successors(current):
            if neighbor in visited:
                continue
            
            # Get edge data
            edge_keys = list(G[current][neighbor].keys())
            if not edge_keys:
                continue
            
            k = edge_keys[0]
            edge_data = G[current][neighbor][k]
            
            # Calculate edge cost
            length = edge_data.get('length', 100)
            
            # Get highway type - prefer major roads for congestion
            highway_type = edge_data.get('highway', '')
            if isinstance(highway_type, list):
                highway_type = highway_type[0]
            
            # Major road bonus (lower cost = preferred)
            if 'primary' in highway_type or 'trunk' in highway_type or 'motorway' in highway_type:
                road_factor = 0.8  # Prefer major roads
            elif 'secondary' in highway_type or 'tertiary' in highway_type:
                road_factor = 0.9
            else:
                road_factor = 1.2  # Avoid small roads for congestion marking
            
            # Calculate direction alignment with target
            neighbor_x = G.nodes[neighbor]['x']
            neighbor_y = G.nodes[neighbor]['y']
            
            # Vector from current to target
            target_dx = target_x - current_x
            target_dy = target_y - current_y
            target_dist = math.sqrt(target_dx**2 + target_dy**2)
            
            # Vector from current to neighbor
            edge_dx = neighbor_x - current_x
            edge_dy = neighbor_y - current_y
            edge_dist = math.sqrt(edge_dx**2 + edge_dy**2)
            
            # Alignment bonus (prefer edges pointing toward target)
            if target_dist > 0 and edge_dist > 0:
                # Dot product normalized
                alignment = (target_dx * edge_dx + target_dy * edge_dy) / (target_dist * edge_dist)
                # alignment ranges from -1 (opposite) to 1 (same direction)
                # Convert to factor: 1.0 (same direction) to 1.5 (opposite)
                alignment_factor = 1.25 - 0.25 * alignment
            else:
                alignment_factor = 1.0
            
            # Total cost with all factors
            edge_cost = length * road_factor * alignment_factor
            new_g_score = g_score + edge_cost
            
            # Heuristic: straight-line distance to target
            h_score = euclidean_distance(G, neighbor, target)
            
            # Total f_score
            new_f_score = new_g_score + h_score
            
            new_path = path + [neighbor]
            heapq.heappush(open_set, (new_f_score, neighbor, new_g_score, new_path))
    
    return [], float('inf')


def increment_path_load(G: nx.MultiDiGraph, path: List[int]) -> None:
    """Increment the load (fe) for all edges along a path."""
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        
        if G.has_edge(u, v):
            edge_keys = list(G[u][v].keys())
            if edge_keys:
                k = edge_keys[0]
                G[u][v][k]['fe'] = G[u][v][k].get('fe', 0) + 1


def increment_path_load_single(G: nx.MultiDiGraph, path: List[int], num_vehicles: int) -> None:
    """
    Tăng load cho 1 chiều duy nhất (không tăng chiều ngược).
    Dùng cho việc thêm tắc nghẽn theo từng bài toán con.
    """
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        
        if G.has_edge(u, v):
            for k in G[u][v]:
                G[u][v][k]['fe'] = G[u][v][k].get('fe', 0) + num_vehicles


def is_bidirectional_edge(G: nx.MultiDiGraph, u: int, v: int) -> bool:
    """
    Kiểm tra xem cạnh u→v có đường ngược v→u không.
    Trả về True nếu là đường 2 chiều.
    """
    return G.has_edge(u, v) and G.has_edge(v, u)


def increment_path_load_bidirectional(G: nx.MultiDiGraph, path: List[int], num_vehicles: int) -> None:
    """
    ✅ TĂNG LOAD CHO CẢ 2 CHIỀU.
    
    Đánh dấu tắc nghẽn cho cả u→v và v→u.
    """
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        
        # Chiều u → v
        if G.has_edge(u, v):
            for k in G[u][v]:
                G[u][v][k]['fe'] = G[u][v][k].get('fe', 0) + num_vehicles
        
        # ✅ Chiều ngược v → u
        if G.has_edge(v, u):
            for k in G[v][u]:
                G[v][u][k]['fe'] = G[v][u][k].get('fe', 0) + num_vehicles


def initialize_graph_for_routing(G: nx.MultiDiGraph, capacity_factor: float = 1.0) -> nx.MultiDiGraph:
    """Initialize graph with necessary attributes for BPR routing."""
    G_routing = G.copy()
    
    for u, v, k, data in G_routing.edges(keys=True, data=True):
        # Get base travel time
        length = data.get('length', 100)
        
        # Get speed
        speed_kph = data.get('maxspeed')
        if isinstance(speed_kph, list) and len(speed_kph) > 0:
            speed_kph = speed_kph[0]
        try:
            speed_kph = float(speed_kph)
        except (TypeError, ValueError):
            highway_type = data.get('highway', '')
            if isinstance(highway_type, list):
                highway_type = highway_type[0]
            
            if 'motorway' in highway_type or 'trunk' in highway_type:
                speed_kph = 80
            elif 'primary' in highway_type:
                speed_kph = 60
            elif 'secondary' in highway_type or 'tertiary' in highway_type:
                speed_kph = 50
            elif 'residential' in highway_type or 'service' in highway_type:
                speed_kph = 30
            else:
                speed_kph = 40
        
        # Calculate base travel time in seconds
        We_base = (length / 1000) / speed_kph * 3600
        data['We_base'] = We_base
        
        # Initialize load
        data['fe'] = 0
        
        # Set capacity
        lanes = data.get('lanes')
        if lanes:
            try:
                if isinstance(lanes, list):
                    lanes = float(lanes[0])
                else:
                    lanes = float(lanes)
            except (TypeError, ValueError):
                lanes = 1
        else:
            lanes = 1
        
        highway_type = data.get('highway', '')
        if isinstance(highway_type, list):
            highway_type = highway_type[0]
        
        if 'motorway' in highway_type or 'trunk' in highway_type:
            base_capacity = 2000
        elif 'primary' in highway_type:
            base_capacity = 1500
        elif 'secondary' in highway_type or 'tertiary' in highway_type:
            base_capacity = 1000
        elif 'residential' in highway_type or 'service' in highway_type:
            base_capacity = 500
        else:
            base_capacity = 800
        
        Ce = base_capacity * lanes / 60 * capacity_factor
        data['Ce'] = max(Ce, 10)
    
    return G_routing


def load_or_create_graph() -> nx.MultiDiGraph:
    """Load graph from cache or create new one from OSM."""
    if os.path.exists(GRAPH_CACHE_FILE):
        print(f"Loading graph from cache: {GRAPH_CACHE_FILE}")
        with open(GRAPH_CACHE_FILE, 'rb') as f:
            G = pickle.load(f)
        
        # Convert to largest strongly connected component for routing
        if not nx.is_strongly_connected(G):
            print("Graph is not strongly connected, extracting largest component...")
            largest_scc = max(nx.strongly_connected_components(G), key=len)
            G = G.subgraph(largest_scc).copy()
            print(f"Using largest component: {len(G.nodes)} nodes, {len(G.edges)} edges")
        else:
            print(f"Graph is strongly connected: {len(G.nodes)} nodes, {len(G.edges)} edges")
        
        return G
    else:
        print(f"Creating new graph from OSM: {PLACE_NAME}")
        ox.settings.use_cache = True
        ox.settings.log_console = False
        G = ox.graph_from_place(PLACE_NAME, network_type='drive')
        
        # Extract largest strongly connected component
        if not nx.is_strongly_connected(G):
            print("Extracting largest strongly connected component...")
            largest_scc = max(nx.strongly_connected_components(G), key=len)
            G = G.subgraph(largest_scc).copy()
        
        # Save to cache
        with open(GRAPH_CACHE_FILE, 'wb') as f:
            pickle.dump(G, f)
        
        print(f"Graph created: {len(G.nodes)} nodes, {len(G.edges)} edges")
        return G


def find_nearest_node(G: nx.MultiDiGraph, lat: float, lon: float, consider_direction: bool = False) -> int:
    """
    Tìm node gần nhất với tọa độ cho trước.
    
    Args:
        G: Đồ thị có hướng
        lat, lon: Tọa độ cần tìm
        consider_direction: Nếu True, tìm node có edge đi RA (outgoing) gần nhất
                          Giúp chọn đúng làn đường khi có đường 1 chiều
    
    Returns:
        Node ID gần nhất
    """
    if not consider_direction:
        # Tìm node gần nhất đơn giản (như cũ)
        return ox.distance.nearest_nodes(G, lon, lat)
    
    # ✅ TÌM NODE CÓ XÉT HƯỚNG ĐƯỜNG
    # Bước 1: Tìm node gần nhất
    nearest_node = ox.distance.nearest_nodes(G, lon, lat)
    
    # Lấy danh sách các node trong bán kính 50m
    nearby_nodes = []
    for node in G.nodes():
        node_data = G.nodes[node]
        dist = ox.distance.great_circle(lat, lon, node_data['y'], node_data['x'])
        if dist <= 50:  # 50 mét
            nearby_nodes.append((node, dist))
    
    if not nearby_nodes:
        return nearest_node
    
    # Bước 2: Trong các nodes gần, ưu tiên node có outgoing edges (có đường đi)
    nearby_nodes.sort(key=lambda x: x[1])  # Sort theo khoảng cách
    
    for node, dist in nearby_nodes:
        # Kiểm tra node có đường đi ra không
        if G.out_degree(node) > 0:
            return node
    
    # Nếu không có node nào có outgoing edge, trả về gần nhất
    return nearest_node


def point_to_line_distance(px: float, py: float, x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculate distance from point (px, py) to line segment (x1,y1)-(x2,y2).
    Used to find edges near the straight line between two points.
    """
    # Line segment length squared
    line_length_sq = (x2 - x1)**2 + (y2 - y1)**2
    
    if line_length_sq == 0:
        # Line segment is actually a point
        return math.sqrt((px - x1)**2 + (py - y1)**2)
    
    # Calculate projection of point onto line segment
    t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / line_length_sq))
    
    # Nearest point on line segment
    proj_x = x1 + t * (x2 - x1)
    proj_y = y1 + t * (y2 - y1)
    
    # Distance from point to projection
    return math.sqrt((px - proj_x)**2 + (py - proj_y)**2)


def find_edges_along_line(G: nx.MultiDiGraph, lat1: float, lon1: float, 
                          lat2: float, lon2: float, max_distance: float = 0.0003) -> List[Tuple[int, int]]:
    """
    ✅ Find edges that lie near the straight line connecting two points.
    
    Instead of using A* (which finds shortest path through graph),
    this directly finds edges that are physically close to the straight line.
    
    UPDATED: Requires BOTH endpoints of edge to be near the line
    (prevents selecting edges perpendicular to the line)
    
    Args:
        G: Graph
        lat1, lon1: Point 1 coordinates
        lat2, lon2: Point 2 coordinates
        max_distance: Maximum distance in degrees (~30m for 0.0003)
    
    Returns:
        List of (u, v) edge tuples near the line, sorted from point 1 to point 2
    """
    edges_near_line = []
    
    # Iterate through all edges
    for u, v, k in G.edges(keys=True):
        u_data = G.nodes[u]
        v_data = G.nodes[v]
        
        # Edge endpoint coordinates
        edge_lat1 = u_data['y']
        edge_lon1 = u_data['x']
        edge_lat2 = v_data['y']
        edge_lon2 = v_data['x']
        
        # ✅ CHECK CẢ 2 ENDPOINTS - không chỉ midpoint
        dist_u = point_to_line_distance(edge_lon1, edge_lat1, lon1, lat1, lon2, lat2)
        dist_v = point_to_line_distance(edge_lon2, edge_lat2, lon1, lat1, lon2, lat2)
        
        # Chỉ chọn edge nếu CẢ 2 endpoints đều gần đường thẳng
        if dist_u <= max_distance and dist_v <= max_distance:
            # Tính khoảng cách từ midpoint đến start point (để sort)
            mid_lat = (edge_lat1 + edge_lat2) / 2
            mid_lon = (edge_lon1 + edge_lon2) / 2
            dist_from_start = math.sqrt((mid_lon - lon1)**2 + (mid_lat - lat1)**2)
            edges_near_line.append((u, v, dist_from_start))
    
    # Sort by distance from point 1 to point 2
    edges_near_line.sort(key=lambda x: x[2])
    
    # Return only (u, v) tuples
    return [(u, v) for u, v, _ in edges_near_line]


def point_in_polygon(px: float, py: float, polygon: List[Tuple[float, float]]) -> bool:
    """
    ✅ Check if point is inside polygon using ray casting algorithm.
    Used for freehand drawing mode.
    """
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if py > min(p1y, p2y):
            if py <= max(p1y, p2y):
                if px <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (py - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or px <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside


def find_edges_in_polygon(G: nx.MultiDiGraph, polygon: List[List[float]]) -> List[Tuple[int, int]]:
    """
    ✅ Find all edges whose midpoints are inside the drawn polygon.
    Used for freehand drawing mode.
    
    Args:
        G: Graph
        polygon: List of [lat, lon] points forming the polygon
    
    Returns:
        List of (u, v) edge tuples inside polygon
    """
    edges_in_polygon = []
    
    # Convert polygon to (lon, lat) for consistency
    poly_coords = [(p[1], p[0]) for p in polygon]  # [lat, lon] -> (lon, lat)
    
    # Iterate through all edges
    for u, v, k in G.edges(keys=True):
        u_data = G.nodes[u]
        v_data = G.nodes[v]
        
        # Edge midpoint
        mid_lat = (u_data['y'] + v_data['y']) / 2
        mid_lon = (u_data['x'] + v_data['x']) / 2
        
        # Check if midpoint is inside polygon
        if point_in_polygon(mid_lon, mid_lat, poly_coords):
            edges_in_polygon.append((u, v))
    
    return edges_in_polygon


def get_edge_geometry(G: nx.MultiDiGraph, u: int, v: int) -> List[Tuple[float, float]]:
    """Get coordinates for an edge."""
    edge_keys = list(G[u][v].keys())
    if not edge_keys:
        return []
    
    k = edge_keys[0]
    data = G[u][v][k]
    
    # Check if edge has geometry
    if 'geometry' in data:
        geom = data['geometry']
        return [(coord[1], coord[0]) for coord in geom.coords]  # (lat, lon)
    else:
        # Use node coordinates
        u_data = G.nodes[u]
        v_data = G.nodes[v]
        return [(u_data['y'], u_data['x']), (v_data['y'], v_data['x'])]


def get_path_geometry(G: nx.MultiDiGraph, path: List[int]) -> List[List[Tuple[float, float]]]:
    """Get full geometry for a path."""
    geometries = []
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        coords = get_edge_geometry(G, u, v)
        geometries.append(coords)
    return geometries


def calculate_path_stats(G: nx.MultiDiGraph, path: List[int], cost: float) -> Dict:
    """Calculate statistics for a path."""
    total_distance = 0
    num_segments = len(path) - 1
    
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        if G.has_edge(u, v):
            edge_keys = list(G[u][v].keys())
            if edge_keys:
                k = edge_keys[0]
                total_distance += G[u][v][k].get('length', 0)
    
    return {
        'distance': total_distance,
        'time': cost,
        'segments': num_segments
    }


class SmartRoutingSystem:
    """Main routing system for the web application."""
    
    def __init__(self, alpha: float = DEFAULT_ALPHA, beta: float = DEFAULT_BETA, 
                 capacity_factor: float = DEFAULT_CAPACITY_FACTOR):
        """Initialize routing system."""
        self.alpha = alpha
        self.beta = beta
        self.capacity_factor = capacity_factor
        
        # Load base graph
        G_base = load_or_create_graph()
        
        # Initialize for routing (directed graph)
        self.G = initialize_graph_for_routing(G_base, capacity_factor)
        
        # ✅ ĐỒ THỊ KHÔNG CÓ HƯỚNG cho đánh dấu tắc nghẽn
        # Key: (u, v) với u < v (chuẩn hóa)
        # Value: vehicle_count
        self.congestion_graph = nx.Graph()  # Undirected graph
        
        # Copy nodes từ graph chính
        for node, data in self.G.nodes(data=True):
            self.congestion_graph.add_node(node, **data)
        
        print(f"Routing system initialized with α={alpha}, β={beta}, capacity={capacity_factor}")
        print(f"Graph: {len(self.G.nodes)} nodes, {len(self.G.edges)} edges")
        print(f"Congestion graph: {len(self.congestion_graph.nodes)} nodes (undirected)")
    
    def find_route(self, start_lat: float, start_lon: float, 
                   end_lat: float, end_lon: float, num_search: int = 20, 
                   num_display: int = 3, max_detour_meters: float = 500) -> Dict:
        """
        Tìm 2-3 lộ trình tốt nhất với điều kiện không vượt quá độ lệch cho phép so với lộ trình thông thoáng.
        
        Quy trình:
        1. Tìm lộ trình tối ưu khi KHÔNG có tắc nghẽn (baseline/thông thoáng)
        2. Áp dụng tắc nghẽn, tìm tối đa num_search lộ trình
        3. Lọc: Chỉ giữ lộ trình có độ dài <= baseline_distance + max_detour_meters
        4. Chọn 2-3 đường tốt nhất: nhanh nhất thời gian, ngắn nhất khoảng cách
        
        Args:
            start_lat, start_lon: Tọa độ xuất phát
            end_lat, end_lon: Tọa độ đích
            num_search: Số lộ trình tìm kiếm tối đa (mặc định: 20)
            num_display: Số lộ trình hiển thị tốt nhất (mặc định: 3)
            max_detour_meters: Độ lệch tối đa (mét) so với lộ trình thông thoáng (mặc định: 500m)
        
        Returns:
            Dict với 2-3 routes tốt nhất thỏa mãn điều kiện độ lệch
        """
        # Find nearest nodes với xét hướng đường (tránh chọn sai làn)
        start_node = find_nearest_node(self.G, start_lat, start_lon, consider_direction=True)
        end_node = find_nearest_node(self.G, end_lat, end_lon, consider_direction=False)
        
        # ✅ BƯỚC 1: TÌM LỘ TRÌNH THÔNG THOÁNG (baseline - không có tắc nghẽn)
        print("🔍 Tìm lộ trình thông thoáng (baseline)...")
        try:
            # Tạm thời clear congestion để tìm đường thông thoáng
            temp_congestion_edges = []
            for u, v, k in self.G.edges(keys=True):
                if self.G[u][v][k].get('fe', 0) > 0:
                    temp_congestion_edges.append((u, v, k, self.G[u][v][k]['fe']))
                    self.G[u][v][k]['fe'] = 0
            
            update_edge_weights(self.G, self.alpha, self.beta)
            baseline_path = nx.shortest_path(self.G, start_node, end_node, weight='weight')
            baseline_cost = nx.shortest_path_length(self.G, start_node, end_node, weight='weight')
            baseline_geometries = get_path_geometry(self.G, baseline_path)
            baseline_stats = calculate_path_stats(self.G, baseline_path, baseline_cost)
            baseline_distance = baseline_stats['distance']
            
            print(f"📏 Lộ trình thông thoáng: {baseline_distance:.0f}m")
            
            # Restore congestion
            for u, v, k, fe_val in temp_congestion_edges:
                self.G[u][v][k]['fe'] = fe_val
                
        except nx.NetworkXNoPath:
            return {
                'success': False,
                'message': 'Không tìm thấy đường đi giữa 2 điểm'
            }
        
        # ✅ BƯỚC 2: ÁP DỤNG CONGESTION và tìm các lộ trình thay thế
        self._apply_congestion_to_directed_graph()
        
        # ✅ LƯU TRẠNG THÁI BAN ĐẦU để restore sau khi tìm
        initial_fe = {}
        for u, v, k in self.G.edges(keys=True):
            initial_fe[(u, v, k)] = self.G[u][v][k].get('fe', 0)
        
        all_routes = []
        
        # ✅ TÌM 20 LỘTRÌNH KHÁC NHAU
        for i in range(num_search):
            # Update weights với congestion hiện tại
            update_edge_weights(self.G, self.alpha, self.beta)
            
            # ✅ DÙNG DIJKSTRA (như notebook) thay vì A*
            try:
                path = nx.shortest_path(self.G, start_node, end_node, weight='weight')
                cost = nx.shortest_path_length(self.G, start_node, end_node, weight='weight')
            except nx.NetworkXNoPath:
                break  # Không còn đường nào
            
            if not path or len(path) < 2:
                break
            
            # Get geometries and stats
            geometries = get_path_geometry(self.G, path)
            stats = calculate_path_stats(self.G, path, cost)
            
            all_routes.append({
                'path': path,
                'geometries': geometries,
                'distance': stats['distance'],
                'time': stats['time'],  # Thời gian tính bằng giây
                'segments': stats['segments'],
                'route_index': i + 1
            })
            
            # ✅ TĂNG LOAD trên path này (như notebook)
            # → Lần tìm tiếp theo sẽ tránh path này
            increment_path_load(self.G, path)
        
        # ✅ RESTORE trạng thái ban đầu (không lưu các fe tăng tạm thời)
        for (u, v, k), fe_val in initial_fe.items():
            if self.G.has_edge(u, v):
                self.G[u][v][k]['fe'] = fe_val
        
        if not all_routes:
            return {
                'success': False,
                'message': 'Không tìm thấy đường đi giữa 2 điểm'
            }
        
        # ✅ BƯỚC 3: LỌC THEO ĐỘ LỆCH - Chỉ giữ routes không vượt quá baseline + max_detour_meters
        max_allowed_distance = baseline_distance + max_detour_meters
        valid_routes = [r for r in all_routes if r['distance'] <= max_allowed_distance]
        
        print(f"📐 Độ lệch cho phép: {max_detour_meters:.0f}m → Khoảng cách tối đa: {max_allowed_distance:.0f}m")
        print(f"✓ Tìm được {len(all_routes)} lộ trình, {len(valid_routes)} thỏa mãn độ lệch")
        
        # ✅ Nếu không tìm được route nào thỏa mãn
        if not valid_routes:
            shortest_found = min(all_routes, key=lambda r: r['distance'])
            return {
                'success': False,
                'message': f'Không tìm được lộ trình nào trong độ lệch {max_detour_meters:.0f}m. Lộ trình thông thoáng: {baseline_distance:.0f}m. Lộ trình ngắn nhất tìm được: {shortest_found["distance"]:.0f}m (vượt {shortest_found["distance"] - max_allowed_distance:.0f}m)',
                'baseline_distance': baseline_distance,
                'max_allowed_distance': max_allowed_distance,
                'shortest_found': shortest_found['distance']
            }
        
        # ✅ BƯỚC 4: CHỌN 2-3 ĐƯỜNG TỐT NHẤT
        # 1. Nhanh nhất về THỜI GIAN (BPR weight)
        routes_by_time = sorted(valid_routes, key=lambda r: r['time'])
        
        # 2. Ngắn nhất về KHOẢNG CÁCH (km)
        routes_by_distance = sorted(valid_routes, key=lambda r: r['distance'])
        
        # ✅ CHỌN ĐƯỜNG ĐỀ XUẤT (2-3 đường)
        selected_routes = []
        selected_paths = set()  # Tránh trùng lặp
        
        # Đường 1: Nhanh nhất về thời gian
        fastest = routes_by_time[0].copy()
        fastest['recommendation'] = '⚡ Nhanh nhất (Thời gian)'
        fastest['rank'] = 1
        selected_routes.append(fastest)
        selected_paths.add(tuple(fastest['path']))
        
        # Đường 2: Ngắn nhất về khoảng cách (nếu khác đường 1)
        shortest = routes_by_distance[0].copy()
        if tuple(shortest['path']) not in selected_paths:
            shortest['recommendation'] = '📏 Ngắn nhất (Khoảng cách)'
            shortest['rank'] = 2
            selected_routes.append(shortest)
            selected_paths.add(tuple(shortest['path']))
        
        # Đường 3: Nhanh thứ 2 về thời gian (nếu có và khác 2 đường trên)
        if len(routes_by_time) > 1:
            second_fastest = routes_by_time[1].copy()
            if tuple(second_fastest['path']) not in selected_paths and len(selected_routes) < num_display:
                second_fastest['recommendation'] = '⚡ Lựa chọn thứ 2'
                second_fastest['rank'] = 3
                selected_routes.append(second_fastest)
        
        print(f"📦 Đề xuất {len(selected_routes)} đường:")
        for route in selected_routes:
            detour = route['distance'] - baseline_distance
            print(f"  {route['recommendation']}: {route['distance']:.0f}m (+{detour:.0f}m), {route['time']/60:.1f} phút")
        
        return {
            'success': True,
            'num_routes_found': len(all_routes),
            'num_routes_display': len(selected_routes),
            'routes': selected_routes,
            'baseline_distance': baseline_distance,
            'max_allowed_distance': max_allowed_distance,
            'max_detour_meters': max_detour_meters,
            'start_node': start_node,
            'end_node': end_node
        }
    
    def add_congestion_path(self, points: List[Dict], vehicle_count: int) -> Dict:
        """
        ✅ THÊM TẮC NGHẼN THEO NHIỀU ĐIỂM - Nối các điểm bằng A* path.
        
        Cách hoạt động:
        1. Nối các điểm liên tiếp bằng A* (dùng khoảng cách thuần)
        2. Thêm edges vào đồ thị không hướng (congestion_graph)
        3. Lần tìm đường sau sẽ áp dụng congestion và tránh đoạn này
        
        Args:
            points: List of {"lat": float, "lon": float}
            vehicle_count: Number of vehicles to add
        
        Returns:
            Dict with geometries, num_segments, distance
        """
        if len(points) < 2:
            return {
                'success': False,
                'message': 'Cần ít nhất 2 điểm'
            }
        
        all_geometries = []
        total_segments = 0
        total_distance = 0.0
        
        # Nối các điểm liên tiếp bằng A* path
        for i in range(len(points) - 1):
            start_lat = points[i]['lat']
            start_lon = points[i]['lon']
            end_lat = points[i + 1]['lat']
            end_lon = points[i + 1]['lon']
            
            # Tìm nearest nodes
            start_node = find_nearest_node(self.G, start_lat, start_lon)
            end_node = find_nearest_node(self.G, end_lat, end_lon)
            
            if start_node == end_node:
                continue
            
            # ✅ TÌM ĐƯỜNG NGẮN NHẤT bằng A* (dùng khoảng cách thuần, không dùng trọng số)
            path, cost = astar_shortest_path_simple(
                self.G, start_node, end_node, use_weight=False
            )
            
            if not path or len(path) < 2:
                continue  # Không tìm thấy đường
            
            # ✅ THÊM EDGES VÀO ĐỒ THỊ KHÔNG HƯỚNG
            for j in range(len(path) - 1):
                u, v = path[j], path[j + 1]
                
                # Chuẩn hóa (u, v) với u < v cho undirected graph
                edge_key = (min(u, v), max(u, v))
                u_norm, v_norm = edge_key
                
                # Thêm hoặc cập nhật edge trong congestion graph
                if self.congestion_graph.has_edge(u_norm, v_norm):
                    # Cộng dồn vehicle_count
                    current = self.congestion_graph[u_norm][v_norm].get('vehicle_count', 0)
                    self.congestion_graph[u_norm][v_norm]['vehicle_count'] = current + vehicle_count
                else:
                    # Thêm edge mới
                    self.congestion_graph.add_edge(u_norm, v_norm, vehicle_count=vehicle_count)
                
                total_segments += 1
                
                # Lưu geometry để vẽ
                coords = get_edge_geometry(self.G, u, v)
                if coords:
                    all_geometries.append([coords])
                
                # Tính khoảng cách
                if self.G.has_edge(u, v):
                    edge_data = self.G[u][v][0]
                    total_distance += edge_data.get('length', 0)
        
        if total_segments == 0:
            return {
                'success': False,
                'message': 'Không tìm được đường giữa các điểm'
            }
        
        return {
            'success': True,
            'geometries': all_geometries,
            'vehicle_count': vehicle_count,
            'num_segments': total_segments,
            'distance': total_distance
        }
    
    def _apply_congestion_to_directed_graph(self):
        """Áp dụng congestion từ đồ thị không hướng sang đồ thị có hướng."""
        # Reset tất cả fe về 0
        for u, v, k in self.G.edges(keys=True):
            self.G[u][v][k]['fe'] = 0
        
        # Áp dụng congestion từ undirected graph với PENALTY MẠNH
        for u, v, data in self.congestion_graph.edges(data=True):
            vehicle_count = data.get('vehicle_count', 0)
            
            # ✅ PENALTY MẠNH: Nhân vehicle_count với 100 để ép xe tránh đoạn này
            # Ví dụ: 50 xe → fe = 5000 → BPR weight tăng CỰC MẠNH → A* tránh
            penalty_multiplier = 100
            effective_load = vehicle_count * penalty_multiplier
            
            # Áp dụng cho cả 2 chiều (nếu tồn tại)
            if self.G.has_edge(u, v):
                for k in self.G[u][v]:
                    self.G[u][v][k]['fe'] = effective_load
            
            if self.G.has_edge(v, u):
                for k in self.G[v][u]:
                    self.G[v][u][k]['fe'] = effective_load
    
    def add_congestion_freehand(self, polygon: List[List[float]], vehicle_count: int) -> Dict:
        """
        ✅ THÊM TẮC NGHẼN BẰNG VẼ TAY - Tìm edges trong vùng polygon.
        
        Args:
            polygon: List of [lat, lon] points forming drawn polygon
            vehicle_count: Number of vehicles to add
        
        Returns:
            Dict with geometries, num_segments, distance
        """
        if len(polygon) < 3:
            return {
                'success': False,
                'message': 'Vùng vẽ quá nhỏ'
            }
        
        # Tìm tất cả edges trong polygon
        edges = find_edges_in_polygon(self.G, polygon)
        
        if not edges:
            return {
                'success': False,
                'message': 'Không tìm thấy đường nào trong vùng vẽ'
            }
        
        all_geometries = []
        total_segments = 0
        total_distance = 0.0
        
        # Tăng load cho từng edge
        for u, v in edges:
            if self.G.has_edge(u, v):
                for k in self.G[u][v]:
                    # Tăng traffic load
                    self.G[u][v][k]['fe'] = self.G[u][v][k].get('fe', 0) + vehicle_count
                    
                    # Lưu geometry
                    coords = get_edge_geometry(self.G, u, v)
                    if coords:
                        all_geometries.append([coords])
                    
                    # Đếm segments
                    total_segments += 1
                    
                    # Tính khoảng cách
                    total_distance += self.G[u][v][k].get('length', 0)
        
        # Cập nhật trọng số BPR
        update_edge_weights(self.G, self.alpha, self.beta)
        
        return {
            'success': True,
            'geometries': all_geometries,
            'vehicle_count': vehicle_count,
            'num_segments': total_segments,
            'distance': total_distance
        }
    
    def add_congestion(self, start_lat: float, start_lon: float, 
                       end_lat: float, end_lon: float, vehicle_count: int) -> Dict:
        """
        ✅ THÊM TẮC NGHẼN - 2 BÀI TOÁN CON.
        
        Bài toán 1: Tìm đường ngắn nhất từ A→B, tăng fe
        Bài toán 2: Tìm đường ngắn nhất từ B→A, tăng fe (nếu có đường 2 chiều)
        """
        # Find nearest nodes
        start_node = find_nearest_node(self.G, start_lat, start_lon)
        end_node = find_nearest_node(self.G, end_lat, end_lon)
        
        # ✅ BÀI TOÁN 1: Tìm đường A→B (dùng khoảng cách vật lý)
        path_forward, cost_forward = astar_shortest_path_simple(
            self.G, start_node, end_node, use_weight=False
        )
        
        if not path_forward:
            return {
                'success': False,
                'message': 'Không tìm được đường giữa 2 điểm này'
            }
        
        # Tăng load cho đường A→B
        increment_path_load_single(self.G, path_forward, vehicle_count)
        
        # Kiểm tra xem có đường 2 chiều không
        all_bidirectional = all(
            is_bidirectional_edge(self.G, path_forward[i], path_forward[i+1])
            for i in range(len(path_forward) - 1)
        )
        
        geometries = [get_path_geometry(self.G, path_forward)]
        total_segments = len(path_forward) - 1
        
        # ✅ BÀI TOÁN 2: Nếu có đường 2 chiều, tìm đường B→A
        if all_bidirectional:
            path_backward, cost_backward = astar_shortest_path_simple(
                self.G, end_node, start_node, use_weight=False
            )
            
            if path_backward:
                # Tăng load cho đường B→A
                increment_path_load_single(self.G, path_backward, vehicle_count)
                
                # Thêm geometry của đường ngược
                geometries.append(get_path_geometry(self.G, path_backward))
                total_segments += len(path_backward) - 1
        
        # Cập nhật trọng số BPR sau khi thêm congestion
        update_edge_weights(self.G, self.alpha, self.beta)
        
        # Tính tổng khoảng cách
        total_distance = sum(
            self.G[path_forward[i]][path_forward[i+1]][0].get('length', 0)
            for i in range(len(path_forward) - 1)
            if self.G.has_edge(path_forward[i], path_forward[i+1])
        )
        
        return {
            'success': True,
            'path': path_forward,
            'geometries': geometries,
            'vehicle_count': vehicle_count,
            'num_segments': total_segments,
            'distance': total_distance,
            'bidirectional': all_bidirectional
        }
    
    def update_parameters(self, alpha: Optional[float] = None, 
                         beta: Optional[float] = None,
                         capacity_factor: Optional[float] = None):
        """Update BPR parameters."""
        if alpha is not None:
            self.alpha = alpha
        if beta is not None:
            self.beta = beta
        if capacity_factor is not None:
            self.capacity_factor = capacity_factor
            # Need to reinitialize graph with new capacity
            G_base = load_or_create_graph()
            self.G = initialize_graph_for_routing(G_base, self.capacity_factor)
        
        return {
            'alpha': self.alpha,
            'beta': self.beta,
            'capacity_factor': self.capacity_factor
        }
    
    def reset_congestion(self):
        """Reset all congestion (fe) to 0 and clear congestion graph."""
        # Clear undirected congestion graph
        self.congestion_graph.clear_edges()
        
        # Reset fe in directed graph
        for u, v, k, data in self.G.edges(keys=True, data=True):
            data['fe'] = 0
        
        return {'success': True, 'message': 'All congestion reset'}
