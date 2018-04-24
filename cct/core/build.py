from PIL import Image
import numpy as np
import os

def build_voxel_array(directory, size, reverse):
    cct= []
    imagelist = sorted(os.listdir(directory))
    if len(size) == 1:
        size = [size[0], size[0], size[0]]
    z_step = len(imagelist)//size[2]
    n = 0
    z_range = range(size[2]) if not reverse else range(size[2], 0, -1)
    for i in z_range:
        imgfile = imagelist[n]
        image = Image.open(os.path.join(directory, imgfile)).convert('L')
        slice = np.array(image)
        x_step = slice.shape[1]//size[0]
        y_step = slice.shape[0]//size[1]
        slice = slice[::x_step,::y_step]
        cct.append(slice)
        n+=z_step
    cct = np.asarray(cct)
    return cct

def create_cct_file(voxels):
    f = open('file.cct', 'w')
    f.write('{},{},{}'.format(voxels.shape[2], voxels.shape[1], voxels.shape[0]))
    for plane in voxels:
        f.write('\n')
        f.write(','.join(map(str,plane.ravel().tolist())))

def build(directory, size, reverse):
    voxels = build_voxel_array(directory, size, reverse)
    create_cct_file(voxels)
    return True




