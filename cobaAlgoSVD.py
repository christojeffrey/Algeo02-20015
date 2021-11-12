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
    pq = np.zeros((a.shape[0], a.shape[0]), int)
    np.fill_diagonal(pq, 1)
    for i in range(0,10):
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
    return pq2.T[0:min].T,np.sqrt(temp)[0:min], pq.T[0:min]



def algo(filename, percentage):
    img = cv.imread(filename)

    grayImage = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # cv abai in metadata. img langsung jadi array numpy. man easier jdie.
    # save image
    print("image berhasil di read, calculating svd...")
    print("grayImage")
    print(grayImage)
    # MENENTUKKAN K
    # compressRatio = percentage/100
    # m = img.shape[0]
    # n = img.shape[1]
    # k = compressRatio*(m*n)/(1 + m + n)
    # k = math.floor(k)
    # kmax = min(m,n)
    # if (k == 0):
    #     k = 1
    # print("compressRatio = ", compressRatio)
    # print("kmax = ", kmax)
    # print("k = ", k)
    # print("ukuran asli = ", m*n)
    # print("ukuran compressed = ", k*(1+m+n))

    # output = np.zeros((3, m, n))
    # print(output[1].shape)
    # print("PROSES COMPRES")



    colorChannel = grayImage
    # PROSES COMPRESSING SVD
    print("proccessing gray")
    u, s, vh = ownSVD(colorChannel)
    # u, s, vh = np.linalg.svd(colorChannel, full_matrices=False)
    print(u.shape)
    print(s.shape)
    print(vh.shape)
    
    # sementara full matrix = false. ini ngaruh ke ukuran dari matriks u sama vh. 
    # akibatnya matriksnya gk 'full' sesuai svd, tapi false dulu soalnya toh bagian matriks yang 'dipotong' gabakal diakses juga
    # kalo mau dibikin true, kita jadi perlu nge modif matriks S lebih jauh. nge debugnya dengan matriks.shape,
    # gagal kalo gk sesuai ketentuan perkalian matriks. 

    # #potong U
    # u = u.T[0:k].T

    # # potong s
    # s = s[0:k]

    # # potong vh
    # vh = vh[0:k]

    # PROSES GABUNGIN LAGI MENJADI SATU MATRIKS
    output = u @ np.diag(s) @ vh
    output = np.absolute(output)
    print("output")
    # print(u)
    # print(s)
    # print(vh)


    imgOut = output
    imgOut = np.round(imgOut)
    print(output)
    # PRINT KE FILE
    status = cv.imwrite('compressed.jpg',imgOut)
    print("status : ", status)


    
# using function
filename='image.jpg'
# algo(filename, 100)



# mencoba membandingkan hasil svd
x = np.random.randint(255, size=(50, 50))
x = np.absolute(x)
x = np.round(x)
# x= cv.imread(filename)

# x = cv.cvtColor(x, cv.COLOR_BGR2GRAY)
print("x")
# print(x)
# print("x @ x.T")
# print(x @ x.T)

# x = np.array([[52,30,49,28],
# [30,50,8,44],
# [49,8,46,16],
# [28,44,16,22]], int)
uown,sown,vhown  = ownSVD(x)

print(np.absolute(np.round(uown@ np.diag(sown)@vhown, decimals=3)))
# w, v = np.linalg.eigh(x.T @ x)
u, s, vh = np.linalg.svd(x, full_matrices=False)

print(np.round(u@ np.diag(s)@vh, decimals=3))
# print(uown.shape)
# print(sown.shape)
# print(vhown.shape)
# print(u.shape)
# print(s.shape)
# print(vh.shape)
print("uown")
print(uown)
print("u")
print(u)
print("sown")
print(np.round(sown, decimals=1))
print("s")
print(np.round(s, decimals=1))
print("vhown")
print(vhown)
print("vh")
print(vh)