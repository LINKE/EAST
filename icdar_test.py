# coding:utf-8
import glob
import csv
import cv2
import time
import os
import numpy as np
import scipy.optimize


def load_annoataion(p):
    '''
    load annotation from the text file
    :param p:
    :return:
    '''
    text_polys = []
    text_tags = []
    if not os.path.exists(p):
        return np.array(text_polys, dtype=np.float32)
    bf = open(p, 'r', encoding='UTF-8').read().splitlines()
    for line in bf:
        line = line.split(',')
        label = line[-1]
        # strip BOM. \ufeff for python3,  \xef\xbb\bf for python2
        line = [i.strip('\ufeff').strip('\xef\xbb\xbf') for i in line]
        print(label)
        x1, y1, x2, y2, x3, y3, x4, y4 = list(map(float, line[:8]))
        text_polys.append([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
        if label == '*' or label == '###':
            text_tags.append(True)
        else:
            text_tags.append(False)
    return np.array(text_polys, dtype=np.float32), np.array(text_tags, dtype=np.bool)


if __name__ == '__main__':
    str = u"痒痒"
    print(str)
    load_annoataion(r'D:\tf_mode\wordtag\icdar_train\labels/gt_IMG_20170608_102831.txt')
