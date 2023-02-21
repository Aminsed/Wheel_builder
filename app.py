import os
from flask import Flask, request, send_from_directory, render_template
from subprocess import run

app = Flask(__name__)

# Set the upload folder and allowed file types
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists('dist'):
    os.makedirs('dist')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_wheel', methods=['POST'])
def create_wheel():
    # Check if dist directory exists
    if not os.path.exists('dist'):
        os.makedirs('dist')
    # Check if file was uploaded
    if 'file' not in request.files:
        return 'No file uploaded'
    file = request.files['file']
    # Check if file is allowed
    if file and allowed_file(file.filename):
        # Save file to disk
        filename = 'requirements.txt'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Check if architecture was selected
        arch = request.form.get('arch')
        if not arch:
            return 'No architecture selected'
        # Create wheel file
        result = run(['python', 'setup.py', 'bdist_wheel', '--plat-name=' + arch])
        if result.returncode != 0:
            print('sheit')
            print(result)
            return 'Failed to create wheel file'
        # Check if wheel file was created
        files = os.listdir('dist')
        if not files:
            return 'Failed to create wheel file'
        # Send wheel file to user
        return send_from_directory('dist', files[0], as_attachment=True)
    return 'Invalid file type'



@app.after_request
def cleanup(response):
    # Delete uploaded files and dist folder
    os.system('rm -rf uploads/* dist/*')
    return response


if __name__ == '__main__':
    app.run(debug=True)
