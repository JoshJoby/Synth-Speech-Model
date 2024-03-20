import librosa
import numpy as np
import pandas as pd
from tqdm import tqdm
from flask import Flask, request, jsonify
import joblib
import traceback
def resample_if_necessary(audio, sr, target_sr):
    if sr != target_sr:
        audio = librosa.resample(audio, sr, target_sr)
    return audio

def extract_features(audio_file, SR):
    y, sr = librosa.load(audio_file, sr=None, duration=5)
    # y = resample_if_necessary(y, sr, SR)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rms = librosa.feature.rms(y=y)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y)
    mfccs = librosa.feature.mfcc(y=y, sr=SR, n_mfcc=20)

    features = np.vstack([
        chroma_stft,
        rms,
        spectral_centroid,
        spectral_bandwidth,
        rolloff,
        zero_crossing_rate,
        mfccs
    ])

    # Transpose the features matrix to have time frames as rows and features as columns
    features = features.T

    return features[:,:26]

# Initialize Flask app
app = Flask(__name__)

# API endpoint for feature extraction and prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the uploaded file from the request
        csv_file = request.files['csv']
        df = pd.read_csv(csv_file)
        # Save the uploaded file
        # audio_path = 'temp_audio.wav'
        # audio_file.save(audio_path)
        SAMPLE_RATE = 16000
        # Extract features
        # features = extract_features(audio_path, SAMPLE_RATE)
        features = df.iloc[:,:]
        # Load the trained Random Forest model
        model = joblib.load('trained_random_forest_model_1000.pkl')

        # Make predictions
        predictions = model.predict(features)
        print(predictions.tolist())
        # Return predictions as JSON
        return jsonify({"predictions": predictions.tolist()})
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)})

# Run the app if this script is the main entry point
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
