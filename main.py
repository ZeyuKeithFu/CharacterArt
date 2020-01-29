import cv2
import sys
import os
import math
import time
import shutil
import imageio

CHAR_DICT = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
LEVELS = len(CHAR_DICT)
UNIT_LEVEL = 256 / LEVELS

# Configs
WIDTH, HEIGHT = shutil.get_terminal_size()
FRAME_RATE = 30  # Default: 30 frames per sec
GIF_FILE = ""


def get_frame_count(file):
    try:
        gif = imageio.mimread(file)
        return len(gif)
    except FileNotFoundError:
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
            str_img = ""
            for row in gray:
                for pixel in row:
                    ch = decode_pixel(pixel)
                    str_img += ch
                str_img += "\n"
            data.append(str_img)
            frame_count += 1


def clear():
    cmd = "cls" if os.name == 'nt' else "printf '\33c\e[3J'"
    os.system(cmd)


def main():
    global FRAME_RATE, GIF_FILE
    # Check input
    if len(sys.argv) < 2:
        print("Please provide an image...")
        return
    
    # Customized frame rate
    if len(sys.argv) > 2:
        FRAME_RATE = int(sys.argv[2])

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
        time.sleep(1/FRAME_RATE)


if __name__ == "__main__":
    main()
