# 🌊 HydroShield — Water Safety Chemical Classification & Screening System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask-green.svg)](https://flask.palletsprojects.org/)
[![Model](https://img.shields.io/badge/ML%20Model-XGBoost-orange.svg)](https://xgboost.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

**HydroShield** is an end-to-end Machine Learning web application designed to evaluate water safety based on chemical contaminant concentrations. Utilizing an optimized **XGBoost classification pipeline**, HydroShield provides instant safety predictions ("Safe" vs. "Not Safe") alongside confidence probabilities to assist environmental analysts, municipal water managers, and researchers in screening water quality.

---

## 📌 Table of Contents

- [Overview & Objectives](#-overview--objectives)
- [Key Features](#-key-features)
- [Monitored Chemical Parameters](#-monitored-chemical-parameters)
- [System Architecture](#-system-architecture)
- [Project Directory Structure](#-project-directory-structure)
- [Installation & Setup](#-installation--setup)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Model & Machine Learning Pipeline](#-model--machine-learning-pipeline)
- [Presentation & Documentation Materials](#-presentation--documentation-materials)

---

## 💧 Overview & Objectives

Ensuring clean and safe drinking water is crucial for public health. Manual chemical evaluation across dozens of parameters can be complex and time-consuming. **HydroShield** addresses this challenge by:

1. **Automating Chemical Safety Classification**: Evaluating 20 distinct chemical, metallic, and microbiological contaminants in water samples.
2. **Accelerated Screening**: Allowing quick field screening by requiring user input for top-priority high-risk contaminants (Cadmium, Aluminium, Silver, Perchlorate, Arsenic) while imputing median values for secondary parameters.
3. **Providing Real-Time Risk Analysis**: Serving predictions via an intuitive, interactive web interface and a REST API.

---

## ✨ Key Features

- **XGBoost Machine Learning Model**: Trained and serialized pipeline ([`water_safety_xgboost_model.pkl`](file:///d:/Machine_learning/Capstone/water_safety_classification_capstone_project/water_safety_xgboost_model.pkl)) delivering high predictive accuracy.
- **Interactive Web Dashboard**: Modern UI built with Flask, HTML5, CSS3 (using Google Fonts *Outfit* & *Plus Jakarta Sans*), and JavaScript.
- **Dual Input Modes**:
  - **Quick Screening Mode**: Input values for the top 5 key contaminants; remaining parameters automatically default to dataset medians.
  - **Full Parameter Mode**: Option to override and supply custom values for all 20 monitored parameters.
- **RESTful API**: JSON `/api/predict` endpoint for seamless integration with external sensors, mobile apps, or IoT pipelines.
- **Comprehensive Jupyter Notebook**: Complete Exploratory Data Analysis (EDA), feature analysis, and model training workflow in [`water_quality_chemical_safety_project.ipynb`](file:///d:/Machine_learning/Capstone/water_safety_classification_capstone_project/water_quality_chemical_safety_project.ipynb).

---

## 🧪 Monitored Chemical Parameters

The classification pipeline evaluates water safety across **20 chemical and biological features** (in milligrams per liter, mg/L, or PPM):

| Feature Parameter | Type | Required in Quick Screening | Default Imputation (Median) |
| :--- | :--- | :---: | :---: |
| **Cadmium** (`cadmium`) | Heavy Metal | ✅ **Yes** | — |
| **Aluminium** (`aluminium`) | Heavy Metal | ✅ **Yes** | — |
| **Silver** (`silver`) | Heavy Metal | ✅ **Yes** | — |
| **Perchlorate** (`perchlorate`) | Industrial Chemical | ✅ **Yes** | — |
| **Arsenic** (`arsenic`) | Metalloid / Toxicant | ✅ **Yes** | — |
| **Ammonia** (`ammonia`) | Chemical Compound | ⚙️ Optional | `14.13` |
| **Barium** (`barium`) | Heavy Metal | ⚙️ Optional | `1.19` |
| **Chloramine** (`chloramine`) | Disinfectant | ⚙️ Optional | `0.53` |
| **Chromium** (`chromium`) | Heavy Metal | ⚙️ Optional | `0.09` |
| **Copper** (`copper`) | Heavy Metal | ⚙️ Optional | `0.75` |
| **Flouride** (`flouride`) | Mineral | ⚙️ Optional | `0.77` |
| **Bacteria** (`bacteria`) | Microbiological | ⚙️ Optional | `0.22` |
| **Viruses** (`viruses`) | Microbiological | ⚙️ Optional | `0.008` |
| **Lead** (`lead`) | Heavy Metal | ⚙️ Optional | `0.102` |
| **Nitrates** (`nitrates`) | Chemical Compound | ⚙️ Optional | `9.93` |
| **Nitrites** (`nitrites`) | Chemical Compound | ⚙️ Optional | `1.42` |
| **Mercury** (`mercury`) | Heavy Metal | ⚙️ Optional | `0.005` |
| **Radium** (`radium`) | Radioactive Element | ⚙️ Optional | `2.41` |
| **Selenium** (`selenium`) | Nonmetal | ⚙️ Optional | `0.05` |
| **Uranium** (`uranium`) | Radioactive Element | ⚙️ Optional | `0.05` |

---

## 🏗️ System Architecture

```text
  ┌─────────────────────────────────────────────────────────────┐
  │                        User Interface                       │
  │                  (Web Browser / REST Client)                 │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                    Flask Web Application                    │
  │                        (app.py)                             │
  │                                                             │
  │  - Routes: GET / (Dashboard), POST /api/predict             │
  │  - Input Parsing & Median Imputation (parse_measurements)   │
  └──────────────────────────────┬──────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                 XGBoost Machine Learning                    │
  │               (water_safety_xgboost_model.pkl)              │
  │                                                             │
  │  - Predicts probability of water safety (Index 1)           │
  │  - Threshold: >= 0.50 -> Safe | < 0.50 -> Not Safe          │
  └─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Directory Structure

```text
water_safety_classification_capstone_project/
├── app.py                                                   # Main Flask web application & API server
├── requirements.txt                                         # Python dependencies
├── water_safety_xgboost_model.pkl                           # Serialized XGBoost model pipeline
├── water_quality_chemical_safety_project.ipynb              # Jupyter notebook with EDA & model training
├── water_safety_classification_datasets.xlsx               # Raw dataset Excel file
├── templates/
│   └── index.html                                           # Main web application UI dashboard
├── HydroShield_Water_Quality_Filled_Presentation_Manish_Purohit.pptx  # Project PowerPoint presentation
├── Water Quality Chemical Safety Classification.docx        # Project report documentation
├── .vscode/
│   └── launch.json                                          # VS Code launch debug configuration
└── README.md                                                # Project documentation
```

---

## 🚀 Installation & Setup

### Prerequisites

- **Python 3.8+** installed on your system.
- `pip` (Python package installer).

### Step-by-Step Setup

1. **Clone or Navigate to the Repository Directory**:
   ```bash
   cd water_safety_classification_capstone_project
   ```

2. **Create and Activate a Virtual Environment** *(Recommended)*:
   - **On Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **On macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💡 Usage Guide

### Running the Web Application

To start the Flask development server:

```bash
python app.py
```

After starting, open your web browser and navigate to:
```text
http://127.0.0.1:5000/
```

### Running the Jupyter Notebook

To explore the dataset, perform data analysis, or retrain the model:

```bash
jupyter notebook water_quality_chemical_safety_project.ipynb
```

---

## 🔌 API Documentation

### Predict Water Safety

**Endpoint**: `POST /api/predict`  
**Content-Type**: `application/json` or `application/x-www-form-urlencoded`

#### Request Body Example (JSON)
```json
{
  "cadmium": 0.003,
  "aluminium": 0.05,
  "silver": 0.02,
  "perchlorate": 4.5,
  "arsenic": 0.01
}
```

#### Example cURL Command
```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "cadmium": 0.003,
    "aluminium": 0.05,
    "silver": 0.02,
    "perchlorate": 4.5,
    "arsenic": 0.01
  }'
```

#### Successful Response (`200 OK`)
```json
{
  "is_safe": true,
  "label": "Safe",
  "probability": 87.45
}
```

#### Validation Error Response (`400 Bad Request`)
```json
{
  "error": "Please enter a value for cadmium."
}
```

---

## 🤖 Model & Machine Learning Pipeline

- **Algorithm**: XGBoost (Extreme Gradient Boosting) Classifier.
- **Target Variable**: Binary Safety Indicator (`1` = Safe, `0` = Not Safe).
- **Features**: 20 numerical parameters covering heavy metals, inorganic compounds, and biological metrics.
- **Handling Missing Inputs**: Automated median imputation strategy ensuring continuous prediction capabilities without sacrificing accuracy.

---

## 📄 Presentation & Documentation Materials

This capstone project includes full presentation slides and formal written reports for stakeholders:
- 📊 **Presentation Deck**: [`HydroShield_Water_Quality_Filled_Presentation_Manish_Purohit.pptx`](file:///d:/Machine_learning/Capstone/water_safety_classification_capstone_project/HydroShield_Water_Quality_Filled_Presentation_Manish_Purohit.pptx)
- 📝 **Detailed Project Report**: [`Water Quality Chemical Safety Classification.docx`](file:///d:/Machine_learning/Capstone/water_safety_classification_capstone_project/Water%20Quality%20Chemical%20Safety%20Classification.docx)

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Machine Learning & Data**: XGBoost, Scikit-Learn, Pandas, NumPy, OpenPyXL
- **Frontend**: HTML5, Vanilla CSS, JavaScript, Google Fonts
- **Development & IDE**: Jupyter Notebook, VS Code

---

## 👨‍💻 Author

**Manish Purohit**  
*Data Science / Machine Learning Capstone Project*
