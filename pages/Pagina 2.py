# mijn_streamlit_app/pages/2_Andere_Pagina.py
import streamlit as st

st.set_page_config(
    page_title="Andere Pagina",
    page_icon="📄"
)

st.title("📄 Dit is een Andere Pagina")
st.write("""
Welkom op een van de extra pagina's van je Streamlit app.
Elk `.py` bestand in de `pages/` map wordt automatisch een item in het zijmenu.
""")

st.slider("Selecteer een waarde", 0, 100, 50)
st.checkbox("Schakel iets in/uit")

st.markdown("---")
st.success("Je kunt hier zoveel pagina's toevoegen als je wilt!")
