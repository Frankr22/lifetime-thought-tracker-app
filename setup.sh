#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run src/main.py
