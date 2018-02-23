import random
import numpy as np
import cv2 as cv2
import os

class DatasetUtil():
    
    def fetch_image_and_label(self, batch_size, time_stamp, frame_range):
        label = []
        file_in = open('data/train.txt', 'r')
        for line in file_in.readlines():
            label.append(float(line))

        x = np.zeros((batch_size, time_stamp, 160, 420, 3)) # (160, 420) (480, 640) 
        y = np.zeros((batch_size, time_stamp - 1))
        for i in range(batch_size):
            # For each batch
            start_frame = random.randint(0,frame_range)
            for j in range(time_stamp):
                index = start_frame + j
                bgr_img = cv2.imread("img/frame" + str(index) + ".jpg")
                
                b,g,r = cv2.split(bgr_img)
                rgb_img = cv2.merge([r,g,b])
                
                x[i,j] = rgb_img[190:350, 100:520, :]
                if j != 0:
                    y[i,j - 1] = label[index]

        x = x.transpose(0, 4, 1, 2, 3) # (batch_size, 3, time_stamp, 480, 640)
        return x, y
    
    def fetch_to_predict_input(self, batch_size, time_stamp, image_num_per_time_stamp, second_range):
        x = np.zeros((batch_size, time_stamp * image_num_per_time_stamp, 160, 420, 3)) # (160, 420) (480, 640) 
        offset_index_map = {} #Key is 0,1,2...59, Value is 1233,1234,1235...1380
        for i in range(batch_size):
            # For each batch
            start_second = random.randint(0,second_range)
            batch_offset = 20 * start_second
            for j in range(time_stamp):
                time_stamp_offset = 20 * j
                arr = sorted(random.sample(range(0, 20), image_num_per_time_stamp))
                for k in range(image_num_per_time_stamp):
                    index = batch_offset + time_stamp_offset + arr[k]
                    bgr_img = cv2.imread("img_test/frame" + str(index) + ".jpg")

                    b,g,r = cv2.split(bgr_img)       # get b,g,r
                    rgb_img = cv2.merge([r,g,b])     # switch it to rgb

                    x[i,j * image_num_per_time_stamp + k] = rgb_img[190:350, 100:520, :] # crop
                    offset_index_map[j * image_num_per_time_stamp + k] = index

        x = x.transpose(0, 4, 1, 2, 3) # (batch_size, 3, time_stamp, 480, 640)
        return x, offset_index_map
