import streamlit as st
import pandas as pd
import time
import random
import matplotlib.pyplot as plt

# --- 1. Fungsi Inti Heap Sort ---

def heapify(arr, n, i, steps, comparisons_count):
    """
    Prosedur untuk membentuk Max Heap dari subtree di indeks i.
    """
    largest = i  # Inisialisasi largest sebagai root
    l = 2 * i + 1  # Indeks anak kiri
    r = 2 * i + 2  # Indeks anak kanan
    
    current_step = {
        'array': list(arr),
        'highlight': [i, l if l < n else -1, r if r < n else -1],
        'action': f"Membandingkan Node {arr[i]} dengan anak-anaknya"
    }
    steps.append(current_step)
    
    comparisons_count[0] += 1
    # Jika anak kiri lebih besar dari root
    if l < n and arr[l] > arr[largest]:
        largest = l
        
    comparisons_count[0] += 1
    # Jika anak kanan lebih besar dari root sekarang
    if r < n and arr[r] > arr[largest]:
        largest = r
        
    # Jika root bukan yang terbesar, tukar dan lanjutkan heapify
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i] # Swap
        
        current_step = {
            'array': list(arr),
            'highlight': [i, largest],
            'action': f"Menukar {arr[largest]} dan {arr[i]} untuk menjaga properti Max Heap"
        }
        steps.append(current_step)
        
        # Rekursif heapify subtree yang terpengaruh
        heapify(arr, n, largest, steps, comparisons_count)

def heap_sort(arr):
    """
    Fungsi utama Heap Sort.
    """
    n = len(arr)
    steps = []
    comparisons_count = [0]
    
    # 1. Membangun Max Heap (proses 'heapify' dari semua node non-leaf)
    st.subheader("Fase 1: Membangun Max Heap")
    
    # Indeks node non-leaf terakhir
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, steps, comparisons_count)
        
    # 2. Ekstraksi elemen satu per satu dari heap
    st.subheader("Fase 2: Ekstraksi dan Pengurutan")
    for i in range(n - 1, 0, -1):
        # Pindahkan root saat ini ke akhir
        arr[i], arr[0] = arr[0], arr[i]
        
        current_step = {
            'array': list(arr),
            'highlight': [i, 0],
            'action': f"Menukar root (terbesar) {arr[0]} dengan elemen terakhir yang belum diurutkan (indeks {i})"
        }
        steps.append(current_step)
        
        # Panggil heapify pada heap yang tersisa
        heapify(arr, i, 0, steps, comparisons_count)
        
    return arr, steps, comparisons_count[0]

# --- 2. Fungsi Visualisasi (Matplotlib) ---

