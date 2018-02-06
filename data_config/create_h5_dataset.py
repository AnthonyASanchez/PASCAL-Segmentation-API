import numpy as np
import matplotlib.image as mpimg
import h5py
from PIL import Image
import os

#DATASETS
background = [0.           ,0.          ,0.       ] # 0,
aeroplane = [ 0.50196081  ,0.          ,0.        ] # 1
bicycle =   [ 0.          ,0.50196081  ,0.        ] # 2
bird =      [ 0.50196081  ,0.50196081 , 0.        ] # 3
boat =      [ 0.          ,0.         , 0.50196081] # 4
bottle =    [ 0.50196081  ,0.         , 0.50196081] # 5
bus =       [ 0.          ,0.50196081  ,0.50196081] # 6
car =       [ 0.50196081  ,0.50196081  ,0.50196081] # 7
cat =       [ 0.25098041  ,0.          ,0.        ] # 8
chair =     [ 0.75294119  ,0.          ,0.        ] # 9
cow =       [ 0.25098041  ,0.50196081  ,0.        ] # 10
diningtable=[ 0.75294119  ,0.50196081  ,0.        ] # 11
dog =       [ 0.25098041  ,0.          ,0.50196081] # 12
horse =     [ 0.75294119  ,0.          ,0.50196081] # 13
motorbike = [ 0.25098041  ,0.50196081  ,0.50196081] # 14
person =    [ 0.75294119  ,0.50196081  ,0.50196081] # 15
pottedplant=[ 0.          ,0.25098041  ,0.        ] # 16
sheep =     [ 0.50196081  ,0.25098041  ,0.        ] # 17
sofa =      [ 0.          ,0.75294119  ,0.        ] # 18
train =     [ 0.50196081  ,0.75294119  ,0.        ] # 19
tvmoniter = [ 0.          ,0.25098041  ,0.50196081] # 20


def check_category(img, row, col):
    if (pixelMatch(img[row, col], aeroplane)):
        return 1
    elif (pixelMatch(img[row, col], bicycle)):
        return 2
    elif (pixelMatch(img[row, col], bird)):
        return 3
    elif (pixelMatch(img[row, col], boat)):
        return 4
    elif (pixelMatch(img[row, col], bottle)):
        return 5
    elif (pixelMatch(img[row, col], bus)):
        return 6
    elif (pixelMatch(img[row, col], car)):
        return 7
    elif (pixelMatch(img[row, col], cat)):
        return 8
    elif (pixelMatch(img[row, col], chair)):
        return 9
    elif (pixelMatch(img[row, col], cow)):
        return 10
    elif (pixelMatch(img[row, col], diningtable)):
        return 11
    elif (pixelMatch(img[row, col], dog)):
        return 12
    elif (pixelMatch(img[row, col], horse)):
        return 13
    elif (pixelMatch(img[row, col], motorbike)):
        return 14
    elif (pixelMatch(img[row, col], person)):
        return 15
    elif (pixelMatch(img[row, col], pottedplant)):
        return 16
    elif (pixelMatch(img[row, col], sheep)):
        return 17
    elif (pixelMatch(img[row, col], sofa)):
        return 18
    elif (pixelMatch(img[row, col], train)):
        return 19
    elif (pixelMatch(img[row, col], tvmoniter)):
        return 20
    elif (rgbVal == background for rgbVal in img[row, col]):
        return 0
    else:
        return 0

def process_image(image, shape, resize_mode=Image.BILINEAR):
    img = Image.open(image)
    img = img.resize(shape, resize_mode)
    return np.asarray(img, dtype="float32")

def pixelMatch(img, cat):
    for _ in range(len(img)):
        if('%.3f'%img[_] != '%.3f'%cat[_]):
            return False
    return True

def parse_list(list_dir):
    list_file = open(list_dir, 'r')
    lists = []
    for f in list_file:
        lists.append((f + '.png').replace("\n", ""))
    return lists

def build_h5_dataset(list_dir, imgs_dir, output_dir, input_dir, name, shape):
    img_list = parse_list(list_dir)
    dataset = h5py.File(output_dir + name + '.h5', 'w')
    dataset.create_dataset('X', (len(img_list), *shape, 3), dtype='f')
    dataset.create_dataset('Y', (len(img_list), *shape), dtype='f')
    percentage_complete = 0
    for index, image_name in enumerate(img_list):
        if(index % int(len(img_list)/100) == 0):
            print(percentage_complete,"% Complete")
            percentage_complete += 1
        img = mpimg.imread(imgs_dir + name + "/" + image_name)
        for row in range(len(img)):
            for col in range(len(img[row])):
                img[row,col] = check_category(img,row,col)
        npImg = np.array(img)
        npImg = np.squeeze(npImg[:, :, 1].reshape(len(npImg),len(npImg[0]), 1))
        input_image = process_image(input_dir + image_name.replace("png","jpg"), shape)
        dataset['X'][index] = input_image
        dataset['Y'][index] = npImg
    dataset.close()


def main():
    shape = (256,256)

    input_dir = '../VOC2012/JPEGImages/'
    imgs_dir = '../datasets/resized_images/'
    list_dir = '../VOC2012/ImageSets/Segmentation/'
    output_dir = '../datasets/h5_dataset/'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(imgs_dir):
        print("Please resize the images before creating the h5 dataset")
        os.makedirs(imgs_dir)

    data_files = {
        'training': 'train.txt',
        'validation': 'val.txt'
    }
    for name, list_path in data_files.items():
        build_h5_dataset(list_dir + list_path, imgs_dir, output_dir,input_dir, name,shape)


if __name__ == "__main__":
    main()