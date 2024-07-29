# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 14:57:26 2024

@author: EliteBook 840
Made by: Leor, Kevin and Harsh 
"""

import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import Canvas, messagebox
import threading
import time

class DataGenerator:
    def __init__(self):
        pass

    def _generate_random(self, n_samples):
        return np.random.rand(n_samples)

    @property
    def generated_data(self):
        n_samples = 20
        random_values = self._generate_random(n_samples)
        m = 21
        c = 18
        output = (m-c) * random_values + c
        return output

class DisplayApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Temperature Display App")
        self.canvas_height = 450  # Increased canvas height by 100 pixels
        self.canvas = Canvas(self.root, width=800, height=self.canvas_height, bg="white")
        self.value_generator = DataGenerator()
        self.values = self.value_generator.generated_data
        self.dynamic_data_thread = None
        self.dynamic_data_running = False
        self.show_data = False
        self.info_text_ids = []  # Keep track of info text objects
        self.init_ui()

    def init_ui(self):
        self.update_button = tk.Button(self.root, text="Go", command=self.toggle_dynamic_movement)
        self.update_button.pack()
        self.info_button = tk.Button(self.root, text="Show Info", command=self.toggle_show_info)
        self.info_button.pack()
        self.canvas.pack()
        self.draw_lines()  # Initial drawing
        self.add_humidity_text()  # Add humidity text box
        self.start_dynamic_data_thread()

    def start_dynamic_data_thread(self):
        self.dynamic_data_thread = threading.Thread(target=self.update_data_series)
        self.dynamic_data_thread.daemon = True
        self.dynamic_data_thread.start()

    def update_data_series(self):
        while True:
            if self.dynamic_data_running:
                self.values = np.roll(self.values, -1)  # Remove first item
                self.values[-1] = np.random.uniform(18, 21)  # Add new random value
                self.draw_lines()  # Update canvas
                if self.show_data:  # Update info text only if show_data is True
                    self.update_info_text()  # Update info text
                time.sleep(0.5)  # Sleep for 0.5 seconds

    def toggle_dynamic_movement(self):
        self.dynamic_data_running = not self.dynamic_data_running
        if self.dynamic_data_running:
            self.update_button.config(text="Stop")
        else:
            self.update_button.config(text="Go")

    def toggle_show_info(self):
        self.show_data = not self.show_data
        if self.show_data:
            self.info_button.config(text="Hide Info")
            self.update_info_text()  # Update info text if show_data is True
        else:
            self.info_button.config(text="Show Info")
            self.canvas.delete("info")  # Clear info text

    def update_info_text(self):
        min_value = min(self.values)
        max_value = max(self.values)
        value_range = max_value - min_value
        # Clear existing info text
        self.canvas.delete("info")
        self.info_text_ids.clear()  # Clear info text ids list
        for i, value in enumerate(self.values):
            x_pos = 100 + i * 30  # Increased separation of the left-hand bar
            y_pos = 200 - (value - 18) / 3 * 180
            info_text_id = self.canvas.create_text(x_pos + 5, y_pos, text=f"{value:.2f}", fill="black", tags="info")
            self.info_text_ids.append(info_text_id)  # Add info text id to list

    def draw_lines(self):
        self.canvas.delete("all")  # Clear canvas
        min_value = min(self.values)
        max_value = max(self.values)
        value_range = max_value - min_value
        spacing = (self.canvas_height - 100) / (len(self.values) - 1)  # Adjust spacing dynamically based on canvas height
        rect_width = 40
        smooth_values = [(80 + i * 30, 200 - (value - min_value) / value_range * 180) for i, value in enumerate(self.values)]
        for i in range(len(smooth_values) - 1):
            x1, y1 = smooth_values[i]
            x2, y2 = smooth_values[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill="green", width=2, tags="line", smooth='true')
            dot_id = self.canvas.create_rectangle(x1 - 3, y1 - 3, x1 + 3, y1 + 3, fill="red", tags="dot")  # Draw a red dot at each data point
        # Draw the last red dot
        x_last, y_last = smooth_values[-1]
        self.canvas.create_rectangle(x_last - 3, y_last - 3, x_last + 3, y_last + 3, fill="red", tags="dot")
        
        # Draw numeric scale on the left side
        scale_values = np.arange(18, max_value + 0.2, 0.2)
        for value in scale_values:
            y_pos = 200 - (value - 18) / value_range * 180
            self.canvas.create_text(60, y_pos, text=f"{value:.2f}", fill="black", anchor="e")  # Adjusted position for the left-hand bar
        # Add "Humidity over time" text box at the bottom
        self.add_humidity_text()
         
    def add_humidity_text(self):
        # Add "Humidity over time" text box at the bottom
        self.canvas.create_text(400, self.canvas_height - 20, text="Humidity over time", fill="black", font=("Helvetica", 12,"normal"), anchor="center")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DisplayApp()
    app.run()
