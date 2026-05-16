# TruthLens — Machine Learning-Based Fake News Detection System

A Data Mining project that uses TF-IDF vectorization and Naive Bayes machine learning to detect fake news articles in real-time.

---

# 🎯 Project Overview

TruthLens is an intelligent system for automatic detection of fake news articles using Natural Language Processing (NLP) and Machine Learning techniques. It provides fast, scalable, and accurate classification of news content as Real or Fake with confidence scores.

---

# 🏗️ Architecture

```text
┌─────────────────┐     ┌──────────────────────┐
│  React Frontend │────▶│  Flask API Backend   │
│  (Vite + TS)    │◀────│  (Python + Flask)    │
└─────────────────┘     └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │ Machine Learning Layer│
                        │  - Text Preprocessing │
                        │  - TF-IDF Vectorizer  │
                        │  - Naive Bayes Model  │
                        └──────────────────────┘
```

---

# 🔬 Process Flow

1. **Input** → Raw news article text  
2. **NLP Preprocessing** → Lowercasing, stop-word removal, punctuation cleaning  
3. **TF-IDF Vectorization** → Convert text into numerical feature vectors  
4. **Naive Bayes Analysis** → Classification using probabilistic machine learning  
5. **Prediction** → Binary classification with confidence probability  

---

# ✨ Features

- 🧠 **Naive Bayes Machine Learning Model** — Fast and lightweight text classification
- 📝 **NLP Preprocessing Pipeline** — Text cleaning and normalization
- 📊 **Interactive Visualizations** — Metrics dashboard and analytics
- 🎯 **Confidence Scoring** — Probability-based prediction results
- 📈 **Model Metrics** — Accuracy, Precision, Recall, and F1-Score evaluation
- 🕐 **Prediction History** — Local storage of previous analyses
- 🌗 **Dark Mode** — Full dark/light theme support

---

# 🛠️ Tech Stack

## Frontend

- React 18 + TypeScript
- Vite — Build tool
- Tailwind CSS + shadcn/ui — Styling
- Recharts — Data visualization

## Backend

- Python — Core language
- Flask — REST API server
- Scikit-learn — TF-IDF and Naive Bayes model
- NLTK — Text preprocessing
- Pandas & NumPy — Data manipulation

---

# 📂 Dataset

**Kaggle Fake News Dataset** — 44,898 labeled news articles

---

# 🚀 Getting Started

## Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- pip or conda

---

## 1. Install Frontend Dependencies

```bash
npm install
```

---

## 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

## 3. Prepare Dataset

```bash
cd backend
python prepare_dataset.py
```

---

## 4. Train the Model

```bash
cd backend
python train.py
```

This trains the TF-IDF + Naive Bayes model and saves the trained files.

---

## 5. Start the Backend

```bash
cd backend
python app.py
```

---

## 6. Start the Frontend

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

in your browser.

---

# 📊 Model Performance

| Metric | Score |
|--------|--------|
| Accuracy | 92.6% |
| Precision | 93.1% |
| Recall | 91.8% |
| F1 Score | 92.4% |

---

# 📁 Project Structure

```text
truthlens/
├── backend/
│   ├── app.py                  # Flask API server
│   ├── train.py                # Model training script
│   ├── prepare_dataset.py      # Dataset preparation script
│   ├── requirements.txt        # Python dependencies
│   ├── model/
│   │   └── preprocess.py       # NLP preprocessing pipeline
│   ├── data/                   # Dataset files
│   └── saved_model/            # Trained model artifacts
│
├── src/
│   ├── components/truthlens/   # React components
│   ├── pages/Index.tsx         # Main application page
│   ├── lib/api.ts              # API client
│   └── index.css               # Design system
│
├── index.html
├── package.json
├── tailwind.config.ts
└── vite.config.ts
```

---

# 🎓 Academic Context

- **Project Title:** TruthLens: Machine Learning-Based Fake News Detection System
- **Course:** Data Mining
- **Objective:** Design an AI-powered system to classify news articles as Real or Fake using TF-IDF vectorization and Naive Bayes machine learning with NLP preprocessing.

---

# 📌 Model Pipeline

```text
News Article
      ↓
Text Preprocessing
      ↓
TF-IDF Vectorization
      ↓
Naive Bayes Classification
      ↓
Prediction Output
```

---

# TruthLens