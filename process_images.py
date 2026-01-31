from PIL import Image, ImageOps
import sys
import os

def process_image(input_path, output_path, target_size=(100, 100)):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} does not exist.")
        return

    try:
        img = Image.open(input_path).convert("RGBA")
        
        # 1. Background Removal (White Background)
        # Create a mask for white pixels (with some tolerance)
        # Using a simple threshold for now since the inputs are generated on white background
        data = img.getdata()
        new_data = []
        tolerance = 30
        for item in data:
            # Check for white-ish background
            if item[0] > 255 - tolerance and item[1] > 255 - tolerance and item[2] > 255 - tolerance:
                new_data.append((255, 255, 255, 0)) # Fully transparent
            else:
                new_data.append(item)
        
        img.putdata(new_data)
        
        # 2. Trim empty space (Autocrop)
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)
            
        # 3. Resize to target size (maintaining aspect ratio)
        # Fit into target_size
        img.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        # 4. Canvas centering (Optional: Create a square canvas of target_size)
        # For this game, we might want the sprite to just be the sprite, but let's stick to just the resized sprite for now
        # or center it on a canvas if consistent size is needed.
        # Let's verify existing images logic later. For now, just save the cropped & resized result.
        
        img.save(output_path, "PNG")
        print(f"Processed: {output_path} (Size: {img.size})")

    except Exception as e:
        print(f"Failed to process {input_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python process_images.py <input_path> <output_path> [width] [height]")
    else:
        width = 100
        height = 100
        if len(sys.argv) >= 5:
            width = int(sys.argv[3])
            height = int(sys.argv[4])
        
        process_image(sys.argv[1], sys.argv[2], target_size=(width, height))
