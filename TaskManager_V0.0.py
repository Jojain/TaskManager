import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import calendar 
import datetime as dt 
import itertools
import json
from global_functions import clear_layout, click_is_inside_widget, substract_time
from popup_windows import TaskWindow, DeleteTaskWindow

class DayWidget(QtWidgets.QWidget):
    _height = 100
    _width = 150
    #Signals
    day_clicked = QtCore.pyqtSignal(object)

    def __init__(self,parent,row,col,date):
        super().__init__(parent)

        #Variables Day widget           
        self.drawing_area = QtWidgets.QLabel(self)  
        self.resize(DayWidget._width,DayWidget._height)
        self.pen_width = 3
        self.row = row
        self.col = col        
        self.date = date # donne l'année et le mois du DayWidget sous la forme : {"year" : int, "month": int}
        self.canvas = QtGui.QPixmap(DayWidget._width, DayWidget._height)     
        self.canvas.fill(QtCore.Qt.GlobalColor.transparent)   
        self.painter = QtGui.QPainter(self.canvas)
        self.painter.setRenderHint(QtGui.QPainter.Antialiasing)  
        pen = QtGui.QPen()
        pen.setWidth(self.pen_width)
        self.painter.setPen(pen)      
        self.rrect = QtGui.QPainterPath()        
        self.setup_look()
        self.setup_push_button()

        #Applique le canvas édité en arrière plan sur le DayWidget 
        #Si appliqué avant le setuplook() il faut réactualiser l'affichage
        self.drawing_area.setPixmap(self.canvas)

        self.tasks = []         
        self.load_tasks()
        self.setup_tasks_display()
        self.init_task_display()
        
        
    def setup_look(self):
        """
        Crée l'affichage du DayWidget, initialise le jour du DayWidget pour correspondre au calendrier classique,
        affiche le fond du DayWidget en gris si le DayWidget ne fait pas parti du mois sélectionné dans le calendrier.
        """
        def draw_rect(self,color,day_nb,days):   
            """
            Sous-fonction qui créée le style du DayWidget.
            """         
            self.rrect.addRoundedRect(pen_width/2,
                                      pen_width/2,
                                      self.canvas.width()-pen_width,
                                      self.canvas.height()-pen_width,
                                      15,
                                      15)

            self.painter.fillPath(self.rrect, color)
            
            self.painter.setFont(QtGui.QFont("Harlow Solid Italic",15, weight = 40))


            if self.date["month"] == 1:
                year = self.date["year"] - 1
                month = 12
            else:
                year = self.date["year"]
                month = self.date["month"]-1
            cal = calendar.Calendar()
            days_last_month = [d for d in cal.itermonthdays(year,month) if d != 0]
            
            days_numbers_last_month = []
            for index,day in enumerate(days,1):
                if day == 0:
                    days_numbers_last_month.append(days_last_month[-index])
                else:
                    break    
            days_numbers_last_month = days_numbers_last_month[::-1]
            
            if day_nb <= max(days) and days[day_nb-1] == 0 :                
                nb = days_numbers_last_month[day_nb-1]
                self.nb = nb                
                self.painter.drawText(0,
                                      0,
                                      self.canvas.width(),
                                      self.canvas.height(),
                                      QtCore.Qt.AlignHCenter,
                                      str(nb))                
            elif day_nb-len(days_numbers_last_month) <= max(days):
                self.nb = day_nb-(len(days_numbers_last_month))
                self.painter.drawText(0,
                                      0,
                                      self.canvas.width(),
                                      self.canvas.height(),
                                      QtCore.Qt.AlignHCenter,
                                      str(day_nb-len(days_numbers_last_month)))
            else:
                self.nb = day_nb-len(days_numbers_last_month)-max(days)
                self.painter.drawText(0,
                                      0,
                                      self.canvas.width(),
                                      self.canvas.height(),
                                      QtCore.Qt.AlignHCenter,
                                      str(day_nb-len(days_numbers_last_month)-max(days)))
            self.painter.drawPath(self.rrect)     

        ##############
        cal = calendar.Calendar()
        days = [d for d in cal.itermonthdays(self.date["year"],self.date["month"])]
        pen_width = self.pen_width
        day_nb = self.col+7*self.row
        
        try:
            
            if days[day_nb-1] == 0:
                draw_rect(self,QtCore.Qt.gray,day_nb,days)
            else :  
                draw_rect(self,QtCore.Qt.white,day_nb,days)
                
        except IndexError:
                draw_rect(self,QtCore.Qt.gray,day_nb,days)

    def setup_push_button(self):
        """
        Créer le bouton qui permet d'ajouter des tâches au DayWidget
        """
        
        #Déclaration du button d'ajoute de tâche
        self.button_task = QtWidgets.QPushButton(self)
        self.button_task.setIcon(QtGui.QIcon(r"D:\Projets_Python\Icones\batch-master\PNG\32x32\add"))
        self.button_task.resize(20,20)
        self.button_task.move(DayWidget._width-35,5)
        self.button_task.clicked.connect(self.open_task_window)

        self.delete_task_btn = QtWidgets.QPushButton(self)
        self.delete_task_btn.resize(20,20)
        self.delete_task_btn.move(10,5)
        self.delete_task_btn.clicked.connect(self.open_delete_task_window)

    def load_tasks(self):
        """
        Charge les tâches à partir d'un fichier et créé les objets task ( des QLabel ) pour le calendrier
        """
        #On défini l'année, le mois et le jour du DayWidget pour récupérer les tâches
        # enregistrée dans le JSON, le numéro du jour correspond au numéro du widget dans le mois
        # c'est à dire un entier entre 1 et 42 (car il y a 42 widget par MonthWidget)
        year = str(self.date["year"])
        month = str(self.date["month"])
        day = str(7*self.row + self.col)

        with open("tasks_file.json","r") as json_file:
            tasks_data = json.load(json_file)            
            self.tasks = [task for task in tasks_data[year][month][day]]
        
    def save_tasks(self):
        """
        Fonction qui enregistre les tâches dans le json
        """
        year = str(self.date["year"])
        month = str(self.date["month"])
        day = str(7*self.row + self.col)

        with open("tasks_file.json","r") as json_file:
            old_json = json.load(json_file)

            #On réinitialise les tâches du DayWidget sans supprimer les tâches des autres DayWidgets
            old_json[year][month][day] = []

        with open("tasks_file.json","w") as updated_json_file:            
            for task in self.tasks:
                old_json[year][month][day].append(task)
            json.dump(old_json,updated_json_file, indent= 4, sort_keys= True)

    def add_task(self):
        """
        Ajoute une tâche à la liste des tâches du DayWidget
        """
        self.tasks.append({"name":"test"})

    def init_task_display(self):
        for task in self.tasks:                
            #Définition des dimensions du tasklabel
            bg_rect_w = DayWidget._width - 2*(self.tasks_holder_layout.spacing() +self.pen_width)
            bg_rect_h = 20

            #Initialisation des objets de dessin     
            canvas = QtGui.QPixmap(bg_rect_w, bg_rect_h)     
            canvas.fill(QtCore.Qt.GlobalColor.transparent)
            task_display = QtWidgets.QLabel(self.tasks_holder)                
            task_display_layout = QtWidgets.QVBoxLayout(task_display)
            painter = QtGui.QPainter(canvas)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            drawing = QtGui.QPainterPath()  

            #Phase de dessin de la tâche
            background_rectangle = QtCore.QRectF(0,0,bg_rect_w,bg_rect_h)            
            drawing.addRoundedRect(background_rectangle,6,6)
            painter.fillPath(drawing, QtCore.Qt.GlobalColor.blue)

            #Application du nom de la tâche sur le fond précedemment créé
            name = QtWidgets.QLabel(task_display)                  
            name.setAlignment(QtCore.Qt.AlignCenter)
            color = "white"  # Spécifier la couleur du texte ici.
            text = f"{task['name']}"
            name.setText(f"<font color = '{color}'> {text} </font>")
   
            
            painter.end()
            
            #Applique le style/dessin à la tâche
            task_display.setPixmap(canvas)
            task_display_layout.addWidget(name)
            task_display_layout.setContentsMargins(0,0,0,0) # à revoir à ce niveau
            self.tasks_holder_layout.addWidget(task_display)      

    def open_task_window(self):
        """
        Fonction qui créer un objet TaskWindow 
        """
        self.task_window = TaskWindow(self)
        self.task_window.show()

    def open_delete_task_window(self):
        """
        Fonction qui ouvre la fênetre qui sert à supprimer les tâches
        """
        self.delete_window = DeleteTaskWindow(self)
        self.delete_window.show()

    def setup_tasks_display(self):
        """
        Affiche les tâches dans le DayWidget
        """
        self.tasks_holder = QtWidgets.QWidget(self)
        # tasks_holder.setAutoFillBackground(True)
        top_offset = 18
        self.tasks_holder.move(0,top_offset)
        self.tasks_holder.resize(DayWidget._width,DayWidget._height-top_offset)
        self.tasks_holder_layout = QtWidgets.QVBoxLayout(self.tasks_holder)
        self.tasks_holder.setLayout(self.tasks_holder_layout)
            

    def update_tasks_display(self):

        #A chaque réaffichage on réinitialise le task holder layout pour ne pas afficher plusieurs fois les mêmes tâches
        clear_layout(self.tasks_holder_layout)

        for task in self.tasks:                
            #Définition des dimensions du tasklabel
            bg_rect_w = DayWidget._width - 2*(self.tasks_holder_layout.spacing() +self.pen_width)
            bg_rect_h = 20

            #Initialisation des objets de dessin     
            canvas = QtGui.QPixmap(bg_rect_w, bg_rect_h)     
            canvas.fill(QtCore.Qt.GlobalColor.transparent)
            task_display = QtWidgets.QLabel(self.tasks_holder)                
            task_display_layout = QtWidgets.QVBoxLayout(task_display)
            painter = QtGui.QPainter(canvas)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            drawing = QtGui.QPainterPath()  

            #Phase de dessin de la tâche
            background_rectangle = QtCore.QRectF(0,0,bg_rect_w,bg_rect_h)            
            drawing.addRoundedRect(background_rectangle,6,6)
            painter.fillPath(drawing, QtCore.Qt.GlobalColor.blue)

            #Application du nom de la tâche sur le fond précedemment créé
            name = QtWidgets.QLabel(task_display)                  
            name.setAlignment(QtCore.Qt.AlignCenter)
            color = "white"  # Spécifier la couleur du texte ici.
            text = f"{task['name']}"
            name.setText(f"<font color = '{color}'> {text} </font>")
   
            
            painter.end()
            
            #Applique le style/dessin à la tâche
            task_display.setPixmap(canvas)
            task_display_layout.addWidget(name)
            task_display_layout.setContentsMargins(0,0,0,0) # à revoir à ce niveau
            self.tasks_holder_layout.addWidget(task_display)    

    def mousePressEvent(self,event):    
        """
        Si un jour du calendrier est cliqué : on envoi les tâches via un signal
        """
        if click_is_inside_widget(self,event):
            
            self.day_clicked.emit(self)
            

        


