from PyQt5 import QtWidgets, QtGui, QtCore
from global_functions import click_is_inside_widget
import sys

class mw(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        holder = test()
        self.setCentralWidget(holder)
        for i in range(DetailedDayWidget.HOURS_DISPLAYED):
            starting_height =  height-task_background_height
            current_height = starting_height + i*hour_spacing
            h = 7+i
            hour = f"{h}h00"
            

            if i == 0 :              
                pen.setWidth(1)
                pen.setStyle(QtCore.Qt.DotLine)
                painter.setPen(pen)

                painter.drawLine(x_offset + hour_x_offset, current_height + hour_spacing/2, width + x_offset , current_height + hour_spacing/2)
                pen.setStyle(QtCore.Qt.SolidLine)                
                painter.setPen(pen)            

            else:
                location = QtCore.QPointF(hour_x_offset/2, current_height-1)
                text_rect = QtCore.QRectF(0,0,hour_x_offset,10)                
                text_rect.moveCenter(location)

                painter.drawText(text_rect, QtCore.Qt.AlignCenter, hour )
                painter.drawLine(x_offset + hour_x_offset, current_height, width + x_offset , current_height)                
                pen.setStyle(QtCore.Qt.DotLine)
                painter.setPen(pen)
                painter.drawLine(x_offset + hour_x_offset, current_height + hour_spacing/2, width + x_offset , current_height + hour_spacing/2)
                pen.setStyle(QtCore.Qt.SolidLine)
                painter.setPen(pen)
                


        painter.end()        
        self.background.setPixmap(canvas)
        self.global_layout.addWidget(self.background)
        
        
if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    main_window = mw()
    main_window.show()
    sys.exit(application.exec_())

