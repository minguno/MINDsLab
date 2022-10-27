import cv2
import os
import numpy as np
from PIL import ImageFont, ImageDraw, Image



def bbox_visualisation(img, path, class_list, obj_list):
    for obj in obj_list:
        # 좌상단 좌표
        x1, y1 = round(obj[1] - obj[3]/2), round(obj[2] - obj[4]/2)
        # 우하단 좌표
        x2, y2 = round(obj[1] + obj[3]/2), round(obj[2] + obj[4]/2)
        img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255))
        # 한글 삽입
        b,g,r,a = 0,255,255,0
        fontpath = "fonts/gulim.ttc"
        font = ImageFont.truetype(fontpath, 12)        
        pil_img = Image.fromarray(img)
        draw = ImageDraw.Draw(pil_img)
        draw.text((x1, y1), class_list[obj[0]], font=font, fill=(b,g,r,a))
        img = np.array(pil_img)   
        # 이미지 저장
        cv2.imwrite(path, img)  


def main():
    # 원본 이미지 디렉토리
    img_path = "img/"
    # YOLO 데이터 디렉토리
    ann_path = "ann/"
    output_path = "img/with_bbox/"
    meta_path = "obj.names"
    noann_path = "img/no_label/"

    if not os.path.exists(output_path):
        os.mkdir(output_path)
    
    # obj.names에서 클래스명 받기
    with open(meta_path, 'r', encoding="UTF-8") as f:
        lines = f.readlines()
        class_list = [line.strip() for line in lines]
    f.close()

    # 이미지파일명 - key, yolo파일명 - value
    img_list = [img for img in os.listdir(img_path) if img.endswith(".jpg")]
    ann_list = [yolo for yolo in os.listdir(ann_path) if yolo.endswith(".txt")]
    img_ann_dict = {}
    for i in range(len(img_list)):
        if img_list[i].strip(".jpg") == ann_list[i].strip(".txt"):
            img_ann_dict[img_list[i]] = ann_list[i]
    
    # 이미지 별로 for문 돌리기
    for img, ann in img_ann_dict.items():
        # 이미지 해상도 구하기
        src = cv2.imread(img_path + img, cv2.IMREAD_UNCHANGED)
        h, w, _ = src.shape
        
        # 이미지에 해당하는 ann 호출
        with open(ann_path + ann, 'r', encoding="UTF-8") as f:
            obj_list = f.readlines()
            obj_list = [obj_list[i].strip() for i in range(len(obj_list))]
        f.close()

        # 레이블링이 없는 이미지의 경우
        if not len(obj_list):
            if not os.path.exists(noann_path):
                os.mkdir(noann_path)
            cv2.imwrite(noann_path + img, src)
            continue

        for i in range(len(obj_list)):
            id, x, y, rw, rh = obj_list[i].split()
            obj_list[i] = [int(id), float(x)*w, float(y)*h, float(rw)*w, float(rh)*h]
        bbox_visualisation(src, output_path + img, class_list, obj_list)
      

if __name__ == "__main__":
    main()