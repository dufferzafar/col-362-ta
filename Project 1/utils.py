import socket
from config import SERVERS

def my_IP():
    """
    Returns primary IP address

    https://stackoverflow.com/a/28950776
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def group_IP(username):
    group_no = int(str(username).split("_")[-1]) % 3 + 1
    key = "vpl" + str(group_no)
    return SERVERS[key]


if __name__ == "__main__":
    
    print(group_IP("group_13"))
    print(group_IP("13"))
