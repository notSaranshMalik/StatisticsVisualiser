from DefaultWindow import DefaultWindow
from ChiPage import ChiPage
from TPage import TPage

import tkinter as tk


class MainPage(DefaultWindow):
    '''MainPage class for the first to start UI element'''
    
    
    def __init__(self, parent):

        # Super instantiation
        super().__init__(parent, width=500, height=300)

        # Initialise components
        self.frame.grid_columnconfigure(0, weight=1, uniform="u")
        self.frame.grid_columnconfigure(1, weight=1, uniform="u")
        self.frame.grid_rowconfigure(0, weight=1, uniform="a")
        self.frame.grid_rowconfigure(1, weight=3, uniform="a")
        
        self.label = tk.Label(self.frame, text = 'Statistics Visualisation', fg = self.fg_color, bg = self.bg_color, font = self.title_font)
        self.label.grid(row = 0, column = 0, columnspan = 2, pady=20)
        
        self.button_chi = tk.Button(self.frame, text = 'Chi Squared Test', fg = self.fg_color, bg = self.bg_color, font = self.text_font, command = self.chi_window)
        self.button_chi.grid(row = 1, column = 0, padx = (20, 10), pady = (0, 20), sticky = "NSEW")

        self.t_test_button = tk.Button(self.frame, text='T Test', fg = self.fg_color, bg = self.bg_color, font = self.text_font, command = self.t_test_window)
        self.t_test_button.grid(row = 1, column = 1, padx = (10, 20), pady = (0, 20), sticky = "NSEW")


    def chi_window(self):
        self.root = tk.Toplevel(self.parent)
        ChiPage(self.root)


    def t_test_window(self):
        self.root = tk.Toplevel(self.parent)
        TPage(self.root)
