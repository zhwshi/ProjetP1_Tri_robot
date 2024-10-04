import socket
import subprocess

# receive the message from java, if received, start the camera code
def receive_robot_pose():
    IP ='172.31.1.140'
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, 30008))
    server.listen(1)


    conn, addr = server.accept()
    data = conn.recv(1024).decode("utf-8")
    conn.close()
    return data

# start the camera code
def start_other_code():
    try:
        print("Starting other script...")
        subprocess.run(["python", "qngle.py"], check=True)
        print("Other script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing the other script: {e}")
    except FileNotFoundError:
        print("The script or command you tried to run was not found.")

#main code
if __name__ == "__main__":

    robot_pose = receive_robot_pose()
    print(robot_pose)
    start_other_code()