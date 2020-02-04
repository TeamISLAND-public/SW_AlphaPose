class PredictorSave:
    def __init__(self, current_frame, predictions):
        self.predictions = predictions
        self.current_frame = current_frame

    def save_instance_predictions(self, predictions):
        num_instances = len(predictions)
        if num_instances == 0:
            return None

        boxes = predictions.pred_boxes.tensor.numpy() if predictions.has("pred_boxes") else None
        scores = predictions.scores if predictions.has("scores") else None
        classes = predictions.pred_classes.numpy() if predictions.has("pred_classes") else None
        keypoints = predictions.pred_keypoints if predictions.has("pred_keypoints") else None

