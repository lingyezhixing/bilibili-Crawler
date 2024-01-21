#客户端
import socket
def tcp_client(ip, port):
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.connect((ip, port))
    message = '不退出'
    while message!='退出':
        # 发送数据
        message = input("请输入要发送的数据：")
        s.send(message.encode("utf-8"))
        response = s.recv(4096)
        print("服务端：", response.decode("utf-8"))
    s.close()
if __name__ == "__main__":
    ip = #修改为服务器ip
    port=9000
    tcp_client(ip, port)
