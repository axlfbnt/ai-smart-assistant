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

def run_webcam_detection():
    st.sidebar.subheader("📷 Real-time Detection Settings")
    confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.05)
    skip_frames = st.sidebar.slider("Skip Frames", 0, 10, 2, 1)
    resize_factor = st.sidebar.slider("Resize Factor", 0.2, 1.0, 0.5, 0.1)
    max_detections = st.sidebar.slider("Max Detections", 1, 100, 20, 1)

    st.markdown("---")
    st.markdown("### Kamera Live Detection")
    video_placeholder = st.empty()

    col1, col2 = st.columns(2)
    with col1:
        start = st.button("Start Camera")
    with col2:
        stop = st.button("Stop Camera")

    if 'cap' in st.session_state and st.session_state.cap is not None:
        st.session_state.cap.release()
        st.session_state.cap = None
        st.session_state.webcam_running = False

    if start:
        camera_options = ["0", "1", "2", "3"]
        selected_camera = st.selectbox("Pilih kamera:", camera_options, index=0)

        try:
            st.session_state.cap = cv2.VideoCapture(int(selected_camera))
            cap = st.session_state.cap
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            if not cap.isOpened():
                st.error(f"Tidak bisa membuka kamera {selected_camera}")
            else:
                st.session_state.webcam_running = True
                st.info("Webcam aktif. Tekan 'Stop Camera' untuk berhenti.")

                while st.session_state.webcam_running:
                    ret, frame = cap.read()
                    if not ret:
                        st.error("Gagal membaca frame dari kamera.")
                        break

                    frame_count = st.session_state.get("frame_count", 0)
                    st.session_state.frame_count = frame_count + 1

                    if frame_count % (skip_frames + 1) != 0:
                        continue

                    if resize_factor < 1.0:
                        h, w = frame.shape[:2]
                        frame = cv2.resize(frame, (int(w * resize_factor), int(h * resize_factor)))

                    processed = detect_objects(frame, confidence_threshold, max_detections)
                    video_placeholder.image(processed, channels="RGB", use_container_width=True)

                    if stop:
                        st.session_state.webcam_running = False
                        break

                cap.release()
                st.session_state.cap = None
                st.session_state.webcam_running = False
                st.success("Webcam dihentikan.")
        except Exception as e:
            st.error(f"Kesalahan kamera: {e}")
            if 'cap' in st.session_state and st.session_state.cap is not None:
                st.session_state.cap.release()
                st.session_state.cap = None

    if 'webcam_running' not in st.session_state:
        st.session_state.webcam_running = False
    if 'cap' not in st.session_state:
        st.session_state.cap = None