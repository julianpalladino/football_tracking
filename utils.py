import os
import ffmpeg
import cv2


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


def draw_text(img,
              text,
              pos,
              font=cv2.FONT_HERSHEY_PLAIN,
              font_scale=2,
              font_thickness=1
              ):

    pos = (int(pos[0]-5), int(pos[1]-5))
    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size[0] + 5, text_size[1] + 5
    cv2.rectangle(img, pos, (x + text_w, y + text_h), (220, 220, 220), -1)
    cv2.putText(img, text, (x, y + text_h + font_scale - 1),
                font, font_scale, (0, 0, 0), font_thickness)
    return text_size
