import tkinter as tk
from tkinter.font import Font


class DefaultWindow:
    '''DefaultWindow class to instantiate new Tkinter window
    using the look and feel of this app'''


    def __init__(self, parent, width, height):

        # Initialise window properties
        self._init_window(parent, width, height)

        # Initialise styles to be used
        self._init_styles()

        # Initialise frame
        self._init_frame()


    def _init_window(self, parent, width, height):

        # Parent definition
        self.parent = parent
        
        # Basic window properties
        self.parent.title('Statistics visualisation')
        self.parent.resizable(width = False, height = False)
        self.parent.geometry(f'{width}x{height}')

        # Centering window on page
        self.screen_width = self.parent.winfo_screenwidth()
        self.screen_height = self.parent.winfo_screenheight()
        self.translate_x = int((self.screen_width - width) / 2)
        self.translate_y = int((self.screen_height - height) / 2)
        self.parent.geometry(f"+{self.translate_x}+{self.translate_y}")


    def _init_styles(self):
        self.bg_color = '#f0f0f0'
        self.fg_color = '#1c1c1c'
        self.title_font = Font(self.parent, family = "Open Sans", size = 22)
        self.text_font = Font(self.parent, family = "Open Sans Light", size = 20)
        self.normal_font = Font(self.parent, family = "Open Sans", size = 14)
        self.normal_light_font = Font(self.parent, family = "Open Sans Light", size = 14)


    def _init_frame(self):
        self.frame = tk.Frame(self.parent, bg = self.bg_color)
        self.frame.pack(fill = tk.BOTH, expand=True)
