import sys
import os
from tkinter import *
import time
import subprocess
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import messagebox        

global actual_combo
global entry

def load_total_time_graphic(segundos):
    load = Image.open("{}sTotalTime.png".format(segundos))
    resize_image = load.resize((500, 400))
    render = ImageTk.PhotoImage(resize_image)
    img = Label(window, image=render)
    img.image = render
    img.place(x=170, y=50)

def load_graphic(name):
    load = Image.open(name)
    resize_image = load.resize((500, 400))
    render = ImageTk.PhotoImage(resize_image)
    img = Label(window, image=render)
    img.image = render
    img.place(x=170, y=50)

def cargar_total_time(segundos):
    # Primero revisamos si las gráficas ya están generadas, si lo estan la devolvemos y se termina
    archives_list = subprocess.check_output(['ls']).decode('utf-8').split('\n')
    if '{}sTotalTime.png'.format(segundos) in archives_list:
        load_total_time_graphic(segundos)
        return

    # Si no lo están, las generamos

    ## Ejecutamos el script que genera las gráficas
    os.system('./time-test.py {}'.format(segundos))
    
    # Tenemos un temporizador que si en 25 segundos no se ha generado la gráfica, se pide que se vuelva a hacer.
    timer = 0
    # Revisamos que se haya generado la imagen de la gráfica en lo que dure el temporizador
    while True:
        timer = timer+1
        if timer <= TIMEOUT:
            archives_list = subprocess.check_output(['ls']).decode('utf-8').split('\n')

            if '{}sTotalTime.png'.format(segundos) in archives_list:
                load_total_time_graphic(segundos)
                break
                
        elif timer > TIMEOUT:
            #print('Foto no encontrada')
             
            # Create label
            l = Label(window, text = "Ha ocurrido un error, por favor inténtalo de nuevo.")
            l.config(font =("Courier", 14))
            l.pack()
            #T.pack()
            break

        time.sleep(1)

def cargar_mail_ip():
    # Primero revisamos si las gráficas ya están generadas, si lo estan la devolvemos y se termina
    archives_list = subprocess.check_output(['ls']).decode('utf-8').split('\n')
    if 'mail_logip.png' in archives_list:
        load_graphic('mail_logip.png')
        return

    # Si no lo están, las generamos

    ## Ejecutamos el script que genera las gráficas
    os.system('./time-test.py')
    
    # Tenemos un temporizador que si en 25 segundos no se ha generado la gráfica, se pide que se vuelva a hacer.
    timer = 0
    # Revisamos que se haya generado la imagen de la gráfica en lo que dure el temporizador
    while True:
        timer = timer+1
        if timer <= TIMEOUT:

            archives_list = subprocess.check_output(['ls']).decode('utf-8').split('\n')
            if 'mail_logip.png' in archives_list:
                load_graphic('mail_logip.png')
                return
                
        elif timer > TIMEOUT:
            #print('Foto no encontrada')
             
            # Create label
            l = Label(window, text = "Ha ocurrido un error, por favor inténtalo de nuevo.")
            l.config(font =("Courier", 14))
            l.pack()
            #T.pack()
            break

        time.sleep(1)


def cargar_access_ip():
    # Primero revisamos si las gráficas ya están generadas, si lo estan la devolvemos y se termina
    archives_list = subprocess.check_output(['ls']).decode('utf-8').split('\n')
    if 'access_logip.png' in archives_list:
        load_graphic('access_logip.png')
        return

    # Si no lo están, las generamos

    ## Ejecutamos el script que genera las gráficas
    os.system('./time-test.py')
    
    # Tenemos un temporizador que si en 25 segundos no se ha generado la gráfica, se pide que se vuelva a hacer.
    timer = 0
    # Revisamos que se haya generado la imagen de la gráfica en lo que dure el temporizador
    while True:
        timer = timer+1
        if timer <= TIMEOUT:

            archives_list = subprocess.check_output(['ls']).decode('utf-8').split('\n')
            if 'access_logip.png' in archives_list:
                load_graphic('access_logip.png')
                return
                
        elif timer > TIMEOUT:
            #print('Foto no encontrada')
             
            # Create label
            l = Label(window, text = "Ha ocurrido un error, por favor inténtalo de nuevo.")
            l.config(font =("Courier", 14))
            l.pack()
            #T.pack()
            break

        time.sleep(1)


def create_entry():
    global entry
    # Crear caja de texto.
    entry = Entry(window)
    # Posicionarla en la ventana.
    entry.place(x=335, y=530)
    l = Label(window, text = "Por favor, introduce un número entero que representa \n los segundos en los que se agrupan todos los logs.")
    l.config(font =("Courier", 14))
    l.place(x=215, y=475)
   

def run():
    global actual_combo
    global entry

    # La selección de la gráfica es necesaria siempre
    combo_value = combo.get()

    # Si no se ha seleccionado ninguna gráfica, se manda un error y se solicita
    if combo_value == '':
        messagebox.showinfo("Error", "Por favor, selecciona una gráfica para mostrar. ")
        return

    if actual_combo != combo_value:
        actual_combo = combo_value
        # Si no se ha seleccionado ninguna gráfica, se manda un error y se solicita
        if combo_value == 'All logs':
            create_entry()
            return

    if actual_combo == 'All logs':
        # Un input de entrada solo es necesaria en la gráfica
        entrada = entry.get()
        # Se ha seleccionado la gráfica, ahora verificamos que la entrada de segundos sea apropiada
        try:
            segundos = int(entrada)
        except Exception:
            #l = Label(window, text = "Formato inválido, por favor, introduzca un número entero")
            #l.config(font =("Courier", 14))
            #l.pack()
            messagebox.showinfo("Error", "Formato inválido, por favor, introduzca un número entero.")
            return
        cargar_total_time(entrada)
    
    elif actual_combo == 'Mail IP':
        cargar_mail_ip()
        return

    elif actual_combo == 'Access IP':
        cargar_access_ip()
        return
    

actual_combo = ''

window=Tk()

window.title("Registro de Logs")
window.geometry('850x750')
# No permitir modificar el tamaño de la pantalla
window.resizable(False, False)

# timeout que puede tardar la obtención de las gráficas
TIMEOUT = 25

# Boton para ejecutar el programa -> llama a run()
btn = Button(window, text="Obtener logs", bg="black", fg="black",command=run)
btn.place(width = 100, height = 50, x = 375, y = 680)


# Selector
combo = ttk.Combobox(window, state='readonly')
combo.place(x=330, y=600)
combo["values"] = ["All logs", "Mail IP", "Access IP"]

l = Label(window, text = "Por favor, seleccione la gráfica que desea visualizar.")
l.config(font =("Courier", 14))
l.place(x=200, y=570)

window.mainloop()