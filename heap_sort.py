# File: heap_sort.py (Revisi Final)

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
    
    # Mulai dari parent terakhir (floor(n/2) - 1)
    for i in range(n // 2 - 1, -1, -1):
        _heapify_down(arr, n, i)

    # 2. Fase Ekstraksi (Pengurutan)
    HISTORY.append({'array': arr[:], 'highlight': (-1, -1, 'Sort Start'), 'action': 'Fase 2: Ekstraksi dan Pengurutan Dimulai...'})
    
    for i in range(n - 1, 0, -1):
        
        # Tukar elemen root (terbesar) dengan elemen terakhir dari heap saat ini (i)
        arr[i], arr[0] = arr[0], arr[i] 
        
        # Catat setelah Penukaran
        HISTORY.append({
            'array': arr[:], 
            'highlight': (0, i, 'Tukar Root'), # Root (0) dan Elemen Akhir (i) ditukar
            'action': f'Tukar Root ({arr[i]}) dengan Elemen Akhir Heap ({arr[0]}). Heap Size: {i}'
        })
        
        # Panggil heapify pada sub-tree yang tersisa (ukuran heap adalah i)
        _heapify_down(arr, i, 0)

    # Catat status Selesai
    HISTORY.append({'array': arr[:], 'highlight': (-1, -1, 'Selesai'), 'action': 'Pengurutan Selesai'})
    
    return arr, HISTORY

def _heapify_down(arr, n, i):
    """
    Prosedur untuk menstabilkan struktur heap pada sub-pohon berakar i.
    n adalah ukuran heap saat ini.
    """
    largest = i  
    left = 2 * i + 1     
    right = 2 * i + 2    

    # 1. Tentukan anak terbesar
    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    # 2. Jika yang terbesar bukan root (i), lakukan penukaran
    if largest != i:
        
        # Catat state saat Membandingkan dan sebelum Menukar
        HISTORY.append({
            'array': arr[:], 
            # i: root/parent, largest: anak yang terbesar
            'highlight': (i, largest, 'Bandingkan/Adjust'), 
            'action': f'Heapify: Bandingkan Indeks {i} ({arr[i]}) dengan Indeks {largest} ({arr[largest]}).'
        })

        # Tukar root dengan yang terbesar
        arr[i], arr[largest] = arr[largest], arr[i] 
        
        # Catat setelah penukaran
        HISTORY.append({
            'array': arr[:], 
            'highlight': (i, largest, 'Tukar Node'), # i dan largest ditukar
            'action': f'Tukar {arr[i]} dan {arr[largest]}. Lanjutkan Heapify.'
        })

        # Rekursif ke sub-tree yang terdampak
        _heapify_down(arr, n, largest)
    elif largest == i and n != len(arr):
        # Tambahkan catatan jika node sudah stabil (hanya saat fase sort)
        HISTORY.append({
            'array': arr[:], 
            'highlight': (i, -1, 'Node Stabil'), 
            'action': f'Node Indeks {i} stabil. Lanjut.'
        })