def plot_bar_chart(arr, highlight=None, title="Visualisasi Array"):
    """
    Membuat visualisasi bar chart untuk array.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['skyblue'] * len(arr)
    
    # Highlight elemen yang sedang diproses
    if highlight:
        for index in highlight:
            if 0 <= index < len(arr):
                colors[index] = 'salmon' # Warna untuk highlight
    
    # Membuat Bar Chart
    bars = ax.bar(range(len(arr)), arr, color=colors)
    ax.set_title(title)
    ax.set_xticks(range(len(arr)))
    ax.set_xticklabels([str(x) for x in arr])
    ax.set_xlabel("Indeks")
    ax.set_ylabel("Nilai")
    
    # Menambahkan nilai di atas bar
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')
        
    st.pyplot(fig)
    plt.close(fig) # Penting untuk membebaskan memori

# --- 3. Fungsi Uji Kinerja ---

def run_performance_test(max_size=10000):
    """
    Menguji kinerja Heap Sort vs. algoritma lain (misalnya Python's built-in Timsort)
    """
    sizes = [10, 100, 500, 1000, 5000, max_size]
    results = []
    
    st.info(f"Melakukan uji kinerja hingga {max_size} data. Mungkin membutuhkan waktu...")
    
    for size in sizes:
        # Data acak
        data = [random.randint(1, 1000) for _ in range(size)]
        
        # Test 1: Heap Sort
        arr_heap = list(data)
        start_time_heap = time.perf_counter()
        
        # Menggunakan versi heap_sort tanpa menyimpan steps untuk kinerja
        def minimal_heap_sort(arr):
            n = len(arr)
            for i in range(n // 2 - 1, -1, -1):
                # Ini hanya kerangka, implementasi penuh dengan comparison_count 
                # akan lebih akurat, tapi ini cukup untuk perbandingan waktu.
                # Untuk tujuan kinerja, kita panggil fungsi standar saja.
                pass 
            # Sebagai pengganti: gunakan tim sort untuk baseline
            return sorted(arr) 

        # Karena Heap Sort di atas mencatat langkah, kita pakai Timsort built-in 
        # untuk perbandingan. Jika perlu metrik Heap Sort, kode perlu diubah.
        # Untuk tujuan lab, kita bandingkan dengan Timsort (standar Python).
        
        # Uji Heap Sort (dengan minimal implementasi untuk mengukur waktu)
        arr_heap_time = list(data)
        n = len(arr_heap_time)
        
        # Implementasi minimal yang hanya mengukur waktu
        def heap_sort_perf(arr, n):
            def heapify_perf(arr, n, i):
                largest = i
                l = 2 * i + 1
                r = 2 * i + 2
                if l < n and arr[l] > arr[largest]:
                    largest = l
                if r < n and arr[r] > arr[largest]:
                    largest = r
                if largest != i:
                    arr[i], arr[largest] = arr[largest], arr[i]
                    heapify_perf(arr, n, largest)
            
            for i in range(n // 2 - 1, -1, -1):
                heapify_perf(arr, n, i)
            for i in range(n - 1, 0, -1):
                arr[i], arr[0] = arr[0], arr[i]
                heapify_perf(arr, i, 0)
        
        heap_sort_perf(arr_heap_time, n)
        end_time_heap = time.perf_counter()
        time_heap = (end_time_heap - start_time_heap) * 1000 # dalam ms
        
        # Test 2: Timsort (Built-in Python)
        arr_timsort = list(data)
        start_time_timsort = time.perf_counter()
        arr_timsort.sort()
        end_time_timsort = time.perf_counter()
        time_timsort = (end_time_timsort - start_time_timsort) * 1000 # dalam ms
        
        results.append({
            'Ukuran Data (N)': size,
            'Heap Sort (ms)': time_heap,
            'Timsort (ms)': time_timsort,
        })
        
    df = pd.DataFrame(results)
    
    st.subheader("📊 Tabel Kinerja")
    st.dataframe(df.set_index('Ukuran Data (N)'))
    
    st.subheader("📈 Grafik Perbandingan Waktu Eksekusi")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['Ukuran Data (N)'], df['Heap Sort (ms)'], marker='o', label='Heap Sort')
    ax.plot(df['Ukuran Data (N)'], df['Timsort (ms)'], marker='x', label='Timsort (Built-in Python)')
    
    ax.set_title('Perbandingan Waktu Eksekusi Berbagai Ukuran Data')
    ax.set_xlabel('Ukuran Data (N)')
    ax.set_ylabel('Waktu Eksekusi (ms)')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
    plt.close(fig)

# --- 4. Streamlit App Interface ---

st.set_page_config(layout="wide", page_title="Virtual Lab: Heap Sort Interaktif")

st.title("🔬 Virtual Lab: Algoritma Heap Sort")
st.markdown("### Memahami Cara Kerja Pengurutan Data Heap Sort")

st.sidebar.header("⚙️ Pengaturan Input Data")

# Input pengguna
input_type = st.sidebar.radio(
    "Pilih Tipe Input:",
    ("Acak (Random)", "Manual Input")
)

initial_data = []

if input_type == "Acak (Random)":
    num_elements = st.sidebar.slider("Jumlah Elemen:", 5, 20, 10)
    max_value = st.sidebar.number_input("Nilai Maksimum:", 10, 100, 50)
    
    if st.sidebar.button("Generate Data Acak"):
        initial_data = [random.randint(1, max_value) for _ in range(num_elements)]
        st.session_state['data'] = initial_data
    
    if 'data' not in st.session_state or not st.session_state['data']:
         st.session_state['data'] = [5, 13, 2, 25, 7, 17, 20, 8, 4] # Data default
         
    initial_data = st.session_state['data']

else: # Manual Input
    data_str = st.sidebar.text_area(
        "Masukkan Data (pisahkan dengan koma):", 
        "5, 13, 2, 25, 7, 17, 20, 8, 4"
    )
    try:
        initial_data = [int(x.strip()) for x in data_str.split(',') if x.strip()]
        if len(initial_data) < 2:
            st.error("Masukkan minimal 2 angka.")
            initial_data = []
    except ValueError:
        st.error("Pastikan semua input adalah angka.")
        initial_data = []

if initial_data:
    st.header("Data Awal")
    st.code(initial_data)
    
    data_to_sort = list(initial_data) # Salinan data untuk diurutkan
    
    if st.button("Mulai Proses Heap Sort"):
        st.balloons()
        
        # Jalankan Heap Sort dan simpan langkah-langkahnya
        start_time = time.perf_counter()
        sorted_arr, steps, comparisons = heap_sort(data_to_sort)
        end_time = time.perf_counter()
        
        execution_time = (end_time - start_time) * 1000 # dalam ms
        
        st.success("✅ Pengurutan Selesai!")
        
        # Tampilkan Metrik
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Waktu Eksekusi (ms)", f"{execution_time:.4f}")
        with col2:
            st.metric("Total Perbandingan", f"{comparisons}")
        
        st.header("Detail Langkah Demi Langkah")
        
        # Slider interaktif untuk melihat setiap langkah
        step_index = st.slider("Pilih Langkah", 0, len(steps) - 1, 0)
        
        current_step = steps[step_index]
        
        st.info(f"**Langkah {step_index + 1}/{len(steps)}:** {current_step['action']}")
        
        # Visualisasi Bar Chart
        plot_bar_chart(
            current_step['array'], 
            current_step['highlight'], 
            title=f"Langkah {step_index + 1}: {current_step['action']}"
        )
        
        # Tampilkan array saat ini
        st.code(current_step['array'])
        
        # Tampilkan Hasil Akhir
        st.header("Hasil Akhir")
        st.code(sorted_arr)
        
# --- 5. Bagian Uji Kinerja ---

st.sidebar.markdown("---")
st.sidebar.header("Uji Kinerja Komparatif")

if st.sidebar.button("Jalankan Uji Kinerja Besar"):
    st.header("Uji Kinerja Algoritma Pengurutan")
    run_performance_test(max_size=10000)

st.sidebar.markdown("""
---
*Lab ini dibuat untuk tujuan edukasi. 
Kode sumber dapat ditemukan di GitHub.*
""")
