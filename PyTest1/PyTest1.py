a = 'hola, mundo!'
a[0]
# from math import log2
# from msilib.schema import Directory
# from stat import filemode
# import sys
# from tkinter import dialog
# from PyQt5 import uic
# from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog

# from random import randint

# class GUI1(QWidget):
#     def __init__(self):
#         super().__init__()
#         uic.loadUi('PyTest1\\test.ui', self)
#         self.inputBtn.clicked.connect(self.get_file)
#         self.createBtn.clicked.connect(self.generate_file)
#         self.testBtn.clicked.connect(self.test)

#         self.editTxt.setPlainText(str(randint(0,255)))
        
    
#     def get_file(self):
#         file = open(QFileDialog.getOpenFileName(self, 'YEAH')[0], 'br')
#         st = file.read()
#         print(int.from_bytes(st, byteorder='big', signed=False))
#         file.close()

#     def generate_file(self):
#         p = QFileDialog.getOpenFileName(self, 'YEAH')[0];
#         if p=='':
#             return
#         file = open(p, 'bw')
#         n = int(self.editTxt.toPlainText())
#         print(n.to_bytes(int(log2(n)//8+1), 'big', signed=True))
#         file.write(n.to_bytes(int(log2(n)//8+1), 'big'))
#         file.close()

#     def test(self):
#         n = int(self.editTxt.toPlainText())
#         print(f'necesitas {int(log2(n)//8+1)} bytes. ')
#         res = n.to_bytes(int(log2(n)//8+1), 'big')
#         print(f'resultado: {res}')


# app = QApplication([])
# GUI = GUI1()
# GUI.show()
# sys.exit(app.exec_())

# # # Seleccionar un directorio
# # dlg = QFileDialog()
# # dlg.setFileMode(2)
# # if (dlg.exec()):
# #     files = dlg.selectedFiles()
# #     print(files)

# # def read_number_from_file(self):
# #         file = open(QFileDialog.getOpenFileName(self, 'YEAH')[0], 'br')
# #         st = file.read()
# #         print(int.from_bytes(st, byteorder='big', signed=False))
# #         file.close()

# def test(self):
#         # Get image
#         im = asarray(Image.open(self.get_new_file_location(custom_extension=False)))
#         if  len(im.shape) == 2:
#             im.resize(im.shape[1], im.shape[0], 1)
#         [iY, iX, depth] = im.shape

#         # Encode image
#         eres = bytes()
#         threads = []
#         with ThreadPoolExecutor() as executor:
#             for i in range(depth):
#                 data = im[:, :, i].flatten('C')
#                 threads.append(executor.submit(RLE_encode, data))
            
#             for i in threads:
#                 eres += i.result()
        
#         # Decode image (eres)
#         dres = asarray(RLE_decode(eres), dtype=np.uint8)
#         dim = np.zeros((iY, iX, len(dres)//(iY*iX)))
#         for i in range(depth):
#             dim[:, :, i] = dres[iY*iX*i:iY*iX*(i+1)].reshape(iY, iX)
#         dim = dim.astype(np.uint8)
        
#         # dim = DECODED_IMAGE!!!!
#         # Tests
#         fdim = dim.astype(np.uint8).flatten('C')
#         fim = im.astype(np.uint8).flatten('C')
#         for i in range(len(fim)):
#             if fim[i] != fdim[i]:
#                 print('WRONG!!')
#         print(np.array_equal(im, dim))
#         print(np.array_equal(im, dim))

#         arim = Image.fromarray(dim).convert('RGB')
#         qim = ImageQt(arim)
#         pixmap = QPixmap.fromImage(qim)
#         h = pixmap.height() / self.image_label.height()
#         w = pixmap.width() / self.image_label.width()
#         if h > w:
#             pixmap = pixmap.scaledToHeight(self.image_label.height())
#         else:
#             pixmap = pixmap.scaledToWidth(self.image_label.width())
#         self.image_label.setPixmap(pixmap)
#         print('ahora si, ¿no?')
