import streamlit as st
import cv2
import numpy as np
import torch
from PIL import Image
from transformers import DetrImageProcessor, DetrForObjectDetection

@st.cache_resource
def load_model():
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
    model = model.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
    return processor, model, model.config.id2label

processor, model, id2label = load_model()

def detect_objects(image, confidence_threshold=0.5, max_detections=20):
    if isinstance(image, np.ndarray):
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    with torch.no_grad():
        inputs = processor(images=image, return_tensors="pt")
        outputs = model(**inputs)

    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=confidence_threshold)[0]

    img_array = np.array(image)
    sorted_indices = sorted(range(len(results["scores"])), key=lambda i: results["scores"][i], reverse=True)[:max_detections]

    for idx in sorted_indices:
        score = results["scores"][idx]
        label = results["labels"][idx]
        box = results["boxes"][idx]
        box = [round(i) for i in box.tolist()]
        class_name = id2label[label.item()]
        confidence = round(score.item(), 3)
        cv2.rectangle(img_array, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
        cv2.putText(img_array, f"{class_name}: {confidence:.2f}", (box[0], box[1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return img_array

def run_image_detection():
    st.sidebar.subheader("🖼️ Image Detection Settings")
    confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.05)
    max_detections = st.sidebar.slider("Max Detections", 1, 100, 20, 1)

    st.markdown("---")
    st.markdown("### Upload Gambar untuk Deteksi")
    uploaded_img = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_img is not None:
        image = Image.open(uploaded_img)
        st.image(image, caption="Gambar Diupload", use_container_width=True)

        if st.button("Detect Objects"):
            with st.spinner("Processing..."):
                result_image = detect_objects(image, confidence_threshold, max_detections)
                st.image(result_image, caption="Hasil Deteksi", use_container_width=True)