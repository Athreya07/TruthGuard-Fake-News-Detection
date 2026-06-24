# TruthGuard Lite - Fake News Detection System

This is a machine learning fake news detection project built using your uploaded dataset.

## Important
- No database
- No SQL
- No login/signup
- No prediction history stored
- Simple Flask web UI
- ML model uses TF-IDF + Logistic Regression

## Dataset Used
The project uses:

- `data/Fake.csv`
- `data/True.csv`

The model combines title + text and trains on two labels:

- `FAKE`
- `REAL`

## Current Model Accuracy

Accuracy on test split: `98.94%`

## How to Run

Open CMD inside the project folder:

```bat
cd Truth Guard
py -3.12 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd backend
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Train Model Again

The trained model is already included, but if you want to retrain:

```bat
cd NoDB_TruthGuard_FakeNews
venv\Scripts\activate
cd backend
python train_model.py
```

## Project Structure

```text
NoDB_TruthGuard_FakeNews/
│
├── data/
│   ├── Fake.csv
│   └── True.csv
│
├── models/
│   ├── fake_news_model.pkl
│   └── metrics.json
│
├── backend/
│   ├── app.py
│   ├── train_model.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── css/
│           └── style.css
│
└── requirements.txt
```

## How It Works

The system converts news text into numerical features using TF-IDF.  
Then Logistic Regression classifies the article as FAKE or REAL.

It does not save user data anywhere.
