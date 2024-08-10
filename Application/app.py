import sqlite3
import pandas as pd
import streamlit as st
import time
import json
import os

@st.cache_data
def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        st.error(f"JSON file not found: {file_path}")
        return None
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON file: {file_path}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while loading JSON: {str(e)}")
        return None

def get_data_from_db(db_path, query):
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except sqlite3.DatabaseError as e:
        st.error(f"Database error: {str(e)}")
        return None
    except sqlite3.OperationalError as e:
        st.error("Database operation failed. Please ensure the database and tables are correctly configured.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return None

def filter_data(checkout_type, vertical_name, methods_of_choice, df):
    df['Method'] = df['Method'].ffill()

    selected_checkout = checkout_type
    selected_vertical = vertical_name
    methods_of_choice = [method.strip() for method in methods_of_choice]

    filtered_df = df[df['Method'].isin(methods_of_choice)]
    relevant_columns = ['Method', 'Name of the Feature', 'Availability', selected_checkout, selected_vertical]

    missing_columns = [col for col in relevant_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Error accessing columns: Missing columns {missing_columns}")
        return None

    filtered_df = filtered_df[relevant_columns]
    filtered_df['Implementation Status'] = 'Select'
    filtered_df['Comments'] = ''  # Adding the Comments column

    return filtered_df

def main():
    st.set_page_config(page_title="Redefine Ready Reckoner", layout="wide")
    
    if 'filtered_df' not in st.session_state:
        st.session_state.filtered_df = None
    if 'show_success' not in st.session_state:
        st.session_state.show_success = False

    # Load full dataset from the database
    db_path = "data/redefine_reckoner.db"
    full_df = get_data_from_db(db_path, "SELECT * FROM features")

    # Load static data from JSON files
    checkout_data = load_json_data('data/checkout_types.json')
    vertical_data = load_json_data('data/vertical_names.json')
    methods_data = load_json_data('data/methods.json')

    st.sidebar.title("Navigation")
    option = st.sidebar.radio("Select a Page", ["Home", "View Ready Reckoner"])

    if option == "Home":
        st.title("🚀 Redefine Ready Reckoner")
        
        col1, col2 = st.columns(2)
        
        with col1:
            checkout_type = st.selectbox("Select Checkout Type:", checkout_data["checkout_types"])
            vertical_name = st.selectbox("Select Vertical Name:", vertical_data["vertical_names"])
        
        with col2:
            methods_of_choice = st.multiselect("Select Methods of Choice:", methods_data["methods"])

        if st.button("Filter Data", type="primary"):
            if methods_of_choice:
                with st.spinner('Filtering data...'):
                    st.session_state.filtered_df = filter_data(checkout_type, vertical_name, methods_of_choice, full_df)
            else:
                st.warning("Please select at least one method.")
        
        if st.session_state.filtered_df is not None:
            st.subheader("Filtered Data")
            
            # Display the DataFrame with the data editor
            column_config = {
                'Implementation Status': st.column_config.SelectboxColumn(
                    options=['Implemented', 'Suggested', 'Not Applicable', 'Not Implemented'],
                    label='Implementation Status',
                    help='Choose the implementation status for each feature.',
                    width='medium',
                    required=True
                )
            }
            
            # Add text input for comments
            st.session_state.filtered_df['Comments'] = st.session_state.filtered_df['Comments'].fillna('')

            edited_df = st.data_editor(
                st.session_state.filtered_df,
                column_config=column_config,
                use_container_width=True,
                disabled=st.session_state.filtered_df.columns[:-2],  # Only Implementation Status and Comments are editable
                hide_index=True,
                key="data_editor"
            )

            if st.button("Save Changes", type="primary"):
                st.session_state.filtered_df = edited_df.copy()
                st.session_state.show_success = True

        if st.session_state.show_success:
            st.success("Changes saved successfully!")
            time.sleep(3)
            st.session_state.show_success = False
            st.rerun()

    elif option == "View Ready Reckoner":
        st.title("Ready Reckoner (Full Dataset)")
        st.dataframe(full_df, use_container_width=True)

if __name__ == "__main__":
    main()
