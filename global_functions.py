from PyQt5 import QtWidgets
import json
import calendar 
import datetime as dt

def clear_layout(layout):
    while layout.count() > 0:
        item = layout.takeAt(0)
        if not item:
            continue
        w = item.widget()
        if w:
            w.deleteLater()

def substract_time(begin_time,end_time):
    """
    Retourne l'interval de temps entre un temps d'entrée et de sortie
    Prend deux objets time, et renvoie un nombre de minutes
    """
    beg = begin_time.hour * 60 + begin_time.minute
    end = end_time.hour * 60 + end_time.minute
    return end-beg    
    
def click_is_inside_widget(widget,event):
    """
    Fonction qui détermine si le click de souris est dans le widget ou non
    Retourne True ou False
    """
    
    x_min = 0
    x_max = widget.width()
    y_min = 0
    y_max = widget.height()
    if event.x()  >= x_min and event.x() <= x_max:
        if event.y()  >= y_min and event.y() <= y_max:
            return True
        else:
            return False

def create_json_file():
    """
    Fonction qui créer le fichier json nécessaire à la sauvegarde des tâches
    """
    days = { i : [] for i in range(1,7*6+1)}
    months = {m : days for m in range(1,13)}
    years = {y : months for y in range(2020,2021)}
    # years_json = json.dumps(years)
    print(len(years))
    with open("tasks_file.json","w") as json_file:    
        json.dump(years,json_file, indent= 4, sort_keys= True)
        
    

    # print(months)

if __name__ == "__main__" :
    create_json_file()