class MonthWidget(QtWidgets.QWidget):

    def __init__(self,parent,date):
        super().__init__(parent)
        h = DayWidget._height
        w = DayWidget._width
        today = dt.date.today().day

        days = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
               
        days_labels = []
        

        self.grid = [[DayWidget(self,row,col,date) for col in range(1,8)] for row in range(6)]
        for h_index,week in enumerate(self.grid):
            for w_index,day in enumerate(week):
                if h_index == 1 :
                    label = QtWidgets.QLabel(self)
                    label.setText(days[w_index])
                    label.resize(w,20) #Dimension écrite en brute à modifier
                    label.setAlignment(QtCore.Qt.AlignHCenter)
                    label.move(w_index*(w-pen_width),3)                    
                    days_labels.append(label)
                if day.nb == today:
                    self.current_day_widget = day
                    self.day_position = w_index #récupère la position du jour pour savoir si c'est un lundi, mardi, mercerdi,etc.
                pen_width = day.pen_width                
                day.move(w_index*(w-pen_width),h_index*(h-pen_width)+20) #Dimension écrite en brute à modifier doit être la même que celle au dessus
              
        self.show()

class TabMonths(QtWidgets.QTabWidget):
    def __init__(self,parent):
        super().__init__(parent)
        
        tabs = []
        months = ["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre",
                  "Octobre","Novembre","Décembre"]
        for month_index,month in enumerate(months,1):
            date = {"year": 2020}
            date["month"] = month_index
            month_widget = MonthWidget(self,date)
            
                       
            self.addTab(month_widget,month)

        today = dt.date.today()
        self.setCurrentIndex(today.month-1)
        self.current_month = self.currentWidget()
        
     

