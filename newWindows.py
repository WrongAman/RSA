import sys
import time, datetime
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QWidget, QPushButton, QLabel, QComboBox, QMessageBox, QTextEdit,\
QLineEdit
from PyQt5.Qt import QTextEdit
import base64
from PyQt5.QtCore import pyqtSignal

class genWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.publicTextbox = QTextEdit(self)
        self.privateTextbox = QTextEdit(self)
        self.publicTextbox.setReadOnly(True)
        self.privateTextbox.setReadOnly(True)
        self.cb = QComboBox(self)
        self.genButton = QPushButton('Generate', self)
        self.public_button = QPushButton('Save', self)
        self.private_button = QPushButton('Save', self)
        self.measure_time = ''
        
        self.newWindowUI()

    def newWindowUI(self):
        self.setWindowTitle("Generate Key")

        # 公钥文本框
        label1 = QLabel(self)
        label1.move(15, 27)
        label1.setText('Public Key')
        self.publicTextbox.move(15, 50)
        self.publicTextbox.resize(180, 200)

        # 密钥文本框
        label2 = QLabel(self)
        label2.move(220, 27)
        label2.setText('Private Key')
        self.privateTextbox.move(210, 50)
        self.privateTextbox.resize(180, 200)

        # 单选框
        self.cb.move(405, 80)
        self.cb.resize(80, 30)
        self.cb.addItem('1024')
        self.cb.addItem('2048')
        self.cb.addItem('4096')
        cb_label = QLabel(self)
        cb_label.setText('Key bits:')
        cb_label.move(405, 50)
        cb_label.resize(80, 30)

        # 生成按钮
        self.genButton.move(405, 130)
        self.genButton.resize(80, 30)
        self.genButton.clicked.connect(self.genKey)

        # 保存公钥
        self.public_button.move(15, 260)
        self.public_button.resize(80, 30)
        self.public_button.clicked.connect(lambda: self.keySave('PublicKey'))

        # 保存私钥
        self.private_button.move(210, 260)
        self.private_button.resize(80, 30)
        self.private_button.clicked.connect(lambda: self.keySave('PrivateKey'))

        # 生成时间计算
        label3 = QLabel(self)
        label3.setText('Elapsed Time:')
        label3.move(405, 170)
        label3.resize(80, 30)
        self.label4 = QLabel(self)
        self.label4.setFixedWidth(80)
        self.label4.move(405, 200)

        # 窗口不可缩放
        self.setFixedSize(500, 300)
        self.show()

    # 生成密钥
    def genKey(self):
        # 时间戳开始时间
        startTime = time.time()
        n = int(self.cb.currentText())
        rsa = RSA.generate(n, Random.new().read)

        # 生成私钥
        self.private_pem = rsa.exportKey()
        private_key = self.private_pem.decode()

        # 生成公钥
        self.public_pem = rsa.publickey().exportKey()
        public_key = self.public_pem.decode()

        # 显示公钥有和私钥
        self.publicTextbox.setPlainText(public_key)
        self.privateTextbox.setPlainText(private_key)

        # 时间戳结束时间        
        endTime = time.time()
        self.measure_time = str(round((endTime - startTime), 6))
        self.label4.setText(self.measure_time + 's')

    # 保存密钥
    def keySave(self, fileName):
        if fileName.startswith('PublicKey'):
            file_txt = self.publicTextbox.toPlainText()
            key = self.public_pem
        if fileName.startswith('PrivateKey'):
            file_txt = self.privateTextbox.toPlainText()
            key = self.private_pem
        if not file_txt:
            msg = QMessageBox()
            msg.setWindowTitle('提示')
            msg.setText('请先生成密钥！')
            msg.exec_()
        else: 
            filename, filetype = QFileDialog.getSaveFileName(self,
                                                             "保存文件",
                                                             fileName,
                                                             "Text Files (*.pem)")
            if not filename:
                return
            with open(filename, 'wb') as f:
                f.write(key)
            msg = QMessageBox()
            msg.setWindowTitle('成功')
            msg.setText('生成密钥成功！')
            msg.exec_()


class cipherWindow(QWidget):
    

    def  __init__(self, text=''):
        super().__init__()
        self.text = text
        # 窗口不可缩放
        self.setFixedSize(500, 110)
        self.cipherWindowUI()

        

    def cipherWindowUI(self):
        self.setWindowTitle('Encode')
        
        # 导入公钥窗口
        import_label = QLabel(self)
        import_label.move(35, 20)
        import_label.resize(175,20)
        import_label.setText('Please import the public key:')
        
        # 显示路径
        self.import_address = QLabel(self)
        self.import_address.move(35,55)
        self.import_address.resize(400,20)

        # 导入公钥
        import_button = QPushButton('import', self)
        import_button.move(235, 20)
        import_button.resize(45,20)
        import_button.clicked.connect(self.uploadKey)
        
        # 加密
        encode_button = QPushButton('encode', self)
        encode_button.move(300,20)
        encode_button.resize(45,20)
        encode_button.clicked.connect(self.rsaEncode)
        
        self.show()

    # 导入pem文件    
    def uploadKey(self):
        file_name, filetype = QFileDialog.getOpenFileName(self,
                                                             "打开文件",
                                                             "C://",
                                                              "Text Files (*.pem)")
        self.import_address.setText(file_name)
        if file_name == "":
            return 
        with open(file_name, 'r') as f:
            self.key = f.read()
            self.rsakey = RSA.importKey(self.key)
            self.cipher = Cipher_pkcs1_v1_5.new(self.rsakey)
        
    def rsaEncode(self):
        self.mySignal = pyqtSignal()
        message = self.text
        self.cipher_text = base64.b64encode(self.cipher.encrypt(message.encode(encoding="utf-8")))
        print(self.cipher_text)
        self.mySignal.emit("hello")
        self.close()
