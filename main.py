from pytube import YouTube
from pytube.exceptions import RegexMatchError
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import *
from tkinter import Entry
import os

class YouTubeURL:
    global downloadformat
    def __init__(self, givenUrl):
        self.givenUrl = givenUrl

    def download_audio(self):
        try:
            yt = YouTube(self.givenUrl)
            audio = yt.streams.filter(only_audio=True).first()
            if audio:
                download_path = os.path.join(os.path.expanduser("~"), "Downloads")
                audio.download(download_path)
                messagebox.showinfo("Abgeschlossen", "Download war erfolgreich!")
            else:
                messagebox.showerror("FEHLER", "Für diese Audio wurde kein Audiostream gefunden.")
        except RegexMatchError:
            messagebox.showerror("FEHLER", "Ungültige YouTube-URL eingegeben.")

    def download_video(self):
        try:
            yt = YouTube(self.givenUrl)
            # Filtert verfügbare Streams nach "progressive" (Video und Audio zusammen) und Dateiendung 'mp4'
            filtered_streams = yt.streams.filter(progressive=True, file_extension='mp4')

            # Sortiert die gefilterten Streams nach Auflösung in aufsteigender Reihenfolge
            sorted_streams = filtered_streams.order_by('resolution')

            # Kehrt die Reihenfolge der Streams um (höchste Auflösung zuerst)
            sorted_desc_streams = sorted_streams.desc()

            # Wählt den ersten Stream aus der Liste (der nun der Stream mit der höchsten Auflösung ist)
            highest_quality_stream = sorted_desc_streams.first()

            # Speicherpfad
            download_path = os.path.join(os.path.expanduser("~"), "Downloads")

            # Stream-Download
            highest_quality_stream.download(output_path=download_path)

            messagebox.showinfo("Abgeschlossen", "Download war erfolgreich!")
        except RegexMatchError:
            messagebox.showerror("FEHLER", "Ungültige YouTube-URL eingegeben.")


def resetall():
    print("Reset all...")
    combo.set('')
    url.delete(0, tk.END)
    pass

def want_download(url):
    if selected_value == 'audio':
        print("Audio downloaden...")
        audio = YouTubeURL(url)
        audio.download_audio()
    elif selected_value == 'video':
        print("Video downloaden...")
        video = YouTubeURL(url)
        video.download_video()
    else:
        print("!ERROR - Format auswählen")
    resetall()
    pass


#MAIN + GUI
def main():
    global downloadformat, url, combo, selected_value
    #Fenster erstellen & Eigenschaften festlegen
    fenster = tk.Tk()
    fenster.geometry("369x369")
    fenster.resizable(False, False)
    fenster.title('YouTubeDL')

    #URL-Eingabe
    instructions = Label(fenster, text='YouTube-URL eingeben:')
    instructions.pack()
    url = Entry(fenster)
    url.pack()

    #Format-Auswahl
    textfeld_downloadformat = Label(fenster, text='Download-Format auswählen:')
    textfeld_downloadformat.pack()

    def on_select(event):
        global selected_value
        selected_value = combo.get()
        print(selected_value)
        if selected_value == 'audio':
            print("Audio downloaden...")
            pass
        elif selected_value == 'video':
            print("Video downloaden...")
        else:
            print("!ERROR - keine Auswahl getroffen!")
        pass

    combo = ttk.Combobox(values=["audio", "video"])
    combo.state(["readonly"])
    combo.bind("<<ComboboxSelected>>", on_select)
    combo.pack()

    #Download-Button
    downloadbutton = Button(fenster, text="Download", command=lambda: want_download(url.get()))
    downloadbutton.pack(padx=10, pady=10)

    #Reset-Button
    resetbutton = Button(fenster, text="Reset", command=lambda: resetall())
    resetbutton.pack()

    #Fenster aufrufen
    fenster.mainloop()
    pass



#Programm-Aufruf
if __name__ == '__main__':
    main()