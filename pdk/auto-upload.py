import logging
import os
import time
import sys
from qiniu import Auth, etag, put_file
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s]-[%(asctime)s]-[%(lineno)s]==> %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
log = logging.getLogger("auto-upload")


class Qiniu:
    def __init__(self):
        access_key = 's8X5IO5gyziT2sbgrbsC3xBcpGf9y_S20c1NKnnh'
        secret_key = 'H0X30bZcJGhh6jVnPRpHvXV88WWKznXFAEMv3UsZ'
        self.__q = Auth(access_key, secret_key)
        self.bucket_name = 'cases-image'

    def upload(self, file):
        """仅上传文件"""
        localfile = file
        key = "new_img/20" + file.split("new_img/20")[-1]
        token = self.__q.upload_token(self.bucket_name, key)
        ret, info = put_file(token, key, localfile)
        log.info(info)
        assert ret['key'] == key
        assert ret['hash'] == etag(localfile)


Q = Qiniu()


class MonitorFileEventHandler(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory:
            return
        Q.upload(event.src_path)


class MonitorFile:
    def __init__(self, path):
        self.observer = Observer()
        self.observer.schedule(MonitorFileEventHandler(), path, recursive=True)

    def __del__(self):
        self.observer.stop()
        self.observer.join()

    def start(self):
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

PATH = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    try:
        method = sys.argv[1]
        if method == "start":
            if not os.path.exists(os.path.join(PATH, "upload")):
                os.mkdir(os.path.join(PATH, "upload"))
            os.system("nohup python3 auto-upload.py > upload/upload.log & echo $! > upload/master.pid")
        elif method == "stop":
            os.system("kill -9 `cat upload/master.pid`")
        elif method == "status":
            os.system("ps -ef|grep auto-upload.py")
        elif method == "upload":
            for root, dirs, files in os.walk(os.path.join(PATH, "new_img")):
                for file in files:
                    log.info("Upload: " + os.path.join(root, file))
                    Q.upload(os.path.join(root, file))
        else:
            sys.exit("""使用正确的方式:
    start  开启
    stop   终止
    status 状态
""")
    except IndexError:
        main = MonitorFile(os.path.join(PATH, "new_img"))
        main.start()
