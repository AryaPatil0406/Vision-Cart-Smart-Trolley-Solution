# Vision-Cart-Smart-Trolley-Solution
Project Overview
VISION CART is a smart shopping cart system that eliminates manual billing and enhances customer experience using real-time object detection. Leveraging a high-definition webcam, YOLOv8, and a custom-trained dataset from Roboflow, it identifies grocery items and updates the bill dynamically as items are added or removed.


## Key Features
🧠 YOLOv8-Based Detection – Highly accurate object detection with up to 98.6% accuracy.

🎥 Real-Time Video Processing – Live detection at 20 FPS using IP camera feed.

📱 Web Interface – Upload video for detection, display billing and invoice in real-time.

🧾 Automated Billing – Itemized billing system with payment gateway integration.

🔐 Fraud Prevention – Prevents misclassification and theft via persistent object tracking.

📊 High-Performance Inference – Optimized with TensorRT for edge deployment.


## Technologies Used
| Component        | Technology                          |
| ---------------- | ----------------------------------- |
| Object Detection | YOLOv8 (Ultralytics)                |
| Dataset Platform | Roboflow (9,935 images, 84 classes) |
| Training Env     | Google Colab with NVIDIA T4 GPU     |
| Inference Device | Intel i5 + NVIDIA MX450             |
| Camera           | 6MP IP camera with night vision     |
| Frontend         | Flask Web Interface                 |
| Model Export     | ONNX / TensorRT                     |
| Deployment       | Edge-Optimized Setup                |


## Dataset Overview
Size: 9,935 images

Classes: 84 grocery items

Split:

Train: 93%

Validation: 6%

Test: 1%

Preprocessing: Resize to 640×640, auto-orient

Augmentation: None applied


## System Architecture
flowchart TD
    A[IP Camera Input] --> B[YOLOv8 Inference]
    B --> C[Object Tracking + Filtering]
    C --> D[Database Lookup for Pricing]
    D --> E[Real-Time Invoice Generation]
    E --> F[Web Interface Display]
    F --> G[Payment Gateway Integration]

## Performance Metrics
Detection Accuracy: 98.4% on Test Set

FPS: 20 (Real-time on GPU setup)

F1-Score: 0.78 at 0.378 confidence threshold

Misclassification: <2%, mostly among visually similar products

## Project Structure
vision-cart/
│
├── dataset/                  # Roboflow-exported dataset
├── yolov8_model/            # YOLOv8 training weights and configs
├── app/                     # Flask-based frontend interface
│   ├── templates/
│   ├── static/
│   └── app.py
├── results/                 # Screenshots, test videos, graphs
├── utils/                   # Helper scripts for tracking, data loading
├── requirements.txt         # Python dependencies
└── README.md


## How to Run
git clone https://github.com/yourusername/vision-cart.git
cd vision-cart

