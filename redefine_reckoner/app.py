import streamlit as st
import time
from redefine_reckoner.utils.database import load_full_data, save_to_database, load_from_database
from redefine_reckoner.utils.data_processing import filter_data, load_static_data

def main():
    st.set_page_config(page_title="Redefine Ready Reckoner", layout="wide")
    
    if 'filtered_df' not in st.session_state:
        st.session_state.filtered_df = load_from_database()
    if 'show_success' not in st.session_state:
        st.session_state.show_success = False

    full_df = load_full_data()

    # Load static data from JSON files
    checkout_data, vertical_data, methods_data = load_static_data()

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
            
            # Configuration for the "Implementation Status" column with color coding
            column_config = {
                'Implementation Status': st.column_config.SelectboxColumn(
                    options=['Select', 'Implemented', 'Suggested', 'Not Applicable', 'Not Implemented'],
                    default='Select',
                    label='Implementation Status',
                    help='Choose the implementation status for each feature.',
                    width='medium',
                    required=True
                )
            }

            # Custom CSS for color coding
            st.markdown("""
            <style>
            .stSelectbox [data-value="Implemented"] {
                background-color: #90EE90 !important;
            }
            .stSelectbox [data-value="Not Implemented"] {
                background-color: #FFB6C1 !important;
            }
            .stSelectbox [data-value="Suggested"] {
                background-color: #ADD8E6 !important;
            }
            .stSelectbox [data-value="Not Applicable"] {
                background-color: #FFFFE0 !important;
            }
            </style>
            """, unsafe_allow_html=True)

            # Display the DataFrame with the data editor
            edited_df = st.data_editor(
                st.session_state.filtered_df,
                column_config=column_config,
                use_container_width=True,
                disabled=st.session_state.filtered_df.columns[:-1],
                hide_index=True,
                key="data_editor"
            )

            if st.button("Save Changes", type="primary"):
                st.session_state.filtered_df = edited_df.copy()
                save_to_database(st.session_state.filtered_df)
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