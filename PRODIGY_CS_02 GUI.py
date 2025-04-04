import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import numpy as np
import os

# Global variables
selected_image_path = ""
save_directory = os.getcwd()  # Default to current directory
key = None  # Custom encryption key

# Function to select an image
def select_image():
    global selected_image_path
    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if file_path:
        selected_image_path = file_path
        show_image(file_path, selected_image_label)
        messagebox.showinfo("Selected", f"Selected Image: {os.path.basename(file_path)}")

# Function to choose save directory
def select_save_directory():
    global save_directory
    save_directory = filedialog.askdirectory(title="Select Save Directory")
    if save_directory:
        messagebox.showinfo("Save Location", f"Images will be saved in: {save_directory}")

# Function to encrypt the image
def encrypt_image():
    global key
    if not selected_image_path:
        messagebox.showerror("Error", "Please select an image first!")
        return

    # Ask user for a custom encryption key
    key = simpledialog.askinteger("Encryption Key", "Enter a numeric key (0-255):", minvalue=0, maxvalue=255)
    if key is None:
        return  # If user cancels input

    try:
        img = Image.open(selected_image_path)
        img_array = np.array(img)

        # XOR encryption
        encrypted_array = img_array ^ key
        encrypted_img = Image.fromarray(encrypted_array)

        encrypted_image_path = os.path.join(save_directory, "encrypted_image.png")
        encrypted_img.save(encrypted_image_path)

        messagebox.showinfo("Success", f"Image encrypted successfully!\nSaved at: {encrypted_image_path}")
        show_image(encrypted_image_path, encrypted_label)
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed: {e}")

# Function to decrypt the image
def decrypt_image():
    if not key:
        messagebox.showerror("Error", "Please encrypt an image first or enter the correct key!")
        return

    encrypted_file_path = filedialog.askopenfilename(
        title="Select Encrypted Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if not encrypted_file_path:
        return

    try:
        encrypted_img = Image.open(encrypted_file_path)
        encrypted_array = np.array(encrypted_img)

        # XOR decryption
        decrypted_array = encrypted_array ^ key
        decrypted_img = Image.fromarray(decrypted_array)

        decrypted_image_path = os.path.join(save_directory, "decrypted_image.png")
        decrypted_img.save(decrypted_image_path)

        messagebox.showinfo("Success", f"Image decrypted successfully!\nSaved at: {decrypted_image_path}")
        show_image(decrypted_image_path, decrypted_label)
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed: {e}")

# Function to display image in GUI
def show_image(image_path, label):
    img = Image.open(image_path)
    img = img.resize((200, 200))  # Resize for display
    img = ImageTk.PhotoImage(img)
    label.config(image=img)
    label.image = img

# Create the GUI window
root = tk.Tk()
root.title("Image Encryption Tool")
root.geometry("650x500")
root.configure(bg="#f0f0f0")

# Title Label
tk.Label(root, text="Image Encryption & Decryption", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

# Select Image Button
btn_select = tk.Button(root, text="Select Image", font=("Arial", 12), command=select_image, bg="#FFA500", fg="white")
btn_select.pack(pady=5)

# Select Save Directory Button
btn_directory = tk.Button(root, text="Choose Save Location", font=("Arial", 12), command=select_save_directory, bg="#8A2BE2", fg="white")
btn_directory.pack(pady=5)

# Encrypt Button
btn_encrypt = tk.Button(root, text="Encrypt Image", font=("Arial", 12), command=encrypt_image, bg="#4CAF50", fg="white")
btn_encrypt.pack(pady=5)

# Decrypt Button
btn_decrypt = tk.Button(root, text="Decrypt Image", font=("Arial", 12), command=decrypt_image, bg="#008CBA", fg="white")
btn_decrypt.pack(pady=5)

# Image display labels
selected_image_label = tk.Label(root, text="Selected Image", bg="#f0f0f0")
selected_image_label.pack(pady=10)

encrypted_label = tk.Label(root, text="Encrypted Image", bg="#f0f0f0")
encrypted_label.pack(pady=10)

decrypted_label = tk.Label(root, text="Decrypted Image", bg="#f0f0f0")
decrypted_label.pack(pady=10)

# Run the GUI application
root.mainloop()
