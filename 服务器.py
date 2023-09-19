import socket,os,time
import requests,threading
from bs4 import BeautifulSoup
def main(url):
    #获取开始时间戳
    starttime = time.time()
    while time.time()-starttime<=2592000:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 获取视频标题
        title = soup.find('h1', class_='video-title').text
        # 获取视频播放量
        play = soup.find('span', class_='view').text
        play=play.replace('\n', '')
        play=play.strip()
        #获取精确到秒的时间戳
        time_stamp=time.time()
        # 获取当前时间
        now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time_stamp))
        # 将结果保存到video_info文件夹的文件中
        with open('video_info//'+title+'.txt', 'a', encoding='utf-8') as f:
            f.write(now_time+' ' + play + '\n')
        if time.time()-starttime<=604800:
            time.sleep(60)
        elif time.time()-starttime<=1209600:
            time.sleep(300)
        elif time.time()-starttime<=2592000:
            time.sleep(600)
        
    

def tcp_server(port):
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.bind(("", port))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        print("连接地址：", addr)
        while True:
            data = conn.recv(4096)
            if not data:
                break
            print("客户端：", data.decode("utf-8"))
            #判断是否是bilibili视频网址
            if "bilibili.com" in data.decode("utf-8"):
                #判断“视频信息”文件夹是否存在
                if not os.path.exists("video_info"):
                    os.mkdir("video_info")
                try:
                    #启动一个线程来运行main，并传入参数data.decode("utf-8")
                    t = threading.Thread(target=main, args=(data.decode("utf-8"),))
                    t.start()
                    #获取目前创建的线程数量
                    n=threading.active_count()
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                    response = requests.get(data.decode("utf-8"), headers=headers)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # 获取视频标题
                    title = soup.find('h1', class_='video-title').text
                    conn.send(('已接收到url,播放量信息将保存到video_info/'+title+'.txt文件中,当前正在运行的爬虫有'+str(n-1)+'个').encode("utf-8"))
                except Exception as e:
                    print(e)
            else:
                conn.send(("请输入正确的bilibili视频网址").encode("utf-8"))
        conn.close()

if __name__ == "__main__":
    port = 9000
    print("服务器启动成功，正在监听端口：", port)
    tcp_server(port)
