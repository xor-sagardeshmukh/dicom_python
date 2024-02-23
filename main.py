# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import pydicom
import numpy as np
import cv2


def to_video(data,out):
    out_path = out + data.PatientID + '.mp4'
    print("Video will be saved to this path -> ",out_path)
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
    print("Video converted and saved to this path -> ", out_path)


def to_jpeg(data, out):
    print("Nothing")


def convert(out, inp):
    dicom_files = [i for i in os.listdir(inp) if i.endswith('.dcm')]
    for i in dicom_files:
        data = pydicom.dcmread(os.path.join(inp,i))
        if "NumberOfFrames" in data:
            n = int(data.NumberOfFrames)
            print("Number of frames -> ",n)
            print("Duration of video will be -> ",n//24)
            to_video(data,out)
        else:
            print(1)
            to_jpeg(data,out)

def dicom():
    inp = "input_files/"            #provide with path for the input dicom files
    out = "output_files/"            #provide with path for the output dicom files
    convert(out, inp)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dicom()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
