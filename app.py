import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import time
from heap_sort_core import heap_sort_with_steps
import random

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
        st.sidebar.error("Input tidak valid. Pastikan hanya angka yang dipisahkan koma.")
        raw_data = []

elif input_method == "Generate Random":
    n_elements = st.sidebar.slider(
        "Jumlah Elemen (Maks. 500 untuk visualisasi grafis yang lancar):", 
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
    st.write(data_to_sort)
    st.write("---")

    # --- Eksekusi Algoritma ---
    if st.button("▶️ Mulai Pengurutan"):
        start_time = time.time()
        
        # Dapatkan array terurut dan semua langkah
        sorted_array, steps = heap_sort_with_steps(data_to_sort)
        
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000 # dalam ms
        
        st.session_state['steps'] = steps
        st.session_state['execution_time'] = execution_time
        st.session_state['sorted_array'] = sorted_array

# --- Visualisasi Hasil (Setelah Proses Selesai) ---
if 'steps' in st.session_state:
    st.subheader("✅ Hasil Pengurutan")
    st.success(f"Array Terurut: {st.session_state['sorted_array']}")
    st.info(f"Waktu Eksekusi: **{st.session_state['execution_time']:.4f} ms**")
    
    st.write("---")
    st.subheader("Visualisasi Langkah Demi Langkah")

    total_steps = len(st.session_state['steps'])
    
    # Slider untuk navigasi langkah
    step_index = st.slider(
        "Pilih Langkah untuk Dilihat:", 
        min_value=0, 
        max_value=total_steps - 1, 
        value=0, 
        key='step_slider'
    )

    current_array = st.session_state['steps'][step_index]
    
    st.markdown(f"**Langkah ke: {step_index + 1} dari {total_steps}**")

    #  - Tambahkan visualisasi pohon biner 
    
    # Visualisasi Bar Chart
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(range(len(current_array)), current_array, color='skyblue')
    
    # Beri warna yang berbeda untuk elemen yang mungkin sedang diproses (misalnya, root atau elemen yang ditukar)
    if total_steps > 1:
        # Tentukan status pengurutan (Tahap Heapify atau Tahap Ekstraksi)
        if step_index < total_steps // 2 and total_steps > 3: # Estimasi kasar untuk tahap heapify
            st.warning("**Tahap 1: Membangun Max-Heap**")
        elif step_index > total_steps // 2 and total_steps > 3:
            st.success("**Tahap 2: Ekstraksi dan Pengurutan**")
            # Highlight elemen yang sudah terurut (di bagian akhir array)
            sorted_count = len(current_array) - (st.session_state['steps'].index(current_array) - (total_steps // 2)) 
            for i in range(len(current_array) - (step_index - (total_steps // 2) + 1), len(current_array)):
                 bars[i].set_color('lightgreen')
    
    # Label dan Judul
    ax.set_title(f"Visualisasi Array pada Langkah {step_index + 1}")
    ax.set_xlabel("Indeks")
    ax.set_ylabel("Nilai")
    
    # Tambahkan nilai di atas bar (jika tidak terlalu banyak elemen)
    if len(current_array) <= 50:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 5, 
                    f'{height}', ha='center', va='bottom', fontsize=8)
    
    st.pyplot(fig)

    st.write("---")
    
    # --- Grafik Komparatif dan Metrik ---
    st.subheader("📈 Analisis Kinerja")
    
    # Contoh data untuk perbandingan (bisa disimulasikan atau statis)
    algorithms = ["Heap Sort (Visualisasi)", "Quick Sort (Simulasi)", "Merge Sort (Simulasi)"]
    times = [st.session_state['execution_time'], 50 + random.random() * 20, 60 + random.random() * 15] # Data simulasi

    df_metrics = pd.DataFrame({
        "Algoritma": algorithms,
        "Waktu Eksekusi (ms)": times,
        "Kompleksitas Waktu Rata-rata": ["O(n log n)", "O(n log n)", "O(n log n)"]
    })

    st.table(df_metrics) # Menggunakan st.table untuk tampilan tabel data
    
    # Grafik Batang untuk Perbandingan Waktu
    fig_comp, ax_comp = plt.subplots(figsize=(8, 4))
    ax_comp.bar(df_metrics["Algoritma"], df_metrics["Waktu Eksekusi (ms)"], color=['darkblue', 'gray', 'gray'])
    ax_comp.set_title("Perbandingan Waktu Eksekusi (Simulasi)")
    ax_comp.set_ylabel("Waktu (ms)")
    ax_comp.tick_params(axis='x', rotation=15)
    st.pyplot(fig_comp)
    
    
else:
    st.info("Silakan masukkan atau *generate* data dan klik 'Mulai Pengurutan' untuk melihat visualisasi.")

# --- Bagian Edukasi ---
st.sidebar.header("📚 Konsep Heap Sort")
st.sidebar.markdown(
    """
    Heap Sort adalah algoritma pengurutan berbasis perbandingan yang menggunakan struktur data *Binary Heap*.

    1.  **Membangun Max-Heap:** Array data diubah menjadi Max-Heap, di mana setiap *node* induk lebih besar dari *node* anak-anaknya.
    2.  **Ekstraksi:** Elemen terbesar (akar Heap) ditukar dengan elemen terakhir array. Ukuran Heap dikurangi 1.
    3.  **Heapify:** Heap yang tersisa di-restore agar menjadi Max-Heap kembali.

    Proses ini diulang sampai seluruh array terurut. Kompleksitas waktunya adalah **O(n log n)**.
    """
)


# --- Kesimpulan dan Next Step ---
st.write("---")
st.markdown("Anda telah mempelajari Heap Sort. Cobalah data yang lebih banyak untuk melihat perbedaan waktu eksekusi!")
