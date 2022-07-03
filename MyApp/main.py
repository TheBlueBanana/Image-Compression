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
from compression_methods.DC import DC_encode, DC_decode
from compression_methods.RLE import RLE_encode, RLE_decode
from compression_methods.entropy import get_all_entropies
from compression_methods.huffman import huffman_encode, huffman_decode
from compression_methods.hybrid import RLE_H_encode, RLE_H_decode, DC_H_encode, DC_H_decode, DC_RLE_H_encode, DC_RLE_H_decode


application.__path__ = os.path.dirname(sys.executable)

build = True

class Main_Form(QWidget):
    def __init__(self):
        super().__init__()
        self.processDict = {0: 'RLE', 1: 'huffman', 2: 'DC', 3: 'RLE_H', 4: 'DC_H', 5: 'DC_RLE_H'}
        self.encoderDict = {'RLE': RLE_encode, 'huffman' : huffman_encode, 'DC' : DC_encode, 'RLE_H' : RLE_H_encode, 'DC_H': DC_H_encode, 'DC_RLE_H': DC_RLE_H_encode}
        self.decoderDict = {0: RLE_decode, 1 : huffman_decode, 2: DC_decode, 3: RLE_H_decode, 4: DC_H_decode, 5:DC_RLE_H_decode}
        self.processDictInv = dict((v,k) for k,v in self.processDict.items())
        self.config = {'byteorder': 'big'}
        self.selected_image = None
        if build:
            uic.loadUi('UI\\compressionTests.ui', self)
        else:
            uic.loadUi('MyApp\\UI\\compressionTests.ui', self)

        self.select_image_btn.clicked.connect(self.select_image)
        self.show_image_btn.clicked.connect(self.show_image)
        self.save_as_PNG_btn.clicked.connect(self.save_as_PNG)
        self.RLE_btn.clicked.connect(self.RLE_compress)
        self.huffman_btn.clicked.connect(self.huffman_compress)
        self.DC_btn.clicked.connect(self.DC_compress)
        self.RLE_H_btn.clicked.connect(self.RLE_H_compress)
        self.DC_H_btn.clicked.connect(self.DC_H_compress)
        self.DC_RLE_H_btn.clicked.connect(self.DC_RLE_H_compress)

        self.entropy_btn.clicked.connect(self.show_entropy)
        self.entropy_txt.setVisible(False)

        self.progress_bar.setMaximum(100)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setVisible(False)
        self.progress_bar_label.setVisible(False)

    def select_image(self):
        self.entropy_txt.setVisible(False)
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
        self.compress_image('RLE')
    def huffman_compress(self):
        self.compress_image('huffman')
    def DC_compress(self):
        self.compress_image('DC')
    def RLE_H_compress(self):
        self.compress_image('RLE_H')
    def DC_H_compress(self):
        self.compress_image('DC_H')
    def DC_RLE_H_compress(self):
        self.compress_image('DC_RLE_H')
    
    def compress_image(self, method):
        new_file = self.get_new_file_location()
        if new_file == '':
            return # If no selected file

        image = asarray(self.selected_image) # (height, width, depth)
        if  len(image.shape) == 2:
            image.resize(image.shape[1], image.shape[0], 1)
        [iY, iX, depth] = image.shape

        file = open(new_file, 'wb') #cambiar a xb and handle errors!!!!!!!!!!!!!!!!
        file.write(bytearray([self.processDictInv[method]]))
        file.write(iX.to_bytes(2, self.config['byteorder']))
        file.write(iY.to_bytes(2, self.config['byteorder']))

        self.progress_bar_label.setVisible(True)
        self.progress_bar.setVisible(True)
        with ThreadPoolExecutor() as executor:
            self.progress_bar.setValue(0)
            threads = []
            for i in range(1, depth):
                data = image[:, :, i].flatten('C')
                threads.append(executor.submit(self.encoderDict[method], data=data))
            data = image[:, :, 0].flatten('C')    
            file.write(self.encoderDict[method](data, progress_bar=self.progress_bar))
            for i in threads:
                file.write(i.result())
                
        self.progress_bar.setVisible(False)
        self.progress_bar_label.setVisible(False)
        print('compression sucessful')
        file.close()
    
    def decompress_my_image(self):
        self.progress_bar_label.setVisible(True)
        self.progress_bar.setVisible(True)

        file = open(self.selected_image, 'rb')
        method = int.from_bytes(file.read(1), byteorder=self.config['byteorder'], signed=False)

        iX = int.from_bytes(file.read(2), byteorder=self.config['byteorder'], signed=False)
        iY = int.from_bytes(file.read(2), byteorder=self.config['byteorder'], signed=False)
        im_string = asarray(self.decoderDict[method](file.read()), dtype=np.uint8)
        depth = len(im_string)//(iY*iX)
        print(f'{iX}x{iY}px with a total of {len(im_string)}')
        decoded_image = np.zeros((iY, iX, depth), dtype=np.uint8)
        for i in range(depth):
            decoded_image[:, :, i] = im_string[iY*iX*i:iY*iX*(i+1)].reshape(iY, iX)
        

        file.close()
        pil_image = Image.fromarray(decoded_image).convert('RGB')
        self.progress_bar_label.setVisible(False)
        self.progress_bar.setVisible(False)
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
    
    def show_entropy(self):
        self.entropy_txt.setVisible(True)
        
        image = asarray(self.selected_image) # (height, width, depth)
        if  len(image.shape) == 2:
            image.resize(image.shape[1], image.shape[0], 1)
        [iY, iX, depth] = image.shape

        self.progress_bar_label.setVisible(True)
        self.progress_bar.setVisible(True)
        entropies = None
        with ThreadPoolExecutor() as executor:
            self.progress_bar.setValue(0)
            threads = []
            for i in range(1, depth):
                data = image[:, :, i].flatten('C')
                threads.append(executor.submit(get_all_entropies, data=data))
            data = image[:, :, 0].flatten('C')    
            entropies = get_all_entropies(data)
            for i in threads:
                entropies = list(map(lambda x: entropies[x] + i.result()[x], range(len(entropies))))
                
        self.progress_bar.setVisible(False)
        self.progress_bar_label.setVisible(False)
        print('analysis sucessful')
        
        base_entropy, RLE_entropy, DC_entropy, DC_RLE_entropy = entropies
        text = 'Entropia de la imatge (/100.000): \nSense comprimir: {base_entropy:.0f} \nRLE: {RLE_entropy:.0f} \n CD: {DC_entropy:.0f}\n DC + RLE: {DC_RLE_entropy:.0f}'
        self.entropy_txt.setPlainText(text.format(base_entropy=base_entropy*10e-5, RLE_entropy=RLE_entropy*10e-5, DC_entropy=DC_entropy*10e-5, DC_RLE_entropy=DC_RLE_entropy*10e-5))

class progress_bar():
    def __init__(self, bar, thread_count):
        self.bar = bar
        self.threads = [0] * thread_count
        self.progress = 0

    def update_progress(self, new_progress, thread):
        self.threads[thread] = new_progress
        if thread == 0:
            self.bar.setValue(int(min(self.threads) * 100))
            print(int(min(self.threads) * 100))
        #set progress to min(self.threads)

if __name__ == '__main__':
    app = QApplication([])
    GUI = Main_Form()
    GUI.show()
    sys.exit(app.exec_())