# file untuk menyimpan algoritma kompresi dan algortima SVD
import cv2 as cv
import numpy as np
import math
import time

def ownSVD(img):
    min = img.shape[1]
    if img.shape[0] < img.shape[1]:
        min = img.shape[0]

    a = img.T @ img
    kanan = np.zeros((a.shape[0], a.shape[0]), int)
    np.fill_diagonal(kanan, 1)
    # iterasi bisa diatur mau berapa kali, semakin tinggi semakin akurat, 
    # tapi (menurutku) gk noticable kalo tinggi2 banget. kalo 1x keliatan ada yg gk rapi, 5x udah relatif clean.
    # jdi ya dibikin 5x iterasi aja
    for i in range(0,5):
        q,r = np.linalg.qr(a)
        kanan = kanan @ q
        a = r @ q
    tengah = np.absolute(np.diag(a))
    tengah = np.sqrt(tengah)
    kiri = img @ kanan / tengah
    return kiri.T[0:min].T,tengah[0:min], kanan.T[0:min]



def algoKompresi(filename, percentage):
    startTime = time.time()
    img = cv.imread("static/img/base/" + filename)
    log = ""
    log += "image berhasil di read...<br>"

    # MENENTUKKAN K
    compressRatio = percentage/100
    m = img.shape[0]
    n = img.shape[1]
    k = compressRatio*(m*n)/(1 + m + n)
    k = math.floor(k)
    kmax = min(m,n)
    if (k == 0):
        k = 1
    log += ("compressRatio = " + str(compressRatio) + "<br>")
    log += ("kmax = "+ str(kmax) +  "<br>")
    log += ("k = " + str(k) + "<br>")
    log += ("ukuran asli = " + str(m*n) + "<br>")
    log += ("ukuran compressed = " + str(k*(1+m+n)) + "<br>")

    output = np.zeros((3, m, n))
    log += ("spliting image and compressing...<br>")
    for i in range (3):
        channelTime = time.time()
        colorChannel = img[:,:,i].astype(float)
        # PROSES COMPRESSING SVD
        u, s, vh = ownSVD(colorChannel)
    
        #potong U
        u = u.T[0:k].T

        # potong s
        s = s[0:k]

        # potong vh
        vh = vh[0:k]

        # PROSES GABUNGIN LAGI MENJADI SATU MATRIKS
        output[i] = (u @ np.diag(s) @ vh)
        output[i][output[i]>255] = 255
        output[i][output[i]<0] = 0
        log += ("proccessing channel " + str(i+1) + " membutuhkan " + str(time.time() - channelTime) + " detik<br>")

    #combining
    log += ("combining...")
    b = output[0]
    g = output[1]
    r = output[2]
    imgOut = cv.merge((b,g,r))
    # PRINT KE FILE
    outputFilename = filename[:-4] + "_compressed" + filename[-4:]
    log += "hasil kompresi akan disimpan dengan nama " + (outputFilename) + "<br>"

    status = cv.imwrite("static/img/"+outputFilename,imgOut)
    if (status):
        log += ("kompresi gambar berhasil<br>")
    else:
        log += ("komprei gagal<br>")
    log += "total waktu yang dibutuhkan untuk melakukan kompresi adalah " + str(time.time() - startTime) + " detik<br>"
    return log
