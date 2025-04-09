from rembg import remove
from rembg.session_factory import new_session
from PIL import Image
import os
import torch

class ImageProcessor:
    def __init__(self):
        self.session_u2net = new_session("u2net")
        self.session_u2netp = new_session("u2netp")
        self.session_silueta = new_session("silueta")

    def process_image(self, input_image, model, use_alpha_matting, fg_threshold, bg_threshold, erode_size, use_gpu):
        session = self.session_u2net if model == 1 else self.session_u2netp if model == 2 else self.session_silueta

        torch_device = torch.device("cuda") if use_gpu else torch.device("cpu")
        # Configurer les paramètres pour Alpha Matting
        return remove(
            input_image,
            session=session,
            alpha_matting=use_alpha_matting,  # Active Alpha Matting
            alpha_matting_foreground_threshold=fg_threshold,
            alpha_matting_background_threshold=bg_threshold,
            alpha_matting_erode_size=erode_size,
            device = torch_device
        )


    def process_whole_folder(self, input_dir="input_files", output_dir="output_files"):
        os.makedirs(output_dir, exist_ok=True)
        for file_name in os.listdir(input_dir):
            input_path = os.path.join(input_dir, file_name)
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    inp = Image.open(input_path)
                    output = self.process_image(inp, 1, 240, 10, 10)
                    base_name = os.path.splitext(file_name)[0]
                    output_path = os.path.join(output_dir, base_name + "_no_bg.png")
                    count = 0
                    while os.path.exists(output_path):
                        count += 1
                        output_path = os.path.join(output_dir, f"{base_name}_{count:03d}.png")
                    output.save(output_path)
                except Exception as e:
                    print(f"Erreur avec {file_name}: {e}")
