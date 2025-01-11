import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import random

class MapMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("D&D Map Maker")
        
        # Canvas setup
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack(fill="both", expand=True)
        
        # Draw the grid
        self.draw_grid()
        
        # Setup for asset placement
        self.images = []  # Store images to prevent garbage collection
        self.canvas.bind("<Button-1>", self.place_asset)

        # Buttons for adding and auto placing assets
        self.add_asset_button = tk.Button(root, text="Add Asset", command=self.add_asset)
        self.add_asset_button.pack(side="bottom")

        self.auto_place_button = tk.Button(root, text="Auto Place Assets", command=lambda: self.auto_place_assets(10))
        self.auto_place_button.pack(side="bottom")

    def draw_grid(self):
        for i in range(0, 800, 40):  # 40 pixels per grid cell
            self.canvas.create_line([(i, 0), (i, 600)], tag='grid_line')
            self.canvas.create_line([(0, i), (800, i)], tag='grid_line')

    def add_asset(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            img = Image.open(filepath)
            img = img.resize((40, 40), Image.ANTIALIAS)  # Resize asset to fit grid
            photo_img = ImageTk.PhotoImage(img)
            self.images.append(photo_img)  # Append to list to prevent garbage collection

    def place_asset(self, event):
        if self.images:  # Check if there is at least one image loaded
            grid_x = (event.x // 40) * 40
            grid_y = (event.y // 40) * 40
            self.canvas.create_image(grid_x, grid_y, image=self.images[-1], anchor="nw")  # Use the last added image

    def auto_place_assets(self, asset_count):
        for _ in range(asset_count):
            if self.images:  # Ensure there are assets loaded
                # Choose a random asset
                image = random.choice(self.images)
                # Randomly select coordinates aligned to the grid
                grid_x = random.randint(0, 19) * 40  # 20 possible positions (0-19) along the width
                grid_y = random.randint(0, 14) * 40  # 15 possible positions (0-14) along the height
                self.canvas.create_image(grid_x, grid_y, image=image, anchor="nw")

if __name__ == "__main__":
    root = tk.Tk()
    app = MapMaker(root)
    root.mainloop()
