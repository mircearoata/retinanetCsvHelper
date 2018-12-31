try:
    # python 3.x
    import tkinter as tk
except ImportError:
    # python 2.x
    import Tkinter as tk
from PIL import ImageTk, Image


class TextInput(tk.Frame):
    def __init__(self, parent, label_text="", placeholder=""):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text=label_text)
        self.input = tk.Entry(self)
        self.input.insert(0, placeholder)

        self.label.grid(row=0, column=0)
        self.input.grid(row=0, column=1)

        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def get(self):
        return self.input.get()


class ImageLabeler(tk.Frame):
    def __init__(self, parent, submit_callback):
        tk.Frame.__init__(self, parent)
        self.lineX = None
        self.lineY = None
        self.submit_callback = submit_callback
        self.annotations = ""
        self.image_name = None
        self.image = None
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.bind("<ButtonPress-1>", self.paint)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.submitButton = tk.Button(self, text="Submit", command=self.submit)

        self.canvas.grid(row=0, column=0, rowspan=4, sticky="ew")
        self.submitButton.grid(row=4, column=0)

        self.no_rows = 5
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(self.no_rows, weight=1)

        self.rectangles = []
        self.points = []
        self.labelInputs = []

    def on_mouse_move(self, event):
        if self.lineX is not None:
            self.canvas.delete(self.lineX)
        if self.lineY is not None:
            self.canvas.delete(self.lineY)
        self.lineX = self.canvas.create_line(0, event.y, 1000000, event.y, fill="red")
        self.lineY = self.canvas.create_line(event.x, 0, event.x, 1000000, fill="red")

    def paint(self, event):
        python_green = "#476042"
        x, y = event.x, event.y
        self.points.append((x, y))
        if len(self.points) == 2:
            self.rectangles.append(((min(self.points[0][0], self.points[1][0]),
                                     min(self.points[0][1], self.points[1][1])),
                                   (max(self.points[0][0], self.points[1][0]),
                                    max(self.points[0][1], self.points[1][1]))))
            self.canvas.create_rectangle(self.points[0][0], self.points[0][1], self.points[1][0], self.points[1][1],
                                         outline=python_green, width=5)
            self.points.clear()
            new_input = TextInput(self, "{0}: ".format(len(self.labelInputs)), "Label")
            new_input.grid(row=len(self.labelInputs) % self.no_rows, column=int(1+len(self.labelInputs) / self.no_rows),
                           sticky="ew")
            self.labelInputs.append(new_input)

        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill=python_green, outline=python_green, width=10)

    def load_image(self, image):
        self.canvas.delete("all")
        self.image_name = image
        self.image = ImageTk.PhotoImage(Image.open(image))
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")
        for label in self.labelInputs:
            label.grid_forget()
        self.points.clear()
        self.rectangles.clear()
        self.labelInputs.clear()

    def submit(self):
        if len(self.rectangles) != len(self.labelInputs):
            raise Exception("Unknown error")
        length = len(self.rectangles)
        lines = []
        for i in range(length):
            lines.append("{0},{1},{2},{3},{4},{5}".format(self.image_name,
                                                          self.rectangles[i][0][0], self.rectangles[i][0][1],
                                                          self.rectangles[i][1][0], self.rectangles[i][1][1],
                                                          self.labelInputs[i].get()))
        self.annotations = self.annotations + ('\n'.join(lines) + '\n')
        self.submit_callback()

    def get_annotations(self):
        return self.annotations

    def clear_annotations(self):
        self.annotations = ""
