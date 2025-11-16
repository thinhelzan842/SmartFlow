import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# Bounding box quanh đường Trường Chinh (tùy chỉnh)
north, south = 10.8800, 10.7800
east, west = 106.6700, 106.6100
bbox = (north, south, east, west)

# Lấy đồ thị đường phố
G = ox.graph_from_bbox(bbox, network_type='all', simplify=True)

# Thêm trọng số
for u, v, k, data in G.edges(keys=True, data=True):
    length = data.get('length', 100)
    speed_kph = data.get('maxspeed')

    # Chuẩn hóa speed_kph
    if isinstance(speed_kph, list):
        speed_kph = speed_kph[0]
    try:
        speed_kph = float(speed_kph)
    except (TypeError, ValueError):
        highway_type = data.get('highway', '')
        if isinstance(highway_type, list):
            highway_type = highway_type[0]
        if 'residential' in highway_type or 'service' in highway_type:
            speed_kph = 30
        else:
            speed_kph = 50

    We_base = (length / 1000) / speed_kph * 3600
    data['We_base'] = We_base
    data['fe'] = 0

    highway_type = data.get('highway', '')
    if isinstance(highway_type, list):
        highway_type = highway_type[0]

    if 'residential' in highway_type or 'service' in highway_type:
        data['Ce'] = 20
        data['motorbike'] = True
    else:
        data['Ce'] = 100
        data['motorbike'] = False

# Vẽ đồ thị
edge_colors = ['blue' if data.get('motorbike', False) else 'gray' for u, v, data in G.edges(data=True)]
fig, ax = ox.plot_graph(
    G,
    node_size=0,
    edge_color=edge_colors,
    edge_linewidth=2,
    show=True,
    close=True
)

# Lưu đồ thị
nx.write_gpickle(G, "truong_chinh_graph.gpickle")
print("Đã lưu đồ thị vào truong_chinh_graph.gpickle")
