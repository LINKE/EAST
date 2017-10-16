# -*- coding:utf-8 -*-
"""
将voc格式的标注转换为icdar2015格式
"""
import os
import sys
import random

import numpy as np
import tensorflow as tf

import xml.etree.ElementTree as ET

import math

DIRECTORY_ANNOTATIONS = '' #'Annotations/'
DIRECTORY_IMAGES = '' # 'JPEGImages/'


def _process_image(directory, name):
    """解析并读取标签文件获得标签和对象的坐标.

    Args:
      directory: 原标签所在目录.
      name: 标签文件的名称.
    Returns:
      bboxes: 坐标.
      labels_text: 标签.
    """
    # Read the XML annotation file.
    filename = os.path.join(directory, DIRECTORY_ANNOTATIONS, name + '.xml')
    tree = ET.parse(filename)
    root = tree.getroot()
    # Find annotations.
    bboxes = []
    labels_text = []
    for obj in root.findall('object'):
        label = obj.find('name').text
        labels_text.append(label)
        bbox = obj.find('bndbox')
        bboxes.append((bbox.find('xmin').text,
                       bbox.find('ymin').text,
                       bbox.find('xmax').text,
                       bbox.find('ymax').text))
    return bboxes, labels_text


def _add_to_txt(dataset_dir, name, out_filename):
    """将标签写入到txt文件.

    Args:
      dataset_dir: Dataset directory;
      name: label file name to add to the txt;
      out_filename: The txt writer to use for writing.
    """
    bboxes, labels_text = _process_image(dataset_dir, name)
    output = open(out_filename, 'w', encoding='UTF-8')
    for i in range(len(labels_text)):
        bbox = bboxes[i]  # 格式为xmin,ymin,xmax,ymax
        # 格式转换为 x1,y1,x2,y2,x3,y3,x4,y4,label
        xmin, ymin, xmax, ymax = bbox
        x1 = xmin
        y1 = ymin
        x2 = xmax
        y2 = ymin
        x3 = xmax
        y3 = ymax
        x4 = xmin
        y4 = ymax
        label = labels_text[i]
        output.write('{},{},{},{},{},{},{},{},{}'.format(x1, y1, x2, y2, x3, y3, x4, y4, label))
        output.write("\n")
    output.close()


def _get_output_filename(output_dir, name):
    # out_file = os.path.join(output_dir, 'gt_{}.txt'.format(name))
    out_file = os.path.join(output_dir, '{}.txt'.format(name))
    return out_file


def run(dataset_dir, output_dir, shuffling=False):
    """Runs the conversion operation.

    Args:
      dataset_dir: The dataset directory where the dataset is stored.
      output_dir: Output directory.
    """

    # Dataset filenames, and shuffling.
    path = os.path.join(dataset_dir, DIRECTORY_ANNOTATIONS)
    if not tf.gfile.Exists(path):
        raise Exception("{} does not exist".format(path))

    filenames = sorted(os.listdir(path))
    if shuffling:
        random.seed(12345)
        random.shuffle(filenames)

    for filename in filenames:
        filename = filename[:-4]
        out_file = _get_output_filename(output_dir, filename)
        _add_to_txt(dataset_dir, filename, out_file)
    print('\nFinished converting the icdar dataset!')


if __name__ == "__main__":
    dataset_dir = r"D:\Develop\AI\data\wordtag\train"
    output_dir = r"D:\Develop\AI\data\wordtag\train"
    run(dataset_dir, output_dir, shuffling=True)
    #     dataset_dir = "../../data/voc/2012_train/VOCdevkit/VOC2012/"
    #     output_dir = "../../data/voc/tfrecords/"
    #     name='voc_train_2012'

#     dataset_dir = r"D:\tf_mode\wordtag\evl/"
#     output_dir = r"D:\tf_mode\wordtag\result/"
#     name = 'voc_test_2007'
#     run(dataset_dir, output_dir, name=name, shuffling=False)
