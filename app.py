# File: app.py (KODE FINAL - Matplotlib)

import streamlit as st
import pandas as pd
import time
from heap_sort import heap_sort 
import matplotlib.pyplot as plt
import numpy as np

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Virtual Lab: Heap Sort (Matplotlib)",
    layout="wide"
)

st.title("🌲 Virtual Lab: Heap Sort Interaktif (Matplotlib)")
st.markdown("### Visualisasi Algoritma Pengurutan Data (Max Heap)")

st.sidebar.header("Konfigurasi Data")

# --- Input Pengguna (Tanpa Batas Input) ---
default_data = "45, 12, 90, 3, 55, 18, 70, 25, 60, 105"
input_data_str = st.sidebar.text_input(
    "Masukkan data (pisahkan dengan koma):", 
    default_data
)
speed = st.sidebar.slider("Kecepatan Simulasi (detik)", 0.1, 2.0, 0.5)

# --- Proses Data Input ---
try:
    data_list = [int(x.strip()) for x in input_data_str.split(',') if x.strip()]
    initial_data = list(data_list)
    if not initial_data:
        st.error("Masukkan setidaknya satu angka.")
        st.stop()
except ValueError:
    st.error("Masukkan data dalam format angka (integer) yang dipisahkan oleh koma (misalnya: 10, 5, 8).")
    st.stop()
    
# --- Penjelasan ---
st.markdown("""
#### Pewarnaan Bar:
* **Kuning (#F1C232):** Elemen **Root** atau **Parent** yang sedang disesuaikan.
* **Hijau (#6AA84F):** Elemen yang baru saja **ditukar**.
* **Merah (#CC0000):** Elemen yang sudah **terurut**.
""")

st.write(f"**Data Awal:** {initial_data}")

# --- Fungsi Plot Matplotlib ---
def plot_array(arr, highlight_data, sorted_boundary, max_val, action_type):
    fig, ax = plt.subplots(figsize=(10, 4))
    n = len(arr)
    x_pos = np.arange(n)
    
    (idx1, idx2, _) = highlight_data

    # Tentukan Warna untuk Setiap Batang
    colors = ['#4A86E8'] * n  # Warna default (Biru)
    
    for i in range(n):
        # 1. Merah (Terurut)
        if i >= sorted_boundary and sorted_boundary != n:
            colors[i] = '#CC0000'
        # 2. Hijau (Ditukar)
        elif action_type in ('Tukar Root', 'Tukar Node') and (i == idx1 or i == idx2):
            colors[i] = '#6AA84F'
        # 3. Kuning (Aktif/Parent)
        elif action_type in ('Bandingkan/Adjust', 'Build Heap') and i == idx1:
            colors[i] = '#F1C232'
    
    # Membuat Bar Plot
    ax.bar(x_pos, arr, color=colors)
    
    # Menambahkan Label Angka di Atas Bar
    for i, height in enumerate(arr):
        ax.text(x_pos[i], height + max_val * 0.02, str(height), ha='center', va='bottom', fontsize=10)
        
    # Konfigurasi Grafik
    ax.set_ylim(0, max_val * 1.1)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f'Posisi {i}' for i in range(n)], rotation=0)
    ax.set_ylabel('Nilai')
    ax.set_title(f"Aksi: {action_type}")
    
    plt.close(fig) 
    return fig


# --- Visualisasi Utama ---
if st.button("Mulai Simulasi Heap Sort"):
    
    sorted_data, history = heap_sort(list(data_list))
    max_data_value = max(initial_data) if initial_data else 10 
    
    st.markdown("---")
    st.subheader("Visualisasi Langkah Demi Langkah")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        vis_placeholder = st.empty()
        status_placeholder = st.empty() 
    with col2:
        table_placeholder = st.empty()
    
    sorted_boundary = len(initial_data)
    
    # --- Loop Simulasi ---
    for step, state in enumerate(history):
        current_array = state['array']
        (idx1, idx2, action_type) = state['highlight']
        action = state['action']
        
        # PENTING: Perbarui batas terurut
        if action_type == 'Tukar Root':
            sorted_boundary = idx2 

        # --- Tampilkan Grafik (Matplotlib) ---
        fig_mpl = plot_array(current_array, state['highlight'], sorted_boundary, max_data_value, action_type)

        with vis_placeholder.container():
            st.pyplot(fig_mpl, clear_figure=True)
        
        # --- TABEL DATA ---
        with table_placeholder.container():
             df_table = pd.DataFrame({'Index': range(len(current_array)), 'Nilai': current_array})
             st.markdown("##### Data Saat Ini (Tabel)")
             st.dataframe(df_table.T, hide_index=True)

        with status_placeholder.container():
            st.info(f"**Langkah ke-{step+1}** | **Aksi:** {action}")
            
            if action_type == 'Selesai':
                 st.success("Array telah terurut! Proses Heap Sort Selesai.")
            elif action_type == 'Tukar Root':
                 st.caption(f"Hijau: Root ditukar ke posisi terurut **{sorted_boundary}**. Lakukan Heapify pada sisa Heap.")
            elif action_type == 'Bandingkan/Adjust':
                 st.caption("Kuning: Parent/Node yang sedang disesuaikan (Heapify).")

        # Jeda untuk simulasi
        time.sleep(speed)

    # --- Hasil Akhir Final (Dipastikan Tampil Setelah Loop Selesai) ---
    st.balloons()
    st.success(f"**Pengurutan Selesai!**")
    st.write(f"**Data Terurut:** {sorted_data}")
    st.info(f"Algoritma Heap Sort selesai dalam **{len(history)-1}** langkah visualisasi.")
