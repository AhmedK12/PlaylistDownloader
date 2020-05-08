import requests
import multiprocessing
import os
import time
import pafy
import bs4
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QLabel, QLineEdit, QPushButton, QFileDialog, QProgressBar, QCheckBox
from PyQt5 import QtCore


class Download:
    def __init__(self, url, location, title, size, cookie):
        self.url = url
        self.title = title
        self.location = location
        self.cookie = cookie
        self.No_of_Proc = multiprocessing.cpu_count()
        self.size = int(size)
        self.remainder = int(self.size) % self.No_of_Proc
        self.process = []
        self.multi()

    def multi(self):
        start_index = '0'
        end_index = '0'
        for i in range(0, self.No_of_Proc):
            if i == 0:
                end_index = str(self.size//self.No_of_Proc)
                self.process.append(multiprocessing.Process(target=self.download, args=(i, start_index, end_index)))
            else:
                start_index = str(int(end_index) + 1)
                end_index = str((i+1)*self.size//self.No_of_Proc)
                self.process.append(multiprocessing.Process(target=self.download, args=(i, start_index, end_index)))
            if i == 7:
                start_index = str(int(end_index) + 1)
                end_index = str((i+1)*self.size//self.No_of_Proc + self.remainder)
                self.process.append(multiprocessing.Process(target=self.download, args=(i, start_index, end_index)))

        for i in range(0, self.No_of_Proc):
            self.process[i].start()
        for i in range(0, self.No_of_Proc):
            self.process[i].join()
        self.concatenate()

    def download(self, n, start_index, end_index,):

        headers = {"Range": "bytes=" + str(start_index) + "-" + str(end_index)}
        headers['user-agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
        try:
            response = requests.get(self.url, headers=headers, stream=True)
            file = open(self.location + '/' + str(n), "wb")
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        except:
            pass

    def concatenate(self):
        filename = ['0', '1', '2', '3', '4', '5', '6', '7']
        open(self.location + '/' + self.title, "w")
        file2 = '\'' + self.location + '/' + self.title + '\''
        for _file in filename:
            file = "\'" + self.location+"/"+_file + "\'"
            command = " cat " + file + " >> " + file2
            os.system(command)
            time.sleep(0.1)
            os.system("rm -rf " + file)


class Video:
    def __init__(self, url, quality):
        self.url = url
        self.video = []
        self.audio = []
        self.normal = []
        self.title = ''
        self.quality = quality
        print('i am in video class')
        self.stream1()
        # print('i am in video class')

    def stream1(self):
        video = pafy.new(self.url)
        self.title = video.title
        ls = []
        ls.append(video.getbestaudio().url)
        ls.append(video.getbestaudio().get_filesize())
        ls.append(self.title)
        self.audio.append(ls)
        # print(video.streams[0])

        for stream in video.streams:
            # print('fuck off ')
            # if 'video' in str(stream) and self.quality in str(stream.resolution):
            #     ls = []
            #     ls.append(stream.url)
            #     ls.append(stream.get_filesize())
            #     ls.append(self.title)
            #     self.video.append(ls)
            # print(str(stream) + "  " + str(stream.resolution) +" "+self.quality + " "+str(stream.get_filesize()))
            if 'normal' in str(stream) and self.quality in str(stream.resolution):
                self.normal.append(stream.url)
                self.normal.append(str(stream.get_filesize()))
                self.normal.append(self.title)
                print(self.normal)


class Gui(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Youtube_DownloaderBy_BlackHat")
        self.setGeometry(800, 400, 900, 400)
        self.setFixedSize(900, 350)
        self.x = 10
        self.y = 10
        self.pg = QProgressBar(self)
        self.pg.resize(0, 0)
        self.Download = QPushButton(self)
        self.lebal = QLabel(self)
        self.title = ''
        self.location = ""
        self.link = ''
        self.quality = "480p"
        self.speed = QLabel(self)
        self.remaining = QLabel(self)
        self.setStyleSheet("""
        QWidget {
   background-color: #008080;
}

QLineEdit {
   background-color: aliceblue;
   color: #618b38;
   font-style: italic;
   font-weight: bold;
   border-radius: 5px;
}

QLabel {
   background-color: #fff;
   color: #0f0;
}

QPushButton {
   background-color: #333;
   color: #fff;
   border-radius: 5px;
   border-style: none;
   height: 25px;
}

QProgressBar{
   background-color: aliceblue;
   color: #fff;
   border-radius: 5px;
   border-style: slid;
   height: 25px;
   text-align: center
   }

   QComboBox{
   background-color: #333;
   color: #fff;
   border-radius: 0px;
   border-style: none;
   height: 25px;
   }

""")

        # self.worker = WorkThread()
        # self.workerThread = QtCore.QThread()
        # self.workerThread.started.connect(self.worker.run)
        # self.worker.moveToThread(self.workerThread)
        # self.worker.UpdateTextBoxSignal.connect(self.UpdateTextBoxFunction)
        self.initui()

    def initui(self):
        self.layout()
        self.show()
        self.styleSheet()

    def layout(self):
        self.enterlink()
        self.getpaths()
        self.select()
        self.download()
        self.settitle()

    def getfilename(self):
        self.location = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.getpath.setText(self.location)

    def StartThreading(self):
        self.workerThread.start()

    def UpdateTextBoxFunction(self, value):
        if len(value) is 5:
            print('Process')
            process1 = multiprocessing.Process(target=Download, args=(value[0], value[3], value[2], value[1], '0'))
            process1.start()
            self.progress()
            self.setspeed()
            self.remain(value[4])

        if len(value) == 3:
            self.pg.setValue(value[1])
            self.lebal.setText(value[0])
            self.speed.setText('Speed: ' + value[2])

    def enterlink(self):
        self.enterthelink = QLineEdit(self)
        self.enterthelink.move(self.x, self.y+30)
        self.enterthelink.resize(self.x+750, 42)
        self.enterthelink.setPlaceholderText('Enter The Url')

    def select(self):
        self.selectquality = QComboBox(self)
        self.selectquality.move(self.x + 770, self.y+30)
        self.selectquality.resize(100, 40)
        list_item = ['Quality', '2160p', '1440p', '1080p', '720p', '480p', '360p', '240p', '144p']
        self.selectquality.clear()
        self.selectquality.addItems(list_item)
        self.selectquality.activated[str].connect(self.onactivated)

    def onactivated(self, text):
        self.quality = text

    def getpaths(self):
        self.getpath = QLineEdit(self)
        self.getpath.setPlaceholderText('Select Location')
        self.getpath.move(self.x, self.y+100)
        self.getpath.resize(200, 40)
        self.path = QPushButton('Browse', self)
        self.path.move(self.x + 220, self.y+100)
        self.path.resize(100, 40)
        self.path.clicked.connect(self.getfilename)

    def progress(self):
        self.pg.move(self.x+20, self.y+230)
        self.pg.setValue(0)
        self.pg.resize(700, 30)

    def download(self):
        self.Download.resize(200, 40)
        self.Download.move(self.x+400, self.y+100)
        self.Download.setText('Start Download')
        self.Download.clicked.connect(self.downloadbtn)

    def downloadbtn(self):
        self.link = self.enterthelink.text()
        print(self.link + " " + self.location + " " + self.quality[:-1])
        self.worker = WorkThread(self.link, self.location, self.quality[:-1])
        self.workerThread = QtCore.QThread()
        self.workerThread.started.connect(self.worker.run)
        self.worker.moveToThread(self.workerThread)
        self.worker.UpdateTextBoxSignal.connect(self.UpdateTextBoxFunction)
        self.StartThreading()

    def settitle(self):
        self.lebal.setText(self.title)
        self.lebal.resize(600, 40)
        self.lebal.move(self.x+50, self.y + 170)

    def setspeed(self):
        self.speed.resize(300, 20)
        self.speed.move(self.x+730, self.y + 233)

    def remain(self, number):
        self.remaining.move(self.x+100, self.y+300)
        self.remaining.setText(str(number) + 'Video is Remaining')




class WorkThread(QtCore.QObject):
    UpdateTextBoxSignal = QtCore.pyqtSignal(list)

    def __init__(self, url, location, quality):
        super().__init__()
        self.size = 0
        self.url = url
        self.title = ''
        self.no_of_videos = 0
        self.current_video = 0
        self.quality = quality
        '''   links contain link of the video Title of links and link2 is 2
              links[0] = link2  = Url of The Video
              links[1] = link2[1] = Title of The Video
              location contains the path of Directory Where Video Will Save
              title  = Title of Playlist                    
         '''
        self.links = []
        self.link2 = []
        self.location = location
        self.No_of_Proc = multiprocessing.cpu_count()
        if 'list' in self.url:
            self.get_url(self.url)
            if os.path.exists(self.location+'/'+self.title) is False:
                os.mkdir(self.location+'/'+self.title)
                self.location = self.location+'/'+self.title
            for link in self.links:
                if link not in self.link2:
                    self.link2.append(link)
        self.no_of_videos = len(self.link2)

    @QtCore.pyqtSlot()
    def run(self):
        for link in self.link2:
            self.current_video += 1
            try:
                video = Video(link[0], self.quality)
                normal = video.normal
                audio = video.audio
                vido = video.video
                normal.append(self.location)
                normal.append(self.no_of_videos-self.current_video)
                print(len(normal))
                if len(normal) > 0:
                    self.UpdateTextBoxSignal.emit(normal)
                # else:
                #     ls = []
                #     ls.append('not normal')
                #     ls.append(vido)
                #     ls.append(audio)
                #     self.UpdateTextBoxSignal.emit(ls.append(self.location))
                size2 = 0
                size3 = 0
                size1 = 0
                while size3 + 10 < int(normal[1]):
                    size3, size2 = self.get_size(normal[2])
                    if size2 > size1:
	                    ls = []
	                    ls.append(normal[2])
	                    ls.append(round(size2/int(normal[1]), 2)*100)
	                    ls.append(str(round((((size2-size1)//1024)//1024)/0.5, 2)))
	                    self.UpdateTextBoxSignal.emit(ls)
	                    size1 = size2
	                    time.sleep(0.5)
            except:
                pass

    def get_size(self, tit):
        size3 = 0
        size2 = 0
        for i in range(0, self.No_of_Proc):
            try:
                if os.path.exists(self.location + "/" + str(i)):
                    size3 = size3 + os.path.getsize(self.location + '/' + str(i))
                size2 = os.path.getsize(self.location + '/' + tit)

            except:
                pass
        return size2, size3

    def get_url(self, url):
        data = bs4.BeautifulSoup(requests.get(self.url).content, 'html.parser')
        if "list" not in self.url:
            self.links.append((url.split('&')[0], data.title.text))
        else:
                h3 = data.find('h3', class_='playlist-title')
                self.title = str(h3.text.lstrip().rstrip().replace('\n', ''))
                for a in data.find_all('a'):
                    lst = str(a.get('href')).split('&')
                    for i in a.find_all('h4'):
                        ls = []
                        ls.append('https://www.youtube.com'+lst[0])
                        ls.append(str(i.text).lstrip().replace('\n', ''))
                        self.links.append(ls)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gui()
    sys.exit(app.exec_())
