from PyQt5.QtWidgets import QTextEdit, QFileDialog


def sub():
    Editor.NextId -= 1


class Editor(QTextEdit):
    NextId = 1

    def __init__(self, fileName=""):
        super().__init__()
        self.fileName = fileName
        if not self.fileName:
            self.fileName = "Unnamed-{0}.txt".format(
                Editor.NextId)
            Editor.NextId += 1

    def load(self):
        with open(self.fileName, 'r') as f:
            file_txt = f.read()
            self.setPlainText(file_txt)

    def save(self):
        if self.fileName.startswith("Unnamed"):
            fileName, fileType = QFileDialog.getSaveFileName(self,
                                                             "保存文件",
                                                             self.fileName,
                                                             "Text Files (*.txt)")
            if not fileName:
                return False
            self.fileName = fileName

        with open(self.fileName, 'w') as f:
            file_txt = self.toPlainText()
            f.write(file_txt)

        return True
