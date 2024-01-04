from PIL import Image
from feature_extractor import FeatureExtractor
from pathlib import Path
import numpy as np
import os

class Train:
    def extract(self):
        fe = FeatureExtractor()

        # Delete all files in the features directory if it exists
        if os.path.isdir("./static/features"):
            for filename in os.listdir("./static/features"):
                os.remove(os.path.join("./static/features", filename))

        for img_path in sorted(Path("C:/wamp64/www/fyp/goodgoods/public/uploads/similar_images").glob("*.jpg")):
            print(img_path)  # e.g., ./static/img/xxx.jpg
            feature = fe.extract(img=Image.open(img_path))
            feature_path = Path("./static/features") / (img_path.stem + ".npy")  # e.g., ./static/feature/abc.npy
            np.save(feature_path, feature)
            
trainer = Train()
trainer.extract()

