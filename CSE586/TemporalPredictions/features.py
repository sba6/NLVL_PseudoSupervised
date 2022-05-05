import os
import csv
import numpy as np

def main():
    dir = "./npy_mean_100/"
    columns = ['f'+str(x) for x in range(1024)]
    print(columns)
    cnt = 0
    for npy_file in os.listdir(dir):
        cnt+=1
        print(cnt)
        #print(npy_file)
        arr = np.load(dir + npy_file, allow_pickle=True).reshape(-1, 1024)
        print(len(arr))
        arr = arr[:100,:]
        if len(arr)<100:
            arr = np.resize(arr, (100,1024))
        print(arr.shape)
        #print(arr.shape)
        csv_file_path = "./csv_mean_100/" + npy_file[:-3] + "csv"
        print(csv_file_path)
        with open(csv_file_path,'w',newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(columns)
            for row in arr:
                writer.writerow(row)

if __name__ == '__main__':
    main()