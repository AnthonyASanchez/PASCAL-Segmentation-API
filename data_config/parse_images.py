from PIL import Image
import os



def resize_img(output_dir,img_dir, img_name, shape):
    image = Image.open(img_dir + img_name)
    image = image.resize(shape, Image.BILINEAR)
    image.save(output_dir + img_name)

def parse_list(list_dir):
    list_file = open(list_dir, 'r')
    lists = []
    for f in list_file:
        lists.append((f + '.png').replace("\n", ""))
    return lists

def convert_images(output_dir,list_dir,img_dir, set_name, shape):
    img_list = parse_list(list_dir)
    percent = 0
    for index, img_name in enumerate(img_list):
        if(index % int(len(img_list)/100) == 0):
            print(percent, "% Complete")
            percent += 1
        resize_img(output_dir + set_name +"/",img_dir, img_name, shape)

def main():

    shape = (256,256)

    output_dir = '../datasets/resized_images/'
    list_dir = '../VOC2012/ImageSets/Segmentation/'
    img_dir = '../VOC2012/SegmentationClass/'




    data_files = {
        'training': 'train.txt',
        'validation': 'val.txt'
    }
    for name, list_path in data_files.items():
        if not os.path.exists(output_dir + name):
            os.makedirs(output_dir + name)
        convert_images(output_dir,list_dir + list_path ,img_dir, name, shape)
if __name__ == "__main__":
    main()