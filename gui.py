#!/usr/bin/env python3.10

import tkinter as tk
import tkinter.ttk
from tkinter import filedialog


def root_window():
    root = tk.Tk()
    root.title("Plate Map Converter")

    root.resizable(False, False)

    # window.attributes('-fullscreen',True)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 1080
    window_height = 720

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    root.grid_columnconfigure(1, weight=1)

    main_frame = tk.LabelFrame(root, padx=10, pady=10)
    main_frame.pack(fill="both")

    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=1)

    nw_frame = tk.LabelFrame(main_frame, padx=10, pady=10)
    nw_frame.grid(column=0, columnspan=2, row=0, rowspan=1, padx=10, pady=10, sticky='nsew')
    # ne_frame = tk.LabelFrame(main_frame, padx=10, pady=10)
    # ne_frame.grid(column=1, columnspan=1, row=0, rowspan=1, padx=10, pady=10, sticky='nsew')
    sw_frame = tk.LabelFrame(main_frame, padx=10, pady=10)
    sw_frame.grid(column=0, columnspan=1, row=1, rowspan=1, padx=10, pady=10, sticky='nsew')
    se_frame = tk.LabelFrame(main_frame, padx=10, pady=10)
    se_frame.grid(column=1, columnspan=1, row=1, rowspan=1, padx=10, pady=10, sticky='nsew')

    tk.Label(nw_frame, text="Input / Output").grid(column=0, columnspan=1,
                                                   row=0, rowspan=1,
                                                   padx=10, pady=10,
                                                   sticky='w')

    input_text = tk.StringVar()
    input_text.set(value="Select Input File...")

    input_label = tk.Label(sw_frame, textvariable=input_text, text="text")
    input_label.grid(column=0, columnspan=1, row=0, rowspan=1, padx=10, pady=10, sticky='w')


    def input_file_prompt():
        input_file_name = filedialog.askopenfile(initialdir="your directory path",
                                                 title="Input File",
                                                 filetypes=(("csv files", "*.csv"),
                                                              ("all files", "*.*")))

    tk.Button(nw_frame, text="Input File",
                             command=input_file_prompt, width=20).grid(column=0, columnspan=1,
                                                             row=1, rowspan=1,
                                                             padx=10, pady=10,
                                                             sticky='w')

    output_text = tk.StringVar()
    output_text.set(value="Select Output File...")

    output_label = tk.Label(nw_frame, textvariable=input_text, text="text")
    output_label.grid(column=0, columnspan=1, row=2, rowspan=1, padx=10, pady=10, sticky='w')


    def output_file_prompt():
        output_file_name = filedialog.askopenfile(initialdir="your directory path",
                                                 title="Output File",
                                                 filetypes=(("csv files", "*.csv"),
                                                              ("all files", "*.*")))

    output_text = tk.Entry(nw_frame, width=50).grid(column=0, columnspan=1,
                                                             row=3, rowspan=1,
                                                             padx=10, pady=10,
                                                             sticky='w')

    tk.Label(sw_frame, text="96 Well Options").grid(column=0, columnspan=1,
                                                  row=0, rowspan=1,
                                                  padx=10, pady=10,
                                                  sticky='w')

    input_radio_var = tk.IntVar()

    ir0 = tk.Radiobutton(sw_frame, text="96 Square <-> 96 Long", variable=input_radio_var, value=0)
    ir0.grid(column=0, columnspan=1, row=1, rowspan=1, padx=10, pady=10, sticky='w')
    ir1 = tk.Radiobutton(sw_frame, text="96 -> Q1", variable=input_radio_var, value=1)
    ir1.grid(column=0, columnspan=1, row=2, rowspan=1, padx=10, pady=10, sticky='w')
    ir2 = tk.Radiobutton(sw_frame, text="96 -> Q2", variable=input_radio_var, value=2)
    ir2.grid(column=0, columnspan=1, row=3, rowspan=1, padx=10, pady=10, sticky='w')
    ir3 = tk.Radiobutton(sw_frame, text="96 -> Q3", variable=input_radio_var, value=3)
    ir3.grid(column=0, columnspan=1, row=4, rowspan=1, padx=10, pady=10, sticky='w')
    ir4 = tk.Radiobutton(sw_frame, text="96 -> Q4", variable=input_radio_var, value=4)
    ir4.grid(column=0, columnspan=1, row=5, rowspan=1, padx=10, pady=10, sticky='w')

    tk.Label(se_frame, text="384 Well Options").grid(column=0, columnspan=1,
                                                  row=0, rowspan=1,
                                                  padx=10, pady=10,
                                                  sticky='w')

    output_radio_var = tk.IntVar()

    or0 = tk.Radiobutton(se_frame, text="384 Square <-> 384 Long", variable=output_radio_var,
                         value=0)
    or0.grid(column=0, columnspan=1, row=1, rowspan=1, padx=10, pady=10, sticky='w')
    or1 = tk.Radiobutton(se_frame, text="384 -> 96", variable=output_radio_var, value=1)
    or1.grid(column=0, columnspan=1, row=2, rowspan=1, padx=10, pady=10, sticky='w')
    or2 = tk.Radiobutton(se_frame, text="384 -> 96 x 4Q", variable=output_radio_var, value=1)
    or2.grid(column=0, columnspan=1, row=3, rowspan=1, padx=10, pady=10, sticky='w')
    or3 = tk.Radiobutton(se_frame, text="384 -> Q1", variable=output_radio_var, value=0)
    or3.grid(column=0, columnspan=1, row=4, rowspan=1, padx=10, pady=10, sticky='w')
    or4 = tk.Radiobutton(se_frame, text="384 -> Q2", variable=output_radio_var, value=0)
    or4.grid(column=0, columnspan=1, row=5, rowspan=1, padx=10, pady=10, sticky='w')
    or5 = tk.Radiobutton(se_frame, text="384 -> Q3", variable=output_radio_var, value=0)
    or5.grid(column=0, columnspan=1, row=6, rowspan=1, padx=10, pady=10, sticky='w')
    or6 = tk.Radiobutton(se_frame, text="384 -> Q4", variable=output_radio_var, value=0)
    or6.grid(column=0, columnspan=1, row=7, rowspan=1, padx=10, pady=10, sticky='w')

    return root


def run_gui():
    root = root_window()
    root.mainloop()