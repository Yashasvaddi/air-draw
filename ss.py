import easyocr
import tkinter as tk
from tkinter import messagebox

# Create a reader object for the languages you want (e.g., English)
reader = easyocr.Reader(['en'], verbose=False)

# Read text from an image file
image_path = "C:\\Users\\YASHAS\\Pictures\\virtual ss\\drawing.png"
result = reader.readtext(image_path)

# Extract the text
extracted_text = "\n".join([detection[1] for detection in result])

# Create a dialog box to display the extracted text
def show_text():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    if extracted_text:
        messagebox.showinfo("Extracted Text", extracted_text)
    else:
        messagebox.showwarning("No Text Found", "No text was found in the image.")

show_text()
