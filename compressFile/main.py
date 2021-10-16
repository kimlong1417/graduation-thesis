import os
import zipfile
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('300x150')

def get_files(images):
    # images = os.scandir('./')
    with zipfile.ZipFile('new.zip', 'w') as new_zip:
        for name in images:
            new_zip.write(name)

def select_file():
    filetypes = (
        ('image files', '*.png'),
        ('image files', '*.jpg'),
        ('All files', '*.*')
    )

    images = fd.askopenfilenames(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    get_files(images)

    showinfo(
        title='Selected File',
        message=images
    )


# open button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)

open_button.pack(expand=True)


# run the application
root.mainloop()


# filename = fd.askopenfilename()


