"""
SmartFlow Web Application
Traffic routing system with congestion simulation
"""

from flask import Flask, render_template, request, jsonify
from routing_logic import SmartRoutingSystem
import traceback

app = Flask(__name__)

# Initialize routing system with Strong BPR parameters
routing_system = None

def init_routing_system():
    """Initialize routing system on first request."""
    global routing_system
    if routing_system is None:
        routing_system = SmartRoutingSystem(
            alpha=1.5,
            beta=8,
            capacity_factor=0.4
        )

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/api/find_route', methods=['POST'])
def find_route():
    """
    Find multiple alternative routes between two points.
    
    Request JSON:
    {
        "start_lat": float,
        "start_lon": float,
        "end_lat": float,
        "end_lon": float,
        "num_search": int (optional, default: 20)
        "num_display": int (optional, default: 2)
    }
    
    Response JSON:
    {
        "success": bool,
        "num_routes_found": int,
        "num_routes_display": int,
        "routes": [
            {
                "route_index": int,
                "geometries": List[List[Tuple]],
                "distance": float,
                "time": float,
                "segments": int
            },
            ...
        ]
    }
    """
    try:
        init_routing_system()
        
        data = request.get_json()
        
        # Validate input
        required_fields = ['start_lat', 'start_lon', 'end_lat', 'end_lon']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Get parameters (defaults: tìm 20, hiển thị 3, độ lệch 500m)
        num_search = int(data.get('num_search', 20))
        num_display = int(data.get('num_display', 3))
        max_detour_meters = float(data.get('max_detour_meters', 500))
        
        # Find routes
        result = routing_system.find_route(
            start_lat=float(data['start_lat']),
            start_lon=float(data['start_lon']),
            end_lat=float(data['end_lat']),
            end_lon=float(data['end_lon']),
            num_search=num_search,
            num_display=num_display,
            max_detour_meters=max_detour_meters
        )
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in find_route: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/add_congestion_freehand', methods=['POST'])
def add_congestion_freehand():
    """
    Add congestion by freehand drawing (polygon area).
    
    Request JSON:
    {
        "polygon": List[List[float]],  # [[lat, lon], [lat, lon], ...]
        "vehicle_count": int
    }
    
    Response JSON:
    {
        "success": bool,
        "geometries": List[List[Tuple]],
        "vehicle_count": int,
        "num_segments": int,
        "distance": float
    }
    """
    try:
        init_routing_system()
        
        data = request.get_json()
        
        # Validate input
        if 'polygon' not in data or 'vehicle_count' not in data:
            return jsonify({
                'success': False,
                'message': 'Missing required fields: polygon, vehicle_count'
            }), 400
        
        polygon = data['polygon']
        if len(polygon) < 3:
            return jsonify({
                'success': False,
                'message': 'Polygon needs at least 3 points'
            }), 400
        
        # Add congestion in polygon area
        result = routing_system.add_congestion_freehand(
            polygon=polygon,
            vehicle_count=int(data['vehicle_count'])
        )
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in add_congestion_freehand: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/add_congestion_path', methods=['POST'])
def add_congestion_path():
    """
    Add congestion through multiple points (user draws path).
    
    Request JSON:
    {
        "points": List[{"lat": float, "lon": float}],
        "vehicle_count": int
    }
    
    Response JSON:
    {
        "success": bool,
        "geometries": List[List[Tuple]],
        "vehicle_count": int,
        "num_segments": int,
        "distance": float
    }
    """
    try:
        init_routing_system()
        
        data = request.get_json()
        
        # Validate input
        if 'points' not in data or 'vehicle_count' not in data:
            return jsonify({
                'success': False,
                'message': 'Missing required fields: points, vehicle_count'
            }), 400
        
        points = data['points']
        if len(points) < 2:
            return jsonify({
                'success': False,
                'message': 'Need at least 2 points'
            }), 400
        
        # Add congestion through multiple points
        result = routing_system.add_congestion_path(
            points=points,
            vehicle_count=int(data['vehicle_count'])
        )
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in add_congestion_path: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/add_congestion', methods=['POST'])
def add_congestion():
    """
    Add congestion to path between two points using A* for straight path.
    
    Request JSON:
    {
        "start_lat": float,
        "start_lon": float,
        "end_lat": float,
        "end_lon": float,
        "vehicle_count": int
    }
    
    Response JSON:
    {
        "success": bool,
        "path": List[int],
        "geometries": List[List[Tuple]],
        "reverse_geometries": List[List[Tuple]],
        "vehicle_count": int,
        "num_segments": int,
        "distance": float,
        "bidirectional": bool
    }
    """
    try:
        init_routing_system()
        
        data = request.get_json()
        
        # Validate input
        required_fields = ['start_lat', 'start_lon', 'end_lat', 'end_lon', 'vehicle_count']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Add congestion using A* for straight path
        result = routing_system.add_congestion(
            start_lat=float(data['start_lat']),
            start_lon=float(data['start_lon']),
            end_lat=float(data['end_lat']),
            end_lon=float(data['end_lon']),
            vehicle_count=int(data['vehicle_count'])
        )
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in add_congestion: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/update_parameters', methods=['POST'])
def update_parameters():
    """
    Update BPR parameters.
    
    Request JSON:
    {
        "alpha": float (optional),
        "beta": float (optional),
        "capacity_factor": float (optional)
    }
    """
    try:
        init_routing_system()
        
        data = request.get_json()
        
        result = routing_system.update_parameters(
            alpha=data.get('alpha'),
            beta=data.get('beta'),
            capacity_factor=data.get('capacity_factor')
        )
        
        return jsonify({
            'success': True,
            'parameters': result
        })
    
    except Exception as e:
        print(f"Error in update_parameters: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/reset_congestion', methods=['POST'])
def reset_congestion():
    """Reset all congestion in the system."""
    try:
        init_routing_system()
        
        result = routing_system.reset_congestion()
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in reset_congestion: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def status():
    """Get current system status."""
    try:
        if routing_system is None:
            return jsonify({
                'initialized': False
            })
        
        return jsonify({
            'initialized': True,
            'nodes': len(routing_system.G.nodes),
            'edges': len(routing_system.G.edges),
            'alpha': routing_system.alpha,
            'beta': routing_system.beta,
            'capacity_factor': routing_system.capacity_factor
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("SmartFlow Traffic Routing System")
    print("=" * 60)
    print("\nInitializing...")
    
    # Pre-initialize routing system
    init_routing_system()
    
    print("\n✓ System ready!")
    print("=" * 60)
    print("\nStarting web server...")
    print("Open http://localhost:5000 in your browser")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
