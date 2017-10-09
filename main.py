import Tkinter as tk
import tkFileDialog as tkf

source = ''
dest = ''

class GUI(tk.Tk):
    def __init__(self):
        # Initialize GUI
        tk.Tk.__init__(self)

        # Set screens
        self.enter = Enter(self)
        self.enter.pack(fill=tk.BOTH, expand=True)
        self.main_screen = MainScreen(self)

        # Set basic parameters
        self.title('MegaCrop')
        self.geometry('960x820')
        # self.icon = tk.PhotoImage(file='graphics/icon.gif')
        # self.tk.call('wm', 'iconphoto', self._w, self.icon)
        self.minsize(width=800, height=800)
        # self.protocol('WM_DELETE_WINDOW', lambda: self.on_closing())

    def set_enter(self, _):
        """
        Set the Welcome screen
        """
        self.main_screen.pack_forget()
        self.enter.pack(fill=tk.BOTH, expand=True)

    def set_main_screen(self, _):
        """
        Set the Vault screen
        """
        self.enter.pack_forget()
        self.main_screen.pack(fill=tk.BOTH, expand=True)

    def on_closing(self):
        """
        Turn the blue LED off and close the port before closing
        """
        self.destroy()


class Enter(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root, bg="#bbeaff")
        self.root = root

        # set a frame, an entry, a label, a string variable, and a create button

        self.title_frame = tk.Frame(self, bg="#bbeaff")
        self.source_frame = tk.Frame(self, bg="#bbeaff")
        self.destination_frame = tk.Frame(self, bg="#bbeaff")

        self.title_label = tk.Label(self.title_frame, text='Choose Directory:', bg="#bbeaff",
                                          font="TkDefaultFont 20")
        self.source_label = tk.Label(self.source_frame, text='Source: -', bg="#bbeaff",
                                     font="TkDefaultFont 20")
        self.destination_label = tk.Label(self.destination_frame, text='Destination: -', bg="#bbeaff",
                                     font="TkDefaultFont 20")

        self.browse_source = ButtonBL(self.source_frame, bg="#bbeaff", w=200, h=50, r=50, color="#00afff", hover_color="#5ab7e2",
                               press_color="#97d8f6", command=self.browse_s, text="Browse",
                               font="TkDefaultFont 20")
        self.browse_destination = ButtonBL(self.destination_frame, bg="#bbeaff", w=200, h=50, r=50, color="#00afff", hover_color="#5ab7e2",
                                      press_color="#97d8f6", command=self.browse_d, text="Browse",
                                      font="TkDefaultFont 20")

        self.go_button = ButtonBL(self, bg="#bbeaff", w=200, h=50, r=50, color="#00afff", hover_color="#5ab7e2",
                                   press_color="#97d8f6", command=lambda x: self.go(), text="Go",
                                   font="TkDefaultFont 20")



    def pack(self, **kwargs):
        """
        pack screen
        """
        tk.Frame.pack(self, **kwargs)

        self.title_frame.pack()
        self.source_frame.pack()
        self.destination_frame.pack()

        self.title_label.pack()
        self.source_label.pack()
        self.destination_label.pack()
        self.browse_destination.pack()
        self.browse_source.pack()
        self.go_button.pack(pady=(20, 0))

    def go(self):
        self.root.set_main_screen('a')

    def browse_s(self, _):
        d = tkf.askdirectory()
        self.source_label.config(text='Source: '+d)
        global source
        source = d

    def browse_d(self, _):
        d = tkf.askdirectory()
        self.destination_label.config(text='Destination: '+d)
        global dest
        dest = d


class MainScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#bbeaff")

        self.master = master


        self.sidebar = tk.Frame(self, bg='#bbeaff')
        self.sidebar.pack(fill=tk.BOTH, side=tk.LEFT)
        self.new_entry = ButtonBL(self.sidebar, bg="#bbeaff", w=330, h=70, r=20, color="#00afff",
                                  hover_color="#5ab7e2",
                                  press_color="#97d8f6",
                                  text="New Entry")






    def pack(self, **kwargs):
        tk.Frame.pack(self, **kwargs)
        self.new_entry.pack(pady=(60, 5), padx=7)
        print source
        print dest


class ButtonBL(tk.Canvas):
    """
    A class used to create round-cornered buttons
    """
    def __init__(self, root, bg, w=0, h=0, r=20, color='red', hover_color='blue', press_color='green',
                 command=lambda: None, text="", font="TkDefaultFont 30", fg="white", enabled=True):
        tk.Canvas.__init__(self, root, width=w, height=h, bg=bg, highlightthickness=0)

        # set geometry
        self.button_parts = [
            self.create_arc(0, 0, r, r, start=90, extent=90),
            self.create_arc(w - r, 0, w, r, start=0, extent=90),
            self.create_arc(0, h - r, r, h, start=180, extent=90),
            self.create_arc(w - r, h - r, w, h, start=270, extent=90),
            self.create_rectangle(r / 2, 0, w - r / 2, h),
            self.create_rectangle(0, r / 2, w, h - r / 2)
        ]
        # set color and text
        self.set_color(color)
        self.create_text(w/2, h/2, font=font, text=text, fill=fg)

        # set hover parameters and button function
        self.color, self.hover_color, self.press_color = color, hover_color, press_color
        self.command = command
        self.set_bindings()

        # allow button disabling
        self.enabled = True
        if not enabled:
            self.disable()

    def set_color(self, color):
        for i in self.button_parts:
            self.itemconfig(i, fill=color, outline=color)

    def set_bindings(self):
        self.bind('<Enter>', lambda event: self.set_color(self.hover_color))
        self.bind('<Leave>', lambda event: self.set_color(self.color))

        self.bind('<Button-1>', lambda event: self.set_color(self.press_color))
        self.bind('<ButtonRelease-1>', self.command)

    def disable(self):
        if not self.enabled:
            return
        self.enabled = False
        self.set_color('#AAAAAA')
        for b in ['<Button-1>', '<ButtonRelease-1>', '<Enter>', '<Leave>']:
            self.unbind(b)

    def enable(self):
        if self.enabled:
            return
        self.enabled = True
        self.set_color(self.color)
        self.set_bindings()



gui = GUI()
gui.mainloop()