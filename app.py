from flask import Flask, Response, request
import os
from convert_to_csv import Final_year
app = Flask(__name__)

@app.route('/')
def home():
    audio_files_fake = ["Super_Fast.mp3"]
    output_csv_file = "extracted_features_final.csv"
    SAMPLE_RATE = 16000
    final_year_instance = Final_year()
    final_year_instance.save_features_to_csv(audio_files_fake, output_csv_file, SAMPLE_RATE, num_cores=-1)
    response_data = "Features extracted and saved to 'extracted_features_final.csv'"
    return Response(response_data, status=200, mimetype='text/plain')
    # final_year_instance.test_csv()    

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    try:
        audio_file = request.files['audioFile']
        # Ensure that the file is an audio file (optional)
        if audio_file and allowed_file(audio_file.filename):
            # Process the audio file as needed (e.g., save it to a folder, perform operations)
            audio_file.save('./tracks/' + audio_file.filename)
            return 'Audio file uploaded successfully'
        else:
            return 'Invalid audio file'
    except Exception as e:
        return f'Error uploading audio: {str(e)}'

def allowed_file(filename):
    # Check if the file extension is allowed (optional)
    allowed_extensions = {'ogg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
