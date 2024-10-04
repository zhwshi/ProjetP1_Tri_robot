import cv2
import numpy as np
import pyrealsense2 as rs
import socket
import subprocess

# Start the "envoyer" script, allowing the computer to wait and listen for information from Java
def start_other_code():
    try:
        print("Starting other script...")
        subprocess.run(["python", "envoyer.py"], check=True)
        print("Other script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing the other script: {e}")
    except FileNotFoundError:
        print("The script or command you tried to run was not found.")


def send_tcp_data(data, host='172.31.1.147', port=30008):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.connect(server_address)
    try:
        # Send data
        sock.sendall(data.encode())
    finally:
        # Close the connection
        sock.close()


# Camera configuration
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  # Enable depth stream
pipeline.start(config)


# Dictionary to store unique identifiers for each shape and color
shape_identifiers = {
    "2": {"5": [], "4": []},
    "3": {"5": [], "4": []},  # Cylinder = 4, Cube = 5
    "1": {"5": [], "4": []},  # 1 = blue; 2 = yellow; 3 = red
}


# Counters to track the number of objects for each color and shape
shape_count = {
    "2": {"5": 1, "4": 1},
    "3": {"5": 1, "4": 1},
    "1": {"5": 1, "4": 1},
}


# List to accumulate the coordinates of the most recently detected objects
all_shape_coords = []


while True:
    
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()  # Get depth frame
   
    if not color_frame or not depth_frame:
        continue


    color_image = np.asanyarray(color_frame.get_data())
    depth_image = np.asanyarray(depth_frame.get_data())
    hsv_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)


    # Clear `all_shape_coords` each time the image refreshes
    all_shape_coords.clear()


    # Color threshold for yellow objects
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])


    # Color threshold for red objects
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])


    # Color threshold for blue objects
    lower_blue = np.array([50, 30, 20])
    upper_blue = np.array([140, 255, 255])


    # Extend blue range to include dark blue
    lower_blue_dark = np.array([90, 50, 50])
    upper_blue_dark = np.array([120, 255, 255])


    # Create masks
    mask_yellow = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    mask_red1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    mask_blue = cv2.inRange(hsv_image, lower_blue, upper_blue)
    mask_blue_dark = cv2.inRange(hsv_image, lower_blue_dark, upper_blue_dark)


    # Combine red masks
    mask_red = cv2.add(mask_red1, mask_red2)


    # Combine blue masks
    mask_blue_combined = cv2.add(mask_blue, mask_blue_dark)


    # Find contours
    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_blue, _ = cv2.findContours(mask_blue_combined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    # Function to draw the center points and label shapes
    def draw_shapes(contours, color, shape_color_name, detect_cubes=True):
        for cnt in contours:
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            if 700 < area < 5000 and perimeter > 0:
                x, y, w, h = cv2.boundingRect(cnt)
                center_x, center_y = x + w // 2, y + h // 2

                # Get the depth value at the center point
                depth = float(depth_image[center_y, center_x])
            
                if depth > 0:  # Check if depth is valid
                    # Convert to 3D coordinates in millimeters
                    z = depth  # Depth is already in millimeters
                    x_3d = (center_x - 320) * z / 640  # Assuming image width is 640
                    y_3d = (center_y - 240) * z / 480  # Assuming image height is 480

                    # Use the minimum enclosing rectangle to compute the angle
                    rect = cv2.minAreaRect(cnt)
                    angle = rect[2]  # Get rotation angle
                    
                    # Ensure the angle is within the range [-90°, 90°]
                    if angle < -45:
                        angle += 90

                    # Determine the shape type (square/circle)
                    if shape_color_name != "1":  # Non-blue shapes
                        shape = "5" if detect_cubes else "4"
                    else:  # For blue shapes
                        if 0.8 < float(w) / h < 1.2 and len(cv2.approxPolyDP(cnt, 0.04 * perimeter, True)) == 4:
                            shape = "5"
                        else:
                            shape = "4"

                    if shape == "5":
                        all_shape_coords.append(f"{x_3d}, {y_3d}, {z}, {shape_color_name}, {shape}, {angle:.2f}")
                    else:
                        all_shape_coords.append(f"{x_3d}, {y_3d}, {z}, {shape_color_name}, {shape}, {0}")

                    # Register the unique identifier for the object
                    identifier = shape_count[shape_color_name][shape]
                    shape_identifiers[shape_color_name][shape].append((x_3d, y_3d, z))

                    # Label color, shape, and unique identifier
                    cv2.circle(color_image, (center_x, center_y), 5, color, -1)
                    if shape == "5":
                        cv2.putText(color_image, f"{shape_color_name} {shape} {identifier}, {angle:.2f}",
                                    (center_x, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    else:
                        cv2.putText(color_image, f"{shape_color_name} {shape} {identifier}",
                                    (center_x, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                    # Increment the counter for the same type of object
                    shape_count[shape_color_name][shape] += 1


    # Draw center points and recognize shapes
    draw_shapes(contours_yellow, (0, 255, 255), "2")
    draw_shapes(contours_red, (0, 0, 255), "3")
    draw_shapes(contours_blue, (255, 0, 0), "1")


    # Display the image
    cv2.imshow('Shape Detection', color_image)


    # Send data and exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        # Send only the latest detection results
        if all_shape_coords:
            # Get the total number of points and include it in the string to be sent
            num_points = len(all_shape_coords)
            data_to_send = f"{num_points}\n" + "1.0,1.0,1.0,1.0,1.0,1.0" + "\n" + "\n".join(all_shape_coords)
            print("Sending the following data:\n", data_to_send)
            send_tcp_data(data_to_send)
        break

pipeline.stop()
cv2.destroyAllWindows()
start_other_code()
