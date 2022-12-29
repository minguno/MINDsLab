from zipfile import ZipFile
import argparse
import os

'''
python zip_contents.py -p {파일명}.zip

OR

python zip_contents.py --file_path {파일명}.zip
'''

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--file_path", nargs= '?', help='file path',type=str, required=True)
args = parser.parse_args()

file = args.file_path

with ZipFile(file,'r',) as f:
    files = f.namelist()
    result = []
    for i in files:
        path, ext = os.path.splitext(i)
        if not ext == '':
            result.append(ext)

    new_result = list(set(result))
    for i in new_result:
        print(i, ':', result.count(i))