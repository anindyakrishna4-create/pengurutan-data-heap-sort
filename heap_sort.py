def heapify(arr, n, i, steps):
    """
    Prosedur untuk menumpuk (heapify) sub-pohon berakar i. 
    n adalah ukuran heap.
    """
    largest = i  # Inisialisasi largest sebagai root
    l = 2 * i + 1  # Indeks kiri
    r = 2 * i + 2  # Indeks kanan

    # Lihat apakah anak kiri dari root ada dan lebih besar dari root
    if l < n and arr[i] < arr[l]:
        largest = l

    # Lihat apakah anak kanan dari root ada dan lebih besar dari yang terbesar saat ini
    if r < n and arr[largest] < arr[r]:
        largest = r

    # Ganti root jika perlu
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # Lakukan pertukaran

        # Simpan state setelah pertukaran
        steps.append(list(arr)) 
        
        # Panggil heapify secara rekursif pada sub-pohon yang terpengaruh
        heapify(arr, n, largest, steps)

def heap_sort_with_steps(arr):
    """
    Fungsi utama Heap Sort yang mengembalikan array terurut dan daftar langkah-langkah.
    """
    n = len(arr)
    steps = [list(arr)] # Langkah awal (array original)

    # 1. Bangun max-heap (atur ulang array)
    # Loop mundur dari indeks non-leaf pertama (n//2 - 1) hingga 0
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, steps)
    
    # Simpan state setelah Max-Heap selesai dibangun
    steps.append(list(arr)) 

    # 2. Ekstraksi elemen satu per satu
    for i in range(n - 1, 0, -1):
        # Pindahkan root saat ini ke akhir
        arr[i], arr[0] = arr[0], arr[i]  # Pertukaran
        
        # Simpan state setelah pertukaran (elemen terakhir adalah elemen yang sudah terurut)
        steps.append(list(arr)) 
        
        # Panggil max heapify pada heap yang tersisa (mengabaikan elemen yang sudah terurut)
        heapify(arr, i, 0, steps) 
        
        # Pastikan ada langkah setelah setiap iterasi ekstraksi
        if steps[-1] != arr:
             steps.append(list(arr))

    return arr, steps
