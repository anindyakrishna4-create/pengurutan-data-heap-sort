# FILE: app.py

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import time
import random

# --- PENTING: IMPORT MODUL LOKAL ---
# Pastikan file heap_sort_core.py berada di direktori yang sama
try:
    from heap_sort_core import heap_sort_with_steps
except ModuleNotFoundError:
    st.error("Gagal memuat modul heap_sort_core. Pastikan file 'heap_sort_core.py' ada di direktori yang sama dengan 'app.py'!")
    st.stop() # Hentikan eksekusi jika modul lokal tidak ditemukan


# --- Konfigurasi Halaman ---
st.set_page_config(layout="wide", page_title="Virtual Lab: Heap Sort Interaktif")

st.title("🔬 Virtual Lab: Heap Sort Interaktif")
st.markdown("Pahami bagaimana algoritma **Heap Sort** bekerja langkah demi langkah.")
st.write("---")

# --- Input Data ---
st.sidebar.header("⚙️ Pengaturan Data")

input_method = st.sidebar.radio(
    "Pilih Metode Input Data:",
    ("Manual", "Generate Random")
)

raw_data = []

if input_method == "Manual":
    default_input = "4, 10, 3, 5, 1, 2"
    user_input = st.sidebar.text_area(
        "Masukkan Angka (dipisahkan koma, tanpa batas):", 
        default_input
    )
    
    try:
        # Filter input dan konversi ke integer
        raw_data = [int(x.strip()) for x in user_input.split(',') if x.strip()]
    except ValueError:
        st.sidebar.error("Input tidak valid. Pastikan hanya angka bulat yang dipisahkan koma.")
        raw_data = []

elif input_method == "Generate Random":
    # Batas visualisasi untuk menjaga performa
    n_elements = st.sidebar.slider(
        "Jumlah Elemen (Maks. 500 disarankan untuk visualisasi):", 
        min_value=5, max_value=500, value=20
    )
    seed_val = st.sidebar.number_input("Seed (opsional):", value=42)
    random.seed(seed_val)
    raw_data = [random.randint(1, 1000) for _ in range(n_elements)]

# Pastikan data ada dan valid sebelum diproses
if raw_data:
    st.sidebar.info(f"Jumlah elemen data: **{len(raw_data)}**")
    
    # Buat salinan data untuk proses sorting
    data_to_sort = list(raw_data) 
    
    st.subheader("📊 Data Awal")
    st.code(f"[{', '.join(map(str, data_to_sort))}]")
    st.write("---")

    # --- Eksekusi Algoritma ---
    if st.button("▶️ Mulai Pengurutan"):
        with st.spinner("Sedang menjalankan Heap Sort..."):
            start_time = time.time()
            
            # Dapatkan array terurut dan semua langkah
            sorted_array, steps = heap_sort_with_steps(data_to_sort)
            
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000 # dalam ms
            
            st.session_state['steps'] = steps
            st.session_state['execution_time'] = execution_time
            st.session_state['sorted_array'] = sorted_array
            st.success("Pengurutan Selesai!")
            st.rerun() # Refresh untuk menampilkan hasil

