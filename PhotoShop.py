import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image
from PyQt5.QtCore import Qt
from PIL.ImageFilter import *

def pil2pixmap(im):
    if im.mode == "RGB":
        r, g, b = im.split()
        im = Image.merge("RGB", (b, g, r))
    elif  im.mode == "RGBA":
        r, g, b, a = im.split()
        im = Image.merge("RGBA", (b, g, r, a))
    elif im.mode == "L":
        im = im.convert("RGBA")
    im2 = im.convert("RGBA")
    data = im2.tobytes("raw", "RGBA")
    qim = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(qim)
    return pixmap


folderName = ""

app = QApplication([])
app.setStyleSheet("""
        QWidget
        {
            background-color: #00BB3F;
         
        }
        QPushButton
        {
            background-color: #FF0000;
        }
        QListWidget
        {
            background-color: #33CCCC;
        }
   """)
window = QWidget()
window.resize(700, 500)
folderBtn = QPushButton("Папка")
imagesList = QListWidget()
pictureLbl = QLabel("Картинка")
leftBtn = QPushButton("Вліво")
rightBtn = QPushButton("Вправо")
bwBtn = QPushButton("ЧБ")
filter1 = QPushButton("Фільтер 1")
filter2 = QPushButton("Фільтер 2")
filter3 = QPushButton("Фільтер 3")
filter4 = QPushButton("Фільтер 4")
mainLine = QHBoxLayout()
leftColumn = QVBoxLayout()
rightColumn = QVBoxLayout()

leftColumn.addWidget(folderBtn)
leftColumn.addWidget(imagesList)
mainLine.addLayout(leftColumn)


rightColumn.addWidget(pictureLbl)
filterLine = QHBoxLayout()
filterLine.addWidget(leftBtn)
filterLine.addWidget(rightBtn)
filterLine.addWidget(bwBtn)
rightColumn.addLayout(filterLine)

filter2Line = QHBoxLayout()
filter2Line.addWidget(filter1)
filter2Line.addWidget(filter2)
filter2Line.addWidget(filter3)
filter2Line.addWidget(filter4)
rightColumn.addLayout(filter2Line)
mainLine.addLayout(rightColumn)
window.setLayout(mainLine)

class WorkWithPicture:
    def __init__(self):
        self.image = None
        self.folderName = None
        self.fileName = None
    def downloadPicture(self):
        imagePath = os.path.join(self.folderName,  self.fileName)
        self.image = Image.open(imagePath)
    def seePicture(self):
        pixel = pil2pixmap(self.image)
        pictureLbl.setPixmap(pixel)
    def blackWhite(self):
        self.image = self.image.convert("L")
        self.seePicture()
    def kontyr(self):
        self.image = self.image.filter(CONTOUR)
        self.seePicture()
    def emboss(self):
        self.image = self.image.filter(EMBOSS)
        self.seePicture()
    def blur(self):
        self.image = self.image.filter(BLUR)
        self.seePicture()
    def smooth(self):
        self.image = self.image.filter(SMOOTH)
        self.seePicture()
    
        
def changeFolder():
    global folderName
    folderName = QFileDialog.getExistingDirectory()
    files = os.listdir(folderName)
    for file in files:
        imagesList.addItem(file)
    print(folderName)

redactor = WorkWithPicture()
def showChonsenImage():
    redactor.folderName = folderName
    redactor.fileName = imagesList.currentItem().text()
    redactor.downloadPicture()
    redactor.seePicture()
imagesList.currentRowChanged.connect(showChonsenImage)
folderBtn.clicked.connect(changeFolder)
bwBtn.clicked.connect(redactor.blackWhite)
filter1.clicked.connect(redactor.kontyr)
filter2.clicked.connect(redactor.emboss)
filter3.clicked.connect(redactor.blur)
filter4.clicked.connect(redactor.smooth)
window.show()
app.exec_()
