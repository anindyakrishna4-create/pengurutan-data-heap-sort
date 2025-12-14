# File: heap_sort_core.py

# List global untuk menyimpan riwayat langkah
HISTORY = []

def heap_sort(data_list):
    """
    Mengimplementasikan Heap Sort dan mencatat setiap langkah di HISTORY.
    """
    global HISTORY
    HISTORY = []
    
    arr = data_list[:] # Salinan array untuk dimodifikasi in-place
    n = len(arr)

    # 1. Fase Build Max-Heap
    HISTORY.append({'array': arr[:], 'highlight': (-1, -1, 'Build Heap'), 'action': 'Fase 1: Membangun Max Heap...'})
    
    # Mulai dari parent terakhir yang mungkin (floor(n/2) - 1)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, True)

    # 2. Fase Ekstraksi (Pengurutan)
    HISTORY.append({'array': arr[:], 'highlight': (-1, -1, 'Sort Start'), 'action': 'Fase 2: Ekstraksi dan Pengurutan Dimulai...'})
    
    for i in range(n - 1, 0, -1):
        
        # Tukar elemen root (terbesar) dengan elemen terakhir dari heap saat ini
        arr[i], arr[0] = arr[0], arr[i] 
        
        # Catat setelah Penukaran
        HISTORY.append({
            'array': arr[:], 
            'highlight': (0, i, 'Tukar Root'), # Root (0) dan Elemen Akhir (i) ditukar
            'action': f'Tukar Root ({arr[i]}) dengan Elemen Akhir Heap ({arr[0]}). Heap Size: {i}'
        })
        
        # Panggil heapify pada sub-tree yang tersisa (mengabaikan elemen yang sudah diurutkan)
        heapify(arr, i, 0, False)

    # Catat status Selesai
    HISTORY.append({'array': arr[:], 'highlight': (-1, -1, 'Selesai'), 'action': 'Pengurutan Selesai'})
    
    return arr, HISTORY

def heapify(arr, n, i, is_build_phase):
    """
    Prosedur untuk menstabilkan struktur heap pada sub-pohon berakar i.
    """
    largest = i  # Inisialisasi root sebagai yang terbesar
    left = 2 * i + 1     # indeks anak kiri
    right = 2 * i + 2    # indeks anak kanan

    # Jika anak kiri lebih besar dari root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # Jika anak kanan lebih besar dari yang terbesar sejauh ini
    if right < n and arr[right] > arr[largest]:
        largest = right

    # Jika yang terbesar bukan root (i)
    if largest != i:
        
        # Catat state saat Membandingkan dan sebelum Menukar
        HISTORY.append({
            'array': arr[:], 
            'highlight': (i, largest, 'Bandingkan/Adjust'), # Root (i) dan yang terbesar (largest)
            'action': f'Heapify: Bandingkan Indeks {i} dengan Indeks {largest}. Tukar.'
        })

        # Tukar root dengan yang terbesar
        arr[i], arr[largest] = arr[largest], arr[i] 

        # Lanjutkan proses heapify secara rekursif ke sub-tree yang terdampak
        heapify(arr, n, largest, is_build_phase)
