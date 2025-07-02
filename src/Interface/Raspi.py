import socket
import rospy
import rostopic
import time

server_host = "192.168.1.21"
server_port = 12346


def send_message_to_server(message, host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ros_client_socket:
            ros_client_socket.connect((host, port))
            ros_client_socket.sendall(message.encode())
            print(f"Sent to server: {message}")
            time.sleep(1)  # Ensure message is sent before continuing
    except Exception as e:
        print(f"Failed to send message to server: {e}")


def send_topics_to_server(topics, host, port):
    for topic in topics:
        topic_message = f"Topic: {topic}"
        send_message_to_server(topic_message, host, port)


def check_ros_connection():
    try:
        rospy.init_node('ros_connection_checker', anonymous=True)

        initial_message = "Admin server started, listening..."
        print(initial_message)
        send_message_to_server(initial_message, host=server_host, port=server_port)

        if rospy.get_master().getPid() == 0:
            error_message = "Unable to connect to ROS master."
            print(error_message)
            send_message_to_server(error_message, host=server_host, port=server_port)
            return False

        success_message = "Connected to ROS master."
        print(success_message)
        send_message_to_server(success_message, host=server_host, port=server_port)

        topics = rostopic.get_topic_list()
        if topics:
            send_topics_to_server(topics, host=server_host, port=server_port)
        else:
            send_message_to_server("No ROS topics available.", host=server_host, port=server_port)

        return True

    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        send_message_to_server(error_message, host=server_host, port=server_port)
        return False


def receive_data_from_server(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")

            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode().strip()
                print(f"Received message: {message}")
    except Exception as e:
        print(f"Failed to receive data from server: {e}")
if __name__ == "__main__":
    connected = check_ros_connection()
    if connected:
        final_message = "Successfully connected to the ROS Master."
        print(final_message)
        send_message_to_server(final_message, host=server_host, port=server_port)
    else:
        final_message = "Failed to connect to the ROS Master."
        print(final_message)
        send_message_to_server(final_message, host=server_host, port=server_port)

    receive_data_from_server(server_host, server_port)
