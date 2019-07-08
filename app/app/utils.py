import os
import re

def check_file_in_dir(dirname, filename_re):

    file_list = os.listdir(dirname)
    for filename in file_list:
        if filename_re.match(filename) is not None:
            return filename
    
    return False

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def parse_html_file(path):

    with open(path, 'r') as f:
        file_content = f.read()

    return file_content