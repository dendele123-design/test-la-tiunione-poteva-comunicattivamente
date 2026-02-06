import streamlit as st
import time

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="La Riunione poteva essere una Mail - Test", page_icon="📧", layout="centered")

# --- STILE CSS (Personalizzato con Rosso #dc061e) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #ffffff !important; }}
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, span, label {{
        color: #1a1a1a !important;
    }}

    /* BOTTONI OPZIONI */
    .stButton>button {{ 
        width: 100%; border-radius: 8px !important; height: 3.5em !important; 
        font-weight: bold !important; background-color: #f1f3f6 !important; 
        color: #1a1a1a !important; border: 1px solid #d1d5db !important;
    }
    .stButton>button:hover {{ border: 1px solid #dc061e !important; color: #dc061e !important; }}

    /* BOTTONE PRIMARIO (Rosso #dc061e) */
    div.stButton > button:first-child[kind="primary"] {{
        background-color: #dc061e !important; color: #ffffff !important; border: none !important;
    }}

    /* HEADER QUESITO */
    .area-header {{ 
        background-color: #000000 !important; color: #ffffff !important; 
        padding: 10px; text-align: center; font-weight: bold; border-radius: 5px; margin-bottom: 20px; 
    }}

    /* BOX FEEDBACK (La Nota dell'Architetto) */
    .lesson-box {{ 
        background-color: #f8f9fa !important; color: #1a1a1a !important; 
        padding: 25px; border-radius: 10px; border-left: 8px solid #dc061e !important; 
        margin-top: 20px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); 
    }}

    .profile-box {{ padding: 30px; border-radius: 15px; border: 2px solid #000 !important; margin-top: 20px; }}
    .contact-box {{ text-align: center; padding: 25px; background-color: #f1f1f1 !important; border-radius: 10px; margin-top: 40px; }}
    header {{visibility: hidden !important;}} footer {{visibility: hidden !important;}} #MainMenu {{visibility: hidden !important;}}
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE DELLE DOMANDE CON DOPPIO FEEDBACK ---
domande = [
    {
        "testo": "L'ULTIMA RIUNIONE AVEVA UN ORDINE DEL GIORNO SCRITTO?",
        "sotto": "Tutti sapevano perché erano lì o lo hanno scoperto strada facendo?",
        "opzioni": [{"testo": "🔴 NO, SIAMO ANDATI A BRACCIO", "punti": 1}, {"testo": "🟢 SÌ, SAPEVAMO COSA DECIDERE", "punti": 0}],
        "feedback_ok": "Ottimo, l'agenda è lo scudo contro la perdita di tempo. Assicurati però che venga rispettata al minuto!",
        "feedback_no": "Attenzione: senza un'agenda, bruciate stipendi per non decidere nulla. È un furto legalizzato di tempo."
    },
    {
        "testo": "USI LE MAIL PER CHIEDERE 'CI SEI MARTEDÌ ALLE 10?'",
        "sotto": "Il classico ping-pong di 5 mail per fissare un solo appuntamento.",
        "opzioni": [{"testo": "🔴 SÌ, SEMPRE", "punti": 1}, {"testo": "🟢 NO, USIAMO IL CALENDARIO CONDIVISO", "punti": 0}],
        "feedback_ok": "Eccellente. Ma controlla che nessuno faccia il 'furbo' bloccando slot finti per non farsi disturbare.",
        "feedback_no": "Pessima idea. L'incertezza uccide la velocità. Automatizza la tua disponibilità o rimarrai bloccato negli anni '80."
    },
    {
        "testo": "RISPONDI AI WHATSAPP DI LAVORO APPENA ARRIVANO?",
        "sotto": "Anche se sei concentrato su un compito importante.",
        "opzioni": [{"testo": "🔴 SÌ, SEMPRE", "punti": 1}, {"testo": "🟢 NO, HO MOMENTI DEDICATI", "punti": 0}],
        "feedback_ok": "Bravo, proteggi il tuo focus. Ma assicurati che il team sappia quando sei 'off' per non creare ansia.",
        "feedback_no": "Sei schiavo delle notifiche. Se reagisci a tutto, il tuo tempo appartiene agli altri, non alla tua azienda."
    },
    {
        "testo": "COME INVÌI I DOCUMENTI AI COLLEGHI?",
        "sotto": "Allegati pesanti nella mail o link diretti al cloud?",
        "opzioni": [{"testo": "🔴 ALLEGATO NELLA MAIL", "punti": 1}, {"testo": "🟢 LINK AL CLOUD", "punti": 0}],
        "feedback_ok": "Corretto. Ma verifica che i permessi del link siano sempre corretti per evitare mail di richiesta accesso.",
        "feedback_no": "Gli allegati sono virus organizzativi. Creano caos e versioni duplicate. Passa al link, salva il tuo server."
    },
    {
        "testo": "QUANTO TEMPO PASSI A CERCARE UN FILE?",
        "sotto": "Contratti, loghi, vecchie fatture o preventivi passati...",
        "opzioni": [{"testo": "🔴 PIÙ DI 5 MINUTI", "punti": 1}, {"testo": "🟢 LO TROVO IN 30 SECONDI", "punti": 0}],
        "feedback_ok": "Bene. Ma ogni sei mesi fai pulizia: le cartelle ordinate tendono a diventare giungle se non curate.",
        "feedback_no": "Stai giocando a nascondino con i tuoi profitti. Cercare file non è lavoro, è un'emorragia finanziaria."
    },
    {
        "testo": "DICI SPESSO 'FACCIO PRIMA A FARLO IO'?",
        "sotto": "Invece di perdere tempo a spiegare o delegare un compito.",
        "opzioni": [{"testo": "🔴 QUASI OGNI GIORNO", "punti": 1}, {"testo": "🟢 NO, DELEGO E CONTROLLO", "punti": 0}],
        "feedback_ok": "Deleghi? Bene. Ma ricorda che delegare senza procedure scritte è solo sperare che vada bene.",
        "feedback_no": "Questa è la lapide della tua crescita. Facendo il lavoro degli altri, impedisci alla tua azienda di scalare."
    },
    {
        "testo": "C'È UN CANALE DEDICATO SOLO PER LE URGENZE?",
        "sotto": "O tutto viaggia ovunque (Mail, WhatsApp, Chat, Chiamate)?",
        "opzioni": [{"testo": "🔴 TUTTO VIAGGIA OVUNQUE", "punti": 1}, {"testo": "🟢 SÌ, ABBIAMO REGOLE CHIARE", "punti": 0}],
        "feedback_ok": "Ottimo filtro. Ma attento: se ogni piccola cosa diventa 'urgenza', il canale perde la sua funzione.",
        "feedback_no": "Se tutto è urgente, niente lo è. State vivendo in un costante stato di allarme che brucia il cervello."
    }
]

# --- STATO SESSIONE ---
if 'step' not in st.session_state: st.session_state.step = 0
if 'total_score' not in st.session_state: st.session_state.total_score = 0
if 'last_choice' not in st.session_state: st.session_state.last_choice = None
if 'show_lesson' not in st.session_state: st.session_state.show_lesson = False

# --- UI APPLICAZIONE ---
st.write("# 📑") 
st.title("TERMOMETRO DELL'INUTILITÀ")

if st.session_state.step < len(domande):
    item = domande[st.session_state.step]
    st.markdown(f"<div class='area-header'>QUESITO {st.session_state.step + 1} di {len(domande)}</div>", unsafe_allow_html=True)
    st.header(item['testo'])
    st.write(f"*{item['sotto']}*")
    st.divider()

    if not st.session_state.show_lesson:
        for i, opt in enumerate(item['opzioni']):
            if st.button(opt['testo'], key=f"btn_{st.session_state.step}_{i}"):
                st.session_state.total_score += opt['punti']
                st.session_state.last_choice = opt['punti']
                st.session_state.show_lesson = True
                st.rerun()
    else:
        # FEEDBACK DIFFERENZIATO
        messaggio = item['feedback_ok'] if st.session_state.last_choice == 0 else item['feedback_no']
        st.markdown(f"<div class='lesson-box'><b>LA NOTA DELL'ARCHITETTO:</b><br><br>{messaggio}</div>", unsafe_allow_html=True)
        
        if st.button("PROSSIMO PASSO ➡️", type="primary"):
            st.session_state.step += 1
            st.session_state.show_lesson = False
            st.rerun()
else:
    # --- RISULTATI FINALI ---
    st.header("📊 LA TUA DIAGNOSI")
    score = st.session_state.total_score
    if score <= 1:
        st.markdown(f"<div class='profile-box' style='background-color: #d4edda;'><h3>😇 ARCHITETTO ZEN</h3><p>Punteggio: {score}/{len(domande)}<br><br>Sei un alieno. La tua azienda è snella e veloce. Attento solo a non diventare troppo rigido.</p></div>", unsafe_allow_html=True)
    elif score <= 4:
        st.markdown(f"<div class='profile-box' style='background-color: #fff3cd;'><h3>🏃 POMPIERE IN AFFANNO</h3><p>Punteggio: {score}/{len(domande)}<br><br>Corri tantissimo per restare fermo. Le inefficienze ti mangiano il 30% della giornata.</p></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='profile-box' style='background-color: #f8d7da;'><h3>🧟 ZOMBIE ORGANIZZATIVO</h3><p>Punteggio: {score}/{len(domande)}<br><br>La tua azienda è posseduta dal caos. Non lavori, sopravvivi a notifiche e riunioni inutili.</p></div>", unsafe_allow_html=True)

    st.divider()
    st.subheader("VUOI GUARIRE?")
    
    col1, col2 = st.columns(2)
    col1.link_button("📘 ACQUISTA IL LIBRO", "https://www.comunicattivamente.it", type="primary")
    col2.link_button("🛠️ PROVA IL TOOLKIT", "https://tuo-toolkit-link.it") # <--- AGGIUNGI QUI IL LINK ALLA TUA WEB APP

    st.markdown(f"""
        <div class="contact-box">
            <b>Daniele Salvatori</b><br>
            <i>Esorcista Aziendale | Partner SuPeR^</i><br><br>
            📧 daniele@comunicattivamente.it<br>
            📞 +39 392 933 4563
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 RIPETI IL TEST"):
        st.session_state.step = 0
        st.session_state.total_score = 0
        st.rerun()
