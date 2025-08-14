import streamlit as st
import pandas as pd
from io import BytesIO

def check_and_rename_columns(df):
    """Check required columns and rename if needed"""
    required_columns = {'Datum', 'Klant'}
    
    if required_columns.issubset(df.columns):
        return df
    
    st.warning("⚠️ Vereiste kolommen 'Datum' en 'Klant' ontbreken in het bestand.")
    
    # Create mapping for column renaming
    col_mapping = {}
    for req_col in required_columns:
        selected_col = st.selectbox(
            f"Selecteer kolom die overeenkomt met '{req_col}'",
            options=df.columns,
            key=f"col_map_{req_col}"
        )
        col_mapping[selected_col] = req_col
    
    if st.button("Bevestig kolomkoppelingen"):
        df = df.rename(columns=col_mapping)
        st.success("Kolommen succesvol hernoemd!")
        return df
    
    return None

def main():
    st.title("📁 Taak 1: Bestand uploaden")
    
    uploaded_file = st.file_uploader(
        "Upload een Excel of CSV bestand",
        type=['csv', 'xlsx', 'xls'],
        accept_multiple_files=False
    )
    
    if uploaded_file is not None:
        try:
            # Read file based on type
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success("Bestand succesvol geladen!")
            
            # Show preview
            st.subheader("Voorbeeld van de data:")
            st.dataframe(df.head())
            
            # Check and rename columns if needed
            processed_df = check_and_rename_columns(df)
            
            if processed_df is not None:
                st.subheader("Verwerkte data")
                st.dataframe(processed_df.head())
                
                # Download button for processed file
                output = BytesIO()
                if uploaded_file.name.endswith('.csv'):
                    processed_df.to_csv(output, index=False)
                    file_extension = 'csv'
                else:
                    processed_df.to_excel(output, index=False, engine='openpyxl')
                    file_extension = 'xlsx'
                
                output.seek(0)
                
                st.download_button(
                    label="Download verwerkt bestand",
                    data=output,
                    file_name=f"verwerkt_bestand.{file_extension}",
                    mime=f"application/{file_extension}"
                )
                
        except Exception as e:
            st.error(f"Fout bij het verwerken van het bestand: {str(e)}")

if __name__ == "__main__":
    main()
