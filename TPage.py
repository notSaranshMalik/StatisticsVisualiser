from DefaultWindow import DefaultWindow

import tkinter as tk

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt

import numpy as np
import pandas as pd
from scipy import stats as scstats

import random
import os


class TPage(DefaultWindow):
    '''TPage class for the T test simulation'''


    def __init__(self, parent):
        
        # Super instantiation
        super().__init__(parent, width = 1000, height = 800)

        # Title
        self.label = tk.Label(self.frame, text = 'T Test Simulation', height = 2, fg = self.fg_color, bg = self.bg_color, font = self.title_font)
        self.label.pack()

        # Initialise components
        self.button_frame = tk.Frame(self.frame, bg = self.bg_color)
        
        self.button_imp = tk.Button(self.button_frame, text = 'Import data', height = 2, font = self.normal_font, command = self._import, padx = 10)
        self.button_imp.pack(padx = 20, expand = True, fill = tk.X, side = 'left')

        self.button_rand2 = tk.Button(self.button_frame, text = 'Random data', height = 2, font = self.normal_font, command = self._random, padx = 10)
        self.button_rand2.pack(padx = 20, expand = True, fill = tk.X, side = 'left')

        self.button_frame.pack()

        self.error_label = tk.Label(self.frame, text = '', height = 2, fg = self.fg_color, bg = self.bg_color, font = self.normal_light_font)
        self.error_label.pack(pady = 10)

        # First init
        self.first = True


    def _import(self):

        # Import file
        self.file_name = tk.filedialog.askopenfilename(initialdir = os.path.join("/Users", os.environ["USER"], "Desktop"), filetypes = (("CSV Files", "*.csv"),))
        if not self.file_name:
            return False
        self.data = pd.read_csv(self.file_name)
        self.data.dropna(axis=1, how='all', inplace = True)
        self.data = self.data.T.reset_index().T

        # Make sure file has 2 columns
        if self.data.shape[1] != 2:
            print(self.data.shape)
            self.error_label.config(text = "Error! File must have 2 columns")
            return False

        # Make sure all values are integers
        try:
            [int(x) for x in self.data if x != None]
        except Exception:
            self.error_label.config(text = "Error! File must have only numbers")
            return False

        # Generate
        try:
            self.a = self.data[0].astype(np.float64)
            self.a = self.a[~np.isnan(self.a)]
            self.b = self.data[1].astype(np.float64)
            self.b = self.b[~np.isnan(self.b)]

            print(self.a, self.b)
            
            self.data = np.array([["", "Data A", "Data B"],
                                  ["Mean", round(self.a.mean(), 2), round(self.b.mean(), 2)],
                                  ["Variance", round(self.a.var(ddof = 1), 2), round(self.b.var(ddof = 1), 2)],
                                  ["Elements", len(self.a), len(self.b)]])
            
            self.mode = 'import'
            self.button_frame.destroy()
            self.error_label.destroy()
            self._generate()
        except Exception:
            self.error_label.config(text = "Error!")

        # Plot
        self._make()
        

    def _random(self):
        
        self.a = np.random.normal(loc = 50, scale = 5, size = random.randint(20, 60))
        self.b = np.random.normal(loc = 50, scale = 5, size = random.randint(20, 60)) + random.randint(-4, 4)

        self.data = np.array([["", "Data A", "Data B"],
                              ["Mean", round(self.a.mean(), 2), round(self.b.mean(), 2)],
                              ["Variance", round(self.a.var(ddof = 1), 2), round(self.b.var(ddof = 1), 2)],
                              ["Elements", len(self.a), len(self.b)]])

        if self.first:
            self.first = False
            self.mode = 'random'
            self.button_frame.destroy()
            self.error_label.destroy()
            self._generate()
        else:
            self._make()

    def _make(self):
        self.data_flat = iter(self.data.flatten().tolist())
        for row in self.grid:
            for col in row:
                col.config(text = next(self.data_flat))

        t, p = scstats.ttest_ind(self.a, self.b)

        self.ax[0].cla()
        self.ax[1].cla()

        self.ax[0].set_title('Data sets (normal distributions)')
        self.ax[1].set_title('T Distribution')

        self.mu_1 = self.a.mean()
        self.sigma_1 = np.sqrt(self.a.var(ddof = 1))
        self.x_1 = np.linspace(self.mu_1 - 3 * self.sigma_1, self.mu_1 + 3 * self.sigma_1, 100)
        self.ax[0].plot(self.x_1, scstats.norm.pdf(self.x_1, self.mu_1, self.sigma_1))
    
        self.mu_2 = self.b.mean()
        self.sigma_2 = np.sqrt(self.b.var(ddof = 1))
        self.x_2 = np.linspace(self.mu_2 - 3 * self.sigma_2, self.mu_2 + 3 * self.sigma_2, 100)
        self.ax[0].plot(self.x_2, scstats.norm.pdf(self.x_2, self.mu_2, self.sigma_2))

        self.df = len(self.a) + len(self.b) - 2
        self.x_3 = np.linspace(scstats.t.ppf(0.001, self.df), scstats.t.ppf(0.999, self.df), 100)
        self.g_1 = scstats.t.pdf(self.x_3, self.df)
        self.ax[1].plot(self.x_3, self.g_1, color = self.fg_color)
    
        self.end = np.linspace(scstats.t.ppf(0.975, self.df), scstats.t.ppf(0.999, self.df), 100)
        self.g_2 = scstats.t.pdf(self.end, self.df)
        self.ax[1].fill_between(self.end, self.g_2, color = self.fg_color)
        
        self.beg = np.linspace(scstats.t.ppf(0.001, self.df), scstats.t.ppf(0.025, self.df), 100)
        self.g_3 = scstats.t.pdf(self.beg, self.df)
        self.ax[1].fill_between(self.beg, self.g_3, color = self.fg_color)

        if p >= 0.005 and p <= 0.995:
            self.ax[1].plot([t, t], [0, scstats.t.pdf(t, self.df)], color = 'orange')
            
        self.fig.canvas.draw()

        self.status_label.config(text = f"T value: {round(t, 2)}, P value: {round(p, 2)}, {'Significant' if p < 0.05 else 'Insignificant'}")            

        
    def _generate(self):

        # Table
        self.table_frame = tk.Frame(self.frame, bg = self.bg_color, highlightbackground = self.fg_color, highlightthickness = 1)

        self.grid = []
        for row in range(self.data.shape[0]):
            self.grid.append([])
            for col in range(self.data.shape[1]):
                if row == 0 or col == 0:
                    tb = tk.Label(self.table_frame, width = 10, text = "", bg = self.bg_color, font = self.normal_font)
                    tb.grid(row = row, column = col)
                else:
                    tb = tk.Label(self.table_frame, width = 10, text = "", bg = self.bg_color, font = self.normal_light_font)
                    tb.grid(row = row, column = col)
                self.grid[row].append(tb)

        self.table_frame.pack()

        # Graphs
        plt.style.use('fast')
        self.fig, self.ax = plt.subplots(1, 2)
        self.fig.patch.set_facecolor(self.bg_color)
        self.ax[0].set_facecolor(self.bg_color)
        self.ax[1].set_facecolor(self.bg_color)

        # Display graph
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill = tk.BOTH, expand = True)

        # Button
        if self.mode == 'random':
            self.run_frame = tk.Frame(self.frame, bg = self.bg_color, pady = 20)
            self.run_but = tk.Button(self.frame, text = 'Run', height = 2, font = self.normal_font, command = self._random, padx = 10)
            self.run_but.pack(pady = (0, 10))

        self.status_label = tk.Label(self.frame, text = "", height = 2, fg = self.fg_color, bg = self.bg_color, font = self.normal_light_font)
        self.status_label.pack(pady = (0, 20))

        if self.mode == 'random':
            self._random()
            
