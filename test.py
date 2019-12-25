import sys
import Edit
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMessageBox, QDesktopWidget, QFileDialog, QApplication, QMainWindow, QTabWidget, \
    QListWidget, QHBoxLayout, QWidget, QTextEdit, QVBoxLayout, QLabel


class MainUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.tabWidget = QTabWidget(self)
        self.listWidget = QListWidget(self)
        self.textArea = QTextEdit(self)
        self.textArea.setReadOnly(True)
        self.initUI()

    def initUI(self):

        # 定义事件相关

        """新建文本文件"""
        newAction = QAction(QIcon('img/new.png'), 'New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New File')
        newAction.triggered.connect(self.new_file)

        """打开文本文件"""
        openAction = QAction(QIcon('img/open.png'), 'Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open File')
        openAction.triggered.connect(self.slot_btn_chooseFile)

        """保存文本文件"""
        saveAction = QAction(QIcon('img/new.png'), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save File')
        saveAction.triggered.connect(self.saveFile)

        """剪切"""
        cutAction = QAction(QIcon('img/new.png'), 'Cut', self)
        cutAction.setShortcut('Ctrl+X')
        cutAction.setStatusTip('Cut File')
        cutAction.triggered.connect(self.saveFile)

        """复制"""
        copyAction = QAction(QIcon('img/new.png'), 'Copy', self)
        copyAction.setShortcut('Ctrl+C')
        copyAction.setStatusTip('Copy File')
        copyAction.triggered.connect(self.saveFile)

        """退出程序"""
        exitAction = QAction(QIcon('img/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(self.close)

        # 菜单栏设置
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)
        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(cutAction)
        editMenu.addAction(copyAction)

        # 工具栏设置
        sysToolbar = self.addToolBar('SYSTEM')
        sysToolbar.addAction(newAction)
        sysToolbar.addAction(openAction)
        sysToolbar.addAction(saveAction)
        editToolbar = self.addToolBar('EDIT')
        editToolbar.addAction(cutAction)
        editToolbar.addAction(copyAction)
        exitToolbar = self.addToolBar('EXIT')
        exitToolbar.addAction(exitAction)

        # 状态栏设置
        status = self.statusBar()
        status.setSizeGripEnabled(True)
        status.showMessage("Ready", 5000)

        # 控件设置
        self.listWidget.doubleClicked.connect(self.doubleClick)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        secretLable = QLabel("密文:", self)

        # 布局

        """全局布局"""
        main_layout = QHBoxLayout()
        """局部布局"""
        right_layout = QVBoxLayout()
        """设置局部布局"""
        right_layout.addWidget(self.tabWidget)
        right_layout.addWidget(secretLable)
        right_layout.addWidget(self.textArea)
        right_layout.setStretch(0, 2)
        right_layout.setStretch(2, 1)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        """设置全局布局"""
        main_layout.addWidget(self.listWidget)
        main_layout.addWidget(right_widget)
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 3)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # 窗口
        self.resize(1000, 500)
        self.center()
        self.setWindowTitle("RSATools")
        self.setWindowIcon(QIcon('img/test.png'))
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        # 获取窗口
        qr = self.frameGeometry()
        # 获取中心点
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def slot_btn_chooseFile(self):
        fileName_choose, fileType = QFileDialog.getOpenFileName(self,
                                                                "选取文件",  # 对话框标题
                                                                "C:/",  # 起始路径
                                                                "Text Files (*.txt)")  # 设置文件扩展名过滤

        if fileName_choose:
            for i in range(self.tabWidget.count()):
                textEdit = self.tabWidget.widget(i)
                if textEdit.fileName == fileName_choose:
                    self.tabWidget.setCurrentWidget(textEdit)
                    break
            else:
                self.loadFile(fileName_choose)

    def loadFile(self, fileName):
        textEdit = Edit.Editor(fileName)
        try:
            textEdit.load()
        except EnvironmentError as e:
            QMessageBox.warning(self,
                                "Tabbed Text Editor -- Load Error",
                                "Failed to load {0}: {1}".format(fileName, e))
            textEdit.close()
            del textEdit
        else:
            self.tabWidget.addTab(textEdit, textEdit.fileName)
            self.tabWidget.setTabsClosable(True)
            self.tabWidget.setCurrentWidget(textEdit)
            self.listWidget.addItem(textEdit.fileName)

    def new_file(self):
        textEdit = Edit.Editor()
        self.tabWidget.addTab(textEdit, textEdit.fileName)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setCurrentWidget(textEdit)
        self.listWidget.addItem(textEdit.fileName)

    def closeTab(self):
        i = self.tabWidget.currentIndex()
        Edit.sub()
        self.tabWidget.removeTab(i)
        self.listWidget.takeItem(i)

    def saveFile(self):
        i = self.tabWidget.currentIndex()
        if i == -1:
            msg = QMessageBox()
            msg.setWindowTitle('提示')
            msg.setText('请选择一个文件进行保存')
            msg.exec_()
        else:
            textEdit = self.tabWidget.currentWidget()
            listEdit = self.listWidget.item(self.tabWidget.currentIndex())
            if textEdit.save():
                Edit.sub()
                self.tabWidget.setTabText(self.tabWidget.currentIndex(), textEdit.fileName)
                listEdit.setText(textEdit.fileName)
                msg = QMessageBox()
                msg.setWindowTitle('成功')
                msg.setText('保存成功！')
                msg.exec_()

    def doubleClick(self):
        i = self.listWidget.currentRow()
        self.tabWidget.setCurrentIndex(i)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainUI()
    sys.exit(app.exec_())
