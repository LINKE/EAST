import os
import glob
from PIL import Image, ImageDraw
# ground truth directory
# gt_text_dir = r"D:\tf_mode\wordtag\icdar_result"
gt_text_dir = r"D:\Develop\AI\data\wordtag\train"

# original images directory
# image_dir = r"D:\tf_mode\wordtag\train\JPEGImages/*.jpg"
image_dir = r"D:\Develop\AI\data\wordtag\train/*.jpg"
imgDirs = []
imgLists = glob.glob(image_dir)

# where to save the images with ground truth boxes
# imgs_save_dir = r"D:\tf_mode\wordtag\icdar_images_result"
imgs_save_dir = r"D:\Develop\AI\data\wordtag\result"

for item in imgLists:
    imgDirs.append(item)

for img_dir in imgDirs:
    img = Image.open(img_dir)
    dr = ImageDraw.Draw(img)

    img_basename = os.path.basename(img_dir)
    (img_name, temp2) = os.path.splitext(img_basename)
    # open the ground truth text file
    # img_gt_text_name = "gt_" + img_name + ".txt"
    img_gt_text_name = img_name + ".txt"
    print(img_gt_text_name)
    bf = open(os.path.join(gt_text_dir, img_gt_text_name), 'r', encoding='UTF-8').read().splitlines()
    # bf = open(os.path.join(gt_text_dir, img_gt_text_name), 'r').read().splitlines()
    for line in bf:
        line = line.split(',')
        label = line[-1]
        # strip BOM. \ufeff for python3,  \xef\xbb\bf for python2
        line = [i.strip('\ufeff').strip('\xef\xbb\xbf') for i in line]
        x1, y1, x2, y2, x3, y3, x4, y4 = list(map(float, line[:8]))
        dr.polygon((x1, y1, x2, y2, x3, y3, x4, y4), outline="red")

    img.save(os.path.join(imgs_save_dir, img_basename))
