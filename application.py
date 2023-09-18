from flask import Flask, render_template, request, jsonify, send_from_directory
import qrcode_my_file
from flask_bootstrap import Bootstrap4
import threading
import time
import os
import schedule
# from flask import static_folder
app = Flask(__name__)
bootstrap = Bootstrap4(app)

# app.add_url_rule('/static/<path:filename>',
#                  'static',
#                  static_folder='static')

generator = qrcode_my_file.QRCodeGenerator()


filename = None

@app.route('/', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        text = request.form.get('text')
        width = request.form.get('settings_size_width')
        height = request.form.get('settings_size_height')
        style = request.form.get('Style')
        foreground_color = request.form.get('settings_foreground_color')
        background_color = request.form.get('settings_background_color')
        color_style = request.form.get('ColorStyle')
        file_type = request.form.get('file_type')

        # print(f"text : {text}")
        # print(f"settings_size_width : {width}")
        # print(f"settings_size_height : {height}")
        # print(f"Style : {style}")
        # print(f"settings_background_color : {background_color}")
        # print(f"settings_foreground_color : {foreground_color}")
        # print(f"ColorStyle : {color_style}")
        #
        # print(f"file type : .{file_type}")


        if text == "":

            return render_template('index(1).html', btn_disabled=True)

        else:
            global filename
            filename = generator.generate_qrcode(text=text, background_color=background_color,
                                                 foreground_color=foreground_color, style=style, width=width,
                                                 height=height, file_type=file_type, color_style=color_style)
            v = filename
            return render_template('index(1).html', filename=filename, btn_disabled=False)


    return render_template('index(1).html', btn_disabled=True)


@app.route('/qrcode/<filename>')
def display_qrcode(filename):
    return render_template('qrcode.html', filename=filename)

def delete_files():
    folder_path = "static"  # The folder where the files are located
    extensions = (".png", ".jpg")  # List of file extensions to delete

    for filename in os.listdir(folder_path):
        if filename.endswith(extensions):
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)
            print(f"Deleted: {file_path}")

# Schedule the cleanup function to run daily at 00:00 hrs
schedule.every().day.at("00:00").do(delete_files)

@app.teardown_appcontext
def teardown(exception):
    t = threading.Thread(target=cleanup_file, args=(generator,))
    t.start()

def cleanup_file(generator):
    time.sleep(600)
    generator.cleanup()

def clearupcache(generator):
    generator.delete_files()
    time.sleep(86400)

cleanup_thread = threading.Thread(target=clearupcache, args=(generator,))
cleanup_thread.start()

@app.route('/check-file/<filename>')
def check_file(filename):
    file_path = os.path.join(app.static_folder, filename)


    try:
        if os.path.exists(file_path):
            print(f"Checking: {file_path}")
            return jsonify(exists=True)
    except Exception as e:
        print(e)
        return jsonify(exists=False)


if __name__ == '__main__':
    app.run(debug=True)
