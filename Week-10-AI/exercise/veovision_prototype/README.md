# VeoVision Prototype – YOLOv8 Football Detector (Gradio)

This is a minimal Gradio app using a Hugging Face YOLOv8 model trained on football:

- Model: `uisikdag/football_players_rf`
- Labels: `['ball', 'goalkeeper', 'player', 'referee']`

## How to Deploy on Hugging Face Spaces

1. Go to Hugging Face → Spaces → New Space.
2. Choose:
   - SDK: **Gradio**
   - Space name: e.g. `veovision-prototype`
3. After the Space is created, upload the following two files:
   - `app.py`
   - `requirements.txt`
4. The Space will auto-build and start. Upload a football frame to see detections.

## Local Run (optional)

```bash
pip install -r requirements.txt
python app.py
```


