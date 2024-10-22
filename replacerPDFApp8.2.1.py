import os
import tkinter as tk
from tkinter import scrolledtext, filedialog, Canvas, Listbox, BooleanVar
import fitz  # PyMuPDF
from PIL import Image, ImageTk

import re

# adds the right logic. also kinda working? pack-> grid. ported version 8 to version 6.

# Global variables to track the PDF document and current page
pdf_doc = None
current_page = 0
auto_process = None

def process_text_helper(text):
    # Replace all newline characters with a space
    text = text.replace('\n', ' ')
    
    # Add a line break before numbers followed by a period and space, while keeping the period number space format
    # text = re.sub(r'\s(\d+)\.\s', r'.\1 ', text)
    
    # Add a line break before Roman numerals followed by a period and space
    text = re.sub(r'(\b[IVXLCDM]+\b)\.\s', r'\n\n \1. ', text)
    
    # Add a line break before capital letters followed by a period and space
    text = re.sub(r'(\b[A-Z]\b)\.\s', r'\n\n\1. ', text)

    # Add a line break before capital letters (without a period) followed by a period and space
    text = re.sub(r'(\b[A-Z]\b)\s', r'\n\n\1. ', text)

    # Add a line break before number followed by a period and space
    text = re.sub(r'(\s[\d+]\b)\.\s', r'\n\n.\1 ', text)

    # Add a line break before number followed by a period and space
    text = re.sub(r'(\s[a-z]\b)\.\s', r'\n\n.\1 ', text)

    # Replace consecutive spaces with single space
    text = re.sub(r'[ ]{2,}', ' ', text)
    
    return text

# Function to replace newlines with spaces
def process_text():
    # Get the content from the input text box
    input_text = text_box.get("1.0", tk.END)

    modified_text = process_text_helper(input_text)
    # Clear the output text box and insert the modified text
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, modified_text)

# Function to replace newlines with spaces
def replace_newlines():
    process_text()
    return

    # input_text = text_box.get("1.0", tk.END)
    # modified_text = input_text.replace("\n", " ").strip()
    # output_box.delete("1.0", tk.END)
    # output_box.insert(tk.END, modified_text)

# Function to clear the top text box
def clear_text():
    text_box.delete("1.0", tk.END)

# Function to copy output text to clipboard
def copy_to_clipboard():
    output_text = output_box.get("1.0", tk.END).strip()
    root.clipboard_clear()
    root.clipboard_append(output_text)

# Function to open PDF file dialog and display the selected PDF
def open_pdf():
    global pdf_doc, current_page
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf_doc = fitz.open(file_path)
        current_page = 0  # Start at the first page
        display_pdf_page(current_page)

# Function to display a specific page of the PDF and extract its text
def display_pdf_page(page_num):
    global pdf_doc, current_page
    
    if pdf_doc is None:
        return
    
    # Load and render the specified page
    page = pdf_doc.load_page(page_num)
    pix = page.get_pixmap()
    
    # Convert the pixmap to an image format tkinter can use
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img = ImageTk.PhotoImage(img)
    
    # Clear the previous content of the canvas
    pdf_canvas.delete("all")
    
    # Update the canvas size to match the image
    pdf_canvas.config(width=img.width(), height=img.height())
    
    # Display the image in the canvas
    pdf_canvas.create_image(0, 0, anchor=tk.NW, image=img)
    
    # Keep a reference to the image to prevent garbage collection
    pdf_canvas.image = img
    
    # Extract text from the specified page
    pdf_text = page.get_text("text")
    
    # Display extracted text in the first text box
    text_box.delete("1.0", tk.END)  # Clear the first text box
    text_box.insert(tk.END, pdf_text)  # Insert the extracted text into the first text box

    # Auto-process the text if the toggle is enabled
    if auto_process.get():
        replace_newlines()
    
    # Update button states
    update_button_states()

# Function to go to the previous page
def previous_page():
    global current_page
    if current_page > 0:
        current_page -= 1
        display_pdf_page(current_page)

# Function to go to the next page
def next_page():
    global current_page
    if pdf_doc is not None and current_page < pdf_doc.page_count - 1:
        current_page += 1
        display_pdf_page(current_page)

# Function to update the state of the navigation buttons
def update_button_states():
    if current_page == 0:
        prev_button.config(state=tk.DISABLED)
    else:
        prev_button.config(state=tk.NORMAL)
    
    if pdf_doc is not None and current_page == pdf_doc.page_count - 1:
        next_button.config(state=tk.DISABLED)
    else:
        next_button.config(state=tk.NORMAL)

