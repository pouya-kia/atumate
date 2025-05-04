# ML Pipeline API with FastAPI

## Overview
This project provides a full pipeline for data preprocessing and machine learning wrapped as a RESTful API using FastAPI. It supports loading data, cleaning, feature transformation, modeling, and evaluation via a single API endpoint.

## Features
- 🚀 Built with FastAPI for high performance
- 🧼 Data cleaning: drop columns, fill missing values, format dates
- 🧪 Feature processing: binning, one-hot encoding, outlier handling, correlation analysis
- 🤖 Machine learning: supports both supervised and unsupervised models
- 📦 Returns model metrics and logs in JSON format
- 🔌 Ready to connect to any frontend

## Quick Start

### Install requirements:
```bash
pip install -r requirements.txt
```

### Run the API:
```bash
uvicorn main:app --reload
```

### Test the API:
Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

Use `POST /api/run-pipeline` with payload including:
- `data`: JSON string of dataset
- `config`: configuration for preprocessing and modeling steps

## Example:
See `test_payload.json` for a working example.