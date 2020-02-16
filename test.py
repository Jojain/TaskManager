import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt





class DeleteTaskWindow(QtWidgets.QWidget):
    """
    Fenêtre qui s'ouvre lorsque l'on clique sur le bouton gauche du DayWidget
    permet de supprimer des tâches
    """
    def __init__(self,parent=None):
        super().__init__()
        btn = ColoredBtn(self)

class ColoredBtn(QtWidgets.QPushButton):
    """
  
    """
    def __init__(self,parent=None):
        super().__init__(parent)
        self.resize(300,300)
        self.setup()
        self.move(60,60)

    def setup(self):
        # self.setStyleSheet(" background-color: white;\
        #                     border-style: solid; \
        #                     border-width:10px;\
        #                     border-radius:25px;\
        #                     border-color: green;\
        #                     max-width:100px;\
        #                     max-height:100px;\
        #                     min-width:100px;\
        #                     min-height:100px;")
        canvas = QtGui.QPixmap(100,100)
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen()
        pen.setColor = "blue"
        painter.setPen(pen)
        painter.drawLine(0,0,50,50)
        painter.end()
        icon = QtGui.QIcon(canvas)
        
        self.setIcon(icon)



        





app = QtWidgets.QApplication(sys.argv)
window = DeleteTaskWindow()
window.show()
app.exec_()

