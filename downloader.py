from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from pydub import AudioSegment
import os
import pafy
import time

class Downloader:

     def __init__(self, mainWindow):
          self.window = mainWindow
          self.window.title('MP4 && MP3 Downloader')
          self.window.resizable(0,0)
          #self.window.iconbitmap('img\\icon.ico')
          self.numLinks = 0
          self.ffmpegRoute = ''

          #Frame Ruta
          frameRuta = LabelFrame(self.window, text='Rutas')
          frameRuta.grid(row=0, column=0, columnspan=10, pady=10, padx=10)

          #Entry URL
          Label(frameRuta, text='URL: ').grid(row=1,column=0, padx=5, pady=2)
          self.url = Entry(frameRuta, width=45)
          self.url.focus()
          self.url.grid(row=1, column=1, padx=5, pady=2)

          #Append Button
          Button(frameRuta, text='Agregar a la lista', command=self.appendToList).grid(row=2, column=0, columnspan=10, sticky=W+E, padx=5, pady=2)

          #Entry directory
          self.currDir = os.getcwd()
          Label(frameRuta, text='').grid(row=3,column=0, padx=5, pady=2)
          Label(frameRuta, text='').grid(row=4,column=0, padx=5, pady=2)
          Label(frameRuta, text='').grid(row=5,column=0, padx=5, pady=2)
          Label(frameRuta, text='Directorio: ').grid(row=6, column=0, padx=5, pady=2)
          self.route = Entry(frameRuta, width=45,textvariable=StringVar(frameRuta, value=self.currDir), state='readonly')
          self.route.grid(row=6, column=1, padx=5, pady=2)

          #Button Directory
          Button(frameRuta, text='Guardar en', command=self.chooseDirectory).grid(row=7, column=0, columnspan=10, sticky=W+E, padx=5, pady=2)

          #Frame Lista
          frameLista = LabelFrame(self.window, text='Lista de descarga')
          frameLista.grid(row=0, column=11, columnspan=10, padx=10, pady=10)

          #Text Area
          self.lista = Text(frameLista, height=5, width=45,state='disable')
          self.lista.grid(row=0, column=0, columnspan=2, padx=5, pady=2)

          #Label
          Label(frameLista, text='Formato de descarga', anchor=CENTER).grid(row=1, column=0, columnspan=10, padx=5, pady=2, sticky=W+E)

          #Radio Buttons
          self.var = IntVar()
          self.mp3RB = Radiobutton(frameLista, text='Audio', variable=self.var, value=1)
          self.mp3RB.grid(row=2, column=0, padx=5, pady=2)
          self.mp3RB.deselect()

          self.mp4RB = Radiobutton(frameLista, text='Video', variable=self.var, value=2)
          self.mp4RB.grid(row=2, column=1, padx=5, pady=2)
          self.mp4RB.select()

          #Download Button
          Button(frameLista, text='Descargar', command=self.downloadFiles).grid(row=3, column=0, columnspan=10, sticky=W+E, padx=5, pady=2)

          #Clean list
          Button(frameLista, text='Vaciar lista', command=self.cleanList).grid(row=4, column=0, columnspan=10, sticky=W+E, padx=5, pady=2)

          #Autor
          Label(self.window, text='Copyright © Jesús Cuautle').grid(row=1, column=0, padx=5, pady=2)
          #Version (NumeVer.NumCommit.Date)
          Label(self.window, text='ver 1.1.2704').grid(row=1, column=1, padx=5, pady=2)

          #ProgressBar
          self.progress = ttk.Progressbar(self.window, length=100)
          self.progress.grid(row=1, column=11, columnspan=10, sticky=W+E, padx=5, pady=5)

     #Agregar de 'Entry' a la lista 'Text'
     def appendToList(self):
          link = self.url.get()
          if len(link) != 0:
               link = link+'\n'
               self.lista['state'] = 'normal'
               self.lista.insert(END, link)
               self.numLinks += 1
          else:
               messagebox.showwarning('Aviso', 'El enlace URL es requerido')
          self.lista['state'] = 'disable'
          self.url.delete(0, END)

     #Seleccionar directorio de salida de archivos
     def chooseDirectory(self):
          self.route['state'] = 'normal'
          self.newDirectory = filedialog.askdirectory()
          self.route.delete(0,END)
          self.route.insert(0, self.newDirectory)
          self.route['state'] = 'readonly'

     #Descargar archivos, según el formato elegido
     def downloadFiles(self):
          #Advertencia!
          if self.numLinks == 0:
               messagebox.showwarning('Aviso', 'La lista de descargas está vacía')
          else:
               pass

          formato = self.var.get()
          percent = 100/self.numLinks

          if formato == 2:
               j = 1.0
               for i in range(self.numLinks):
                    link = self.lista.get(j, j+1)
                    j+=1.0
                    videoOBJ = pafy.new(link)
                    self.downVideo(videoOBJ)
                    self.progress['value'] = self.progress['value'] + percent
                    self.window.update_idletasks()
                    time.sleep(1)

          elif formato == 1:
               j=1.0
               for i in range(self.numLinks):
                    link = self.lista.get(j, j+1)
                    j+=1.0
                    audioOBJ = pafy.new(link)
                    self.downAudio(audioOBJ)
                    self.progress['value'] = self.progress['value'] + percent
                    self.window.update_idletasks()
                    time.sleep(1)
          else:
               pass

          #time.sleep(3)
          self.progress['value'] = 0
          self.lista['state'] = 'normal'
          self.lista.delete(1.0, END)
          self.lista['state'] = 'disable'
          self.numLinks = 0
          self.progress['value'] = 0
          self.window.update()

     def cleanList(self):
          self.lista['state'] = 'normal'
          self.lista.delete(1.0, END)
          self.lista['state'] = 'disable'

     #Descargar video
     def downVideo(self, video):
          best = video.getbestvideo(preftype='mp4')
          best.download(self.route.get())

     #Descargar Audio
     #Solucionar la compatibilidad con TODOS los nombres de los videos (caracteres especiales)
     def downAudio(self, audio):
          best = audio.getbestaudio()
          best.download(self.route.get())
          AudioSegment.ffmpeg = os.getcwd()+'\\codec'+'\\bin'+'\\ffmpeg.exe'
          Audio_webm = audio.title+'.webm'
          Audio_mp3 = audio.title+'.mp3'
          sound = AudioSegment.from_file(self.route.get()+'\\'+Audio_webm)
          sound.export(self.route.get()+'\\'+Audio_mp3, format='mp3', bitrate='320k')
          os.remove(self.route.get()+'\\'+Audio_webm)

#Mantenr en ejecución
if __name__ == "__main__":
     mainWindow = Tk()
     app = Downloader(mainWindow)
     mainWindow.mainloop()