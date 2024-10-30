import cv2
import numpy as np

def get_dominant_color(frame, x, y, w, h):
    # Extract region of interest
    roi = frame[y:y+h, x:x+w]
    # Convert to HSV color space
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # Calculate average HSV values
    avg_color = np.mean(hsv_roi, axis=(0,1))
    return avg_color

def compare_colors(color1, color2):
    # Calculate difference in Hue, Saturation, and Value
    h_diff = abs(color1[0] - color2[0])
    s_diff = abs(color1[1] - color2[1])
    v_diff = abs(color1[2] - color2[2])
    
    # Normalize hue difference (since hue is circular)
    if h_diff > 180:
        h_diff = 360 - h_diff
        
    return h_diff, s_diff, v_diff

# Initialize video capture
cap = cv2.VideoCapture(0)

# Define regions for comparison (left and right side of frame)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
region_width = frame_width // 4
region_height = frame_height // 4

# Define regions for left and right objects
left_region = {
    'x': frame_width // 4,
    'y': frame_height // 3,
    'w': region_width,
    'h': region_height
}

right_region = {
    'x': (frame_width * 3) // 4 - region_width,
    'y': frame_height // 3,
    'w': region_width,
    'h': region_height
}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Get colors from both regions
    left_color = get_dominant_color(frame, **left_region)
    right_color = get_dominant_color(frame, **right_region)
    
    # Compare colors
    h_diff, s_diff, v_diff = compare_colors(left_color, right_color)
    
    # Draw rectangles around regions
    cv2.rectangle(frame, 
                 (left_region['x'], left_region['y']), 
                 (left_region['x'] + left_region['w'], left_region['y'] + left_region['h']), 
                 (0, 255, 0), 2)
    cv2.rectangle(frame, 
                 (right_region['x'], right_region['y']), 
                 (right_region['x'] + right_region['w'], right_region['y'] + right_region['h']), 
                 (0, 255, 0), 2)
    
    # Display color difference information
    info_text = f"Hue diff: {h_diff:.1f}, Sat diff: {s_diff:.1f}, Val diff: {v_diff:.1f}"
    cv2.putText(frame, info_text, (10, frame_height - 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Show the frame
    cv2.imshow('Color Comparison', frame)
    
    # Break loop on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()