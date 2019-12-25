from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMessageBox, QDesktopWidget, QFileDialog, QApplication, QMainWindow, QTabWidget, \
    QListWidget, QHBoxLayout, QWidget, QPushButton, QLabel, QComboBox
from PyQt5.Qt import QTextEdit


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

    def newWindowUI(self):
        self.setWindowTitle("Generate Key")

        # 窗口
        self.resize(500, 300)

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

        # 保存方法
        # def bt_save(self):
        # filename=QFileDialog.getSaveFileName(self,'save file','C:\\')
        # with open(filename[0],'w') as f:
        # my_text=self.text.toPlainText()
        # f.write(my_text)

        self.show()

    def genKey(self):
        self.publicTextbox.setPlainText('123')
        self.privateTextbox.setPlainText('456')

    def keySave(self, fileName):
        if fileName.startswith('PublicKey'):
            file_txt = self.publicTextbox.toPlainText()
        if fileName.startswith('PrivateKey'):
            file_txt = self.privateTextbox.toPlainText()
        if not file_txt:
            msg = QMessageBox()
            msg.setWindowTitle('提示')
            msg.setText('请先生成密钥！')
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
            msg.setText('生成密钥成功！')
            msg.exec_()


