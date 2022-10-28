import os
import json


def restructure_json(src_path, dst_path):
    vid_list = [file for file in os.listdir(src_path) if file.endswith('.mp4')]

    # 영상 디렉토리 접근
    for dir in vid_list:
        file_src_path = f'{src_path + dir}/'
        if not os.path.exists(f'{dst_path + dir}/'):
            os.mkdir(f'{dst_path + dir}/')        

        # json 파일 접근
        json_list = [file for file in os.listdir(file_src_path) if file.endswith('.json')]
        for file in json_list:
            file_dst_path = f'{dst_path + dir}/{file}'
            with open(file_src_path + file, 'r', encoding="UTF-8") as f:
                data = json.load(f)

            # 기존 json의 "images", "annotations" key 접근
            dataI = data['images']
            dataA = data['annotations']

            # "images"의 "labeling_count" 원소 삭제
            del dataI[0]['labeling_count']
            data['images'] = dataI

            # "annotaions"의 iscrowd, category_id, num_keypoints value값 int로 수정 및 id key-value 추가
            for i in range(len(dataA)):
                dataA[i]["iscrowd"] = int(dataA[i]["iscrowd"])
                dataA[i]["category_id"] = int(dataA[i]["category_id"])
                dataA[i]["num_keypoints"] = int(dataA[i]["num_keypoints"])
                if len(dataA) <= 1:
                    dataA[i]["id"] = 1
                else:
                    dataA[i]["id"] = i + 1
                    print(f'{dir}\t{file}\t{len(dataA)}')
            data["annotations"] = dataA

            with open(file_dst_path, 'w', encoding="UTF-8") as f:
                json.dump(data, f, indent='\t', ensure_ascii=False)

            f.close()


def main():
    src_path = 'merged/'
    dst_path = 'annotation/'
    
    if not os.path.exists(dst_path):
        os.mkdir(dst_path)

    restructure_json(src_path, dst_path)

if __name__ == '__main__':
    main()