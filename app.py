from flask import Flask, jsonify
import os
from convert_to_csv import Final_year
app = Flask(__name__)

@app.route('/api')
def home():
    audio_files_fake = ["Super_Fast.mp3"]
    output_csv_file = "extracted_features_final.csv"
    SAMPLE_RATE = 16000
    final_year_instance = Final_year()
    final_year_instance.save_features_to_csv(audio_files_fake, output_csv_file, SAMPLE_RATE, num_cores=-1)
    print("Features extracted and saved to 'extracted_features_final.csv'")
    final_year_instance.test_csv()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
