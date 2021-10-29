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
u, s, vh = np.linalg.svd(grayImage, full_matrices=False) # sementara full matrix = false. ini ngaruh ke ukuran dari matriks u sama vh. 
# akibatnya matriksnya gk 'full' sesuai svd, tapi false dulu soalnya toh bagian matriks yang 'dipotong' gabakal diakses juga
# kalo mau dibikin true, kita jadi perlu nge modif matriks S lebih jauh. nge debugnya dengan matriks.shape,
# gagal kalo gk sesuai ketentuan perkalian matriks. 

status = cv.imwrite('uncompressed.jpg',grayImage)

# PROSES COMPRESSING SVD
print("PROSES COMPRES")
kmax = s.shape[0]

percentage = 0.1
# percentage = 1 artinya k = kmax. 

k = math.floor(percentage * kmax)
if (k == 0):
    k = 1

#potong U
print("POTONG U")
u = u.T[0:k].T

# potong s
print("POTONG S")
s = s[0:k]

# potong vh
print("POTONG VH")
vh = vh[0:k]

# PROSES GABUNGIN LAGI MENJADI SATU MATRIKS
b = u @ np.diag(s) @ vh

# PRINT KE FILE
status = cv.imwrite('compressed.jpg',b)
print("status : ", status)