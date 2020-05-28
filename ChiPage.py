from DefaultWindow import DefaultWindow

import tkinter as tk

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt

import numpy as np
import pandas as pd
from scipy import stats as scstats

import random
import os
import math
from collections import Counter
import pickle


# NOTE - USE GLOBAL VARIABLES ONLY FOR FUNCTIONS, UI ELEMENTS AND THOSE DEFINED IN INIT

class ChiPage(DefaultWindow):
    '''ChiPage class for the Chi Square simulation'''


    def __init__(self, parent):
        
        # Super instantiation
        super().__init__(parent, width = 1000, height = 800)

        # Placing title label
        tk.Label(self.frame, text = 'Chi Square Simulation', height = 2, fg = self.fg_color, bg = self.bg_color, font = self.title_font).pack()

        # Initialise  buttons
        self.button_frame = tk.Frame(self.frame, bg = self.bg_color)
        
        tk.Button(self.button_frame, text = 'Input data', height = 2, font = self.normal_font, command = self._input_chosen, padx = 10).pack(padx = 20, expand = True, fill = tk.X, side = 'left')
        tk.Button(self.button_frame, text = 'Random 2x2', height = 2, font = self.normal_font, command = self._random_2_chosen, padx = 10).pack(padx = 20, expand = True, fill = tk.X, side = 'left')
        tk.Button(self.button_frame, text = 'Random 3x3', height = 2, font = self.normal_font, command = self._random_3_chosen, padx = 10).pack(padx = 20, expand = True, fill = tk.X, side = 'left')

        self.button_frame.pack()

        # Instantiate variables - data
        self.sample_size = None
        self.data_values = None
        self.dof = None
        self.default_table = None
        self.default_sample = None

        # Instantiate variables - graph
        self.nearest_square = None
        self.data = None
        self.data2 = None
        self.line_shown = False

        # Instantiate variables - animation
        self.cycle_count = None
        self.total_runs = None


    def _input_chosen(self):

        # Clear screen
        self.button_frame.destroy()

        # Add instruction label
        self.inst = tk.Label(self.frame, text = 'Input a table below, with a 2x2 or bigger table', height = 2, fg = self.fg_color, bg = self.bg_color, font = self.normal_font)
        self.inst.pack()

        # Input table
        self.table_frame = tk.Frame(self.frame, bg = self.bg_color, highlightbackground = self.fg_color, highlightthickness = 1)
        self.default_table = True
        self.default_sample = True

        self.entries = [[] for i in range(4)]
        for row in range(4):
            for col in range(4):
                if row == 0 and col == 0:
                    pass
                elif row == 0 or col == 0:
                    entry = tk.Entry(self.table_frame, bg = self.bg_color, font = self.normal_font)
                    entry.insert(tk.END, 'Title')
                    entry.bind("<Button-1>", self._clear_instructions)
                    entry.grid(row = row, column = col)
                    self.entries[row].append(entry)
                else:
                    entry = tk.Entry(self.table_frame, bg = self.bg_color, font = self.normal_light_font)
                    entry.bind("<Button-1>", self._clear_instructions)
                    entry.grid(row = row, column = col)
                    self.entries[row].append(entry)

        self.table_frame.pack(padx = 20, pady = 20)

        # Sample size
        self.sample_entry = tk.Entry(self.frame, bg = self.bg_color, font = self.normal_light_font)
        self.sample_entry.insert(tk.END, 'Sample size')
        self.sample_entry.bind("<Button-1>", self._sample_clear)
        self.sample_entry.pack(padx = 20, pady = (0, 20))

        # Submit button
        self.button_go = tk.Button(self.frame, text = 'Go', height = 2, width = 10, font = self.normal_font, command = self._input_run, padx = 10)
        self.button_go.pack()

        self.label_status = tk.Label(self.frame, text = '', bg = self.bg_color, fg = self.fg_color, height = 2, font = self.normal_light_font)
        self.label_status.pack()

        # Second frame
        self.files_frame = tk.Frame(self.frame, bg = self.bg_color, padx = 20, pady = 20)

        files_button_frame = tk.Frame(self.files_frame, bg = self.bg_color, padx = 20, pady = 20, width = 40)
        
        tk.Button(files_button_frame, text = 'Import file', height = 2, width = 10, font = self.normal_font, command = self._import_chosen, padx = 20).pack(side = 'left', padx = 10)
        tk.Button(files_button_frame, text = 'Export file', height = 2, width = 10, font = self.normal_font, command = self._export_chosen, padx = 20).pack(side = 'right', padx = 10)

        files_button_frame.pack(side = 'bottom', padx = 20)

        self.files_frame.pack(side = 'bottom', fill = tk.BOTH, expand = True)


    def _import_chosen(self):
        
        try:

            # Get files
            file_name = tk.filedialog.askopenfilename(initialdir = os.path.join("/Users", os.environ["USER"], "Desktop", "save.stat"), filetypes = (("Stat Files", "*.stat"),))
            if not file_name:
                return False
            self.data_values, self.sample_size = pickle.load(open(file_name, "rb"))
            
            # Discard elements
            self.table_frame.destroy()
            self.button_go.destroy()
            self.sample_entry.destroy()
            self.inst.destroy()
            self.files_frame.destroy()
            
            # Generate simulation page
            self._simulation_page()
            
        except Exception as e:
            self.label_status['text'] = 'Error'


    def _export_chosen(self):
        self._input_run(export = True)


    def _clear_instructions(self, event):
        if self.default_table:
            self.default_table = False
            for i in self.entries:
                for j in i:
                    j.delete(0, tk.END)


    def _sample_clear(self, event):
        if self.default_sample:
            self.default_sample = False
            self.sample_entry.delete(0, tk.END)


    def _input_run(self, export = False):
        
        # Read inputs from entries, saving in the values Np Array
        values = [[] for i in range(4)]
        values[0].append('_')
        for entry_row_int, entry_row in enumerate(self.entries):
            for entry in entry_row:
                values[entry_row_int].append(entry.get().strip())
        values = np.array(values)
        
        # Check if at least 2 rows and 2 columns are given, with titles
        if not all(values[0:3, 0:3].flatten().tolist()):
            self.label_status['text'] = 'Invalid, must have at least 2 rows and columns, with titles'
            return False

        shape = [2, 2]
        
        # Check that if a third column / row is given it's full, with titles
        if any(values[3].tolist()):
            if not (values[3][0] and values[3][1] and values[3][2]):
                self.label_status['text'] = 'Invalid, can\'t have a partial row'
                return False
            shape[0] = 3

        if any(values[:, 3].tolist()):
            if not (values[0][3] and values[1][3] and values[2][3]):
                self.label_status['text'] = 'Invalid, can\'t have a partial column'
                return False
            shape[1] = 3

        if any(values[3]) and any(values[:, 3].tolist()):
            if not (values[3][3]):
                self.label_status['text'] = 'Invalid, can\'t have a partial rows / colummns'
                return False

        values[0, 0] = ''

        # Check that all column titles are strings
        for item in values[0][1:shape[0] + 1]:
            for i in item:
                if i.isdigit():
                    self.label_status['text'] = 'Invalid, column titles may not have numbers in them'
                    return False

        # Check that all row titles are strings
        for item in values.T[0][1:shape[0] + 1]:
            for i in item:
                if i.isdigit():
                    self.label_status['text'] = 'Invalid, row titles may not have numbers in them'
                    return False

        # Check that all row and columns have unique names
        names = list(values[0][1:shape[1] + 1]) + list(values.T[0][1:shape[0] + 1])
        for i in range(len(names)):
            names[i] = names[i].strip()
        names = set(names)
        if len(names) != sum(shape):
            self.label_status['text'] = 'Invalid, row and column titles must all be unique'
            return False

        # Check if all values are integers! 
        try:
            values_only = values[1:shape[0] + 1, 1:shape[1] + 1].astype(np.int)
        except Exception:
            self.label_status['text'] = 'Invalid, data values need to be integers'
            return False

        # Check for null rows
        for row in values_only:
            if not any(row):
                self.label_status['text'] = 'Invalid, may not have null rows'
                return False

        # Check for null columns
        for col in values_only.T:
            if not any(col):
                self.label_status['text'] = 'Invalid, may not have null columns'
                return False

        # Check if sample size is given
        if self.sample_entry.get().strip():
            try:
                self.sample_size = int(self.sample_entry.get())
            except Exception:
                self.label_status['text'] = 'Invalid, sample size must be an integer'
                return False
        else:
            self.label_status['text'] = 'Invalid, sample size must be given'
            return False

        # Check if sum > sample size
        if sum(values_only.flatten()) < self.sample_size:
            self.label_status['text'] = 'Invalid, sample size must be smaller than the number of data points'
            return False

        # Check if sample size is a multiple of 10
        if self.sample_size % 10 != 0:
            self.label_status['text'] = 'Invalid, sample size must be a multiple of 10'
            return False
            
        # Generate data_values with the full list version of a pd df
        rows = values[:, 0][1:shape[0] + 1]
        cols = values[0][1:shape[1] + 1]
        self.data_values = self.make_df(values_only.tolist(), rows, cols)

        if not export:

            # Discard elements
            self.table_frame.destroy()
            self.button_go.destroy()
            self.sample_entry.destroy()
            self.inst.destroy()
            self.files_frame.destroy()
            
            # Generate function
            self._simulation_page()
            
        else:
            try:
                data_export = (self.data_values, self.sample_size)
                pickle.dump(data_export, open(os.path.join("/Users", os.environ["USER"], "Desktop", "save.stat"), "wb"))
            except Exception:
                self.label_status['text'] = 'Error'


    def _random_2_chosen(self):

        # Formatting data for use
        data = [[random.randint(211, 225), random.randint(211, 225)], [random.randint(211, 225), random.randint(211, 225)]]
        columns = ["Democrats", "Republicans"]
        rows = ["Men", "Women"]
        self.data_values = self.make_df(data, rows, columns)
        self.sample_size = 100

        # Starts generation
        self.button_frame.destroy()
        self._simulation_page()


    def _random_3_chosen(self):

        # Formatting data for use
        data = [[random.randint(94, 100), random.randint(94, 100), random.randint(94, 100)], [random.randint(94, 100), random.randint(94, 100), random.randint(94, 100)], [random.randint(94, 100), random.randint(94, 100), random.randint(94, 100)]]
        columns = ["Democrats", "Republicans", "Independent"]
        rows = ["Men", "Women", "Undeclared"]
        self.data_values = self.make_df(data, rows, columns)
        self.sample_size = 100

        # Starts generation
        self.button_frame.destroy()
        self._simulation_page()


    def make_df(self, data, rows, columns):
        df = pd.DataFrame.from_records(data, index = rows, columns = columns)
        df.loc['Total'] = df.sum(numeric_only=True, axis=0)
        df.loc[:,'Total'] = df.sum(numeric_only=True, axis=1)
        data_values = df.reset_index().T.reset_index().T.values
        data_values[0, 0] = ''
        return data_values


    def _simulation_page(self):

        # Initialise components - table
        table_frame = tk.Frame(self.frame, bg = self.bg_color, highlightbackground = self.fg_color, highlightthickness = 1)
        
        for row in range(self.data_values.shape[0]):
            for col in range(self.data_values.shape[1]):
                if row == 0 or col == 0:
                    tk.Label(table_frame, text = self.data_values[row, col], bg = self.bg_color, font = self.normal_font).grid(row = row, column = col)
                else:
                    tk.Label(table_frame, text = self.data_values[row, col], bg = self.bg_color, font = self.normal_light_font).grid(row = row, column = col)

        table_frame.pack()

        # Initialise simulation
        self.cycle_count = 0
        self.nearest_square = math.ceil(self.data_values[-1, -1] ** 0.5)

        # Configure graph
        plt.style.use('fast')
        self.fig, self.ax = plt.subplots(1, 2)
        self.fig.patch.set_facecolor(self.bg_color)
        self.ax[0].set_title('Random choice')
        self.ax[0].get_yaxis().set_visible(False)
        self.ax[0].get_xaxis().set_visible(False)
        self.ax[1].set_title('Chi Square Distribution')
        self.ax[1].set_facecolor(self.bg_color)
        self.ax[1].get_yaxis().set_visible(False)

        # Set data
        self.total_runs = 0
        self.data = np.zeros((self.nearest_square, self.nearest_square)) + 0.06
        self.data2 = []
        self.plot = self.ax[0].imshow(self.data, cmap='binary', vmin = 0, vmax = 1)
        self.ax[1].hist(self.data2)

        # Display graph
        canvas = FigureCanvasTkAgg(self.fig, master = self.frame)
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill = tk.BOTH, expand = True)

        # Initialise new button frame
        bottom_frame = tk.Frame(self.frame, bg = self.bg_color)
        button_frame = tk.Frame(bottom_frame, bg = self.bg_color)
        
        self.button_start = tk.Button(button_frame, text = 'Run once', height = 2, font = self.normal_font, command = self._run, padx = 10)
        self.button_start.pack(expand = True, fill = tk.X, side = 'left')

        self.button_start2 = tk.Button(button_frame, text = 'Run 100 times', height = 2, font = self.normal_font, command = self._run_100, padx = 10)
        self.button_start2.pack(padx = 20, expand = True, fill = tk.X, side = 'left')

        self.button_start3 = tk.Button(button_frame, text = 'Run 1000 times', height = 2, font = self.normal_font, command = self._run_1000, padx = 10)
        self.button_start3.pack(expand = True, fill = tk.X, side = 'left')

        self.line_shown = False
        tk.Button(button_frame, text = 'Show line', height = 2, font = self.normal_font, command = self._show_line, padx = 10).pack(padx = 20, expand = True, fill = tk.X, side = 'left')

        button_frame.pack(pady = (0, 20))
        
        self.chi_label = tk.Label(bottom_frame, text = '', bg = self.bg_color, font = self.normal_light_font)
        self.chi_label.pack(pady = (0, 20))

        bottom_frame.pack()
            

    def _run(self):

        # Animate for a 100 points
        if self.cycle_count < 10:
            self.button_start['state'] = tk.DISABLED
            self.button_start2['state'] = tk.DISABLED
            self.button_start3['state'] = tk.DISABLED
            for _ in range(int(self.sample_size / 10)):
                point = (random.randint(0, self.nearest_square - 1), random.randint(0, self.nearest_square - 1))
                while self.data[point[0], point[1]] != 0.06:
                    point = (random.randint(0, self.nearest_square - 1), random.randint(0, self.nearest_square - 1))
                self.data[point[0], point[1]] = 0.89
            self.plot.set_data(self.data)
            self.fig.canvas.draw()
            self.canvas_widget.after(100, self._run)
            self.cycle_count += 1
        else:
            self.cycle_count = 0
            self.total_runs += 1
            self.button_start['state'] = tk.NORMAL
            self.button_start2['state'] = tk.NORMAL
            self.button_start3['state'] = tk.NORMAL
            self.data = np.zeros((self.nearest_square, self.nearest_square)) + 0.06
            try:
                self._chi(single = True)
                self._chi_update()
            except ValueError:
                self.chi_label['text'] = 'Error: Got a 0 column'


    def _run_100(self):
        self.button_start['state'] = tk.DISABLED
        self.button_start2['state'] = tk.DISABLED
        self.button_start3['state'] = tk.DISABLED
        for _ in range(100):
            try:
                self._chi()
            except ValueError:
                continue
        self.button_start['state'] = tk.NORMAL
        self.button_start2['state'] = tk.NORMAL
        self.button_start3['state'] = tk.NORMAL
        self.total_runs += 100
        self._chi_update()
        self.chi_label['text'] = ''


    def _run_1000(self):
        self.button_start['state'] = tk.DISABLED
        self.button_start2['state'] = tk.DISABLED
        self.button_start3['state'] = tk.DISABLED
        for _ in range(100):
            try:
                self._chi()
            except ValueError:
                continue
        self.button_start['state'] = tk.NORMAL
        self.button_start2['state'] = tk.NORMAL
        self.button_start3['state'] = tk.NORMAL
        self.total_runs += 1000
        self._chi_update()
        self.chi_label['text'] = ''
        

    def _show_line(self):
        if self.line_shown:
            self.line_shown = False
            self._chi_update()
        else:
            self.line_shown = True
            self._chi_update()


    def _chi(self, single = False):
        
        # Make random selection
        counter = 0
        weights = []
        data_og = self.data_values[1:-1, 1:-1]
        data_prob = data_og.flatten()
        data_prob = data_prob / sum(data_prob)
        choices = random.choices(range(len(data_prob)), data_prob, k = self.sample_size)
        new_data = list(Counter(choices).items())

        if len(new_data) != len(data_prob):
            chosen_elements = set()
            for i in new_data:
                if i[0] not in chosen_elements:
                    chosen_elements.add(i[0])
            unchosen = set(range(len(data_prob))) - chosen_elements
            for i in list(unchosen):
                new_data.append((i, 0))
        new_data = np.array([j for i,j in sorted(new_data)]).reshape(data_og.shape)

        # Chi runner
        try:
            chi2, p, self.dof, expected = scstats.chi2_contingency(new_data, correction = False)
            self.data2.append(chi2)
            if single:
                self.chi_label['text'] = f'Chi Squared Value: {round(chi2, 4)}, degrees of freedom: {self.dof}, p-value: {round(p, 4)}'
        except Exception:
            raise ValueError
            

    def _chi_update(self):
        self.ax[1].cla()
        self.ax[1].hist(self.data2, bins = 50)
        self.ax[1].set_title('Chi Square Distribution')
        try:
            if self.line_shown:
                x = np.linspace(0.01, max(self.data2), 50)
                area = len(self.data2) * (x[1] - x[0])
                self.ax[1].plot(x, area * scstats.chi2.pdf(x, df = self.dof), color='r', lw=2)
        except Exception:
            pass
        self.fig.canvas.draw()
        if self.total_runs >= 10000:
            self.button_start['state'] = tk.DISABLED
            self.button_start2['state'] = tk.DISABLED
            self.button_start3['state'] = tk.DISABLED
