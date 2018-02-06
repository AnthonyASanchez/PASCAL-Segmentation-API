 # PASCAL-Segmentation-API
This API is meant can be used for configuring the data for PASCAL VOC 2012 Segmentation challenge. The "VOC2012" folder from the PASCAL Voc dataset needs to be placed in the directory of the repo. Run parse_images.py then create_h5_dataset.py and after completion the data will be ready to use.

Dependencies:
- matplotlib
- h5py
- PIL
- os

The final input will be in a h5 format (# of images, 256, 256, 3). The annotations will be (# of images, 256, 256). In the annotations each number will be the corresponding class up to 20. i.e airplane - 1, background - 0.
