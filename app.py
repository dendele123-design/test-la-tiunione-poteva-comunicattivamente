import streamlit as st
import time

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="La Riunione poteva essere una Mail - Test", page_icon="📧", layout="centered")

# --- STILE CSS (Blindato contro tasti neri e scritte invisibili) ---
st.markdown("""
    <style>
    /* SFONDO E TESTO GENERALE */
    .stApp { background-color: #ffffff !important; }
    
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, span, label {
        color: #1a1a1a !important;
    }

    /* BOTTONI NORMALI (Opzioni) */
    .stButton>button { 
        width: 100%; 
        border-radius: 8px !important; 
        height: 3.5em !important; 
        font-weight: bold !important; 
        background-color: #f1f3f6 !important; /* Grigio chiaro */
        color: #1a1a1a !important; /* Testo nero */
        border: 1px solid #d1d5db !important;
    }
    
    .stButton>button:hover {
        border: 1px solid #ff4b4b !important;
        color: #ff4b4b !important;
    }

    /* BOTTONE PRIMARIO (Prossimo Passo / Risultati) */
    div.stButton > button:first-child[kind="primary"] {
        background-color: #ff4b4b !important; /* Rosso */
        color: #ffffff !important; /* TESTO BIANCO OBBLIGATORIO */
        border: none !important;
    }
    
    div.stButton > button:first-child[kind="primary"]:hover {
        background-color: #e03e3e !important;
    }

    /* HEADER QUESITO */
    .area-header { 
        background-color: #000000 !important; 
        color: #ffffff !important; 
        padding: 10px; 
        text-align: center; 
        font-weight: bold; 
        border-radius: 5px; 
        margin-bottom: 20px; 
    }

    /* BOX LEZIONE */
    .lesson-box { 
        background-color: #f8f9fa !important; 
        color: #1a1a1a !important; 
        padding: 25px; 
        border-radius: 10px; 
        border-left: 8px solid #ff4b4b !important; 
        margin-top: 20px; 
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05); 
    }

    /* PROFILI FINALI */
    .profile-box { 
        padding: 30px; 
        border-radius: 15px; 
        border: 2px solid #000 !important; 
        margin-top: 20px; 
        color: #1a1a1a !important;
    }

    /* CONTATTI */
    .contact-box { 
        text-align: center; 
        padding: 25px; 
        background-color: #f1f1f1 !important; 
        border-radius: 10px; 
        margin-top: 40px; 
    }

    /* NASCONDE MENU DI SISTEMA */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE DELLE DOMANDE ---
domande = [
    {"testo": "L'ULTIMA RIUNIONE AVEVA UN ORDINE DEL GIORNO SCRITTO?", "sotto": "Tutti sapevano perché erano lì o lo hanno scoperto strada facendo?", "opzioni": [{"testo": "🔴 NO, SIAMO ANDATI A BRACCIO", "punti": 1}, {"testo": "🟢 SÌ, SAPEVAMO COSA DECIDERE", "punti": 0}], "lezione": "Senza un'agenda, la riunione è un podcast dal vivo dove tutti parlano e nessuno ascolta. Un furto legalizzato di stipendi."},
    {"testo": "USI LE MAIL PER CHIEDERE 'CI SEI MARTEDÌ ALLE 10?'", "sotto": "Il classico ping-pong di 5 mail per fissare un solo appuntamento.", "opzioni": [{"testo": "🔴 SÌ, SEMPRE", "punti": 1}, {"testo": "🟢 NO, USIAMO IL CALENDARIO CONDIVISO", "punti": 0}], "lezione": "L'Agenda di Schrödinger uccide la velocità. Se devi chiedere il permesso per occupare un buco bianco, sei rimasto agli anni '80."},
    {"testo": "RISPONDI AI WHATSAPP DI LAVORO APPENA ARRIVANO?", "sotto": "Anche se sei concentrato su un compito importante.", "opzioni": [{"testo": "🔴 SÌ, SONO SEMPRE REATTIVO", "punti": 1}, {"testo": "🟢 NO, HO MOMENTI DEDICATI", "punti": 0}], "lezione": "Reattività non significa produttività. Se reagisci a ogni notifica, il tuo tempo appartiene agli altri, non a te."},
    {"testo": "COME INVÌI I DOCUMENTI AI COLLEGHI?", "sotto": "Allegati pesanti nella mail o link diretti al cloud?", "opzioni": [{"testo": "🔴 ALLEGATO NELLA MAIL", "punti": 1}, {"testo": "🟢 LINK ALLA 'FONTE DELLA VERITÀ'", "punti": 0}], "lezione": "Un allegato è un virus organizzativo. Crea versioni infinite dello stesso file. Il link è la cura, l'allegato è l'infezione."},
    {"testo": "QUANTO TEMPO PASSI A CERCARE UN FILE?", "sotto": "Contratti, loghi, vecchie fatture o preventivi passati...", "opzioni": [{"testo": "🔴 PIÙ DI 5 MINUTI", "punti": 1}, {"testo": "🟢 LO TROVO IN 30 SECONDI", "punti": 0}], "lezione": "Cercare file non è lavoro. È giocare a nascondino con i tuoi profitti. Una struttura unica è l'esorcismo minimo necessario."},
    {"testo": "SE UN COLLABORATORE SPARISCE, L'INFO RESTA?", "sotto": "L'informazione è scritta o è 'ostaggio' nella testa di qualcuno?", "opzioni": [{"testo": "🔴 È TUTTO NELLA SUA TESTA", "punti": 1}, {"testo": "🟢 SÌ, È TUTTO PROCEDURATO", "punti": 0}], "lezione": "L'oralità è il Medioevo dell'azienda. Se l'info non è scritta, la tua azienda morirà con il primo raffreddore del dipendente chiave."},
    {"testo": "DICI SPESSO 'FACCIO PRIMA A FARLO IO'?", "sotto": "Invece di perdere tempo a spiegare o delegare un compito.", "opzioni": [{"testo": "🔴 SÌ, QUASI OGNI GIORNO", "punti": 1}, {"testo": "🟢 NO, DELEGO E CONTROLLO", "punti": 0}], "lezione": "Questa frase è la lapide del tuo tempo. Facendo il lavoro degli altri, impedisci alla tua azienda di crescere e a te di respirare."},
    {"testo": "LE TUE DECISIONI SI BASANO SUI DATI O SUL 'NASO'?", "sotto": "Analisi dei report vs Sensazione viscerale del mattino.", "opzioni": [{"testo": "🔴 VADO MOLTO A INTUITO", "punti": 1}, {"testo": "🟢 GUARDO I NUMERI", "punti": 0}], "lezione": "L'intuito è spesso un pregiudizio travestito. Senza dati sei solo uno che sta scommettendo i propri soldi al casinò dell'inefficienza."},
    {"testo": "C'È UN CANALE DEDICATO SOLO PER LE URGENZE?", "sotto": "O tutto viaggia ovunque (Mail, WhatsApp, Chat, Chiamate)?", "opzioni": [{"testo": "🔴 TUTTO VIAGGIA OVUNQUE", "punti": 1}, {"testo": "🟢 SÌ, ABBIAMO REGOLE CHIARE", "punti": 0}], "lezione": "Se tutto è urgente, niente lo è. Confondere la chat del calcetto con le scadenze dei clienti è il primo passo verso il burnout."},
    {"testo": "QUANTO TEMPO DEDICHI ALLA STRATEGIA OGNI SETTIMANA?", "sotto": "Tempo puro per pensare al futuro, non per gestire il presente.", "opzioni": [{"testo": "🔴 ZERO / QUASI NULLA", "punti": 1}, {"testo": "🟢 ALMENO 4 ORE", "punti": 0}], "lezione": "Se non guidi tu l'azienda, lei guida te. E di solito ti sta portando dritti contro un muro di stanchezza."}
]

# --- STATO SESSIONE ---
if 'step' not in st.session_state: st.session_state.step = 0
if 'total_score' not in st.session_state: st.session_state.total_score = 0
if 'show_lesson' not in st.session_state: st.session_state.show_lesson = False

# --- LOGICA APPLICAZIONE ---
st.write("# 📧") # Sostituisce il logo con un'icona
st.title("TERMOMETRO DELL'INUTILITÀ")
st.write("Diagnosi rapida per aziende che vogliono smettere di correre a vuoto.")

if st.session_state.step < len(domande):
    item = domande[st.session_state.step]
    st.markdown(f"<div class='area-header'>QUESITO {st.session_state.step + 1} di {len(domande)}</div>", unsafe_allow_html=True)
    st.header(item['testo'])
    st.write(f"*{item['sotto']}*")
    st.divider()

    if not st.session_state.show_lesson:
        for opt in item['opzioni']:
            if st.button(opt['testo']):
                st.session_state.total_score += opt['punti']
                st.session_state.show_lesson = True
                st.rerun()
    else:
        st.markdown(f"<div class='lesson-box'><b>L'ESORCISTA DICE:</b><br><br>{item['lezione']}</div>", unsafe_allow_html=True)
        if st.button("PROSSIMO PASSO ➡️", type="primary"):
            st.session_state.step += 1
            st.session_state.show_lesson = False
            st.rerun()

else:
    # --- RISULTATI ---
    with st.spinner("L'Esorcista sta elaborando..."):
        time.sleep(1.5)
    
    st.header("📊 DIAGNOSI FINALE")
    score = st.session_state.total_score
    
    if score <= 2:
        st.markdown(f"<div class='profile-box' style='background-color: #d4edda;'><h3>😇 IL MONACO ZEN</h3><p>Punteggio: {score}/{len(domande)}<br><br>Sei un alieno. La tua azienda gira come un orologio svizzero. Chiamami, voglio imparare io da te!</p></div>", unsafe_allow_html=True)
    elif score <= 6:
        st.markdown(f"<div class='profile-box' style='background-color: #fff3cd;'><h3>🏃 IL POMPIERE IN AFFANNO</h3><p>Punteggio: {score}/{len(domande)}<br><br>Sei nella media. Corri tantissimo, ma la tua ruota sta cigolando. Le inefficienze ti mangiano il 30% del tempo.</p></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='profile-box' style='background-color: #f8d7da;'><h3>🧟 IL POSSEDUTO DAL CAOS</h3><p>Punteggio: {score}/{len(domande)}<br><br>Allarme Rosso. Non lavori, sopravvivi. La tua azienda è una setta di riunioni inutili e notifiche compulsive. Serve un esorcismo procedurale immediato.</p></div>", unsafe_allow_html=True)

    st.divider()
    st.subheader("VUOI GUARIRE?")
    
    col1, col2 = st.columns(2)
    col1.link_button("📘 ACQUISTA IL LIBRO", "https://www.comunicattivamente.it", type="primary")
    col2.link_button("📅 FISSA UN ESORCISMO", "mailto:daniele@comunicattivamente.it")

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
