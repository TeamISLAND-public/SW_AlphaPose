# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import argparse
import multiprocessing as mp
import os
import cv2
import torch
import numpy as np

from PyQt5.QtWidgets import QMessageBox

# config get_cfg, import read_image, import setup_logger is the one that import the file
from detectron2.config import get_cfg
from detectron2.utils.pre_visualizer import VisualizationDemo

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
    def __init__(self, video_input, effect_type, current_frame, clicked_positions):
        mp.set_start_method("spawn", force=True)
        self.args = get_parser(video_input).parse_args()
        cfg = setup_cfg(self.args)

        self.clicked_positions = clicked_positions
        self.effect_type = effect_type
        self.current_frame = current_frame
        self.result_list = []
        self.truth_list = []
        self.summarized_truth_list = []
        self.visualizer = VisualizationDemo(cfg)

    def run(self):
        args = self.args
        if not self.clicked_positions:
            print("no position selected")
            return
        else:
            self.np_clicked_positions = np.array(self.clicked_positions)

        if args.video_input:
            video = cv2.VideoCapture(args.video_input)
            output_fname = os.path.splitext(args.video_input)[0]
            if os.path.isfile('{}.pt'.format(output_fname)):
                prediction_result = torch.load('{}.pt'.format(output_fname))
                for i in range(prediction_result[self.current_frame]["num_instances"]):
                    print(i)
                    self.truth_list.clear()
                    for position in self.np_clicked_positions:
                        self.truth_list.append(prediction_result[self.current_frame]["masks"][i][position[1]][position[0]])
                    print(self.truth_list)
                    if not any(self.truth_list):
                        for a in range(40):
                            prediction_result[self.current_frame+a-10]["masks"][i] = False
                    self.summarized_truth_list.append(any(self.truth_list))
                print(self.summarized_truth_list)
                if not any(self.summarized_truth_list):
                    print("selected part is not compatible with prediction")
                    self.summarized_truth_list.clear()
                    # due to return nothing in this progress self.clicked_position is not initialized
                    return
                else:
                    for vis_frame in self.visualizer.run_on_video(video, prediction_result, self.effect_type,
                                                                  self.current_frame):
                        self.result_list.append((True, vis_frame))
                    return self.result_list
            else:
                print("There is some error include .pt")
                return
        else:
            print("video_input is not correct")
            return