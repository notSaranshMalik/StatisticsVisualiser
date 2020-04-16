from DefaultWindow import DefaultWindow
from ChiPage import ChiPage

import tkinter as tk


class MainPage(DefaultWindow):
    '''MainPage class for the first to start UI element'''
    
    
    def __init__(self, parent):

        # Super instantiation
        super().__init__(parent, width=500, height=300)

        # Initialise components
        self.label = tk.Label(self.frame, text = 'Statistics Visualisation', fg = self.fg_color, bg = self.bg_color, font = self.title_font)
        self.label.pack(pady=20)
        
        self.button_chi = tk.Button(self.frame, text = 'Chi Squared Test', fg = self.fg_color, bg = self.bg_color, font = self.text_font, command = self.chi_window)
        self.button_chi.pack(padx = (20, 10), pady = (0, 20), fill = tk.BOTH, expand = True, side = 'left')

        self.button_bessel = tk.Button(self.frame, text='Bessel\'s Correction', fg = self.fg_color, bg = self.bg_color, font = self.text_font, command = self.bessel_window)
        self.button_bessel.pack(padx = (10, 20), pady = (0, 20), fill = tk.BOTH, expand = True, side = 'left')


    def chi_window(self):
        self.root = tk.Toplevel(self.parent)
        ChiPage(self.root)


    def bessel_window(self):
        self.root = tk.Toplevel(self.parent)
        BesselPage(self.root)
