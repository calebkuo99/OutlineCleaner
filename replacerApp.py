import tkinter as tk
from tkinter import scrolledtext
import re

def process_text(text):
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
    
    return text

# Function to replace newlines with spaces
def replace_newlines():
    # Get the content from the input text box
    input_text = text_box.get("1.0", tk.END)
    # Replace all newlines with spaces
    # modified_text = input_text.replace("\n", " ").strip()
    modified_text = process_text(input_text)
    # Clear the output text box and insert the modified text
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, modified_text)

# Function to copy output text to clipboard
def copy_to_clipboard():
    # Get the content from the output text box
    output_text = output_box.get("1.0", tk.END).strip()
    # Clear the clipboard and append the text
    root.clipboard_clear()
    root.clipboard_append(output_text)

# Create the root window
root = tk.Tk()
root.title("Replace Newlines with Spaces")
root.geometry("800x1000")  # Set window size

# Create a label for input
label_input = tk.Label(root, text="Paste your text below:")
label_input.pack(pady=10)

# Create a text box (scrolledtext for larger input) for the input text
text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=150, height=30)
text_box.pack(padx=10, pady=10)

# Create a frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Create a button to trigger the newline replacement
replace_button = tk.Button(button_frame, text="Replace Newlines with Spaces", command=replace_newlines)
replace_button.pack(side=tk.LEFT, padx=5)

# Create a button to copy output text to clipboard
copy_button = tk.Button(button_frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(side=tk.LEFT, padx=5)

# Create a label for output
label_output = tk.Label(root, text="Resulting text:")
label_output.pack(pady=10)

# Create a text box (scrolledtext) for displaying the modified text
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=150, height=30)
output_box.pack(padx=10, pady=10)

# Run the application
root.mainloop()