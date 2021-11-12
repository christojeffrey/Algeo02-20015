# untuk mencoba membuat algo svd tanpa linalg.svd
import cv2 as cv
import numpy as np
import math



# function 

def ownSVD(img):
    min = img.shape[1]
    if img.shape[0] < img.shape[1]:
        min = img.shape[0]
    

    a = img.T @ img
    kanan = np.zeros((a.shape[0], a.shape[0]), int)
    np.fill_diagonal(kanan, 1)
    for i in range(0,100):
        q,r = np.linalg.qr(a)
        kanan = kanan @ q
        a = r @ q
    tengah = np.absolute(np.diag(a))
    tengah = np.sqrt(tengah)
    kiri = img @ kanan / tengah
    return kiri.T[0:min].T,tengah[0:min], kanan.T[0:min]



def algo(filename, percentage):
    img = cv.imread(filename)
    print("image berhasil di read, calculating svd...")

    # MENENTUKKAN K
    compressRatio = percentage/100
    m = img.shape[0]
    n = img.shape[1]
    k = compressRatio*(m*n)/(1 + m + n)
    k = math.floor(k)
    kmax = min(m,n)
    if (k == 0):
        k = 1
    print("compressRatio = ", compressRatio)
    print("kmax = ", kmax)
    print("k = ", k)
    print("ukuran asli = ", m*n)
    print("ukuran compressed = ", k*(1+m+n))

    output = np.zeros((3, m, n))
    print(output[1].shape)
    print("PROSES COMPRES")
    for i in range (3):
        colorChannel = img[:,:,i]
        # PROSES COMPRESSING SVD
        print("proccessing channel ",i+1)
        u, s, vh = ownSVD(colorChannel)
        # sementara full matrix = false. ini ngaruh ke ukuran dari matriks u sama vh. 
        # akibatnya matriksnya gk 'full' sesuai svd, tapi false dulu soalnya toh bagian matriks yang 'dipotong' gabakal diakses juga
        # kalo mau dibikin true, kita jadi perlu nge modif matriks S lebih jauh. nge debugnya dengan matriks.shape,
        # gagal kalo gk sesuai ketentuan perkalian matriks. 

        #potong U
        u = u.T[0:k].T

        # potong s
        s = s[0:k]

        # potong vh
        vh = vh[0:k]

        # PROSES GABUNGIN LAGI MENJADI SATU MATRIKS
        output[i] = u @ np.diag(s) @ vh

    #combining
    printf("combining...")
    b = output[0]
    g = output[1]
    r = output[2]
    imgOut = cv.merge((b,g,r))
    # PRINT KE FILE
    status = cv.imwrite('ALGOSENDIRICOMPRES.jpg',imgOut)
    print("status : ", status)


    
# using function
filename='image.jpg'
algo(filename, 100)