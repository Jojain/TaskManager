from PyQt5 import QtWidgets, QtGui, QtCore

class TaskWindow(QtWidgets.QWidget):
    """
    Popup qui permet à l'utilisateur de renseigner une tâche avec les attributs suivant :
    - Nom
    - Date de début et fin
    - Heure à laquelle la tâche doit être effectuée 
    """
    def __init__(self,day_widget):
        super().__init__()
        self.name = ""
        self.details = ""        
        self.time = {"begin" : 0, "end" : 0}
        self.repetition = {"days" : False, "months" : False}        
        self.setup_look()        
        self.day_widget = day_widget
        self.setup_signals()
        self.setWindowTitle("Ajouter une tâche")

        
    def setup_look(self):
        #Définition des widgets
        self.name_entry = QtWidgets.QLineEdit(self)
        self.name_entry.setPlaceholderText("Entrez le nom de la tâche ici")
        self.comment_entry = QtWidgets.QLineEdit(self)
        self.comment_entry.setPlaceholderText("Ajoutez les détails de la tâche ici")
        self.comment_entry.height = 50        
        self.every_day_check_box = QtWidgets.QCheckBox(self)
        self.every_month_check_box = QtWidgets.QCheckBox(self)
        self.begin_time = QtWidgets.QTimeEdit(self)
        self.end_time = QtWidgets.QTimeEdit(self)


        #Définition des widgets containters
        entry_container = QtWidgets.QWidget(self)
        check_box_container = QtWidgets.QWidget(self)
        time_container = QtWidgets.QWidget(self)
        upper_container = QtWidgets.QWidget(self)

        entry_form_layout = QtWidgets.QFormLayout(entry_container)
        entry_form_layout.addRow("Nom",self.name_entry)
        entry_form_layout.addRow("Détails",self.comment_entry)
        
        check_box_form_layout = QtWidgets.QFormLayout(check_box_container)
        check_box_form_layout.addRow("Répéter tous les jours ?", self.every_day_check_box)
        check_box_form_layout.addRow("Répéter tous les mois ?", self.every_month_check_box)

        time_form_layout = QtWidgets.QFormLayout(time_container)
        time_form_layout.addRow("Heure de départ",self.begin_time)
        time_form_layout.addRow("Heure de fin",self.end_time)

        self.validation_btn = QtWidgets.QPushButton(self)
        self.validation_btn.setText("Valider")

        #Définition et setup des layouts
        h_layout = QtWidgets.QHBoxLayout(upper_container)
        h_layout.addWidget(entry_container)
        h_layout.addWidget(check_box_container)
        v_layout = QtWidgets.QVBoxLayout(self)
        v_layout.addWidget(upper_container)
        v_layout.addWidget(time_container)
        v_layout.addWidget(self.validation_btn)



        self.setLayout(v_layout)
        self.setFixedSize(600,300)

    def validate_task(self, day_widget):
        """
        Fonction qui récupère les infos entrées par l'utilisateur et les ajoutes à la liste des tâches du DayWidget
        """
        task = {"name" : "",
                "details": "",
                "time" : (0,0),
                "repetition" : {"days" : False ,
                                "months" : False}} 

        task["name"] = self.name_entry.text()
        task["details"] = self.comment_entry.text()
        
        if self.every_day_check_box.isChecked():
            task["repetition"]["days"] = True

        if self.every_month_check_box.isChecked():
            task["repetition"]["months"] = True

        b_hour = self.begin_time.time().hour()
        b_min = self.begin_time.time().minute()
        e_hour = self.end_time.time().hour()
        e_min = self.end_time.time().minute()
        task["time"] = ((b_hour,b_min) ,  (e_hour,e_min))          

        #Ajoute la tâche à la liste des tâches du DayWidget
        self.day_widget.tasks.append(task)        
        self.day_widget.update_tasks_display()
        self.close()

    def setup_signals(self):

        self.validation_btn.clicked.connect(self.validate_task)
        self.validation_btn.clicked.connect(self.day_widget.save_tasks)    

class DeleteTaskWindow(QtWidgets.QWidget):
    """
    Fenêtre qui s'ouvre lorsque l'on clique sur le bouton gauche du DayWidget
    permet de supprimer des tâches
    """
    def __init__(self,parent=None):
        super().__init__()
        
        
        self.day_widget = parent   
        self.tasks = parent.tasks
        self.resize(300,200)
        self.setWindowTitle("Supprimer des tâches")        
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.setup()
        self.setup_signals()
        self.show()
        
    def setup(self):
        """
        Fonction qui dispose et initialise la fenêtre
        """
        self.general_layout = QtWidgets.QVBoxLayout(self)

        self.btn_valid = QtWidgets.QPushButton(self)
        self.btn_valid.setText("Valider")
        self.btn_cancel = QtWidgets.QPushButton(self)
        self.btn_cancel.setText("Annuler")

        btn_container = QtWidgets.QWidget(self)
        btn_layout = QtWidgets.QHBoxLayout(btn_container)
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_valid)

        self.tasks_list = QtWidgets.QListWidget(self)
        self.tasks_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        for task in self.tasks:
            self.tasks_list.addItem(task["name"])

        self.general_layout.addWidget(self.tasks_list)
        self.general_layout.addWidget(btn_container)
        
    def setup_signals(self):
        """
        Initialise les signaux des boutons 
        """
        self.btn_cancel.clicked.connect(self.close)
        self.btn_valid.clicked.connect(self.delete_tasks)
        
    def delete_tasks(self):
        """
        Fonction qui supprime les tâches selectionnées du DayWidget
        """
        old_tasks_list = self.day_widget.tasks
        updated_tasks_list = []
        
        for task in old_tasks_list:            
            if task["name"] not in [selected_task.text() for selected_task in self.tasks_list.selectedItems()]:
                updated_tasks_list.append(task)
        self.day_widget.tasks = updated_tasks_list
        self.day_widget.save_tasks()
        self.day_widget.update_tasks_display()
        
        self.close()

       

