import os
import torch
import numpy as np

def main():
    ## from numpy to torch file
    dir = "./npy_mean_100/"
    for npy_file in os.listdir(dir):
        #print(npy_file)
        nump = np.load(dir + npy_file, allow_pickle=True).reshape(-1, 1024)
        x_dim = nump.shape[0]
        tensor = torch.from_numpy(np.resize(nump,(x_dim, 2048)))
        print(tensor.shape)
        torch_file_path = "./torch_features/" + npy_file[:-4]
        print(torch_file_path)
        torch.save(tensor, torch_file_path)


if __name__ == '__main__':
    main()