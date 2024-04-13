import os
import cv2
import json
import numpy as np
import tqdm

import argparse
'''
class
0 : 검은색 연기
1 : 회색 연기
2 : 하얀 연기
3 : 화재
'''
def process(data_path):
    
    data_dir_images = os.path.join(data_path, 'images')
    data_dir_masks = os.path.join(data_path, 'masks')

    if os.path.exists(data_dir_masks)== False:
        os.makedirs(data_dir_masks)

    with open(data_path+'/labels.json') as f:
        data = json.load(f)

    success = 0
    failed = []

    it = tqdm.tqdm(range(len(data['annotations'])))
    for i in it:
        filename = data['annotations'][i]['file_name']
        if os.path.exists(os.path.join(data_dir_images, filename)):
            img = cv2.imread(os.path.join(data_dir_images, filename))

            h, w, _ = img.shape

            mask = np.zeros((h, w), dtype= np.uint8)

            #클래스별 도형 만들어주기
            for j in range(len(data['annotations'][i]['objects'])):
                poly = np.array(data['annotations'][i]['objects'][j]['polygon'],dtype=np.int32)
                mask = cv2.fillPoly(mask, [poly], color = data['annotations'][i]['objects'][j]['class'])

            #파일의 정보표시 후 저장 (성공 개수/실행 횟수/총 개수) jpg로 저장시 이미지에 변화가 생김 ex) 0,0,255 -> 24,24,255
            it.set_description(f'저장 중:{i}.png-{mask.shape}-({success}/{i}/'+str(len(data['annotations']))+')')
            cv2.imwrite(os.path.join(data_dir_masks, str(i)+'.png'), mask)

            success += 1
        else :
            failed.append(failed)

    if len(failed):
        print(f'{len(failed)}개의 마스크를 만드는데 실패하였습니다.')
        print(failed)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type="str", default="./data/")
    
    args = parser.parse_args()

    process(args.data_path)