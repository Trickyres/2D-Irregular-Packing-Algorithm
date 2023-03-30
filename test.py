import shapely
import numpy as np
import pandas as pd

def testimport():
    print("test成功!")
    # print(shapely.__version__)
    a = np.arange(3,8)
    b = np.arange(1,6)
    print('a+b = {}'.format(a+b))
    aa = [1, 2, 3]
    myvar = pd.Series(aa)
    print(myvar[1])
    print("结束")

if __name__ == '__main__':
    # PlacePolygons(getData())
    testimport()