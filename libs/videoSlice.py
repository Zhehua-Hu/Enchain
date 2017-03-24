#!/usr/bin/python
# coding=utf-8
""" """

import argparse
import os
import cv2


# TODO:
# add gray img


def showVideoInfo(video_path):
    try:
        vhandle = cv2.VideoCapture(video_path.encode('utf-8'))  # For read Chinease-name video
        fps = vhandle.get(cv2.CAP_PROP_FPS)
        count = vhandle.get(cv2.CAP_PROP_FRAME_COUNT)
        size = (int(vhandle.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(vhandle.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        ret, firstframe = vhandle.read()
        if ret:
            print("FPS: %.2f" % fps)
            print("COUNT: %.2f" % count)
            print("WIDTH: %d" % size[0])
            print("HEIGHT: %d" % size[1])
            return vhandle, fps, size, firstframe
        else:
            print("Video can not read!")
    except:
        "Error in showVideoInfo"

def videoSlice(video_path, save_path, progressbarsetter=None, save_type="png", img_comp=0, start_idx=1):
    """

    :param video_path:
    :param save_path:
    :param save_type:
    :param img_comp: default0:
                    None Higher number increase compressive level
                    png[0-9], jpg[0-100]
    :return:
    """

    # For read Chinease-name video
    vid_handle = cv2.VideoCapture(video_path.encode('utf-8'))
    fps = vid_handle.get(cv2.CAP_PROP_FPS)
    count = vid_handle.get(cv2.CAP_PROP_FRAME_COUNT)
    size = (int(vid_handle.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(vid_handle.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    prefix = os.path.basename(save_path)
    idx = start_idx  # start from 000001.xxx
    cnt_idx = 1

    params = None
    suffix = None
    if save_type.upper() == "JPEG" or save_type.upper() == "JPG":
        img_type = int(cv2.IMWRITE_JPEG_OPTIMIZE)
        suffix = ".jpg"
        params = [img_type, img_comp]
    elif save_type.upper() == "PNG":
        img_type = int(cv2.IMWRITE_PNG_COMPRESSION)
        suffix = ".png"
        params = [img_type, img_comp]
    else:
        print("Do not support %s format!" % save_type)

    while True:
        ret, frame = vid_handle.read()
        if ret:
            cur_progress = cnt_idx/(count/100.0)
            if progressbarsetter is not None:
                progressbarsetter(cur_progress)
            print("Progress %.2f%%" % cur_progress)
            img_name = save_path + "/" + ("%06d" % idx) + suffix
            # print img_name
            print params
            cv2.imwrite(img_name, frame, params)
            idx += 1
            cnt_idx += 1
        else:
            break
    print("Slicing Done!")
    return count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video_path_arg", help="Path of video", type=str)
    parser.add_argument("save_path_arg", help="Path of saved images", type=str)
    parser.add_argument("--save_type", help="Format of images", type=str)
    parser.add_argument("--img_comp", help="Compress level of images", type=int)
    args = parser.parse_args()
    if args.save_type is None:
        args.save_type = "png"
    if args.img_comp is None:
        args.img_comp = 0
    videoSlice(args.video_path, args.save_path, args.save_type)

