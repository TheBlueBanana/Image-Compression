from base64 import decode
from concurrent.futures import thread, ThreadPoolExecutor
import concurrent.futures
from email.mime import application
from math import log2
from unittest import result
from PIL import Image
from PIL.ImageQt import ImageQt
from numpy import asarray
import numpy as np
import sys, os
import time
from threading import Thread
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from compression_methods.RLE import RLE_encode, RLE_decode

application.__path__ = os.path.dirname(sys.executable)

class Main_Form(QWidget):
    def __init__(self):
        super().__init__()
        self.processDict = {0 : 'RLE'}
        self.methodsDict = {0: self.RLE_decompress}
        self.processDictInv = dict((v,k) for k,v in self.processDict.items())
        self.config = {'byteorder': 'big'}
        self.selected_image = None
        uic.loadUi('MyApp\\UI\\compressionTests.ui', self)
        # uic.loadUi('UI\\compressionTests.ui', self)

        self.select_image_btn.clicked.connect(self.select_image)
        self.show_image_btn.clicked.connect(self.show_image)
        self.save_as_PNG_btn.clicked.connect(self.save_as_PNG)
        self.RLE_btn.clicked.connect(self.RLE_compress)
        # self.TEST_btn.clicked.connect(self.test)

    def select_image(self):
        self.selected_image = None
        self.selected_image = image_name = QFileDialog.getOpenFileName(self, 'Selecciona la imatge que vulguis comprimir', 'C:\\Users\\nuvir\\Pictures\\media_militia_sample_image_pack_001', 'Images (*.png *.xpm *.jpeg *.jpg *bmp *webp *viet)')[0]
        if self.selected_image == '':
            return
        if self.selected_image[-5:] == '.viet':
            self.selected_image = self.decompress_my_image()
        else:
            self.selected_image = Image.open(self.selected_image)
        self.imageInfoTxt.setPlainText(
            f'Imatge: {image_name.split("/")[-1]}\n' +  
            f'Tamany de la imatge: {self.selected_image.width}x{self.selected_image.height}px, amb un pes en cru de {round(self.selected_image.width*self.selected_image.height*3e-6, 2)} MB')
        if self.visualize_cb.isChecked():
            self.selected_image.show()

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

        image = asarray(self.selected_image) # (height, width, depth)
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

        file.close()
        pil_image = Image.fromarray(value).convert('RGB')
        return pil_image

    def show_image(self):
        if self.selected_image == None:
            return
        self.selected_image.show()

    def save_as_PNG(self):
        path = self.get_new_file_location(custom_extension=False)
        if not path[:-4].__contains__('.'):
            path += '.png'
        self.selected_image.save(path, format='PNG')

if __name__ == '__main__':
    app = QApplication([])
    GUI = Main_Form()
    GUI.show()
    sys.exit(app.exec_())