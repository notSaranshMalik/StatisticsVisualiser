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

        # Initialise components
        title_label = tk.Label(self.frame, text = 'T Test Simulation', height = 2, fg = self.fg_color, bg = self.bg_color, font = self.title_font).pack()

        self.button_frame = tk.Frame(self.frame, bg = self.bg_color)
        button_imp = tk.Button(self.button_frame, text = 'Import data', height = 2, font = self.normal_font, command = self._import, padx = 10).pack(padx = 20, expand = True, fill = tk.X, side = 'left')
        button_rand2 = tk.Button(self.button_frame, text = 'Random data', height = 2, font = self.normal_font, command = self._random, padx = 10).pack(padx = 20, expand = True, fill = tk.X, side = 'left')
        self.button_frame.pack()

        self.error_label = tk.Label(self.frame, text = '', height = 2, fg = self.fg_color, bg = self.bg_color, font = self.normal_light_font)
        self.error_label.pack(pady = 10)

        # Set variables
        self.screen_generated = False


    def _import(self):

        # Import file
        file_name = tk.filedialog.askopenfilename(initialdir = os.path.join("/Users", os.environ["USER"], "Desktop"), filetypes = (("CSV Files", "*.csv"),))
        if not file_name:
            return False

        # Access CSV data
        data = pd.read_csv(file_name)
        data = data.dropna(axis=1, how='all')
        data = data.T.reset_index().T

        # Make sure data has 2 columns
        if data.shape[1] != 2:
            print(data.shape)
            self.error_label.config(text = "Error! File must have 2 columns")
            return False

        # Make sure all values are integers
        try:
            [int(x) for x in data if x != None]
        except Exception:
            self.error_label.config(text = "Error! File must have only numbers")
            return False

        # Generate table data
        try:

            a = data[0].astype(np.float64)
            a = a[~np.isnan(a)]
            b = data[1].astype(np.float64)
            b = b[~np.isnan(b)]
            
            table_data = np.array([["", "Data A", "Data B"],
                                  ["Mean", round(a.mean(), 2), round(b.mean(), 2)],
                                  ["Variance", round(a.var(ddof = 1), 2), round(b.var(ddof = 1), 2)],
                                  ["Elements", len(a), len(b)]])

        except Exception:
            self.error_label.config(text = "Error!")

        # Make the graph
        self._make_screen()

        # Disable run button
        self.run_but.config(state = "disabled")

        self._update(table_data, a, b)
        

    def _random(self):
        
        # Generate the screen, then plot the random values
        self._make_screen()
        self._new_random()


    def _new_random(self):

        # Generate random data
        a = np.random.normal(loc = 50, scale = 5, size = random.randint(20, 60))
        b = np.random.normal(loc = 50, scale = 5, size = random.randint(20, 60)) + random.randint(-4, 4)

        # Generate table data
        table_data = np.array([["", "Data A", "Data B"],
                              ["Mean", round(a.mean(), 2), round(b.mean(), 2)],
                              ["Variance", round(a.var(ddof = 1), 2), round(b.var(ddof = 1), 2)],
                              ["Elements", len(a), len(b)]])

        # Plot the appropriate values
        self._update(table_data, a, b)


    def _make_screen(self):

        # Clear current screen
        self.button_frame.destroy()
        self.error_label.destroy()

        # Generate table
        table_frame = tk.Frame(self.frame, bg = self.bg_color, highlightbackground = self.fg_color, highlightthickness = 1)

        self.grid = [[], [], [], []]
        for row in range(4):
            for col in range(3):
                if row == 0 or col == 0:
                    tb = tk.Label(table_frame, width = 10, text = "", bg = self.bg_color, font = self.normal_font)
                    tb.grid(row = row, column = col)
                else:
                    tb = tk.Label(table_frame, width = 10, text = "", bg = self.bg_color, font = self.normal_light_font)
                    tb.grid(row = row, column = col)
                self.grid[row].append(tb)

        table_frame.pack()

        # Generate graphs
        plt.style.use('fast')
        self.fig, self.ax = plt.subplots(1, 2)
        self.fig.patch.set_facecolor(self.bg_color)
        self.ax[0].set_facecolor(self.bg_color)
        self.ax[1].set_facecolor(self.bg_color)
        canvas = FigureCanvasTkAgg(self.fig, master = self.frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill = tk.BOTH, expand = True)

        # Make run button
        self.run_but = tk.Button(self.frame, text = 'Run', height = 2, font = self.normal_font, command = self._new_random, padx = 10)
        self.run_but.pack(pady = (0, 10))

        # Make label for the T values
        self.status_label = tk.Label(self.frame, text = "", height = 2, fg = self.fg_color, bg = self.bg_color, font = self.normal_light_font)
        self.status_label.pack(pady = (0, 20))


    def _update(self, table_data, a, b):

        # Update table
        data_flat = iter(table_data.flatten().tolist())
        for row in self.grid:
            for col in row:
                col.config(text = next(data_flat))

        # Find T and P values
        t, p = scstats.ttest_ind(a, b)

        # Clear graphs and titles
        self.ax[0].cla()
        self.ax[1].cla()

        # Set the titles
        self.ax[0].set_title('Data sets (normal distributions)')
        self.ax[1].set_title('T Distribution')

        # Plot the left graph
        mu = a.mean()
        sigma = np.sqrt(a.var(ddof = 1))
        x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
        self.ax[0].plot(x, scstats.norm.pdf(x, mu, sigma))
    
        mu = b.mean()
        sigma = np.sqrt(b.var(ddof = 1))
        x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 100)
        self.ax[0].plot(x, scstats.norm.pdf(x, mu, sigma))

        # Plot the right graph
        dof = len(a) + len(b) - 2

        x = np.linspace(scstats.t.ppf(0.001, dof), scstats.t.ppf(0.999, dof), 100)
        self.ax[1].plot(x, scstats.t.pdf(x, dof), color = self.fg_color)
    
        # Plot the tail regions below the right graph
        x = np.linspace(scstats.t.ppf(0.975, dof), scstats.t.ppf(0.999, dof), 100)
        self.ax[1].fill_between(x, scstats.t.pdf(x, dof), color = self.fg_color)
        
        x = np.linspace(scstats.t.ppf(0.001, dof), scstats.t.ppf(0.025, dof), 100)
        self.ax[1].fill_between(x, scstats.t.pdf(x, dof), color = self.fg_color)

        # Plot the t value
        if p >= 0.005 and p <= 0.995:
            self.ax[1].plot([t, t], [0, scstats.t.pdf(t, dof)], color = 'orange')
            
        # Update the graph
        self.fig.canvas.draw()

        # Update the label
        self.status_label.config(text = f"T value: {round(t, 2)}, P value: {round(p, 2)}, {'Significant' if p < 0.05 else 'Insignificant'}")            
            
