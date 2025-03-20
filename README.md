# 🎬 SmartScene Navigator  
*An interactive video player with automatic scene detection and structured navigation.*

## 📌 Overview  
SmartScene Navigator processes videos by **automatically detecting scenes, shots, and subshots**, generating a structured **table of contents** for easy navigation. The interactive player allows users to **jump between different segments seamlessly**, with synchronized **video and audio playback**.

## 🛠 Tech Stack  
- **Python** – Core development  
- **OpenCV** – Video processing & analysis  
- **SceneDetect** – Scene and shot segmentation  
- **Pygame** – Audio playback & synchronization  
- **JSON** – Storing scene-shot metadata  

## 🚀 Features  
✔ **Automated Scene & Shot Detection** using motion analysis  
✔ **Interactive Video Player** with real-time navigation  
✔ **Hierarchical Indexing** (Scenes → Shots → Subshots)  
✔ **Seamless Audio-Video Synchronization**  
✔ **JSON-Based Metadata for Easy Integration**  



## ▶ How to Run  

### 1️⃣ Install Dependencies  
```bash
pip install -r requirements.txt
```

### 2️⃣ Extract Scene-Shot Metadata  
```bash
python scripts/script.py --file output.json --folder /path/to/video
```

### 3️⃣ Verify JSON Structure  
```bash
python scripts/parse_json.py output.json
```

### 4️⃣ Convert Video to RGB (if needed)  
```python
import cv2

cap = cv2.VideoCapture("InputVideo.mp4")
with open("InputVideo.rgb", "wb") as f:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        f.write(frame.tobytes())
cap.release()
```

### 5️⃣ Run the Interactive Video Player  
```bash
python scripts/ui.py InputVideo.rgb InputAudio.wav
```

## 📜 License  
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.  

## 📬 Contact  
For any questions, feel free to reach out via **GitHub Issues** or submit a **Pull Request**! 🚀
