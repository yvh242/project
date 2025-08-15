import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def extract_matches_from_text(text):
    # Deze functie parseert de tekst in het formaat zoals in de afbeelding
    matches = []
    current_date = None
    
    # Split de tekst in regels en verwerk elke regel
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Check voor datum/tijd regel (bijv. "VRUDAG 01 AUGUSTUS - 20:30")
        date_match = re.match(r'^([A-Z]+)\s(\d{1,2})\s([A-Z]+)\s-\s(\d{1,2}:\d{2})', line)
        if date_match:
            current_date = f"{date_match.group(1)} {date_match.group(2)} {date_match.group(3)} - {date_match.group(4)}"
            continue
            
        # Check voor wedstrijdregel (bijv. "5 KVCDT BORSEEKE DAMES A    3 - 2    SV ZULTE-WAREGEM EWII")
        match_match = re.match(r'^(.+?)\s+(\d+\s*-\s*\d+)\s+(.+)$', line)
        if match_match and current_date:
            home_team = match_match.group(1).strip()
            away_team = match_match.group(3).strip()
            matches.append({
                'Datum': current_date,
                'Thuisploeg': home_team,
                'Uitploeg': away_team
            })
            
    return matches

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        visible_text = soup.get_text()
        
        matches = extract_matches_from_text(visible_text)
        
        if matches:
            return pd.DataFrame(matches)
        else:
            st.warning("Geen wedstrijden gevonden in de opgegeven website.")
            return None
            
    except Exception as e:
        st.error(f"Fout bij het scrapen van de website: {e}")
        return None

# Streamlit UI
st.title("Voetbalwedstrijden Scraper")

url = st.text_input("Voer de website URL in:", "")

if st.button("Scrape wedstrijden"):
    if url:
        st.info(f"Bezig met scrapen van: {url}")
        df = scrape_website(url)
        
        if df is not None:
            st.success(f"{len(df)} wedstrijden gevonden!")
            st.dataframe(df)
            
            # Optioneel: download knop
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download als CSV",
                data=csv,
                file_name='voetbalwedstrijden.csv',
                mime='text/csv'
            )
    else:
        st.warning("Voer een geldige URL in")

st.markdown("""
**Instructies:**
1. Voer de URL in van een website met voetbalwedstrijden
2. Klik op "Scrape wedstrijden"
3. De app zal proberen wedstrijden te extraheren in tabelvorm

**Opmerking:** De app werkt het beste met websites die een vergelijkbaar formaat hebben als de voorbeeldafbeelding.
""")