class DetailedDayWidget(QtWidgets.QWidget):
    TASK_WIDTH = 415
    TASK_HEIGHT = 715
    HOURS_DISPLAYED = 18

    def __init__(self,*args):
        super().__init__(args[0])
        self.days = { 0 : "Lundi",
                      1 : "Mardi",
                      2 : "Mercredi",
                      3 : "Jeudi",
                      4 : "Vendredi",
                      5 : "Samedi",
                      6 : "Dimanche"}

        
        self.resize(DetailedDayWidget.TASK_WIDTH,DetailedDayWidget.TASK_HEIGHT)
        self.pen_width = 3
        self.global_layout = QtWidgets.QVBoxLayout(self)
        self.tab_calendar_widget = args[1]
        self.tasks = self.tab_calendar_widget.current_month.current_day_widget.tasks        
        self.day = self.tab_calendar_widget.current_month.day_position
        self.current_day_widget_displayed = self.tab_calendar_widget.current_month.current_day_widget
        
        self.setup_backgroup()        
        self.setup_header()
        self.tasks_labels = []  
        # self.update_foreground()

    
    def update_foreground(self,day_clicked):
        #Update header
        day_number = day_clicked.nb
        self.update_header(day_number)
        tasks = day_clicked.tasks  

        if day_clicked != self.current_day_widget_displayed:
            for task_displayed in self.tasks_labels:
                task_displayed.deleteLater()

            self.tasks_labels = []  
        
        for task in tasks :
            label =  QtWidgets.QLabel(self.background) #Si ca bug (s'affiche pas) mettre self.label ici   
            self.tasks_labels.append(label)         
            style_sheet = "background-color : blue; border : 1px solid black; border-radius : 8px"
            label.setStyleSheet(style_sheet)                
           
            title = task["name"]
            details = task["details"]
            text = f'<font color = "white" ><b><center>{title}</center></b></font-color><br><center>{details}</center>'
            label.setText(text)            
            minute_spacing = self.hour_spacing/60
            
            b_time = dt.time(*task["time"][0])
            e_time = dt.time(*task["time"][1])
           
            task_length = substract_time(b_time, e_time)
            label_height = minute_spacing * task_length
            x = self.background.width() - self.hour_x_offset - 4*self.pen_width
            label.resize(x-3,label_height)

            

            label.move(self.hour_x_offset,self.starting_height + (b_time.hour - 7) * self.hour_spacing + b_time.minute * minute_spacing)
            label.show()
            # x_pos = self.x_offset

        self.current_day_widget_displayed = day_clicked


    def update_header(self, day_number):
        
        day_to_display = f"{self.days[self.day]}  {day_number}"
        self.header.setText(day_to_display)

    def setup_header(self):
        """
        Fonction qui initialise l'en tête du DetailedDayWidget avec le jour actuel
        """
        date = dt.date.today()
        self.header = QtWidgets.QLabel(self.background)
        day_to_display = f"{self.days[self.day]}  {str(self.tab_calendar_widget.current_month.current_day_widget.nb)}"    
        self.header.setText(day_to_display)
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setStyleSheet(' color : red ; font-size : 28px; font-family: "Haettenschweiler"')
        self.header.resize(DetailedDayWidget.TASK_WIDTH - self.pen_width*4 ,self.starting_height)        



    def setup_backgroup(self):
        """
        Fonction qui initialise le fond du DetailedDayWidget.
        L'initialisation prend en compte tous les objets tracés via le QPainter ainsi que le texte des heures
        """

        #Initialisation des variables
        self.background = QtWidgets.QLabel(self)  
        self.background.setFixedSize(DetailedDayWidget.TASK_WIDTH,DetailedDayWidget.TASK_HEIGHT)               
        canvas = QtGui.QPixmap(DetailedDayWidget.TASK_WIDTH,DetailedDayWidget.TASK_HEIGHT)      #Changer la taille de canvas pour agrandir le widget
        canvas.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(canvas)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)  
        pen = painter.pen()
        pen.setWidth(self.pen_width)
        painter.setPen(pen)

        width = 400
        height = 700
        x_offset = pen.width()/2
        
        y_offset = pen.width()/2
        hour_x_offset = 50  
        self.hour_x_offset = hour_x_offset

        task_background_height = 0.9 * height        
        self.x_offset = x_offset + hour_x_offset
        

        painter.drawRoundedRect(x_offset,y_offset,width,height,15,15)
        painter.drawLine(x_offset,0.1* height, width + x_offset, 0.1* height)

        #Découpage de l'espace des tâches en nombre d'heure spécifique
        hour_spacing = task_background_height / (DetailedDayWidget.HOURS_DISPLAYED - 1)   
        self.hour_spacing = hour_spacing   # On sauvegarde la valeur du hour spacing pour pouvoir savoir ou positionner les tâches du DayWidget
        starting_height =  height-task_background_height
        self.starting_height = starting_height # Même chose que pour l'hour spacing
        current_hour_height = starting_height
        current_half_hour_height = starting_height

        #Tracé des pointillés demi-heures
        for i in range(1,(DetailedDayWidget.HOURS_DISPLAYED)*2-1):
            current_half_hour_height += hour_spacing/2
            if i%2 != 0 : # On ne trace qu'une ligne sur deux pour ne pas tracer de pointillés sur le traits des heures               
                pen.setWidth(1)
                pen.setStyle(QtCore.Qt.DotLine)
                painter.setPen(pen)
                painter.drawLine(x_offset + hour_x_offset, current_half_hour_height, width - x_offset , current_half_hour_height)

        #Tracé des traits heures et textes heures
        for i in range(1,DetailedDayWidget.HOURS_DISPLAYED-1):
            current_hour_height += hour_spacing
            h = 24 - DetailedDayWidget.HOURS_DISPLAYED+1 + i
            hour = f"{h}h00"

            pen.setStyle(QtCore.Qt.SolidLine)                
            painter.setPen(pen) 
            location = QtCore.QPointF(hour_x_offset/2, current_hour_height-1)
            text_rect = QtCore.QRectF(0,0,hour_x_offset,10)                
            text_rect.moveCenter(location)
            painter.drawText(text_rect, QtCore.Qt.AlignCenter, hour)
            painter.drawLine(x_offset + hour_x_offset, current_hour_height, width + x_offset , current_hour_height)  
            
            


        painter.end()        
        self.background.setPixmap(canvas)
        self.global_layout.addWidget(self.background)
        
        

class TaskMasterMainWindow(QtWidgets.QMainWindow):
    def __init__(self,*args,**kwargs):
        super(TaskMasterMainWindow,self).__init__(*args,**kwargs)    
        self.setWindowTitle('TaskMaster')


        central_widget = QtWidgets.QWidget(self)  
        central_widget_layout = QtWidgets.QHBoxLayout()

        calendar = TabMonths(self)
        central_widget_layout.addWidget(calendar)
        detailed_day = DetailedDayWidget(self,calendar)
        central_widget_layout.addWidget(detailed_day)    
        central_widget.setLayout(central_widget_layout)

        for i in range(calendar.count()):
            month = calendar.widget(i)
            list_of_day_widget = list(itertools.chain.from_iterable(month.grid))
            for day_widget in list_of_day_widget:
                day_widget.day_clicked.connect(lambda d = day_widget: detailed_day.update_foreground(d))

        self.setCentralWidget(central_widget)        



if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    main_window = TaskMasterMainWindow()
    main_window.showMaximized()
    sys.exit(application.exec_())

