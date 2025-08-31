import tkinter as tk
from tkinter import filedialog, messagebox
import json
import numpy as np
import matplotlib.pyplot as plt

def load_file():
    filepath = filedialog.askopenfilename(
        filetypes=[("JSON files", "*.json"), 
                   ("NumPy files", "*.npy"), 
                   ("Text files", "*.txt"), 
                   ("CSV files", "*.csv")]
    )
    if not filepath:
        return
    try:
        if filepath.endswith('.json'):
            with open(filepath, 'r') as f:
                data = json.load(f)
            data = np.array(data)
        elif filepath.endswith('.npy'):
            data = np.load(filepath)
        elif filepath.endswith('.txt'):
            data = np.loadtxt(filepath, delimiter=',')
        elif filepath.endswith('.csv'):
            data = np.genfromtxt(filepath, delimiter=',')
        else:
            messagebox.showerror("Error", "Unsupported file type!")
            return
        # If data is flattened, you can ask for reshape manually or infer if possible
        plt.figure(figsize=(8, 8))
        if data.ndim == 2:
            plt.imshow(data, cmap='gray', vmin=0, vmax=255)
        elif data.ndim == 3 and data.shape[2] == 3:
            plt.imshow(data.astype(np.uint8))
        else:
            messagebox.showwarning("Warning", f"Unexpected data shape: {data.shape}")
        plt.axis('off')
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file:\n{e}")
# Create GUI window
root = tk.Tk()
root.title("Numerical Image Drawer")
root.geometry("300x150")
label = tk.Label(root, text="Load a file to draw its image", font=("Arial", 12))
label.pack(pady=20)
button = tk.Button(root, text="Load File", command=load_file, font=("Arial", 12))
button.pack()
root.mainloop()
