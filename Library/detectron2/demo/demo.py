# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import argparse
import glob
import multiprocessing as mp
import os
import time
import cv2
import tqdm
import json
import numpy

# config get_cfg, import read_image, import setup_logger is the one that import the file
from detectron2.config import get_cfg
from detectron2.data.detection_utils import read_image
from detectron2.utils.video_visualizer import VideoVisualizer
from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2.utils.logger import setup_logger

from predictor import PredictionDemo
from visualizer import VisualizationDemo

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


def get_parser():
    parser = argparse.ArgumentParser(description="Detectron2 Demo")
    parser.add_argument(
        "--config-file",
        default="configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml",
        metavar="FILE",
        help="path to config file",
    )
    parser.add_argument("--video-input", help="Path to video file.")
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
        default=[],
        nargs=argparse.REMAINDER,
    )
    return parser


if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    args = get_parser().parse_args()
    logger = setup_logger()
    logger.info("Arguments: " + str(args))

    cfg = setup_cfg(args)

    predictor = PredictionDemo(cfg)
    visualizer = VisualizationDemo(cfg)

    if args.video_input:
        video = cv2.VideoCapture(args.video_input)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frames_per_second = video.get(cv2.CAP_PROP_FPS)
        current_frame = video.get(cv2.CAP_PROP_POS_FRAMES)
        num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        basename = os.path.basename(args.video_input)

        if args.output:
            if os.path.isdir(args.output):
                output_fname = os.path.join(args.output, basename)
                output_fname = os.path.splitext(output_fname)[0]
            else:
                output_fname = args.output
            assert not os.path.isfile(output_fname), output_fname
        assert os.path.isfile(args.video_input)

        try:
            f = open("{}.json".format(output_fname))
            loaded_json = json.load(f)
            for x in loaded_json:
                print(x)
                # print(loaded_json[x])
            # Temporary unlock
            # output_file = cv2.VideoWriter(
            #     filename=output_fname,
            #     # some installation of opencv may not support x264 (due to its license),
            #     # you can try other format (e.g. MPEG)
            #     fourcc=cv2.VideoWriter_fourcc(*"MP4V"),
            #     fps=float(frames_per_second),
            #     frameSize=(width, height),
            #     isColor=True,
            # )
            # for vis_frame in tqdm.tqdm(visualizer.run_on_video(video), total=num_frames):
            #     if args.output:
            #         output_file.write(vis_frame)
            #     else:
            #         cv2.namedWindow(basename, cv2.WINDOW_NORMAL)
            #         cv2.imshow(basename, vis_frame)
            #         if cv2.waitKey(1) == 27:
            #             break  # esc to quit
            # video.release()
            # if args.output:
            #     output_file.release()
            # else:
            #     cv2.destroyAllWindows()

        except IOError:
            predictor_data = []
            for predictions in tqdm.tqdm(predictor.run_on_video(video), total=num_frames):
                cnt = predictions[0]
                prediction = predictions[1]
                item = {"current_frame": cnt}

                num_instances = len(predictions)
                # if num_instances == 0:
                #     return None
                #
                # boxes = predictions.pred_boxes.tensor.numpy() if predictions.has("pred_boxes") else None
                # scores = predictions.scores if predictions.has("scores") else None
                # classes = predictions.pred_classes.numpy() if predictions.has("pred_classes") else None
                # keypoints = predictions.pred_keypoints if predictions.has("pred_keypoints") else None

                item["num_instances"] = num_instances
                # item["boxes"] = boxes

                predictor_data.append(item)
                print(predictor_data)
                # if predictions[1].has("pred_masks"):
                #     masks = predictions[1].pred_masks
                # frame = predictions[0]
                # a = (masks.any(dim=0) > 0).numpy() if masks is not None else None
                # masks_numpy = a * 1
                # masks_numpy = masks_numpy.tolist()
            jsonData=json.dumps(item)
                # json_data[frame] = predictions[1]
            with open("{}.json".format(output_fname), "w") as write_file:
                 json.dump(jsonData, write_file)