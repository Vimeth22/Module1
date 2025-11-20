import numpy as np

INITIAL_CAMERA_MATRIX = np.array([
    [991.3966961255147, 0, 	671.2440144735679],  # fx and cx
    [0, 991.6283280689119, 371.28640788315386],  # fy and cy
    [0, 0, 1]
])

# Define the resolution the camera was originally calibrated at
ORIGINAL_CALIB_WIDTH, ORIGINAL_CALIB_HEIGHT = 1280, 720

# Define the resolution of the *current* image being measured (e.g., rubik's cube image)
CURRENT_IMAGE_WIDTH, CURRENT_IMAGE_HEIGHT = 2220, 1480

# 2. Scale the Camera Matrix for New Resolution 

# Calculate the scaling factors necessary to adapt the intrinsic parameters
# from the calibration resolution to the current image resolution.
scale_factor_x = CURRENT_IMAGE_WIDTH / ORIGINAL_CALIB_WIDTH
scale_factor_y = CURRENT_IMAGE_HEIGHT / ORIGINAL_CALIB_HEIGHT

# Apply scaling to the focal lengths (fx, fy) and the principal points (cx, cy)
# Note: Python passes arrays by reference, so this updates INITIAL_CAMERA_MATRIX in place.
SCALED_CAMERA_MATRIX = INITIAL_CAMERA_MATRIX.copy() # Make a copy for clarity
SCALED_CAMERA_MATRIX[0, 0] *= scale_factor_x  # Update fx (row 0, col 0)
SCALED_CAMERA_MATRIX[0, 2] *= scale_factor_x  # Update cx (row 0, col 2)
SCALED_CAMERA_MATRIX[1, 1] *= scale_factor_y  # Update fy (row 1, col 1)
SCALED_CAMERA_MATRIX[1, 2] *= scale_factor_y  # Update cy (row 1, col 2)

print("Updated Camera Matrix (Scaled to current image resolution):\n", SCALED_CAMERA_MATRIX)

# 3. Measurement Inputs

# Pixel coordinates (u, v) of the two clicked points in the current image
PIXEL_U1, PIXEL_V1 = 974, 958
PIXEL_U2, PIXEL_V2 = 1241, 959

# Known constant distance (Z) from the camera to the object plane (in cm)
OBJECT_DISTANCE_Z = 34.0

# --- 4. Calculate Real-World Distance ---

# Extract the scaled focal lengths from the matrix
FOCAL_LENGTH_X = SCALED_CAMERA_MATRIX[0, 0]
FOCAL_LENGTH_Y = SCALED_CAMERA_MATRIX[1, 1]

# Calculate the difference in pixel coordinates
delta_u_pixels = abs(PIXEL_U2 - PIXEL_U1)
delta_v_pixels = abs(PIXEL_V2 - PIXEL_V1)

# Apply the Perspective Projection Inversion (simplified for differences at constant Z).
# The relationship is: World_Delta = (Pixel_Delta * Z) / Focal_Length
DELTA_X_WORLD = (delta_u_pixels * OBJECT_DISTANCE_Z) / FOCAL_LENGTH_X
DELTA_Y_WORLD = (delta_v_pixels * OBJECT_DISTANCE_Z) / FOCAL_LENGTH_Y

# Calculate the final Euclidean distance (diagonal) using the Pythagorean theorem
REAL_WORLD_DISTANCE_DIAGONAL = np.sqrt(DELTA_X_WORLD**2 + DELTA_Y_WORLD**2)

# --- 5. Output Results ---

print("\n--- Camera Dimension Measurement Summary ---")
print(f"Clicked Points: P1=({PIXEL_U1},{PIXEL_V1}), P2=({PIXEL_U2},{PIXEL_V2})")
print(f"Constant Object Distance (Z) = {OBJECT_DISTANCE_Z:.2f} cm")
print(f"Pixel Differences: Δu_pixels = {delta_u_pixels}, Δv_pixels = {delta_v_pixels}")
print("\n") # Illustrates the math

print(f"Real-World Horizontal Difference (ΔX_world) = {DELTA_X_WORLD:.4f} cm")
print(f"Real-World Vertical Difference (ΔY_world) = {DELTA_Y_WORLD:.4f} cm")
print(f"Diagonal Distance between points = {REAL_WORLD_DISTANCE_DIAGONAL:.4f} cm")
