import os
from flask import Flask, request, send_from_directory
from subprocess import run

app = Flask(__name__)

# Set the upload folder and allowed file types
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return '''
    <html>
        <body>
            <h1>Create a Wheel File</h1>
            <form method="POST" action="/create_wheel" enctype="multipart/form-data">
                <input type="file" name="file"><br><br>
                <select name="arch">
                    <option value="x86">x86</option>
                    <option value="x86_64">x86_64</option>
                    <option value="macosx_10_6_intel">macosx_10_6_intel</option>
                    <option value="macosx_10_9_intel">macosx_10_9_intel</option>
                    <option value="macosx_10_9_x86_64">macosx_10_9_x86_64</option>
                    <option value="macosx_10_10_intel">macosx_10_10_intel</option>
                    <option value="macosx_10_10_x86_64">macosx_10_10_x86_64</option>
                    <option value="macosx_10_11_intel">macosx_10_11_intel</option>
                    <option value="macosx_10_11_x86_64">macosx_10_11_x86_64</option>
                    <option value="macosx_10_12_intel">macosx_10_12_intel</option>
                    <option value="macosx_10_12_x86_64">macosx_10_12_x86_64</option>
                    <option value="macosx_10_13_intel">macosx_10_13_intel</option>
                    <option value="macosx_10_13_x86_64">macosx_10_13_x86_64</option>
                    <option value="macosx_10_14_intel">macosx_10_14_intel</option>
                    <option value="macosx_10_14_x86_64">macosx_10_14_x86_64</option>
                    <option value="macosx_10_15_intel">macosx_10_15_intel</option>
                    <option value="macosx_10_15_x86_64">macosx_10_15_x86_64</option>
                    <option value="win32">win32</option>
                    <option value="win_amd64">win_amd64</option>
                    <option value="manylinux1_x86_64">manylinux1_x86_64</option>
                    <option value="manylinux1_i686">manylinux1_i686</option>
                    <option value="manylinux2010_x86_64">manylinux2010_x86_64</option>
                    <option value="manylinux2010_i686">manylinux2010_i686</option>
                    <option value="manylinux2014_x86_64">manylinux2014_x86_64</option>
                    <option value="manylinux2014_i686">manylinux2014_i686</option>
                    <option value="manylinux_x86_64">manylinux_x86_64</option>
                    <option value="manylinux_i686">manylinux_i686</option>
                    <option value="raspbian_9_armhf">raspbian_9_armhf</option>
                    <option value="raspbian_10_armhf">raspbian_10_armhf</option>
                    <option value="linux_armv6l">linux_armv6l</option>
                    <option value="linux_armv7l">linux_armv7l</option>
                    <option value="linux_aarch64">linux_aarch64</option>
                </select><br><br>
                <input type="submit" value="Create Wheel">
            </form>
        </body>
    </html>
    '''

@app.route('/create_wheel', methods=['POST'])
def create_wheel():
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
        run(['python', 'setup.py', 'bdist_wheel', '--plat-name=' + arch])
        # Send wheel file to user
        return send_from_directory('dist', os.listdir('dist')[0], as_attachment=True)
    return 'Invalid file type'

@app.after_request
def cleanup(response):
    # Delete uploaded files and dist folder
    os.system('rm -rf uploads/* dist/')
    return response


if __name__ == '__main__':
    app.run(debug=True)