# --- Visualisasi Hasil (Setelah Proses Selesai) ---
if 'steps' in st.session_state and st.session_state['steps']:
    steps = st.session_state['steps']
    
    st.subheader("✅ Hasil Pengurutan")
    st.success(f"Array Terurut: [{', '.join(map(str, st.session_state['sorted_array']))}]")
    st.info(f"Waktu Eksekusi: **{st.session_state['execution_time']:.4f} ms**")
    
    st.write("---")
    st.subheader("Visualisasi Langkah Demi Langkah")

    total_steps = len(steps)
    
    # Slider untuk navigasi langkah
    step_index = st.slider(
        "Pilih Langkah untuk Dilihat:", 
        min_value=0, 
        max_value=total_steps - 1, 
        value=total_steps - 1, # Default ke langkah terakhir (terurut)
        key='step_slider'
    )

    current_array = steps[step_index]
    
    # Tentukan keterangan langkah
    if step_index == 0:
        step_description = "Data Awal."
        highlight_color = 'skyblue'
    elif step_index < total_steps * 0.5:
        step_description = "**Tahap 1: Membangun Max-Heap** (Mengatur ulang pohon)."
        highlight_color = 'orange'
    else:
        step_description = "**Tahap 2: Ekstraksi dan Pengurutan** (Memindahkan elemen terbesar ke akhir)."
        highlight_color = 'red'

    st.markdown(f"**Langkah ke: {step_index + 1} dari {total_steps}** - *{step_description}*")

    # Visualisasi Bar Chart
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(range(len(current_array)), current_array, color='lightgray')
    
    n = len(current_array)

    # 1. Warna Default (Tahap Heapify)
    color_map = ['skyblue'] * n

    # 2. Highlight elemen yang sudah terurut (Tahap Ekstraksi)
    if step_index >= total_steps * 0.5 and total_steps > 1:
        # Hitung jumlah elemen yang sudah terurut di bagian akhir array
        sorted_elements_count = 0
        
        # Cari tahu indeks pertama yang sudah terurut (elemen setelah heap yang tersisa)
        # Sulit memetakan indeks langkah ke indeks yang terurut tanpa state tambahan
        # Kita asumsikan elemen di akhir array setelah tahap 2 dimulai sudah terurut
        
        # Logika: Elemen yang sudah di-swap keluar dari heap
        # Jumlah elemen yang sudah terurut = n - (Ukuran heap saat ini)
        
        # Kita ambil cara paling sederhana: highlight 
        # setelah tahap build heap selesai, sisanya adalah proses ekstraksi
        
        # Perkiraan indeks terurut:
        # Indeks langkah ekstraksi dimulai sekitar total_steps * 0.5
        extractions_made = step_index - int(total_steps * 0.5)
        
        # Jika sedang dalam tahap ekstraksi
        if extractions_made > 0:
            for i in range(n - extractions_made, n):
                color_map[i] = 'lightgreen' # Elemen yang sudah terurut
            
            # Highlight elemen yang sedang ditukar (misalnya, root)
            if step_index < total_steps -1:
                color_map[0] = 'red' # Root yang akan ditukar

    # Terapkan warna
    for i, bar in enumerate(bars):
        bar.set_color(color_map[i])

    # Label dan Judul
    ax.set_title(f"Visualisasi Array pada Langkah {step_index + 1}")
    ax.set_xlabel("Indeks")
    ax.set_ylabel("Nilai")
    
    # Tambahkan nilai di atas bar (jika elemen <= 30)
    if len(current_array) <= 30:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + max(current_array)*0.01, 
                    f'{height}', ha='center', va='bottom', fontsize=8)
    
    # Menyesuaikan batas y-axis
    ax.set_ylim(0, max(raw_data) * 1.1)

    st.pyplot(fig)

    st.write("---")
    
    # --- Grafik Komparatif dan Metrik ---
    st.subheader("📈 Analisis Kinerja dan Kompleksitas")
    
    # Contoh data simulasi untuk perbandingan 
    algorithms = ["Heap Sort (Visualisasi)", "Quick Sort (Simulasi)", "Merge Sort (Simulasi)"]
    # Waktu simulasi dihitung relatif terhadap jumlah elemen (N)
    N = len(raw_data)
    time_sim_quick = st.session_state['execution_time'] * random.uniform(0.8, 1.2)
    time_sim_merge = st.session_state['execution_time'] * random.uniform(0.9, 1.1)
    
    data_for_table = {
        "Algoritma": algorithms,
        "Waktu Eksekusi (ms)": [st.session_state['execution_time'], time_sim_quick, time_sim_merge],
        "Kompleksitas Waktu Rata-rata": ["$O(n \log n)$", "$O(n \log n)$", "$O(n \log n)$"],
        "Kompleksitas Kasus Terburuk": ["$O(n \log n)$", "$O(n^2)$", "$O(n \log n)$"]
    }
    
    df_metrics = pd.DataFrame(data_for_table)

    st.markdown("#### Tabel Perbandingan")
    st.dataframe(df_metrics, hide_index=True)
    
    # Grafik Batang untuk Perbandingan Waktu
    fig_comp, ax_comp = plt.subplots(figsize=(8, 4))
    ax_comp.bar(df_metrics["Algoritma"], df_metrics["Waktu Eksekusi (ms)"], 
                color=['darkblue', 'gray', 'gray'])
    ax_comp.set_title("Perbandingan Waktu Eksekusi (Simulasi vs Nyata)")
    ax_comp.set_ylabel("Waktu (ms)")
    ax_comp.tick_params(axis='x', rotation=15)
    st.pyplot(fig_comp)
    
    
else:
    st.info("Masukkan atau *generate* data di sidebar, lalu klik 'Mulai Pengurutan' untuk melihat visualisasi interaktif.")

# --- Bagian Edukasi ---
st.sidebar.header("📚 Konsep Heap Sort")
st.sidebar.markdown(
    """
    Heap Sort adalah algoritma yang selalu menjamin kompleksitas waktu $O(n \log n)$, bahkan dalam kasus terburuk.

    1.  **Membangun Max-Heap:** Array diubah menjadi Max-Heap, di mana *node* induk $\geq$ anak.
    2.  **Ekstraksi:** Elemen terbesar (akar) ditukar dengan elemen terakhir, dan ukuran *heap* dikurangi 1.
    3.  **Heapify:** *Heap* yang tersisa diperbaiki.
    """
)

# --- Kesimpulan dan Next Step ---
st.write("---")
st.markdown("Selamat! Anda telah mempelajari Heap Sort. Eksplorasi dengan data yang lebih banyak untuk mengamati kompleksitas waktunya.")
