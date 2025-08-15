import streamlit as st
import requests
from bs4 import BeautifulSoup

def scrape_all_text(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Verwijder scripts en styles
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Haal alle tekst op
        text = soup.get_text(separator='\n', strip=True)
        
        # Schoon op: verwijder lege regels en veelvoudige newlines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        cleaned_text = '\n'.join(lines)
        
        return cleaned_text
        
    except Exception as e:
        return f"Fout bij het scrapen: {str(e)}"

# Streamlit UI
st.title("RBFa Pagina Text Scraper")

default_url = "https://www.rbfa.be/nl/club/1931/ploeg/346664/kalender"
url = st.text_input("Voer de RBFa URL in:", default_url)

if st.button("Scrape pagina tekst"):
    if url:
        st.info(f"Bezig met scrapen van: {url}")
        with st.spinner('Pagina-inhoud ophalen...'):
            text = scrape_all_text(url)
        
        st.subheader("Volledige pagina tekst:")
        st.text_area("Gescrapete tekst", text, height=500)
        
        # Download knop
        st.download_button(
            label="Download als tekstbestand",
            data=text,
            file_name='rbfa_pagina_tekst.txt',
            mime='text/plain'
        )
    else:
        st.warning("Voer een geldige URL in")

st.markdown("""
**Instructies:**
1. De standaard URL is al ingevuld (SV Zulte-Waregem Dames)
2. Klik op "Scrape pagina tekst"
3. Bekijk de volledige tekst om te zien welke informatie beschikbaar is

**Volgende stappen:**
- Analyseer de output om te zien waar de wedstrijdgegevens staan
- Pas de scraping code aan om specifiek die informatie te extraheren
""")
