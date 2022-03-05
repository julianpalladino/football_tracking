import os
import ffmpeg
from pdb import set_trace as st

def convert_all_data_from_mkv_to_mp4(data_folder):
    for path, folder, files in os.walk(data_folder):
        for file in files:
            if file.endswith('.mkv'):
                print("Found file: %s" % file)
                convert_from_mkv_to_mp4(os.path.join(data_folder, file))

def convert_from_mkv_to_mp4(mkv_filepath):
    name, ext = os.path.splitext(mkv_filepath)
    out_name = name + ".mp4"
    ffmpeg.input(mkv_filepath).output(out_name).run()
    print("Finished converting {}".format(mkv_filepath))