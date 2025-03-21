# 🎬 SmartScene Navigator  
**An interactive video player with automatic scene detection & structured navigation.**  

[![Demo Video](https://img.youtube.com/vi/7ZWW_gZ76U8/maxresdefault.jpg)](https://youtu.be/7ZWW_gZ76U8)

## 📌 Overview  
SmartScene Navigator processes videos by **automatically detecting scenes, shots, and subshots**, creating a structured **table of contents** for seamless navigation. The interactive player allows users to **jump between different segments**, ensuring synchronized **video and audio playback**.  

---

## 🛠 Tech Stack  
- **Python** – Core development  
- **OpenCV** – Video processing & analysis  
- **SceneDetect** – Scene and shot segmentation  
- **Pygame** – Audio playback & UI integration  
- **JSON** – Storing scene-shot metadata  

---

## 🚀 Features  
✔ **Automatic Scene, Shot, & Subshot Detection**  
✔ **Clickable Navigation Through Video Segments**  
✔ **Real-time Video & Audio Synchronization**  
✔ **User-friendly Interface for Seamless Playback**  
✔ **JSON-based Metadata Storage for Easy Access**  

---

## 📂 Project Structure  
```
SmartSceneNavigator/
├── data/                 # Sample video & audio files
├── scripts/              # Core processing scripts
│   ├── main.py           # Extracts scenes, shots, subshots
│   ├── parse_json.py     # Reads & verifies JSON structure
│   ├── ui.py             # Interactive video player
│   ├── shot.py           # Defines Shot class & motion analysis
├── utils/                # Helper functions (motion detection, indexing)
├── requirements.txt      # Dependencies
├── README.md             # Project documentation
```

---

## ▶ How to Run  

### 1️⃣ Install Dependencies  
```bash
pip install -r requirements.txt
```

### 2️⃣ Run the Interactive Video Player  
```bash
python ui.py InputVideo.rgb InputAudio.wav
```

This opens the player, displaying the video alongside an interactive **scene-shot hierarchy**.

---

## 📜 License  
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.  

---

## 📬 Contact  
For any questions, feel free to open an issue or submit a pull request. Happy exploring! 🎥  

