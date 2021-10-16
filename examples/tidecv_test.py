import urllib.request # For downloading the sample Mask R-CNN annotations
from tidecv import TIDE
import json
# Import the datasets we want to use
import tidecv.datasets as datasets
import os

bbox_file = 'infer_val2017_10_5e-2.json'
gt_file = 'instances_val2017.json'

with open(bbox_file) as f:
    ann = json.load(f)
# print(f'Ori the numbers of annotations {}',len(ann))

# urllib.request.urlretrieve('https://dl.fbaipublicfiles.com/detectron/35861795/12_2017_baselines/e2e_mask_rcnn_R-101-FPN_1x.yaml.02_31_37.KqyEK4tT/output/test/coco_2014_minival/generalized_rcnn/bbox_coco_2014_minival_results.json', bbox_file)

# print('Results Downloaded!')
gt = datasets.COCO(path=gt_file)
# gt = datasets.COCOResult(gt_file)
bbox_results = datasets.COCOResult(bbox_file)
tide = TIDE(pos_threshold=0.5)

# tide.evaluate_range(gt=gt, preds=bbox_results, mode=TIDE.BOX, outfile='./'+str(bbox_file[:-5])) # Several options are available here, see the functions
tide.evaluate_range(gt=gt, preds=bbox_results, mode=TIDE.BOX) # Several options are available here, see the functions


tide.summarize()
