from PIL import Image
from PIL import ImageFilter
import numpy as np
import cv2

def resize_image(image_path, size):
    img = Image.open(image_path)
    return img.resize(size)

def convert_to_grayscale(image_path):
    img = Image.open(image_path)
    return img.convert("L")

def detect_edges(image_path, method='canny', low_threshold=50, high_threshold=200):
    img = cv2.imread(image_path, 0)
    if img is None:
        raise FileNotFoundError(f"Cannot read image at path: {image_path}")
    if method == 'canny':
        edges = cv2.Canny(img, low_threshold, high_threshold)
    elif method == 'sobel':
        edges = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
    return Image.fromarray(edges)

def blur_image(image_path, radius=2):
    img = Image.open(image_path)
    return img.filter(ImageFilter.GaussianBlur(radius))

tools = {
    "resize": resize_image,
    "grayscale": convert_to_grayscale,
    "edge_detection": detect_edges,
    "blur": blur_image,
}

tools = {
    "resize": resize_image,
    "grayscale": convert_to_grayscale,
    "edge_detection": detect_edges,
    "blur": blur_image,
}

class Memory:
    def __init__(self):
        self.history = []

    def add(self, step, data):
        self.history.append({"step": step, "data": data})

    def get_last(self):
        return self.history[-1] if self.history else None

    def show(self):
        return self.history
    
def planner(goal_description, memory):
    if "resize" in goal_description:
        return "resize", {"size": (100, 100)}
    elif "grayscale" in goal_description:
        return "grayscale", {}
    elif "edges" in goal_description:
        return "edge_detection", {}
    elif "blur" in goal_description:
        return "blur", {"radius": 3}
    else:
        return None, {}
class ImageProcessingAgent:
    def __init__(self, tools, memory):
        self.tools = tools
        self.memory = memory

    def run(self, image_path, goal_description):
        action, params = planner(goal_description, self.memory)
        if not action:
            print("No valid action found.")
            return None

        tool = self.tools.get(action)
        if tool:
            output = tool(image_path, **params)
            self.memory.add(action, {"params": params, "output": output})
            return output
        else:
            print(f"Tool {action} not found.")
            return None
memory = Memory()
agent = ImageProcessingAgent(tools, memory)
result = agent.run("kento-nanami-jujutsu-kaisen-4k-wallpaper-uhdpaper.com-544@0@e.jpg", "get edges")
if result is not None:
    result.show()