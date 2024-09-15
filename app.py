from flask import Flask, request, render_template, send_file, url_for
from moviepy.editor import concatenate_audioclips, AudioFileClip
import os
import random

app = Flask(__name__)

# Route for the upload form
@app.route('/')
def upload_form():
    return render_template('upload.html')

# Route for handling file uploads and concatenation
@app.route('/upload', methods=['POST'])
def upload_files():
    mp3_files = request.files.getlist("mp3_files")

    clips = []
    temp_files = []

    for mp3 in mp3_files:
        if not mp3.filename.lower().endswith('.mp3'):
            return "Invalid file type. Only MP3 files are allowed.", 400

        # Save the uploaded MP3 data to the current working directory
        mp3_path = os.path.join(os.getcwd(), mp3.filename)
        temp_files.append(mp3_path)
        
        # Save the uploaded file to the current working directory
        mp3.save(mp3_path)

        # Use the saved file with AudioFileClip
        clip = AudioFileClip(mp3_path)
        clips.append(clip)
    random.shuffle(clips)
    # Concatenate the audio clips
    combined = concatenate_audioclips(clips)

    # Define the path for the output combined file in the current working directory
    output_file_path = os.path.join(os.getcwd(), "combined.mp3")
    
    # Write the combined audio to the output file
    combined.write_audiofile(output_file_path, codec="mp3")

    # Close all the AudioFileClip objects and delete the input files
    for clip in clips:
        clip.close()
    for temp_file_path in temp_files:
        os.remove(temp_file_path)  # Clean up the input files

    # Render the template with the download link
    return render_template('upload.html', download_link=url_for('download_file', filename="combined.mp3"))

# Route to serve the combined file for download
@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(os.getcwd(), filename)  # Get the full path of the file in the current directory
    return send_file(file_path, as_attachment=True, download_name="combined.mp3", mimetype='audio/mp3')

if __name__ == '__main__':
    app.run(debug=True)

