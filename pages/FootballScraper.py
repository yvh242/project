import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_rbfa_matches(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        matches = []
        
        # Zoek alle wedstrijd containers
        match_containers = soup.find_all('div', class_='match-row')
        
        if not match_containers:
            st.warning("Geen wedstrijd containers gevonden. Mogelijk is de HTML-structuur gewijzigd.")
            return None
        
        for container in match_containers:
            try:
                # Extract datum en tijd
                date_time = container.find('div', class_='match-date').get_text(strip=True)
                
                # Extract teams
                home_team = container.find('div', class_='team-home').get_text(strip=True)
                away_team = container.find('div', class_='team-away').get_text(strip=True)
                
                # Extract score (indien beschikbaar)
                score = container.find('div', class_='match-score').get_text(strip=True) if container.find('div', class_='match-score') else 'Nog niet gespeeld'
                
                matches.append({
                    'Datum': date_time,
                    'Thuisploeg': home_team,
                    'Uitploeg': away_team,
                    'Uitslag': score
                })
                
            except Exception as e:
                st.warning(f"Fout bij verwerken van een wedstrijd: {e}")
                continue
                
        return pd.DataFrame(matches)
        
    except Exception as e:
        st.error(f"Fout bij het scrapen van de website: {e}")
        return None

# Streamlit UI
st.title("RBFa Voetbalwedstrijden Scraper")

default_url = "https://www.rbfa.be/nl/club/1931/ploeg/346664/kalender"
url = st.text_input("Voer de RBFa kalender URL in:", default_url)

if st.button("Scrape wedstrijden"):
    if url:
        st.info(f"Bezig met scrapen van: {url}")
        with st.spinner('Wedstrijden aan het ophalen...'):
            df = scrape_rbfa_matches(url)
        
        if df is not None and not df.empty:
            st.success(f"{len(df)} wedstrijden gevonden!")
            
            # Datum opmaak verbeteren
            df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce').dt.strftime('%A %d %B %Y - %H:%M')
            
            st.dataframe(df)
            
            # Download knop
            csv = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
            st.download_button(
                label="Download als CSV",
                data=csv,
                file_name='rbfa_wedstrijden.csv',
                mime='text/csv'
            )
        else:
            st.warning("Geen wedstrijden gevonden. Controleer de URL of probeer het later opnieuw.")
    else:
        st.warning("Voer een geldige URL in")

st.markdown("""
**Instructies:**
1. De standaard URL is al ingevuld (SV Zulte-Waregem Dames)
2. Klik op "Scrape wedstrijden"
3. De app toont de gevonden wedstrijden in een tabel

**Let op:** Websites veranderen soms hun structuur, waardoor de scraper mogelijk moet worden aangepast.
""")
