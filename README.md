# HO_DPR Dataset Analysis and API Application 🧠📈
Welcome to the HO_DPR Dataset Analysis and API Application, a professional project designed for an Algorithms course. This project uses FastAPI to build a RESTful API and Streamlit for an interactive user interface to analyze and predict patterns in the provided HO_DPR dataset. The project showcases the integration of web APIs, machine learning models, and data visualization.

---
# Features 📊

# 1- Interactive API:
. Read predictions: Post structured inputs to receive predictions.
. Homepage: A friendly introduction to the API.
# 2- Streamlit Dashboard:
. Visualize the HO_DPR dataset interactively.
. User-friendly interface with real-time charts and model insights.
# 3- Machine Learning:
. Pre-trained machine learning model to generate predictions.

---
# Requirements

Python >= 3.8
FastAPI
Uvicorn
Streamlit
Pandas, NumPy, scikit-learn
Pickle (for loading saved models and scalers)

---
# Usage
1. Start the FastAPI server to host the RESTful API.
2. Launch the Streamlit dashboard to explore the dataset and interact with model predictions.
3. Send POST requests to the /predict endpoint with structured inputs to receive model predictions.

---
# Project Structure

HO_DPR-Project/

│
├── api/                           # FastAPI-related files

│   ├── main.py                    # API entry point

│   └── model_utils.py             # Utilities for model loading and preprocessing

│

├── dashboard/                     # Streamlit-related files

│   └── streamlit_app.py           # Streamlit dashboard

│

├── models/                        # Saved machine learning models

│   ├── ho_dpr_model.pkl           # Trained model

│   └── ho_dpr_scaler.pkl          # Scaler for preprocessing

│

├── data/                          # Data-related files

│   └── HO_DPR.csv                 # Dataset used in the project

│

├── requirements.txt               # Project dependencies

├── README.md                      # Project documentation (this file)

└── LICENSE                        # Project license (e.g., MIT)


---
# Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
git checkout -b feature/new-feature

3. Commit your changes:
git commit -am 'Add new feature'

4. Push to the branch:
git push origin feature/new-feature

5. Open a pull request.


---
# License
This project is licensed under the MIT License. See the LICENSE file for details.


---
# Developed by YasamanBadeli 
Feel free to suggest additional enhancements or share feedback! 🚀
