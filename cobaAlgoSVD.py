# untuk mencoba membuat algo svd tanpa linalg.svd
import cv2 as cv
import numpy as np
import math



# function 
def ownSVD(img):
    a = img.T @ img
    pq = np.zeros((a.shape[0], a.shape[0]), int)
    np.fill_diagonal(pq, 1)
    for i in range(0,3):
        q,r = np.linalg.qr(a)
        pq = pq @ q
        a = r @ q

    b = img @ img.T
    pq2 = np.zeros((b.shape[0], b.shape[0]), int)
    np.fill_diagonal(pq2, 1)
    for i in range(0,10):
        q,r = np.linalg.qr(b)
        pq2 = pq2 @ q
        b = r @ q
    temp = np.absolute(np.diag(a))
    # temp = np.diag(b)
    return pq2,temp, pq.T



def algo(filename, percentage):
    img = cv.imread(filename)

    grayImage = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # cv abai in metadata. img langsung jadi array numpy. man easier jdie.
    # save image
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



    colorChannel = grayImage
    # PROSES COMPRESSING SVD
    print("proccessing gray")
    # u, s, vh = ownSVD(colorChannel)
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
    output = u @ np.diag(s) @ vh


    imgOut = output
    # PRINT KE FILE
    status = cv.imwrite('compressed.jpg',imgOut)
    print("status : ", status)


    
# using function
# filename='image.jpg'
# algo(filename, 1)



# mencoba membandingkan hasil svd
# x = np.random.rand(5,5)
x = np.array([[52,30,49,28],
[30,50,8,44],
[49,8,46,16],
[28,44,16,22]], int)
uown,sown,vhown  = ownSVD(x)
# w, v = np.linalg.eigh(x.T @ x)
u, s, vh = np.linalg.svd(x, full_matrices=False)

print(np.round(sown,decimals = 2))
print(uown)
print(u)