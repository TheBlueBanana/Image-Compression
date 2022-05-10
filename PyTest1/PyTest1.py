from math import log2
from msilib.schema import Directory
from stat import filemode
import sys
from tkinter import dialog
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog

from random import randint

class GUI1(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('test.ui', self)
        self.inputBtn.clicked.connect(self.get_file)
        self.createBtn.clicked.connect(self.generate_file)
        self.testBtn.clicked.connect(self.test)

        self.editTxt.setPlainText(str(randint(0,255)))
        
    
    def get_file(self):
        file = open(QFileDialog.getOpenFileName(self, 'YEAH')[0], 'br')
        st = file.read()
        print(int.from_bytes(st, byteorder='big', signed=False))
        file.close()

    def generate_file(self):
        p = QFileDialog.getOpenFileName(self, 'YEAH')[0];
        if p=='':
            return
        file = open(p, 'bw')
        n = int(self.editTxt.toPlainText())
        print(n.to_bytes(int(log2(n)//8+1), 'big', signed=True))
        file.write(n.to_bytes(int(log2(n)//8+1), 'big'))
        file.close()

    def test(self):
        n = int(self.editTxt.toPlainText())
        print(f'necesitas {int(log2(n)//8+1)} bytes. ')
        res = n.to_bytes(int(log2(n)//8+1), 'big')
        print(f'resultado: {res}')


app = QApplication([])
GUI = GUI1()
GUI.show()
sys.exit(app.exec_())

# # Seleccionar un directorio
# dlg = QFileDialog()
# dlg.setFileMode(2)
# if (dlg.exec()):
#     files = dlg.selectedFiles()
#     print(files)

# def read_number_from_file(self):
#         file = open(QFileDialog.getOpenFileName(self, 'YEAH')[0], 'br')
#         st = file.read()
#         print(int.from_bytes(st, byteorder='big', signed=False))
#         file.close()