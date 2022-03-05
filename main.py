from tkinter import W
import cv2
import os
import ffmpeg
from pdb import set_trace as st # For debugging
import config

def convert_all_data_from_mkv_to_mp4(data_folder):
    print('Converting all files at {} from mkv to mp4'.format(data_folder))
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

def main():
    input_filepath = os.path.join('data', 'messi.mp4')
    # input_filepath = os.path.join('data', 'maradona_1986_raw.mp4')

    cap = cv2.VideoCapture(input_filepath)
    object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

    while True:
        ret, frame = cap.read()
        mask = object_detector.apply(frame)
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area >= config.MINIMUM_CONTOUR_AREA:
                cv2.drawContours(frame, [cnt], -1, (255, 0, 0), 2)
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        cv2.imshow(input_filepath + ' raw', frame)
        # cv2.imshow(input_filepath + ' mask', mask)
        key = cv2.waitKey(30)
        if key == 27:
            break
    cap.release()

if __name__ == '__main__':
    # convert_all_data_from_mkv_to_mp4('data')
    main()