#!/usr/bin/env python
# coding: utf-8
# 摄像头实时人脸识别
import os
import dlib          # 人脸处理的库 Dlib
import sys
import numpy as np   # 数据处理的库 numpy
from cv2 import cv2 as cv2           # 图像处理的库 OpenCv
import pandas as pd  # 数据处理的库 Pandas
import Db_school_1

def get(room='一号楼',date='2020-5-4'):
    student = Db_school_1.Student()
    sql = 'select classes from schedule where room=\'%s\' and date=\'%s\''%(room,date)
    student.get(sql)
    classes = student.get_one()['classes']
    
    sql = 'select c_id from schedule where room=\'%s\' and date=\'%s\''%(room,date)
    student.get(sql)
    c_id = student.get_one()['c_id']

    sql = 'select c_name from class where c_id=\'%s\''%c_id
    student.get(sql)
    c_name = student.get_one()['c_name']

    Class = classes.split(',')
    list1 = []
    
    for x in Class:
        sql = 'select * from student where class_id=\'%s\'' %(x)
        student.get(sql)
        list1 = list1 + list(student.get_all())

    list2 = []
    for x in list1:
        list2.append([x['s_id'],x['s_name'],x['face'],x['department'],x['class_id'],c_id,c_name,date,'未签到'])
    return list2

def commit(list1=[['20174595', 'yzm', '[1.1213213,1.2323232]', 'cs', '1703', '0001', '生理健康', '2020-5-4', '未签到']]):
    student = Db_school_1.Student()
    for  x in list1:
        try:
            sql = 'insert into sign_in(s_id,c_id,date,state) values (\'%s\',\'%s\',\'%s\',\'%s\')'%(x[0],x[-4],x[-2],x[-1])
            print(sql)
            student.update(sql)
        
        except Exception:
            print('error')

# 人脸识别模型，提取128D的特征矢量
facerec = dlib.face_recognition_model_v1("./model/dlib_face_recognition_resnet_model_v1.dat")

# 计算两个128D向量间的欧式距离
# compute the e-distance between two 128D features
def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    return dist

#连接数据库，获得学生信息
student_infromation = get()

# 用来存放所有录入人脸特征的数组
# the array to save the features of faces in the database
features_known_arr = []

# 读取已知人脸数据
# print known faces
for i in student_infromation:
    features_someone_arr = i[2].split(',')
    features_someone_arr_float = []
    for num in features_someone_arr:
        features_someone_arr_float.append(float(num))
    features_known_arr.append(features_someone_arr_float)
print("Faces in Database：", len(features_known_arr))

# Dlib 检测器和预测器
# The detector and predictor will be used
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./model/shape_predictor_68_face_landmarks.dat')

# 创建 cv2 摄像头对象
cap = cv2.VideoCapture(0)

# 设置视频参数，propId 设置的视频参数，value 设置的参数值
cap.set(3, 480)

# cap.isOpened() 返回 true/false 检查初始化是否成功
while cap.isOpened():

    flag, img_rd = cap.read()
    kk = cv2.waitKey(1)

    # 取灰度
    img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)

    # 人脸数 faces
    faces = detector(img_gray, 0)

    # 待会要写的字体 font to write later
    font = cv2.FONT_HERSHEY_COMPLEX

    # 存储当前摄像头中捕获到的所有人脸的坐标/名字
    # the list to save the positions and names of current faces captured
    pos_namelist = []
    name_namelist = []

    # 按下 q 键退出
    if kk == ord('q'):
        break
    else:
        # 检测到人脸 when face detected
        if len(faces) != 0:  
            # 获取当前捕获到的图像的所有人脸的特征，存储到 features_cap_arr
            # get the features captured and save into features_cap_arr
            features_cap_arr = []
            for i in range(len(faces)):
                shape = predictor(img_rd, faces[i])
                features_cap_arr.append(facerec.compute_face_descriptor(img_rd, shape))

            # 遍历捕获到的图像中所有的人脸
            # traversal all the faces in the database
            for k in range(len(faces)):
                print("##### camera person", k+1, "#####")
                # 让人名跟随在矩形框的下方
                # 确定人名的位置坐标
                # 先默认所有人不认识，是 unknown
                name_namelist.append("unknown")

                # 每个捕获人脸的名字坐标 the positions of faces captured
                pos_namelist.append(tuple([faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top())/4)]))

                # 对于某张人脸，遍历所有存储的人脸特征
                e_distance_list = []
                for i in range(len(features_known_arr)):
                    # 如果 person_X 数据不为空
                    if str(features_known_arr[i][0]) != '0.0':
                        print("with person", str(i + 1), "the e distance: ", end='')
                        e_distance_tmp = return_euclidean_distance(features_cap_arr[k], features_known_arr[i])
                        print(e_distance_tmp)
                        e_distance_list.append(e_distance_tmp)
                    else:
                        # 空数据 person_X
                        e_distance_list.append(999999999)
                # 找出最接近的一个人脸数据是第几个
                # Find the one with minimum e distance
                similar_person_num = e_distance_list.index(min(e_distance_list))
                print("Minimum e distance with person", int(similar_person_num)+1)
                
                # 计算人脸识别特征与数据集特征的欧氏距离
                # 距离小于0.4则标出为可识别人物
                if min(e_distance_list) < 0.4:
                    # 这里可以修改摄像头中标出的人名
                    # 最接近的人脸
                    name_namelist[k] = student_infromation[similar_person_num][0]
                    student_infromation[similar_person_num][-1] = '已签到'
                            
                else:
                    print("Unknown person")
                
                # 矩形框
                # draw rectangle
                for kk, d in enumerate(faces):
                    # 绘制矩形框
                    cv2.rectangle(img_rd, tuple([d.left(), d.top()]), tuple([d.right(), d.bottom()]), (0, 255, 255), 2)

            # 在人脸框下面写人脸名字
            # write names under rectangle
            for i in range(len(faces)):
                cv2.putText(img_rd, name_namelist[i], pos_namelist[i], font, 0.8, (0, 255, 255), 1, cv2.LINE_AA)

    print("Faces in camera now:", name_namelist, "\n")

    cv2.putText(img_rd, "Face Recognition", (20, 40), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(img_rd, "Visitors: " + str(len(faces)), (20, 100), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

    # 窗口显示 show with opencv
    cv2.imshow("camera", img_rd)

#上传数据库
commit(student_infromation)

# 释放摄像头 release camera
cap.release()

# 删除建立的窗口 delete all the windows
cv2.destroyAllWindows()