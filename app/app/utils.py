import os
import re

def check_file_in_dir(dirname, filename_re):

    file_list = os.listdir(dirname)
    for filename in file_list:
        if filename_re.match(filename) is not None:
            return filename
    
    return False

# TODO: fix import dependency for mail
def send_async_email(app, msg, mail):
    with app.app_context():
        mail.send(msg)

def parse_html_file(path):

    with open(path, 'r') as f:
        file_content = f.read()

    return file_content

def create_content_folder(path, default_dir_name, id):
    
    try:
        os.mkdir(os.path.join(path, default_dir_name + f"_{id}"))
    except FileExistsError:
        return False
    else:
        return True
