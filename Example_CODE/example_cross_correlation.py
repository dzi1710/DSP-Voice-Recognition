#Khai bao thu vien
import numpy as np               #Thu vien chuyen dung de tinh toan va khai bao mang 
import matplotlib.pyplot as plt  #Thu vien chuyen dung de ve do thi trong python 
  
#Khai bao cac tin hieu dau vao
x = np.array([0, 1, 3, 1, 0])    #Khai bao tin hieu dau vao
y = np.array([0, 1, 3, 1, 0])    #Khai bao tin hieu dau vao

#Nhiem vu la ta se so sanh tuong quan cheo cross-correlation 2 tin hieu dau vao va dau ra de xem lieu giong nhat o dau
#Dung ham correlate trong thu vien numpy de so tuong quanh x va y => He so tuong quan r_xy 
r_xy = np.correlate(x, y, mode ='full')
#Mode full de python tinh day du tu khoang cach moi cham nhau va phan tu cuoi cung cua ca 2 tin hieu

#Tiep theo voi mang goc x(n) va mang truot y(n), ta co
#       x(n) =                  0   1   3   1*   0
#       y(n) =                            0   1*   3  1   0           => Vi tri   n = 0
#                                        0   1   3    1  0                           n = -1
#                                   0   1   3   1    0                              n = -2
#                              0   1   3   1   0                                   n = -3
#                         0   1   3   1   0                                       n = -4      => Tu n = -4 
#                   0   1   3   1   0                                           n = -5      r_xy = 0
#              0   1   3   1   0                                               n = -6      r_xy = 0

#Ta se chua mang chieu lai length tu -4 -> len(x) + len(y) - 1
#length_lags = len(x) + len(y) - 1
lags = np.arange(-4, 5)          #Khai bao mang do tre l khi truot y(n)
#-4, 5 la tu n = -4 truot den khi n = 5 - 1 vi ta tinh toan o tren xac dinh duoc chieu dai mang se la tu n = -4 ma vi python mac dinh bat dau tu 0 nen ta tru 4

#Khi truot y(n) nhu vay r_xy se ghi nhan cac tin hieu khac nhau qua moi lan truot, va ta can biet o dau la lon nhat chinh cho do la tuong quan cao nhat
max_r_xy = np.max(r_xy)
max_lags = lags[np.argmax(r_xy)]
#max_lags se cho ta biet vi tri cua chi so tuong quan cao nhat nam o dau trong mang de de xac dinh vi tri cua no hon


#TRUC QUAN HOA
plt.stem(lags, r_xy, basefmt='k-')
plt.xlabel('l')
plt.ylabel('r_xy')
plt.show()
