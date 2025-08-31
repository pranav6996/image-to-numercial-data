#!/usr/bin/env python3
"""
GUI Image to Numerical Data Converter
Select an image and export RGB / optional grayscale arrays.
"""
import os
import json
import gzip
from tkinter import Tk, filedialog, Button, Checkbutton, IntVar, Label
from PIL import Image
import numpy as np
import pandas as pd

def convert_image(image_path, outdir, grayscale=False):
    os.makedirs(outdir, exist_ok=True)
    base = os.path.splitext(os.path.basename(image_path))[0]
    # Load image and convert to RGB
    img = Image.open(image_path).convert("RGB")
    arr_uint8 = np.array(img, dtype=np.uint8)
    h, w, c = arr_uint8.shape
    arr_float32 = arr_uint8.astype(np.float32)/255.0
    # Save arrays
    np.save(os.path.join(outdir, f"{base}_rgb_uint8.npy"), arr_uint8)
    np.save(os.path.join(outdir, f"{base}_rgb_float32.npy"), arr_float32)
    np.savez_compressed(os.path.join(outdir, f"{base}_rgb_both.npz"),
                        rgb_uint8=arr_uint8, rgb_float32=arr_float32)
    # Save JSON (gzipped)
    with gzip.open(os.path.join(outdir, f"{base}_rgb.json.gz"), "wt", encoding="utf-8") as f:
        json.dump(arr_uint8.tolist(), f, separators=(",", ":"))
    # Save CSV (gzipped)
    y_idx, x_idx = np.indices((h, w))
    flat = arr_uint8.reshape(-1, 3)
    df = pd.DataFrame({"x": x_idx.ravel(), "y": y_idx.ravel(),
                       "r": flat[:,0], "g": flat[:,1], "b": flat[:,2]})
    df.to_csv(os.path.join(outdir, f"{base}_pixels.csv.gz"), index=False)
    # Optional grayscale
    if grayscale:
        gray = (0.299*arr_uint8[:,:,0] + 0.587*arr_uint8[:,:,1] + 0.114*arr_uint8[:,:,2]).round().astype(np.uint8)
        np.save(os.path.join(outdir, f"{base}_gray_uint8.npy"), gray)
        df_gray = pd.DataFrame({"x": x_idx.ravel(), "y": y_idx.ravel(), "gray": gray.ravel()})
        df_gray.to_csv(os.path.join(outdir, f"{base}_gray_pixels.csv.gz"), index=False)
    print(f"✓ Conversion done! Files saved in: {outdir}")
def select_image():
    filepath = filedialog.askopenfilename(title="Select an image",
                                          filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
    if not filepath:
        return
    outdir = filedialog.askdirectory(title="Select output folder")
    if not outdir:
        return
    convert_image(filepath, outdir, grayscale=grayscale_var.get())
# GUI setup
root = Tk()
root.title("Image to Numerical Data Converter")
Label(root, text="Select an image to convert").pack(pady=10)
Button(root, text="Select Image", command=select_image).pack(pady=5)
grayscale_var = IntVar()
Checkbutton(root, text="Also export grayscale", variable=grayscale_var).pack(pady=5)
root.geometry("300x150")
root.mainloop()
