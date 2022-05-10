from base64 import decode
from concurrent.futures import thread, ThreadPoolExecutor
import concurrent.futures
from math import log2
from unittest import result
from PIL import Image
from PIL.ImageQt import ImageQt
from numpy import asarray
import numpy as np
import sys
import time
from threading import Thread
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap, QImage

# import cgitb
# cgitb.enable(format='text')
import pythoncom

from RLE import RLE_encode, RLE_decode

class Main_Form(QWidget):
    def __init__(self):
        super().__init__()
        self.processDict = {0 : 'RLE'}
        self.methodsDict = {0: self.RLE_decompress}
        self.processDictInv = dict((v,k) for k,v in self.processDict.items())
        self.config = {'byteorder': 'big'}
        self.selected_image = ''
        uic.loadUi('compressionTests.ui', self)

        self.select_image_btn.clicked.connect(self.select_image)
        self.RLE_btn.clicked.connect(self.RLE_compress)
        self.TEST_btn.clicked.connect(self.test)

    def select_image(self):
        self.selected_image = selected_image = None
        self.selected_image = selected_image = QFileDialog.getOpenFileName(self, 'Selecciona la imatge que vulguis comprimir', 'C:\\Users\\nuvir\\Pictures\\media_militia_sample_image_pack_001', 'Images (*.png *.xpm *.jpeg *.jpg *bmp *webp *viet)')[0]
        pixmap=''
        if selected_image == '':
            return
        if selected_image[-5:] == '.viet':
            # time.sleep(0.5)
            pixmap = self.decompress_my_image()
        else:
            pixmap = QPixmap(selected_image)
        self.imageInfoTxt.setPlainText(f'Tamany de la imatge: {pixmap.width()}x{pixmap.height()}px, amb un pes en cru de {round(pixmap.width()*pixmap.height()*3e-6, 2)} MB')
        print('Starting size checks')
        # pythoncom.PumpWaitingMessages()

        h = pixmap.height() / self.image_label.height()
        w = pixmap.width() / self.image_label.width()
        print('Ending var time')
        # time.sleep(0.5)
        if h > w:
            print('Ending var time')
            pixmap = pixmap.scaledToHeight(self.image_label.height())
        else:
            print(self.image_label.width())
            pixmap = pixmap.scaledToWidth(self.image_label.width())
        print('size checked')
        self.image_label.setPixmap(pixmap)
        print('Image decompressed')

    def get_new_file_location(self, custom_extension=True):
        dlg = QFileDialog()
        dlg.setFileMode(0)
        dlg.setNameFilter('Image(*.viet)' if custom_extension else 'Image(*.png *.xpm *.jpeg *.jpg *bmp *webp *viet)')
        dlg.setDirectory('C:\\Users\\nuvir\\Pictures\\')
        dlg.selectFile('My_Image')
        new_file = ''
        if (dlg.exec()):
            new_file = dlg.selectedFiles()[0]
        if new_file == '':
            return ''# If no selected file
        if new_file[-5:] != '.viet' and custom_extension:
            new_file += '.viet'  # If no extension specified
        return new_file

    def RLE_compress(self):
        new_file = self.get_new_file_location()
        if new_file == '':
            return # If no selected file

        image = asarray(Image.open(self.selected_image)) # (height, width, depth)
        if  len(image.shape) == 2:
            image.resize(image.shape[1], image.shape[0], 1)
        [iY, iX, depth] = image.shape

        file = open(new_file, 'wb') #cambiar a xb and handle errors!!!!!!!!!!!!!!!!
        file.write(bytearray([self.processDictInv['RLE']]))
        file.write(iX.to_bytes(2, self.config['byteorder']))
        file.write(iY.to_bytes(2, self.config['byteorder']))

        with ThreadPoolExecutor() as executor:
            threads = []
            for i in range(depth):
                data = image[:, :, i].flatten('C')
                threads.append(executor.submit(RLE_encode, data))
            
            for i in threads:
                file.write(i.result())
        print('compression sucessful')
        file.close()
        # del file 

    def RLE_decompress(self, data):
        iX = int.from_bytes(data.read(2), byteorder=self.config['byteorder'], signed=False)
        iY = int.from_bytes(data.read(2), byteorder=self.config['byteorder'], signed=False)
        im_string = asarray(RLE_decode(data.read()), dtype=np.uint8)
        depth = len(im_string)//(iY*iX)
        print(f'{iX}x{iY}px with a total of {len(im_string)}')
        decoded_image = np.zeros((iY, iX, depth), dtype=np.uint8)
        for i in range(depth):
            decoded_image[:, :, i] = im_string[iY*iX*i:iY*iX*(i+1)].reshape(iY, iX)
        return decoded_image
    
    def decompress_my_image(self):
        file = open(self.selected_image, 'rb')
        method = int.from_bytes(file.read(1), byteorder=self.config['byteorder'], signed=False)
        value = self.methodsDict[method](file)

        # pythoncom.PumpWaitingMessages()
        print(value)
        file.close()
        im = ImageQt(Image.fromarray(value).convert('RGB'))
        # time.sleep(0.5)
        return QPixmap.fromImage(im)

    def test(self):
        # Get image
        im = asarray(Image.open(self.get_new_file_location(custom_extension=False)))
        if  len(im.shape) == 2:
            im.resize(im.shape[1], im.shape[0], 1)
        [iY, iX, depth] = im.shape

        # Encode image
        eres = bytes()
        threads = []
        with ThreadPoolExecutor() as executor:
            for i in range(depth):
                data = im[:, :, i].flatten('C')
                threads.append(executor.submit(RLE_encode, data))
            
            for i in threads:
                eres += i.result()
        
        # Decode image (eres)
        dres = asarray(RLE_decode(eres), dtype=np.uint8)
        dim = np.zeros((iY, iX, len(dres)//(iY*iX)))
        for i in range(depth):
            dim[:, :, i] = dres[iY*iX*i:iY*iX*(i+1)].reshape(iY, iX)
        dim = dim.astype(np.uint8)
        
        # dim = DECODED_IMAGE!!!!
        # Tests
        fdim = dim.astype(np.uint8).flatten('C')
        fim = im.astype(np.uint8).flatten('C')
        for i in range(len(fim)):
            if fim[i] != fdim[i]:
                print('WRONG!!')
        print(np.array_equal(im, dim))
        print(np.array_equal(im, dim))

        arim = Image.fromarray(dim).convert('RGB')
        qim = ImageQt(arim)
        pixmap = QPixmap.fromImage(qim)
        h = pixmap.height() / self.image_label.height()
        w = pixmap.width() / self.image_label.width()
        if h > w:
            pixmap = pixmap.scaledToHeight(self.image_label.height())
        else:
            pixmap = pixmap.scaledToWidth(self.image_label.width())
        self.image_label.setPixmap(pixmap)
        print('ahora si, ¿no?')


if __name__ == '__main__':
    app = QApplication([])
    GUI = Main_Form()
    GUI.show()
    sys.exit(app.exec_())
