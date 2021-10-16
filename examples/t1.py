import numpy as np
ann = np.array([1,2,3,4,2,3,2,1])
a_re = np.concatenate((np.repeat(ann[0], -2, axis=0), ann), axis=0)
print(a_re)

# [{'_id': 63550, 'score': 0.9967881441116333, 'image_id': 375493, 'class': 1, 'bbox': [254.6083984375, 29.804187774658203, 112.082275390625, 436.7032470703125], 'mask': None, 'ignore': False}, {'_id': 63550, 'score': 0.9967881441116333, 'image_id': 375493, 'class': 1, 'bbox': [254.6083984375, 29.804187774658203, 112.082275390625, 436.7032470703125], 'mask': None, 'ignore': False}]
