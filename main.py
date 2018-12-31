import tkinter as tk
from ImageLabeler import ImageLabeler
from tkinter import filedialog
from os import listdir
from os.path import isfile, join
from os import curdir

SINGLE = 0
FOLDER = 1

files = []
currentFile = 0
mode = SINGLE


def load_image():
    global mode, currentFile
    filename = filedialog.askopenfilename(initialdir=curdir, title="Select image",
                                          filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    if filename is None:
        return
    mode = SINGLE
    imageLabeler.load_image(filename)


def load_image_folder():
    global mode, currentFile, files
    imageLabeler.clear_annotations()
    folder_name = filedialog.askdirectory(initialdir=curdir, title="Select folder containing only images")
    if folder_name is None:
        return
    mode = FOLDER
    currentFile = 0
    files = [join(folder_name, f) for f in listdir(folder_name) if isfile(join(folder_name, f))]
    on_submit()


def on_submit():
    global currentFile
    if mode == FOLDER:
        if currentFile < len(files):
            imageLabeler.load_image(files[currentFile])
            currentFile = currentFile + 1
        else:
            generate_classes(save_annotations())


def save_annotations():
    filename = filedialog.asksaveasfilename(initialdir=curdir, title="Save annotations file",
                                            filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    if filename is None:
        return
    if not filename.endswith('.csv'):
        filename = filename + '.csv'
    with open(filename, 'w') as f:
        f.write(imageLabeler.get_annotations())
        imageLabeler.clear_annotations()
    return filename


def generate_classes(filename=None):
    if filename is None:
        filename = filedialog.askopenfilename(initialdir=curdir, title="Select annotations file",
                                              filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    if filename is None:
        return
    if not filename.endswith('.csv'):
        filename = filename + '.csv'
    with open(filename, 'r') as f:
        lines = f.readlines()
    classes = []
    for line in lines:
        current_class_name = line.split(',')[5].strip()
        if current_class_name not in classes:
            classes.append(current_class_name)
    filename = filedialog.asksaveasfilename(initialdir=curdir, title="Select classes save file",
                                            filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    if not filename.endswith('.csv'):
        filename = filename + '.csv'
    if filename is None:
        return
    cnt = 0
    with open(filename, 'w') as f:
        for class_name in classes:
            f.write('{0},{1}\n'.format(class_name, cnt))
            cnt = cnt + 1


root = tk.Tk()
root.title("RetinaNetCsvHelper")
root.geometry("1000x800")
root.configure(background='grey')
menu = tk.Menu(root)
root.config(menu=menu)
file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
# file_menu.add_command(label="Open...", command=load_image)
file_menu.add_command(label="Open folder...", command=load_image_folder)
file_menu.add_separator()
file_menu.add_command(label="Save annotations", command=save_annotations)
file_menu.add_command(label="Generate classes from annotations", command=generate_classes)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
imageLabeler = ImageLabeler(root, submit_callback=on_submit)
imageLabeler.place(x=0, y=0, relwidth=1, relheight=1)
root.mainloop()


