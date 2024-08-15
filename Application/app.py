import sqlite3
import pandas as pd
import streamlit as st
import time
import json

@st.cache_data
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
    
    methods_of_choice = [method.strip() for method in methods_of_choice]

    filtered_df = df[df['Method'].isin(methods_of_choice)]
    relevant_columns = ['id', 'Method', 'Name_of_the_Feature', 'Availability', checkout_type, vertical_name]

    missing_columns = [col for col in relevant_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Error accessing columns: Missing columns {missing_columns}")
        return None

    filtered_df = filtered_df[relevant_columns]
    filtered_df['Implementation Status'] = 'Select'
    filtered_df['Comments'] = ''  # Adding the Comments column

    return filtered_df

def get_feature_flags(db_path, reckoner_id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT flags, description FROM features WHERE reckoner_id = ?", (reckoner_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            flags = json.loads(result[0])
            description = result[1]
            return flags, description
        return None, None
    except Exception as e:
        st.error(f"An error occurred while fetching feature flags: {str(e)}")
        return None, None

def main():
    st.set_page_config(page_title="Redefine Ready Reckoner", layout="wide")
    
    if 'filtered_df' not in st.session_state:
        st.session_state.filtered_df = None
    if 'show_success' not in st.session_state:
        st.session_state.show_success = False

    # Load full dataset from the database
    db_path = "data/redefine_reckoner.db"
    full_df = get_data_from_db(db_path, "SELECT * FROM reckoner")

    # Load static data from database tables
    checkout_types_df = get_data_from_db(db_path, "SELECT checkout FROM checkout_types")
    vertical_names_df = get_data_from_db(db_path, "SELECT vertical FROM vertical_names")
    methods_df = get_data_from_db(db_path, "SELECT method FROM methods")

    if checkout_types_df is not None and vertical_names_df is not None and methods_df is not None:
        checkout_data = checkout_types_df['checkout'].tolist()
        vertical_data = vertical_names_df['vertical'].tolist()
        methods_data = methods_df['method'].tolist()
    else:
        st.error("Failed to load static data from the database.")
        return

    st.sidebar.title("Navigation")
    option = st.sidebar.radio("Select a Page", ["Home", "View Ready Reckoner"])

    if option == "Home":
        st.title("🚀 Redefine Ready Reckoner")
        
        col1, col2 = st.columns(2)
        
        with col1:
            checkout_type = st.selectbox("Select Checkout Type:", checkout_data)
            vertical_name = st.selectbox("Select Vertical Name:", vertical_data)
        
        with col2:
            methods_of_choice = st.multiselect("Select Methods of Choice:", methods_data)

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
                ),
                'Availability': st.column_config.Column(
                    width='medium',
                    help='See "Feature Requests" section for details'
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

            # Feature Requests section
            st.subheader("\nFeature Requests aligned with the Reckoner")

            feature_requests = edited_df[edited_df['Availability'] == 'Feature Request']

            if not feature_requests.empty:
                # Group feature requests by Method
                grouped_requests = feature_requests.groupby('Method')
                
                for method, group in grouped_requests:
                    with st.expander(f"{method}"):
                        for index, row in group.iterrows():
                            st.markdown(f"#### {row['Name_of_the_Feature']}")
                            reckoner_id = row['id']
                            flags, description = get_feature_flags(db_path, reckoner_id)
                            if flags and description:
                                st.write(f"**Description:** {description}")
                                st.write("**Feature Flags:**")
                                for flag in flags:
                                    st.write(f"- {flag}")
                            else:
                                st.warning("No feature flags found for this feature request.")
                            st.markdown("---")  # Add a separator between feature requests
            else:
                st.info("No feature requests found in the filtered data.")

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
