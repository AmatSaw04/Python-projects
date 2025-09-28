import tkinter as tk
from tkinter import filedialog, messagebox, Entry, Button, Label, Canvas, Frame, StringVar
from PIL import Image, ImageTk, ImageDraw, ImageFont

# --- Global state to hold image data ---
# Using a dictionary to hold state instead of class variables
app_state = {
    "original_image": None,
    "processed_image": None,
    "tk_image": None,  # To prevent garbage collection
}


# --- Functions to handle events ---

def open_image():
    """Opens a file dialog to select an image and displays it."""
    image_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg"), ("All files", "*.*")]
    )
    if not image_path:
        return

    app_state["original_image"] = Image.open(image_path).convert("RGBA")
    app_state["processed_image"] = app_state["original_image"].copy()
    display_image(app_state["processed_image"])
    status_var.set(f"Image loaded: {image_path.split('/')[-1]}")


def add_text_watermark():
    """Adds the text from the entry field as a watermark."""
    if not app_state["original_image"]:
        messagebox.showwarning("No Image", "Please upload an image first.")
        return

    text_to_add = watermark_entry.get()
    if not text_to_add:
        messagebox.showwarning("No Text", "Please enter watermark text.")
        return

    # Work on a fresh copy of the original image
    processed_image = app_state["original_image"].copy()
    draw = ImageDraw.Draw(processed_image)

    # Calculate font size and position
    img_width, img_height = processed_image.size
    font_size = int(img_width / 25)

    font = ImageFont.truetype("arial.ttf", font_size)


    text_bbox = draw.textbbox((0, 0), text_to_add, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    margin = 15
    position = (img_width - text_width - margin, img_height - font_size - margin)

    draw.text(position, text_to_add, font=font, fill=(255, 255, 255, 128))

    app_state["processed_image"] = processed_image
    display_image(app_state["processed_image"])
    status_var.set("Text watermark added. Ready to save.")


def save_image():
    """Saves the watermarked image to a new file."""
    if not app_state["processed_image"]:
        messagebox.showwarning("No Image", "There is no image to save.")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG file", "*.png"), ("JPEG file", "*.jpg")]
    )
    if not save_path:
        return

    try:
        # Convert to RGB for saving as JPG, which doesn't support transparency
        image_to_save = app_state["processed_image"].convert("RGB")
        image_to_save.save(save_path)
        messagebox.showinfo("Success", f"Image saved successfully to:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image: {e}")


def display_image(image):
    """Resizes and displays the given PIL image on the canvas."""
    canvas.delete("all")
    canvas_width, canvas_height = 700, 550

    # Resize image to fit canvas while maintaining aspect ratio
    img_copy = image.copy()
    img_copy.thumbnail((canvas_width, canvas_height), Image.LANCZOS)

    app_state["tk_image"] = ImageTk.PhotoImage(img_copy)
    canvas.create_image(canvas_width / 2, canvas_height / 2, image=app_state["tk_image"])


# --- GUI Setup ---
root = tk.Tk()
root.title("Simple Watermarking App")
root.config(padx=50, pady=50, bg="#2c3e50")

# Top frame for controls
control_frame = Frame(root, bg="#2c3e50")
control_frame.pack(pady=10, fill="x")

Button(control_frame, text="Upload Image", command=open_image, bg="#3498db", fg="#ecf0f1").pack(side="left", padx=5)
Label(control_frame, text="Watermark Text:", bg="#2c3e50", fg="#ecf0f1").pack(side="left", padx=(10, 5))
watermark_entry = Entry(control_frame, width=30)
watermark_entry.pack(side="left", padx=5)
watermark_entry.insert(0, "© MyPhotos")
Button(control_frame, text="Add Watermark", command=add_text_watermark, bg="#3498db", fg="#ecf0f1").pack(side="left",
                                                                                                         padx=5)
Button(control_frame, text="Save Image", command=save_image, bg="#2ecc71", fg="#ecf0f1").pack(side="left", padx=5)

# Canvas for image display
canvas = Canvas(root, width=700, height=550, bg="#34495e", highlightthickness=0)
canvas.pack()
canvas.create_text(350, 275, text="Upload an image to get started.", fill="#ecf0f1", font=("Helvetica", 16))

# Status bar
status_var = StringVar(value="Ready.")
status_label = Label(root, textvariable=status_var, bg="#2c3e50", fg="#ecf0f1")
status_label.pack(fill="x", pady=5)

root.mainloop()