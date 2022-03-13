"""""
        This script includes several functions used during the keys generation process by the gvt

        Author: Guillaume A. Khayat
        Date: 2022/02/19
"""""
def jsonSecAll(secV):
    return(
        {
            "secKeyV": secV[0],
            "nonceECptV": secV[1],
            "nonceRightV": secV[2],
            "sigL": secV[3],
        }
    )
