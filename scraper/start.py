import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

from scrapy.crawler import CrawlerProcess
from scraper.spiders.kinopoisk import KinopoiskSpider
from scrapy.utils.project import get_project_settings

def create_gui():
    # Create a new Tkinter window
    root = tk.Tk()

    # Set the title of the window
    root.title("KinoExport")

    # Set the window size to 200x200 and center it on the screen
    window_width = 200
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width/2) - (window_width/2))
    y = int((screen_height/2) - (window_height/2))
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

    # Set the window to be non-resizable
    root.resizable(False, False)

    # Create a label for the user ID field
    user_id_label = ttk.Label(root, text="User ID:")
    user_id_label.pack()

    # Create an entry widget for the user ID field
    user_id_entry = ttk.Entry(root)
    user_id_entry.pack()

    # Create a label for the Ya Sess ID field
    ya_sess_id_label = ttk.Label(root, text="Ya Sess ID:")
    ya_sess_id_label.pack()

    # Create an entry widget for the Ya Sess ID field
    ya_sess_id_entry = ttk.Entry(root)
    ya_sess_id_entry.pack()

    user_id = ''
    ya_sess_id = ''

    def submit_form():
        user_id = user_id_entry.get()
        ya_sess_id = ya_sess_id_entry.get()
        start_crawler(user_id, ya_sess_id)
        messagebox.showinfo("Processing", "Processing complete")
        root.destroy()

    # Create a submit button
    submit_button = tk.Button(root, text="Submit", command=submit_form)
    submit_button.pack()

    # Start the tkinter event loop
    root.mainloop()

def start_crawler(user_id, ya_sess_id):
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(KinopoiskSpider)
    process.crawl(KinopoiskSpider, input='inputargument', user_id=user_id, ya_sess_id=ya_sess_id)
    process.start()


if __name__ == "__main__":
    if os.path.exists("ratings.csv"):
        os.remove("ratings.csv")
    create_gui()