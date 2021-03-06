
import argparse
import sys
import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn

FILE = Path(__file__).absolute()
sys.path.append(FILE.parents[0].as_posix())  # add yolov5/ to path

from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import check_img_size, non_max_suppression, scale_coords
from utils.torch_utils import select_device


def detect(tooth_info, weights='models/step_two.pt',  # model.pt path(s)
        source='tmp',  # file/dir/URL/glob, 0 for webcam
        imgsz=640,  # inference size (pixels)
        conf_thres=0.6,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device=''  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        ):


    # Initialize
    device = select_device(device)

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check image size
    names = model.module.names if hasattr(model, 'module') else model.names  # get class names

    # Dataloader
    dataset = LoadImages(source, img_size=imgsz, stride=stride)
    bs = 1  # batch_size

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    t0 = time.time()
    results = []
    for path, img, im0s, _ in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference

        mulpicplus = "3"     #1 for normal,2 for 4pic plus,3 for 9pic plus and so on
        assert(int(mulpicplus)>=1)
        if mulpicplus == "1":
            pred = model(img, augment=False, visualize=False)[0]

        else:
            xsz = img.shape[2]
            ysz = img.shape[3]
            mulpicplus = int(mulpicplus)
            x_smalloccur = int(xsz / mulpicplus * 1.2)
            y_smalloccur = int(ysz / mulpicplus * 1.2)
            for i in range(mulpicplus):
                x_startpoint = int(i * (xsz / mulpicplus))
                for j in range(mulpicplus):
                    y_startpoint = int(j * (ysz / mulpicplus))
                    x_real = min(x_startpoint + x_smalloccur, xsz)
                    y_real = min(y_startpoint + y_smalloccur, ysz)
                    if (x_real - x_startpoint) % 64 != 0:
                        x_real = x_real - (x_real-x_startpoint) % 64
                    if (y_real - y_startpoint) % 64 != 0:
                        y_real = y_real - (y_real - y_startpoint) % 64
                    dicsrc = img[:, :, x_startpoint:x_real,
                                                    y_startpoint:y_real]
                    pred_temp = model(dicsrc, augment=False, visualize=False)[0]
                    pred_temp[..., 0] = pred_temp[..., 0] + y_startpoint
                    pred_temp[..., 1] = pred_temp[..., 1] + x_startpoint
                    if i==0 and j == 0:
                        pred = pred_temp
                    else:
                        pred = torch.cat([pred, pred_temp], dim=1)


        # Apply NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, None, False, max_det=max_det)

        # Apply Classifier

        im_sub = im0s.copy()
        # Process detections
        for i, det in enumerate(pred):  # detections per image

            p, s, im0, frame = path, '', im0s.copy(), getattr(dataset, 'frame', 0)
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                
                for index, (*xyxy, conf, cls) in enumerate(reversed(det)):


                    c = int(cls)  # integer class
                    label = names[c]
                    tooth_index = int(p.split('.')[0].split('/')[-1])
                    tooth_topleft_x, tooth_topleft_y = tooth_info[tooth_index]['topleft']
                    results.append({'label':label, 'confidence':float(conf), 'topleft':(int(xyxy[0])+tooth_topleft_x, int(xyxy[1])+tooth_topleft_y), 'bottomright':(int(xyxy[2])+tooth_topleft_x, int(xyxy[3])+tooth_topleft_y)})

                    # cv2.imwrite(str(save_dir / p.name).split(".")[0] + "_" + str(index) + ".jpg", im_sub[ int(xyxy[1]):int(xyxy[3]),int(xyxy[0]):int(xyxy[2])])
    return results


# tooth_info = [{'topleft': (1997, 1855), 'bottomright': (2097, 1982)}, {'topleft': (2279, 1742), 'bottomright': (2383, 1835)}, {'topleft': (1439, 1766), 'bottomright': (1603, 1888)}, {'topleft': (2134, 1722), 'bottomright': (2199, 1809)}, {'topleft': (2134, 1723), 'bottomright': (2302, 1813)}, {'topleft': (1391, 1836), 'bottomright': (1476, 1956)}, {'topleft': (1930, 1831), 'bottomright': (2100, 1977)}, {'topleft': (1482, 1877), 'bottomright': (1562, 1963)}, {'topleft': (1350, 1731), 'bottomright': (1438, 1852)}, {'topleft': (1230, 1675), 'bottomright': (1367, 1846)}, {'topleft': (2096, 1804), 'bottomright': (2198, 1940)}, {'topleft': (1800, 1831), 'bottomright': (1930, 1981)}, {'topleft': (1682, 1847), 'bottomright': (1792, 1964)}, {'topleft': (1332, 1840), 'bottomright': (1397, 1925)}, {'topleft': (1809, 1741), 'bottomright': (1958, 1868)}, {'topleft': (1564, 1851), 'bottomright': (1673, 1963)}, {'topleft': (2094, 1788), 'bottomright': (2313, 1942)}, {'topleft': (1998, 1728), 'bottomright': (2147, 1874)}, {'topleft': (1610, 1766), 'bottomright': (1780, 1870)}]
# results = detect(tooth_info, weights='models/step_two.pt',source='tmp', imgsz=640, conf_thres=0.6, iou_thres=0.5, max_det=100)
# print(results)

