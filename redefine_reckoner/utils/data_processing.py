import json
import pandas as pd
import streamlit as st
from redefine_reckoner.config import CHECKOUT_TYPES_FILE, VERTICAL_NAMES_FILE, METHODS_FILE

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def filter_data(checkout_type, vertical_name, methods_of_choice, df):
    df['Method'] = df['Method'].ffill()

    selected_checkout = checkout_type
    selected_vertical = vertical_name
    methods_of_choice = [method.strip() for method in methods_of_choice]

    filtered_df = df[df['Method'].isin(methods_of_choice)]
    relevant_columns = ['Method', 'Name of the  Feature', 'Availability', selected_checkout, selected_vertical]

    missing_columns = [col for col in relevant_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Error accessing columns: Missing columns {missing_columns}")
        return None

    filtered_df = filtered_df[relevant_columns]
    filtered_df['Implementation Status'] = 'Select'
    
    return filtered_df

def load_static_data():
    checkout_data = load_json_data(CHECKOUT_TYPES_FILE)
    vertical_data = load_json_data(VERTICAL_NAMES_FILE)
    methods_data = load_json_data(METHODS_FILE)
    return checkout_data, vertical_data, methods_data