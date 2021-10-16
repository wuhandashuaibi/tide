import os

from collections import defaultdict
import numpy as np
import cv2

from . import functions as f

class Data():
	"""
	A class to hold ground truth or predictions data in an easy to work with format.
	Note that any time they appear, bounding boxes are [x, y, width, height] and masks
	are either a list of polygons or pycocotools RLEs.

	Also, don't mix ground truth with predictions. Keep them in separate data objects.
	
	'max_dets' specifies the maximum number of detections the model is allowed to output for a given image.
	"""

	def __init__(self, name:str, max_dets:int=100):
		self.name     = name
		self.max_dets = max_dets

		self.classes     = {}  # Maps class ID to class name 
		self.annotations = []  # Maps annotation ids to the corresponding annotation / prediction
		
		# Maps an image id to an image name and a list of annotation ids
		self.images      = defaultdict(lambda: {'name': None, 'anns': []})


	def _get_ignored_classes(self, image_id:int) -> set:
		anns = self.get(image_id)

		classes_in_image = set()
		ignored_classes  = set()

		for ann in anns:
			if ann['ignore']:
				if ann['class'] is not None and ann['bbox'] is None and ann['mask'] is None:
					ignored_classes.add(ann['class'])
			else:
				classes_in_image.add(ann['class'])
		
		return ignored_classes.difference(classes_in_image)


	def _make_default_class(self, id:int):
		""" (For internal use) Initializes a class id with a generated name. """

		if id not in self.classes:
			self.classes[id] = 'Class ' + str(id)

	def _make_default_image(self, id:int):
		if self.images[id]['name'] is None:
			self.images[id]['name'] = 'Image ' + str(id)

	def _prepare_box(self, box:object):
		return box

	def _prepare_mask(self, mask:object):
		return mask

	def _add(self, image_id:int, class_id:int, box:object=None, mask:object=None, score:float=1, ignore:bool=False):
		""" Add a data object to this collection. You should use one of the below functions instead. """
		self._make_default_class(class_id)
		self._make_default_image(image_id)
		new_id = len(self.annotations)

		self.annotations.append({
			'_id'   : new_id,
			'score' : score,
			'image_id' : image_id,
			'class' : class_id,
			'bbox'  : self._prepare_box(box),
			'mask'  : self._prepare_mask(mask),
			'ignore': ignore,
		})

		self.images[image_id]['anns'].append(new_id)

	def add_ground_truth(self, image_id:int, class_id:int, box:object=None, mask:object=None):
		""" Add a ground truth. If box or mask is None, this GT will be ignored for that mode. """
		self._add(image_id, class_id, box, mask)

	def add_detection(self, image_id:int, class_id:int, score:int, box:object=None, mask:object=None):
		""" Add a predicted detection. If box or mask is None, this prediction will be ignored for that mode. """
		self._add(image_id, class_id, box, mask, score=score)

	def add_ignore_region(self, image_id:int, class_id:int=None, box:object=None, mask:object=None):
		"""
		Add a region inside of which background detections should be ignored.
		You can use these to mark a region that has deliberately been left unannotated
		(e.g., if is a huge crowd of people and you don't want to annotate every single person in the crowd).

		If class_id is -1, this region will match any class. If the box / mask is None, the region will be the entire image.
		"""
		self._add(image_id, class_id, box, mask, ignore=True)

	def add_class(self, id:int, name:str):
		""" Register a class name to that class ID. """
		self.classes[id] = name
	
	def add_image(self, id:int, name:str):
		""" Register an image name/path with an image ID. """
		self.images[id]['name'] = name


	def get(self, image_id:int):
		""" Collects all the annotations / detections for that particular image. """
		return [self.annotations[x] for x in self.images[image_id]['anns']]

	def cat_name(self, class_id):
		cat_map = {1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
				   7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
				   13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
				   18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
				   24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag', 32: 'tie',
				   33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard', 37: 'sports ball',
				   38: 'kite', 39: 'baseball bat', 40: 'baseball glove', 41: 'skateboard', 42: 'surfboard',
				   43: 'tennis racket', 44: 'bottle', 46: 'wine glass', 47: 'cup', 48: 'fork',
				   49: 'knife', 50: 'spoon', 51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich',
				   55: 'orange', 56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
				   61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed', 67: 'dining table',
				   70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse', 75: 'remote', 76: 'keyboard',
				   77: 'cell phone', 78: 'microwave', 79: 'oven', 80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock', 86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}
		return cat_map[class_id]