
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import pydicom
import numpy as np
import cv2
from PIL import Image
from datetime import datetime

def next_num(physician_id,out):
    count = 0
    for i in os.listdir(out):
        if i.startswith(physician_id):
            count = count + 1
    return count


def to_video(data,out):
    out_path = out + str(data.ReferringPhysicianName) + '_' + datetime.now().strftime("%Y%m%d-%H%M") + '_' + str(next_num(data.ReferringPhysicianName,out)+1) + '.mp4'
    print(f"Video will be saved to this path -> {out_path}")
    if 'PixelData' in data:
        pixel_data = data.pixel_array
    else:
        raise ValueError("DICOM file does not contain pixel data.")
    height, width, _ = pixel_data.shape[1:]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, 24, (width, height))
    for frame_num in range(pixel_data.shape[0]):
        frame_data = pixel_data[frame_num]
        frame_data = np.uint8(frame_data)
        out.write(frame_data)
    out.release()
    print(f"Video converted and saved to this path -> {out_path}")


def to_image(data, out):
    out_path = out + str(data.ReferringPhysicianName) + '_' + datetime.now().strftime("%Y%m%d-%H%M") + '_' + str(next_num(data.ReferringPhysicianName,out)+1) + '.png'
    print(f"Image will be saved to this path -> {out_path}")
    if 'PixelData' in data:
        pixel_data = data.pixel_array
    else:
        raise ValueError("DICOM file does not contain pixel data.")
    img = Image.fromarray(pixel_data)
    img.save(out_path)
    print(f"Image saved to this path -> {out_path}")


def convert(out, inp):
    print('-------------------Execution Started-------------------')
    for i in os.listdir(inp):
        inp_path = os.path.join(inp, i)
        out_path = out
        dicom_files = [i for i in os.listdir(inp_path) if i.endswith('.dcm')]
        for i in dicom_files:
            data = pydicom.dcmread(os.path.join(inp_path,i))
            n = 1
            if "NumberOfFrames" in data:
                n = int(data.NumberOfFrames)
                print(f"Number of frames -> {n} frames")
                print(f"Duration of video will be -> {n//24} seconds")
                to_video(data,out_path)
            else:
                print(f'Number of frames -> {n} frame')
                to_image(data,out_path)
    print('--------------------Execution Ended--------------------')

def dicom():
    inp = "input_files/"            #provide with path for the input dicom files
    out = "output_files/"            #provide with path for the output dicom files
    convert(out, inp)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dicom()