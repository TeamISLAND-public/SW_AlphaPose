# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import argparse
import multiprocessing as mp
import os
import cv2
import torch
import tqdm

# config get_cfg, import read_image, import setup_logger is the one that import the file
from detectron2.config import get_cfg
from detectron2.utils.predictor_save import PredictorSave
from detectron2.utils.logger import setup_logger

# from predictor import PredictionDemo
# from visualizer import VisualizationDemo
from detectron2.utils.predictor import PredictionDemo
from detectron2.utils.pre_visualizer import VisualizationDemo

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
        # default=[],
        default=['MODEL.WEIGHTS', 'detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl',
                 'MODEL.DEVICE', 'cpu'],
        nargs=argparse.REMAINDER,
    )
    return parser

class open_demo:
    def __init__(self, video_input):
        mp.set_start_method("spawn", force=True)
        args = get_parser(video_input).parse_args()
        logger = setup_logger()
        logger.info("Arguments: " + str(args))

        cfg = setup_cfg(args)

        predictor = PredictionDemo(cfg)

        if args.video_input:
            video = cv2.VideoCapture(args.video_input)
            num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            output_fname = os.path.splitext(args.video_input)[0]

            try:
                prediction_result = torch.load('{}.pt'.format(output_fname)) #pt file is called Panther, a visual programming toolkit

            except IOError:
                predictor_data = []
                # item_list = ['num_instances','boxes','scores','classes','keypoints','masks']
                for predictions in tqdm.tqdm(predictor.run_on_video(video), total=num_frames):
                    cnt = predictions[0]
                    prediction = predictions[1]

                    predictor_save = PredictorSave()
                    prediction_output = predictor_save.save_instance_predictions(prediction)
                    if prediction_output is None:
                        item = {"current_frame": cnt}
                    else:
                        item = {"current_frame": cnt}
                        item["num_instances"] = prediction_output[0]
                        item["boxes"] = prediction_output[1]
                        item["scores"] = prediction_output[2]
                        item["classes"] = prediction_output[3]
                        item["keypoints"] = prediction_output[4]
                        item["masks"] = prediction_output[5]

                    predictor_data.append(item)
                    torch.save(predictor_data, '{}.pt'.format(output_fname))
        else:
            ("video_input is not correct")

if __name__ == "__main__":
    open_demo("C:/Users/daniel/PycharmProjects/Project1/test3.mp4")