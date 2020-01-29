import cv2
import sys
import os
import math
import time
import imageio

CHAR_DICT = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
LEVELS = len(CHAR_DICT)
UNIT_LEVEL = 256 / LEVELS
WIDTH = 143
HEIGHT = 40
GIF_FILE = ""


def get_frame_count(file):
    try:
        gif = imageio.mimread(file)
        return len(gif)
    except:
        print("File not found!")
        exit(1)


def decode_pixel(pixel):
    return CHAR_DICT[math.floor(pixel / UNIT_LEVEL)]


def decode_frames(data, total, file):
    # Read by frame
    cap = cv2.VideoCapture(file)
    frame_count = 0
    while frame_count < total:
        ret, frame = cap.read()
        if frame is not None:
            gray = cv2.cvtColor(cv2.resize(frame, (WIDTH, HEIGHT)), cv2.COLOR_BGR2GRAY)
            strImg = ""
            for row in gray:
                for pixel in row:
                    ch = decode_pixel(pixel)
                    strImg += ch
                strImg += "\n"
            data.append(strImg)
            frame_count += 1


def clear():
    cmd = "cls" if os.name == 'nt' else "printf '\33c\e[3J'"
    os.system(cmd)


def main():
    # Check input
    if len(sys.argv) < 2:
        print("Please provide an image...")
        return

    # Initialize frame data
    GIF_FILE = sys.argv[1]
    total_frame = get_frame_count(GIF_FILE)
    data = []
    decode_frames(data, total_frame, GIF_FILE)

    # Print to console
    fpos = 0
    while True:
        clear()
        print(data[fpos])
        fpos += 1
        if fpos >= total_frame:
            fpos = 0
        time.sleep(1 / 30)


if __name__ == "__main__":
    main()
