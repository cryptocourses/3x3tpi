import streamlit as st
import pandas as pd

# 1. Inicjalizacja stanu aplikacji (pamięci)
if 'history' not in st.session_state:
    st.session_state.history = []  # Historia akcji
if 'game_finished' not in st.session_state:
    st.session_state.game_finished = False  # Czy mecz jest zakończony

st.set_page_config(page_title="3x3 TPI Tracker", layout="centered")
st.title("🏀 3x3 TPI Live Tracker")

# 2. Przeliczanie statystyk na bieżąco z historii akcji
tpi_history = [0.0]  # Start od 0.0
curr_pts, curr_to, curr_mfg, curr_oreb, curr_f = 0, 0, 0, 0, 0

for action in st.session_state.history:
    if action == "PTS1": curr_pts += 1
    elif action == "PTS2": curr_pts += 2
    elif action == "TO": curr_to += 1
    elif action == "MFG": curr_mfg += 1
    elif action == "OREB": curr_oreb += 1
    elif action == "F": curr_f += 1
    
    # Wzór: TPI = PTS / (TO + MFG + 1 + F - OREB)
    mianownik = curr_to + curr_mfg + 1 + curr_f - curr_oreb
    if mianownik <= 0:
        tpi = 0.0
    else:
        tpi = curr_pts / mianownik
    tpi_history.append(round(tpi, 2))

# Przygotowanie danych do wykresu (dostępne globalnie dla obu ekranów)
chart_data = pd.DataFrame({
    "TPI Drużyny": tpi_history,
    "Słaba gra (0.67)": [0.67] * len(tpi_history),
    "Świetna gra (1.05)": [1.05] * len(tpi_history)
})


# ==========================================
# EKRAN 1: MECZ W TRAKCIE (Trwa wpisywanie)
# ==========================================
if not st.session_state.game_finished:
    st.write("Klikaj przyciski na żywo podczas meczu. Statystyki i wykres aktualizują się natychmiast.")

    # Układ przycisków statystyk
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    with col1:
        if st.button("➕ 1 PTS", use_container_width=True):
            st.session_state.history.append("PTS1")
            st.rerun()
    with col2:
        if st.button("➕ 2 PTS", use_container_width=True):
            st.session_state.history.append("PTS2")
            st.rerun()
    with col3:
        if st.button("➕ TO (Strata)", use_container_width=True):
            st.session_state.history.append("TO")
            st.rerun()
    with col4:
        if st.button("➕ MFG (Pudło)", use_container_width=True):
            st.session_state.history.append("MFG")
            st.rerun()
    with col5:
        if st.button("➕ OREB (Zbiórka)", use_container_width=True):
            st.session_state.history.append("OREB")
            st.rerun()
    with col6:
        if st.button("➕ F (Faul)", use_container_width=True):
            st.session_state.history.append("F")
            st.rerun()

    st.write("---")

    # Przyciski zarządzania
    col_undo, col_finish = st.columns(2)
    with col_undo:
        if st.button("⬅️ Cofnij ostatnie", disabled=len(st.session_state.history) == 0, use_container_width=True):
            st.session_state.history.pop()
            st.rerun()
            
    with col_finish:
        if st.button("🏁 ZAKOŃCZ MECZ", type="primary", disabled=len(st.session_state.history) == 0, use_container_width=True):
            st.session_state.game_finished = True
            st.rerun()

    st.write("---")
    
    # PODGLĄD NA ŻYWO Z WYKRESEM
    st.write("### 📊 Podgląd live drużyny:")
    st.metric(label="Aktualny TPI Drużyny", value=tpi_history[-1])
    st.text(f"Punkty: {curr_pts} | Straty: {curr_to} | Pudła: {curr_mfg} | Zbiórki: {curr_oreb} | Faule: {curr_f}")
    
    # Wykres na żywo w trakcie klikania
    st.line_chart(chart_data)


# ==========================================
# EKRAN 2: PODSUMOWANIE KOŃCOWE
# ==========================================
else:
    st.success("🎉 MECZ ZAKOŃCZONY! Oto końcowy raport drużyny:")
    
    # 1. Wielki, czytelny końcowy wynik TPI
    st.metric(label="🏆 KOŃCOWY WSKAŹNIK TPI DRUŻYNY", value=tpi_history[-1])
    
    st.write("---")
    
    # 2. Ładne, kafelkowe podsumowanie wszystkich statystyk
    st.subheader("📊 Łączne statystyki drużyny:")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Punkty", curr_pts)
    c2.metric("Straty (TO)", curr_to)
    c3.metric("Pudła (MFG)", curr_mfg)
    c4.metric("Zbiórki (OREB)", curr_oreb)
    c5.metric("Faule (F)", curr_f)
    
    st.write("---")
    
    # 3. Wykres przebiegu meczu z liniami pomocniczymi
    st.subheader("📈 Wykres TPI z progami efektywności")
    st.line_chart(chart_data)
    
    st.write("---")
    
    # 4. Opcje po zakończeniu meczu
    col_back, col_reset = st.columns(2)
    with col_back:
        if st.button("🔙 Wróć do meczu (popraw błąd)", use_container_width=True):
            st.session_state.game_finished = False
            st.rerun()
    with col_reset:
        if st.button("🔄 Rozpocznij nowy mecz", use_container_width=True):
            st.session_state.history = []
            st.session_state.game_finished = False
            st.rerun()