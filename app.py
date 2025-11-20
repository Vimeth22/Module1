#Module1: app

from flask import Flask, render_template, request, jsonify
import math

# --- Setup: Initialize the Flask application ---
app = Flask(__name__)

# Focal lengths (in pixels)
FOCAL_X = 1667.53      # fx: Focal length along the X-axis
FOCAL_Y = 1983.20      # fy: Focal length along the Y-axis

# Principal point (center of projection) coordinates (in pixels)
CENTER_X = 1073.56     # cx: Principal point X-coordinate
CENTER_Y = 703.16      # cy: Principal point Y-coordinate

# Known real-world distance
PLANE_DISTANCE_Z = 34.0   


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        point_1_pixel = data['p1']
        point_2_pixel = data['p2']

        # 1. Extract pixel coordinates (u, v)
        pixel_x1, pixel_y1 = point_1_pixel['x'], point_1_pixel['y']
        pixel_x2, pixel_y2 = point_2_pixel['x'], point_2_pixel['y']

        # 2. Apply the Perspective Projection (Pinhole Camera Model) Inversion
        # The formula converts pixel coordinates (u, v) to real-world coordinates (X, Y)
        # on the fixed Z-plane: X = (u - cx) * Z / fx
        
        # Calculate real-world coordinates for Point 1
        real_world_x1 = (pixel_x1 - CENTER_X) * PLANE_DISTANCE_Z / FOCAL_X
        real_world_y1 = (pixel_y1 - CENTER_Y) * PLANE_DISTANCE_Z / FOCAL_Y
        
        # Calculate real-world coordinates for Point 2
        real_world_x2 = (pixel_x2 - CENTER_X) * PLANE_DISTANCE_Z / FOCAL_X
        real_world_y2 = (pixel_y2 - CENTER_Y) * PLANE_DISTANCE_Z / FOCAL_Y

        # 3. Calculate the differences (dX, dY) and Euclidean distance
        delta_x = real_world_x2 - real_world_x1
        delta_y = real_world_y2 - real_world_y1
        
        # Distance is calculated using the Pythagorean theorem: distance = sqrt(dX^2 + dY^2)
        measured_distance = math.sqrt(delta_x**2 + delta_y**2)

        # Log the detailed process for debugging/monitoring
        print(f"--- Measurement Log ---", flush=True)
        print(f"Point 1 (Pixel): ({pixel_x1}, {pixel_y1}) -> Real-World (X, Y): ({real_world_x1:.2f}, {real_world_y1:.2f})", flush=True)
        print(f"Point 2 (Pixel): ({pixel_x2}, {pixel_y2}) -> Real-World (X, Y): ({real_world_x2:.2f}, {real_world_y2:.2f})", flush=True)
        print(f"Calculated ΔX: {delta_x:.4f}, ΔY: {delta_y:.4f}, Total Distance: {measured_distance:.4f} cm", flush=True)

        # 4. Return the results, rounded to four decimal places as requested
        return jsonify({
            "dX": round(abs(delta_x), 4),
            "dY": round(abs(delta_y), 4),
            "distance": round(measured_distance, 4)
        })

    except Exception as e:
        print(f"An error occurred during calculation: {e}", flush=True)
        return jsonify({"error": "Invalid input or calculation failure", "details": str(e)}), 400


if __name__ == '__main__':
    # Flask runs on port 5000 by default
    app.run(debug=True)