# Function to load PDF when selected from the Listbox
def load_pdf_from_list(event):
    global pdf_doc, current_page
    selection = pdf_listbox.curselection()
    if selection:
        pdf_name = pdf_listbox.get(selection[0])
        file_path = os.path.join("pdfs", pdf_name)
        if os.path.isfile(file_path):
            pdf_doc = fitz.open(file_path)
            current_page = 0
            display_pdf_page(current_page)

# Function to list all PDFs in the "pdfs" directory
def list_pdfs():
    pdf_listbox.delete(0, tk.END)  # Clear the Listbox
    if not os.path.exists("pdfs"):
        os.makedirs("pdfs")  # Create the directory if it doesn't exist
    
    pdf_files = [f for f in os.listdir("pdfs") if f.endswith(".pdf")]
    for pdf in pdf_files:
        pdf_listbox.insert(tk.END, pdf)  # Add PDFs to the Listbox

# Create the root window
root = tk.Tk()
root.title("Text and PDF Viewer with Page Navigation")
root.geometry("1200x600")  # Adjust window size for the PDF viewer

# Initialize the BooleanVar for the auto-process toggle
auto_process = BooleanVar()

# Top Frame - Auto Process Toggle
top_frame = tk.Frame(root)
top_frame.grid(row=0, column=0, columnspan=2, sticky='ew', padx=10, pady=5)

# Toggle for auto-processing text
auto_process_toggle = tk.Checkbutton(top_frame, text="Auto-process text", variable=auto_process)
auto_process_toggle.pack(side=tk.LEFT, padx=10)

# Left side - Text processing
left_frame = tk.Frame(root)
left_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

# Create a label for input
label_input = tk.Label(left_frame, text="Paste your text below:")
label_input.pack(pady=10)

# Create a text box for the input text
text_box = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, width=40, height=10)
text_box.pack(padx=10, pady=10)

# Create a frame to hold the buttons
button_frame = tk.Frame(left_frame)
button_frame.pack(pady=10)

# Create a button to trigger the newline replacement
replace_button = tk.Button(button_frame, text="Replace Newlines with Spaces", command=replace_newlines)
replace_button.pack(side=tk.LEFT, padx=5)

# Create a button to copy output text to clipboard
copy_button = tk.Button(button_frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(side=tk.LEFT, padx=5)

# Create a button to clear the top text box
clear_button = tk.Button(button_frame, text="Clear Text", command=clear_text)
clear_button.pack(side=tk.LEFT, padx=5)

# Create a label for output
label_output = tk.Label(left_frame, text="Resulting text:")
label_output.pack(pady=10)

# Create a text box for displaying the modified text
output_box = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, width=40, height=10)
output_box.pack(padx=10, pady=10)

# Right side - PDF viewer
right_frame = tk.Frame(root)
right_frame.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

# Create a button to open a PDF file manually
pdf_button = tk.Button(right_frame, text="Open PDF", command=open_pdf)
pdf_button.pack(pady=10)

# Create a canvas to display the PDF page
pdf_canvas = Canvas(right_frame, width=400, height=500, bg="white")
pdf_canvas.pack(padx=10, pady=10)

# Navigation buttons (Previous, Next)
nav_frame = tk.Frame(right_frame)
nav_frame.pack(pady=10)

# Create Previous and Next buttons for page navigation
prev_button = tk.Button(nav_frame, text="Previous Page", command=previous_page)
prev_button.pack(side=tk.LEFT, padx=5)

next_button = tk.Button(nav_frame, text="Next Page", command=next_page)
next_button.pack(side=tk.LEFT, padx=5)

# Disable navigation buttons initially
prev_button.config(state=tk.DISABLED)
next_button.config(state=tk.DISABLED)

# Create a Listbox for displaying available PDFs in the "pdfs" directory
pdf_listbox_frame = tk.Frame(root)
pdf_listbox_frame.grid(row=1, column=2, sticky='nsew', padx=10, pady=10)

pdf_listbox_label = tk.Label(pdf_listbox_frame, text="Available PDFs:")
pdf_listbox_label.pack(pady=10)

pdf_listbox = Listbox(pdf_listbox_frame, width=30, height=20)
pdf_listbox.pack(fill=tk.BOTH, padx=10, pady=10)

# Bind the Listbox click event to load the selected PDF
pdf_listbox.bind("<<ListboxSelect>>", load_pdf_from_list)

# Populate the Listbox with available PDFs
list_pdfs()

# Run the application
root.mainloop()
