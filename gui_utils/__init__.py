#!/usr/bin/env python3

import customtkinter as ctk


class BrowseFile(ctk.CTkFrame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.filePath = ctk.StringVar()

        self.entry = ctk.CTkEntry(self, textvariable=self.filePath, width=200)
        self.entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)

        self.browse_button = ctk.CTkButton(
            self, text="Browse", command=self.browse_file
        )
        self.browse_button.pack(side="right", padx=(5, 10), pady=10)

    def browse_file(self):
        # Open the file dialog to choose a file
        file_path = ctk.filedialog.askopenfilename()

        # Update the entry with the selected file path
        if file_path:  # Ensure a file path was selected
            self.filePath.set(file_path)
