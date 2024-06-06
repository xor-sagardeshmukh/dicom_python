import os
import pydicom
import numpy as np
import cv2
from PIL import Image
from datetime import datetime


def photometric(data):
    print("--------Photometric Data--------")
    if 'PhotometricInterpretation' in data:
        photometric_interp = data.PhotometricInterpretation
        if photometric_interp.startswith('MONOCHROME'):
            print("Black and White")
            print("--------Photometric Data Extracted--------")
            return 'MONOCHROME'
        elif photometric_interp in ['RGB', 'YBR_FULL', 'YBR_FULL_422', 'YBR_PARTIAL_422']:
            print("Color1")
            print("--------Photometric Data Extracted--------")
            return photometric_interp
    if 'SamplesPerPixel' in data:
        samples_per_pixel = data.SamplesPerPixel
        if samples_per_pixel == 1:
            print("Black and White")
            print("--------Photometric Data Extracted--------")
            return 'MONOCHROME'
        elif samples_per_pixel >= 3:
            print("Color2")
            print("--------Photometric Data Extracted--------")
            return 'COLORED'
    return None

def next_num(physician_id,out):
    count = 0
    physician_id = str(physician_id)
    for i in os.listdir(out):
        if i.startswith(physician_id):
            count = count + 1
    return count

#function converts the dicom file as MP4
def to_video(data,out):
    out_path = out + str(data.ReferringPhysicianName) + '_' + datetime.now().strftime("%Y%m%d-%H%M") + '_' + str(next_num(data.ReferringPhysicianName,out)+1) + '.mp4'
    print(f"Video will be saved to this path -> {out_path}")
    if 'PixelData' in data:
        pixel_data = data.pixel_array
    else:
        raise ValueError("DICOM file does not contain pixel data.")
    print('----------------Extracting the Frame Rate Per Second-------------------')
    fps = None
    photoelement = photometric(data)
    if 'CineRate' in data:
        fps = data.CineRate
    elif 'FrameTime' in data:
        frame_time_ms = data.FrameTime
        fps = 1000 // frame_time_ms
        fps = int(fps)
    elif 'FrameIncrementPointer' in data:
        pointer = data.FrameIncrementPointer
        if pointer in data:
            frame_increment = data[pointer].value
            fps = 1000 / frame_increment
    elif 'TemporalResolution' in data:
        temporal_resolution = data.TemporalResolution
        fps = 1000 // temporal_resolution
    elif 'FrameTimeVector' in data:
        frame_time_vector = data.FrameTimeVector
        if frame_time_vector:
            average_frame_time_ms = sum(frame_time_vector) / len(frame_time_vector)
            fps = 1000 // average_frame_time_ms
    else:
        raise ValueError("No CineRate or FrameTime attribute found in DICOM file")
    if fps is not None:
        fps = int(fps)
    print('fps:', fps)
    n = int(data.NumberOfFrames)
    print(f"Number of frames -> {n} frames")
    print(f"Duration of video will be -> {n // fps} seconds")
    print('----------------Video Conversion process-------------------')
    rows = int(data.Rows)
    cols = int(data.Columns)
    num_frames = data.NumberOfFrames
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps, (cols, rows))
    for frame_num in range(num_frames):
        frame_data = pixel_data[frame_num]     #getting the ith frame data from the pixel array
        frame_data = np.uint8(frame_data)      #Converting the frame data array into Unsigned integer 8-bot
        out.write(frame_data)
    out.release()
    print(f"Video converted and saved to this path -> {out_path}")


def to_png(data,out):
    print("--------PNG Conversion Process-----------")
    out_path = out + str(data.ReferringPhysicianName) + '_' + datetime.now().strftime("%Y%m%d-%H%M") + '_' + str(next_num(str(data.ReferringPhysicianName), out) + 1) + '.png'
    print(f"Image will be saved to this path -> {out_path}")
    if 'PixelData' in data:
        pixel_data = data.pixel_array
    else:
        raise ValueError("DICOM file does not contain pixel data.")
    img = Image.fromarray(pixel_data)
    img.save(out_path)
    print(f"Image saved to this path -> {out_path}")
    print("--------PNG Conversion Process Completed-----------")

def to_jpeg(data,out):
    print("-----------JPEG Conversion Process-------------")
    out_path = out + str(data.ReferringPhysicianName) + '_' + datetime.now().strftime("%Y%m%d-%H%M") + '_' + str(next_num(data.ReferringPhysicianName,out)+1) + '.jpg'
    print(f"Image will be saved to this path -> {out_path}")
    if 'PixelData' in data:
        pixel_data = data.pixel_array
    else:
        raise ValueError("DICOM file does not contain pixel data.")
    img = Image.fromarray(pixel_data)
    img.save(out_path)
    print(f"Image saved to this path -> {out_path}")
    print("--------JPEG Conversion Process Completed-----------")

def to_image(data, out):
    to_png(data,out)
    to_jpeg(data,out)


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
                to_video(data,out_path)
            else:
                print(f'Number of frames -> {n} frame')
                to_image(data,out_path)
    print('--------------------Execution Ended--------------------')

def dicom():
    inp = "../test/"            #provide with path for the input dicom files
    out = "../output_files/"            #provide with path for the output dicom files
    convert(out, inp)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dicom()