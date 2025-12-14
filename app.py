# File: app.py

import streamlit as st
import pandas as pd
import time
from heap_sort import heap_sort 
import altair as alt

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Virtual Lab: Heap Sort",
    layout="wide"
)

st.title("🌲 Virtual Lab: Heap Sort Interaktif")
st.markdown("### Visualisasi Algoritma Pengurutan Data (Max Heap)")

st.sidebar.header("Konfigurasi Data")

# --- Input Pengguna (Tanpa Batas Input) ---
default_data = "45, 12, 90, 3, 55, 18, 70, 25, 60"
# Tidak ada batasan jumlah input di sini, Python akan menangani list berapapun panjangnya.
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
#### Cara Kerja Heap Sort:
Heap Sort bekerja dalam dua fase: **Build Heap** (membuat pohon terbesar di atas) dan **Sorting** (berulang kali mengekstrak elemen terbesar).
* **Kuning:** Elemen **Root** atau **Parent** yang sedang disesuaikan.
* **Hijau:** Elemen yang baru saja ditukar (Root dan Elemen Terakhir).
* **Merah:** Elemen yang sudah terurut (berada di posisi akhir).
""")

st.write(f"**Data Awal:** {initial_data}")

# --- Visualisasi Awal ---
if st.button("Mulai Simulasi Heap Sort"):
    
    sorted_data, history = heap_sort(list(data_list))
    
    st.markdown("---")
    st.subheader("Visualisasi Langkah Demi Langkah")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        vis_placeholder = st.empty()
    with col2:
        table_placeholder = st.empty()
        status_placeholder = st.empty()
    
    # Variabel untuk melacak batas array yang sudah terurut
    sorted_boundary = len(initial_data)
    
    # --- Loop Simulasi ---
    for step, state in enumerate(history):
        current_array = state['array']
        # UNPACKING 3 ELEMEN: (idx1, idx2, action_type)
        (idx1, idx2, action_type) = state['highlight']
        action = state['action']
        
        if action_type == 'Tukar Root':
            # Jika menukar root, artinya elemen di idx2 sudah terurut
            sorted_boundary = idx2 

        # Membuat Dataframe untuk Visualisasi Altair
        df_vis = pd.DataFrame({
            'Index': [f'Posisi {i}' for i in range(len(current_array))],
            'Nilai': current_array,
            
            # Tentukan warna berdasarkan status:
            'Tipe': [
                # Merah: Elemen sudah diurutkan (posisi akhir)
                'Terurut' if i >= sorted_boundary and sorted_boundary != len(initial_data) else
                # Hijau: Elemen yang baru saja ditukar (Root & Akhir)
                'Ditukar' if action_type == 'Tukar Root' and (i == idx1 or i == idx2) else
                # Kuning: Elemen yang sedang disesuaikan (Parent/Largest)
                'Aktif/Parent' if action_type in ('Bandingkan/Adjust', 'Build Heap') and i == idx1 else
                'Normal'
                for i in range(len(current_array))
            ]
        })
        
        # --- GRAFIK BATANG VERTIKAL (Interaktif) ---
        chart = alt.Chart(df_vis).mark_bar().encode(
            x=alt.X('Index', axis=None), 
            y=alt.Y('Nilai', scale=alt.Scale(domain=[0, max(initial_data) * 1.1])), 
            
            color=alt.Color('Tipe', 
                            scale=alt.Scale(domain=['Aktif/Parent', 'Ditukar', 'Terurut', 'Normal'], 
                                            range=['#F1C232', '#6AA84F', '#CC0000', '#4A86E8']), 
                            legend=None),
            tooltip=['Index', 'Nilai', 'Tipe']
        ).properties(
            title=f"Visualisasi Heap Sort (Langkah {step+1}) | Aksi: {action_type}"
        ).interactive()

        # --- Tampilkan di Placeholder ---
        with vis_placeholder.container():
            st.altair_chart(chart, use_container_width=True)
        
        # --- TABEL DATA (Untuk Keterangan Lebih Jelas) ---
        with table_placeholder.container():
             df_table = pd.DataFrame({'Index': range(len(current_array)), 'Nilai': current_array})
             st.markdown("##### Data Saat Ini (Tabel)")
             st.dataframe(df_table.T, hide_index=True)

        with status_placeholder.container():
            st.info(f"**Langkah ke-{step+1}** | **Aksi:** {action}")
            if action_type == 'Selesai':
                 st.success("Array telah terurut! Selesai.")
            elif action_type == 'Tukar Root':
                 st.caption("Hijau: Root (terbesar) ditukar ke posisi terurut (Merah).")
            elif action_type == 'Bandingkan/Adjust':
                 st.caption("Kuning: Parent/Node yang sedang disesuaikan (Heapify).")


        # Jeda untuk simulasi
        time.sleep(speed)

    # --- Hasil Akhir ---
    st.balloons()
    st.success(f"**Pengurutan Selesai!**")
    st.write(f"**Data Terurut:** {sorted_data}")
    st.info(f"Algoritma Heap Sort selesai dalam **{len(history)-1}** langkah visualisasi.")
