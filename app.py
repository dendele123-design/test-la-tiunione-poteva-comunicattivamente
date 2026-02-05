import streamlit as st
import time

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="La Riunione poteva essere una Mail - Test", page_icon="📧", layout="centered")

# --- STILE CSS (Look "Ansia SPA" - Pulito, Aggressivo, Anti Dark Mode) ---
st.markdown("""
    <style>
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, span, label {
        color: #1a1a1a !important;
    }
    .stApp { background-color: #ffffff !important; }
    .stButton>button { 
        width: 100%; border-radius: 5px; height: 3.5em; font-weight: bold; 
        text-transform: uppercase; background-color: #f0f2f6 !important; color: #1a1a1a !important;
    }
    div.stButton > button:first-child[kind="primary"] {
        background-color: #000000 !important; color: white !important;
    }
    .area-header { 
        background-color: #ff4b4b !important; color: white !important; 
        padding: 10px; text-align: center; font-weight: bold; border-radius: 5px; 
        margin-bottom: 20px; letter-spacing: 1px; 
    }
    .lesson-box { 
        background-color: #f8f9fa !important; color: #1a1a1a !important; 
        padding: 25px; border-radius: 10px; border-left: 8px solid #000000 !important; 
        margin-top: 20px; font-style: italic; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); 
    }
    .profile-box { padding: 30px; border-radius: 15px; border: 2px solid #000 !important; margin-top: 20px; }
    .contact-box { text-align: center; padding: 25px; background-color: #f1f1f1 !important; border-radius: 10px; margin-top: 40px; }
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE DELLE DOMANDE (Riorganizzato per il nuovo libro) ---
domande = [
    {"testo": "L'ULTIMA RIUNIONE AVEVA UN ORDINE DEL GIORNO SCRITTO?", "sotto": "Tutti sapevano perché erano lì o lo hanno scoperto strada facendo?", "opzioni": [{"testo": "🔴 NO, SIAMO ANDATI A BRACCIO", "punti": 1}, {"testo": "🟢 SÌ, SAPEVAMO COSA DECIDERE", "punti": 0}], "lezione": "Senza un'agenda, la riunione è un podcast dal vivo dove tutti parlano e nessuno ascolta. Un furto legalizzato di stipendi."},
    {"testo": "USI LE MAIL PER CHIEDERE 'CI SEI MARTEDÌ ALLE 10?'", "sotto": "Il classico ping-pong di 5 mail per fissare un solo appuntamento.", "opzioni": [{"testo": "🔴 SÌ, SEMPRE", "punti": 1}, {"testo": "🟢 NO, USIAMO IL CALENDARIO CONDIVISO", "punti": 0}], "lezione": "L'Agenda di Schrödinger uccide la velocità. Se devi chiedere il permesso per occupare un buco bianco, sei rimasto agli anni '80."},
    {"testo": "RISPONDI AI WHATSAPP DI LAVORO APPENA ARRIVANO?", "sotto": "Anche se stai facendo altro o sei concentrato su un compito.", "opzioni": [{"testo": "🔴 SÌ, SONO SEMPRE REATTIVO", "punti": 1}, {"testo": "🟢 NO, HO MOMENTI DEDICATI", "punti": 0}], "lezione": "Reattività non significa produttività. Se reagisci a ogni notifica, il tuo tempo appartiene agli altri, non a te."},
    {"testo": "COME INVÌI I DOCUMENTI AI COLLEGHI?", "sotto": "Allegati pesanti nella mail o link diretti al cloud?", "opzioni": [{"testo": "🔴 ALLEGATO NELLA MAIL", "punti": 1}, {"testo": "🟢 LINK ALLA 'FONTE DELLA VERITÀ'", "punti": 0}], "lezione": "Un allegato è un virus per l'organizzazione. Crea versioni infinite dello stesso file. Il link è la via, l'allegato è il peccato."},
    {"testo": "QUANTO TEMPO PASSI A CERCARE UN FILE?", "sotto": "Contratti, loghi, vecchie fatture o comunicazioni passate...", "opzioni": [{"testo": "🔴 PIÙ DI 5 MINUTI", "punti": 1}, {"testo": "🟢 LO TROVO IN 30 SECONDI", "punti": 0}], "lezione": "Se cerchi i file, non stai lavorando. Stai giocando a nascondino con i tuoi profitti. Una cartella AZIENDA unica non è un optional."},
    {"testo": "SE UN COLLABORATORE SPARISCE, L'INFO RESTA?", "sotto": "L'informazione è scritta o è 'ostaggio' nella testa di qualcuno?", "opzioni": [{"testo": "🔴 È TUTTO NELLA SUA TESTA", "punti": 1}, {"testo": "🟢 SÌ, È TUTTO PROCEDURATO", "punti": 0}], "lezione": "L'oralità è il Medioevo dell'azienda. Se l'informazione non è scritta, la tua azienda morirà con il primo raffreddore del dipendente chiave."},
    {"testo": "DICI SPESSO 'FACCIO PRIMA A FARLO IO'?", "sotto": "Invece di perdere tempo a spiegare o delegare un compito.", "opzioni": [{"testo": "🔴 SÌ, QUASI OGNI GIORNO", "punti": 1}, {"testo": "🟢 NO, DELEGO E CONTROLLO", "punti": 0}], "lezione": "Questa frase è la lapide del tuo tempo. Facendo il lavoro degli altri, impedisci alla tua azienda di crescere e a te di respirare."},
    {"testo": "LE TUE DECISIONI SI BASANO SUI DATI O SUL 'NASO'?", "sotto": "Analisi dei report vs Sensazione del mattino.", "opzioni": [{"testo": "🔴 VADO MOLTO A INTUITO", "punti": 1}, {"testo": "🟢 GUARDO I NUMERI", "punti": 0}], "lezione": "L'intuito è spesso un pregiudizio travestito. Senza dati sei solo uno che sta scommettendo i propri soldi al casinò dell'inefficienza."},
    {"testo": "C'È UN CANALE DEDICATO SOLO PER LE URGENZE?", "sotto": "O tutto viaggia ovunque (Mail, WhatsApp, Chat, Chiamate)?", "opzioni": [{"testo": "🔴 TUTTO VIAGGIA OVUNQUE", "punti": 1}, {"testo": "🟢 SÌ, ABBIAMO REGOLE CHIARE", "punti": 0}], "lezione": "Se tutto è urgente, niente lo è. Confondere la chat del calcetto con le scadenze dei clienti è il primo passo verso il burnout."}
]

# --- STATO SESSIONE ---
if 'step' not in st.session_state: st.session_state.step = 0
if 'total_score' not in st.session_state: st.session_state.total_score = 0
if 'show_lesson' not in st.session_state: st.session_state.show_lesson = False

# --- LOGICA APPLICAZIONE ---
st.image("https://www.comunicattivamente.it/wp-content/uploads/2023/logo-comunicattivamente.png", width=150)
st.title("📧 TERMOMETRO DELL'INUTILITÀ")
st.write("Diagnosi rapida per aziende che vogliono smettere di correre a vuoto.")

if st.session_state.step < len(domande):
    item = domande[st.session_state.step]
    st.markdown(f"<div class='area-header'>QUESITO {s
