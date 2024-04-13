import tensorflow as tf
import numpy as np
import cv2
import argparse
import os
import time
from cfg import *


pallete = [
    [0,0,0],
    [0,0,255],
    [127,127,127],
    [255,255,255],
    [255,0,0]
    ]

def applycolor(pred):
    #클래스 이미지에 색 적용
    h,w = pred.shape

    img = np.zeros((h,w,3),dtype = np.uint8)

    for i in range(h):
        for j in range(w):
            img[i,j] = pallete[pred[i,j]]

    return img

def inference(model, img, pred_only = True):
    h, w, _ = img.shape

    processed = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2RGB)
    processed = cv2.resize(processed,(IMAGE_WIDTH, IMAGE_HEIGHT)) # resize
    processed = processed / 255.0 # norm
    processed = np.expand_dims(processed,0) # h, w, c -> 1, h, w, c

    pred = model.predict(processed,verbose=0)
    pred = np.argmax(pred[0], -1) # 1, h, w, 5 -> h, w, 5 -> h, w
    pred_c = applycolor(pred)
    pred_c = cv2.resize(pred_c, (w,h),interpolation=cv2.INTER_LINEAR)
    pred_c = cv2.cvtColor(pred_c, cv2.COLOR_RGB2BGR)
    
    if pred_only:
        return pred_c
    else:
        return cv2.addWeighted(img, 1, pred_c, 0.5,0)
    
def cam(model, cam_num, pred_only=True):
    cap = cv2.VideoCapture(cam_num)

    cnt = 0
    t = 0.0
    if cap.isOpened():
        while True:
            ret, img = cap.read()
            start_time = time.time()
            result = inference(model, img, pred_only)
            t = t + time.time()-start_time
            cnt += 1

            if ret:
                cv2.imshow("camera",result)
                if cv2.waitKey(1) != -1:
                    break
            else:
                print("no fram")
                break
    else:
        print("can't open camera")
    print(f"평균 FPS:{cnt/t}")


if __name__ == "main":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoints", type="str", default="")
    parser.add_argument("--image", type="str", default="", help="If you want to use cam, Input your cam number")
    parser.add_argument("--pred_only", action="store_true", help="If you set this true, Inference return only Colored Prediction, else blended prediction")
    args = parser.parse_args()
    model = tf.keras.models.load_model(args.checkpoints)

    if os.path.exists(args.image):
        print(f"{args.image}가 존재하므로 추론 결과를 출력합니다.")
        img = cv2.imread(args.image)
        inference(model,img,args.pred_only)
    else : 
        print(f"카메라 {args.image}로 추론을 시작합니다.")
        cam(model, args.image, args.pred_only)

