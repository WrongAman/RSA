import sys
import time
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


class EncodeWindow(QWidget):
    

    def  __init__(self, text=''):
        super().__init__()
        self.text = text
        # 窗口不可缩放
        self.setFixedSize(500, 300)
        self.encodeWindowUI()


    def encodeWindowUI(self):
        
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

        # 保存密文
        save_ciphertext = QPushButton('save', self)
        save_ciphertext.move(365,20)
        save_ciphertext.resize(45,20)
        save_ciphertext.clicked.connect(lambda: self.cipherSave('CipherText'))

        
         # 密文文本框
        cipher_label = QLabel(self)
        cipher_label.move(35,90)
        cipher_label.resize(70,20)
        cipher_label.setText('Ciphertext: ')
        self.cipherTextBox = QTextEdit(self)
        self.cipherTextBox.move(35,125)
        self.cipherTextBox.resize(430,145)
        self.cipherTextBox.setReadOnly(True)

        self.show()

    # 导入PublicKey.pem文件    
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
    
    # 加密方法
    def rsaEncode(self):
        encode_startTime = time.time()
        
        # 明文加密过程
        message = self.text
        self.cipher_text = base64.b64encode(self.cipher.encrypt(message.encode(encoding="utf-8")))
        
        encode_endTime = time.time()
        # 获取时间戳
        self.measure_encode_time = str(round((encode_endTime - encode_startTime), 6))
        
        # 密文文本框显示密文内容
        ciphertext = self.cipher_text.decode()
        self.cipherTextBox.setPlainText(ciphertext)
        print(ciphertext)
        
        # 弹出提示窗
        msg = QMessageBox()
        msg.setWindowTitle('成功')
        msg.setText('加密成功！\n用时' + self.measure_encode_time + ' s')
        msg.exec_()

    # 保存密文
    def cipherSave(self, fileName):
        if fileName.startswith('CipherText'):
            file_txt = self.cipherTextBox.toPlainText()
            print(file_txt)
        if not file_txt:
            msg = QMessageBox()
            msg.setWindowTitle('提示')
            msg.setText('请先加密！')
            msg.exec_()
        else: 
            filename, filetype = QFileDialog.getSaveFileName(self,
                                                             "保存文件",
                                                             fileName,
                                                             "Text Files (*.txt)")
            if not filename:
                return
            with open(filename, 'w') as f:
                f.write(file_txt)
            msg = QMessageBox()
            msg.setWindowTitle('成功')
            msg.setText('保存成功！')
            msg.exec_()


class DecodeWindow(QWidget):

    def  __init__(self, text=''):
        self.text = text
        super().__init__()
        # 窗口不可缩放
        self.setFixedSize(500, 300)
        self.decodeWindowUI()


    def decodeWindowUI(self):
        self.setWindowTitle('Decode')
        
        # 导入公钥窗口
        import_label = QLabel(self)
        import_label.move(35, 20)
        import_label.resize(175,20)
        import_label.setText('Please import the private key:')
        
        # 显示路径
        self.import_address = QLabel(self)
        self.import_address.move(35,55)
        self.import_address.resize(400,20)

        # 导入公钥
        import_button = QPushButton('import', self)
        import_button.move(235, 20)
        import_button.resize(45,20)
        import_button.clicked.connect(self.uploadKey)
        
        # 解密
        encode_button = QPushButton('decode', self)
        encode_button.move(300,20)
        encode_button.resize(45,20)
        encode_button.clicked.connect(self.rsaDecode)

        # 保存明文
        save_ciphertext = QPushButton('save', self)
        save_ciphertext.move(365,20)
        save_ciphertext.resize(45,20)
        # save_ciphertext.clicked.connect(lambda: self.cipherSave('CipherText'))

        
         # 密文文本框
        plain_label = QLabel(self)
        plain_label.move(35,90)
        plain_label.resize(70,20)
        plain_label.setText('Plaintext: ')
        self.plainTextBox = QTextEdit(self)
        self.plainTextBox.move(35,125)
        self.plainTextBox.resize(430,145)
        self.plainTextBox.setReadOnly(True)

        self.show()

        # 导入PrivateKey.pem文件    
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

    def rsaDecode(self):
        decode_startTime = time.time()
        
        # 明文加密过程
        cipher_text = self.text
        self.plain_text = self.cipher.decrypt(base64.b64decode(cipher_text), "ERROR")
        
        decode_endTime = time.time()
        # 获取时间戳
        self.measure_encode_time = str(round((decode_endTime - decode_startTime), 6))
        
        # 密文文本框显示密文内容
        plaintext = self.plain_text.decode()
        self.plainTextBox.setPlainText(plaintext)
        print(plaintext)
        
        # 弹出提示窗
        msg = QMessageBox()
        msg.setWindowTitle('成功')
        msg.setText('加密成功！\n用时' + self.measure_encode_time + ' s')
        msg.exec_()

