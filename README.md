# Module 1 – Object Dimension Measurement from a Single Image

## 1. Overview

This module implements a small **Flask web application** that measures the **real-world distance between two points on a known planar object** (the Rubik’s cube) from a single image.  
Using the **pinhole camera model** and the **intrinsic camera parameters** obtained from prior calibration, the app converts pixel distances into distances in centimeters, assuming a fixed distance of the object from the camera.

The web UI lets the user click two points on the Rubik’s cube and then displays:

- The pixel coordinates of each point  
- The horizontal and vertical distances in centimeters  
- The final Euclidean distance between the two points  

The two screenshots for this module show:

1. **Initial screen** – only the image and the “Clicking…” status button.  
2. **After two clicks** – red dots marking the selected points and a text box with the numerical results.

---

## 2. Learning Objectives

By completing this module, I practiced:

- Using **camera calibration results** (intrinsic matrix) in a practical measurement task.
- Applying the **pinhole camera projection equations** to go from pixel space to 3-D coordinates on a plane.
- Building a minimal **Flask + JavaScript** app to interact with an image and send pixel coordinates to the backend.
- Structuring numerical computations cleanly in Python (separating calibration/math logic from the web server).

---

## 3. Project Structure

The main files for Module 1 are:

- `app.py`  
  - Flask application that serves the web page and exposes a `/calculate` endpoint.  
  - Receives two pixel points from the front end, performs the geometric calculations, and returns a JSON response with distances.

- `A1.py`  
  - Stand-alone script that demonstrates the same math using hard-coded pixel coordinates.  
  - Shows how the intrinsic camera matrix is **scaled from the original calibration resolution (1280×720) to the current image resolution (2220×1480)** and how ΔX, ΔY, and the diagonal distance are computed.

- `templates/index.html`  
  - Front-end page that loads the Rubik’s cube image, captures mouse clicks, draws the red dots, and calls `/calculate` via AJAX/`fetch`.

- `requirements.txt`  
  - Currently contains:
    - `Flask>=2.0.0`

You should also have a `static/` folder containing the Rubik’s cube image that is displayed on the page.

---

## 4. Dependencies and Setup

### 4.1. Create and activate a virtual environment (recommended)

```bash
# From the Module1 directory
python3 -m venv venv
source venv/bin/activate      # On macOS / Linux
# venv\Scripts\activate       # On Windows
                    