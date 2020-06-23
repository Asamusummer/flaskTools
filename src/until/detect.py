"""
Face detect

Requirements:
  Python 3.6+
"""
import os

import face_recognition
import numpy as np
import cv2

import datetime

CWD = os.getcwd()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class FaceDetect():
    """Find all the faces that appear in a picture
    """

    def __init__(self):
        self.init_dir()

    @staticmethod
    def init_dir():
        """
        访客初始化文件夹，根据当天的时间分日期文件夹存放
        :return:
        """
        # 获取当前的日期
        date = datetime.datetime.now().date()
        path_info = f'{BASE_DIR}/media/visitor/{str(date)}'
        os.mkdir(f"{BASE_DIR}/media/upload") if not os.path.exists(BASE_DIR + '/media/upload') else ''
        os.makedirs(path_info) if not os.path.exists(path_info) else ''

    @staticmethod
    def _read_img(path):
        err = None
        img = cv2.imread(path)
        if img is None:
            err = "Image reading failed, please check the path!"

        return img, err

    def get_location(self, path):
        """Get all the faces in the picture
        """
        img, err = self._read_img(path)
        if err is not None:
            return None, err

        face_locations = face_recognition.face_locations(img)
        if len(face_locations) < 1:
            img_1 = np.rot90(img, -1)
            face_locations = face_recognition.face_locations(img_1)
            if len(face_locations) < 1:
                img_2 = np.rot90(img)
                face_locations = face_recognition.face_locations(img_2)
                if len(face_locations) >= 1:
                    cv2.imwrite(path, img_2)
            else:
                cv2.imwrite(path, img_1)

        return face_locations, None

        # return None, None

    def resize(self, path, size="200*200"):
        """Resize the picture
        """
        img, err = self._read_img(path)
        if err is not None:
            return None, err

        try:
            size = size.split("*")
            w = size[0]
            h = size[1]
        except IndexError:
            err = "Parameter error"

            return None, err

        name = os.path.basename(path)
        resized = cv2.resize(img, (int(w), int(h)), interpolation=cv2.INTER_CUBIC)
        path = f"{CWD}/images/resized/{name}".replace("\\", "/")
        cv2.imwrite(path, resized)

        return path, None

    def get_faces(self, path, width, height):
        """Gets all face paths
        """
        head_pic_name = path.split('/')[3]
        date = datetime.datetime.now().date()


        locations, err = self.get_location(path)
        if err is not None:
            return None, err

        img, err = self._read_img(path)
        if err is not None:
            return None, err

        object_ls = []
        size = 50
        for index, rec_position in enumerate(locations):
            path = f'{BASE_DIR}/media/visitor/{str(date)}'

            pos1 = rec_position[0] - size if rec_position[0] - size > 0 else 0
            pos2 = rec_position[2] + size
            pos3 = rec_position[3] - size if rec_position[3] - size > 0 else 0
            pos4 = rec_position[1] + size

            if (width - pos4) < 10:
                pos4 = width

            if (height - pos2) < 10:
                pos4 = height

            face = img[pos1: pos2, pos3: pos4]

            # 记录图片处理的日志
            # with open(os.path.dirname(BASE_DIR) + '/logs/imgsize.log', 'a+') as f:
            #     f.write(path.split('media')[1])
            #     f.write('\n')
            #     f.write(str((rec_position[0], rec_position[2], rec_position[3], rec_position[1])))
            #     f.write('\n')
            #     f.write(str((pos1, pos2, pos3, pos4)))
            #     f.write('\n')
            #     f.write("*"*60)
            #     f.write('\n')

            if str(face) == '[]':
                continue

            _ = cv2.imwrite(f"{path}/{head_pic_name}", face)
            object_ls.append(f"visitor/{str(date)}/{head_pic_name}")

        return object_ls, None


def preprocess_upload_img(student, img_path):
    """
    根据人员信息，对修改的图片进行预处理
    :return:
    """
    class_path = f'{student.school_code}/{student.grade_code}/{student.class_code}'
    class_img_path = os.path.join(BASE_DIR, f'media/{class_path}').replace('\\', '/')
    os.makedirs(f"{class_img_path}") if not os.path.exists(class_img_path) else ''

    img, err = FaceDetect._read_img(img_path)
    if err is not None:
        return None, err

    face_locations = face_recognition.face_locations(img)

    if len(face_locations) > 1:
        return None, "检测到存在多张人脸，请重新上传！"

    elif len(face_locations) < 1:
        return None, "未检测到人脸，请重新上传！"

    else:
        size = 50
        rec_position = face_locations[0]
        path = f"{class_img_path}/{student.stu_code}.jpg"

        height = img.shape[0]
        width = img.shape[1]

        pos1 = rec_position[0] - size if rec_position[0] - size > 0 else 0
        pos2 = rec_position[2] + size
        pos3 = rec_position[3] - size if rec_position[3] - size > 0 else 0
        pos4 = rec_position[1] + size

        if (width - pos4) < 10:
            pos4 = width

        if (height - pos2) < 10:
            pos4 = height

        # face = img[face_locations[0][0] - 50: face_locations[0][2] + 50,
        #        face_locations[0][3] - 50: face_locations[0][1] + 50]
        face = img[pos1: pos2, pos3: pos4]

        _ = cv2.imwrite(path, face)

    return f'{class_path}/{student.stu_code}.jpg', None
