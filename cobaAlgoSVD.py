# untuk uji coba compressing pake python, tanpa web2 an
import cv2 as cv
import numpy as np
import math

filename='src/image.jpg'
img = cv.imread(filename,cv.IMREAD_GRAYSCALE)
print("image di baca..")
# grayImage = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# cv abai in metadata. img langsung jadi array numpy. man easier jdie.
# save image
print("image berhasil di read, calculating svd...")
# print(img)
print("tes")
print(img.shape)
u, s, vh = np.linalg.svd(img, full_matrices=True)
print("baris satu u")
print(u[0][0])
q,r = np.linalg.qr(np.matmul(img.T,img))
print("baris satu q")
print(q[0][0])
print(u.shape, q.shape)
# print(np.allclose(u,q))