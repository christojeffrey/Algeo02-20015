# untuk uji coba compressing pake python, tanpa web2 an
import cv2 as cv
import numpy as np
import math

# read image as grey scale
img = cv.imread('image.jpg')

grayImage = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# cv abai in metadata. img langsung jadi array numpy. man easier jdie.
# save image
print("image berhasil di read, calculating svd...")

# MENENTUKKAN K
compressRatio = 0.1
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
    print("proccessing channel ",i)
    u, s, vh = np.linalg.svd(colorChannel, full_matrices=False) 
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
b = output[0]
g = output[1]
r = output[2]
imgOut = cv.merge((b,g,r))
# PRINT KE FILE
status = cv.imwrite('compressed.jpg',imgOut)
print("status : ", status)