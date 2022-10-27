import pandas as pd
import json
import os

### 폴더 구조
# .py는 성추행 / 의료상황 디렉토리와 같은 레벨
# 성추행 / 의료상황 하위 디렉토리로 가공 필요한 데이터가 담겨있는 디렉토리

def merge_excel(excel_file, dir_path, data_path, merge_path):
    # 추가할 엑셀 파일 불러오기
    df = pd.read_excel(excel_file)

    # 영상별 디렉토리 폴더 접근
    for dir in os.listdir(dir_path + data_path):
        input_path = f'{dir_path + data_path + dir}/'

        # output/ 폴더 생성
        if not os.path.exists(f'{dir_path + merge_path}'):
            os.mkdir(f'{dir_path + merge_path}')
        # 영상 이름을 폴더명으로 output/ 하위 디렉토리 생성
        if not os.path.exists(f'{dir_path + merge_path + dir}'):
            os.mkdir(f'{dir_path + merge_path + dir}')

        # JSON 파일 접근
        for file in os.listdir(input_path):
            with open(input_path + file, 'r', encoding='UTF-8') as f:
                data = json.load(f)
            # JSON 파일 내 video key 접근
            dataV = data['video']

            # JSON 파일마다 동영상 정보 추가
            for i in range(len(df.values)):
                if df.values[i][0] == dataV['file_name']:
                    # columns 총 22개
                    for j in range(1, len(df.columns)):
                        dataV[f'{df.columns[j]}'] = df.values[i][j]
                    # update
                    data['video'] = dataV

            output_path = f'{dir_path + merge_path + dir}/{file}'
            with open(output_path, 'w', encoding='UTF-8') as f:
                json.dump(data, f, indent='\t', ensure_ascii=False)


def main():
    excel_file = '의료사항/의료사항_추가레이블.xlsx'
    dir_path = '의료사항/'
    # 가공할 데이터가 담겨있는 디렉토리
    data_path = 'files/'
    # output 파일이 저장될 디렉토리 (없으면 코드에서 생성)
    merge_path = 'merged/'
    merge_excel(excel_file, dir_path, data_path, merge_path)

if __name__ == '__main__':
    main()