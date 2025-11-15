import gradio as gr
from ultralyticsplus import YOLO, render_result

# Load YOLOv8 football model from Hugging Face
model = YOLO("uisikdag/football_players_rf")

# Optional: tune model thresholds (from model README)
model.overrides["conf"] = 0.25  # confidence threshold
model.overrides["iou"] = 0.45   # NMS IoU threshold
model.overrides["agnostic_nms"] = False
model.overrides["max_det"] = 1000


def detect_football_objects(image):
    # Run inference
    results = model.predict(image)
    result = results[0]

    # Render bounding boxes on the image
    rendered = render_result(
        model=model,
        image=image,
        result=result
    )

    return rendered


demo = gr.Interface(
    fn=detect_football_objects,
    inputs=gr.Image(type="pil", label="Upload a football frame"),
    outputs=gr.Image(type="pil", label="Detections"),
    title="VeoVision Prototype – YOLOv8 Football Detector",
    description=(
        "Simple prototype using a Hugging Face YOLOv8 model trained on football. "
        "Upload a frame to detect players, referees, goalkeepers, and the ball."
    ),
)


if __name__ == "__main__":
    demo.launch()


