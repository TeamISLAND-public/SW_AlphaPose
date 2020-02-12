# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import argparse
import multiprocessing as mp
import os
import cv2
import torch
import tqdm

# config get_cfg, import read_image, import setup_logger is the one that import the file
from detectron2.config import get_cfg
from detectron2.utils.pre_visualizer import VisualizationDemo
from PyQt5.QtGui import QImage, QPixmap

# constants
WINDOW_NAME = "COCO detections"

def setup_cfg(args):
    # load config from file and command-line arguments
    cfg = get_cfg()
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    # Set score_threshold for builtin models
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = args.confidence_threshold
    cfg.freeze()
    return cfg

def get_parser(video_input):
    parser = argparse.ArgumentParser(description="Detectron2 Demo")
    parser.add_argument(
        "--config-file",
        default="Library/detectron2/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml",
        metavar="FILE",
        help="path to config file",
    )
    parser.add_argument(
        "--video-input",
        default="{}".format(video_input),
        help="Path to video file.")
    parser.add_argument(
        "--output",
        help="A file or directory to save output visualizations. "
        "If not given, will show output in an OpenCV window.",
    )
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.5,
        help="Minimum score for instance predictions to be shown",
    )
    parser.add_argument(
        "--opts",
        help="Modify config options using the command-line 'KEY VALUE' pairs",
        default=['MODEL.WEIGHTS', 'detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl',
                 'MODEL.DEVICE', 'cpu'],
        nargs=argparse.REMAINDER,
    )
    return parser

class run_demo:
    def __init__(self, video_input, effect_type, current_frame):
        mp.set_start_method("spawn", force=True)
        self.args = get_parser(video_input).parse_args()
        cfg = setup_cfg(self.args)

        self.effect_type = effect_type
        self.current_frame = current_frame
        self.list = []
        self.visualizer = VisualizationDemo(cfg)

    def run(self):
        args = self.args
        if args.video_input:
            video = cv2.VideoCapture(args.video_input)
            num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            output_fname = os.path.splitext(args.video_input)[0]

            try:
                # pt file is called Panther, a visual programming toolkit
                prediction_result = torch.load('{}.pt'.format(output_fname))
                for vis_frame in tqdm.tqdm(self.visualizer.run_on_video(video, prediction_result, self.effect_type, self.current_frame),
                                           total=num_frames):
                    img = QImage(vis_frame, vis_frame.shape[1], vis_frame.shape[0], QImage.Format_BGR888)
                    pix = QPixmap.fromImage(img)
                    resized_pix = pix.scaled(640, 480)
                    self.list.append((True, resized_pix))
                return self.list

            except IOError:
                print("There is no compatible .pt file")
        else:
            ("video_input is not correct")

if __name__ == "__main__":
    run_demo("C:/Users/daniel/PycharmProjects/Project1/test3.mp4")