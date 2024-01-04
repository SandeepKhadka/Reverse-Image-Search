import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from datetime import datetime
from flask import Flask, request, render_template, jsonify
from pathlib import Path
from train import Train

app = Flask(__name__)

# Read image features
fe = FeatureExtractor()
off = Train()
features = []
img_paths = []
for feature_path in Path("./static/features").glob("*.npy"):
    print("features: "+str(features))
    features.append(np.load(feature_path))
    img_paths.append(Path("./static/img") / (feature_path.stem + ".jpg"))
features = np.array(features)

print("features all: "+str(features))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['query_img']

        # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)

        # Run search
        query = fe.extract(img)
        dists = np.linalg.norm(features-query, axis=1)  # L2 distances to features
        ids = np.argsort(dists)[:30]  # Top 30 results
        scores = [(dists[id], str(img_paths[id])) for id in ids]
        
        # Return search results as JSON response
        # return jsonify({'message': 'Training successful'})
        score_values = [score[1] for score in scores]
        # return jsonify({'query_path': uploaded_img_path})
        return jsonify(score_values)

    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run("0.0.0.0")
