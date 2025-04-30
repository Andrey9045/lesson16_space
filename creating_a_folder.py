import os

def creating_a_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)