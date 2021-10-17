from typing import Union

<<<<<<< HEAD
import cv2, os
=======
import cv2
>>>>>>> 49a5d2a4aeb56795e93a3ed7cc7e6d25757bb4c1
from .. import functions as f

class Error:
	""" A base class for all error types. """

	def fix(self) -> Union[tuple, None]:
		"""
		Returns a fixed version of the AP data point for this error or
		None if this error should be suppressed.

		Return type is:
			class:int, (score:float, is_positive:bool, info:dict)
		"""
		raise NotImplementedError

	def unfix(self) -> Union[tuple, None]:
		""" Returns the original version of this data point. """

		if hasattr(self, 'pred'):
			# If an ignored instance is an error, it's not in the data point list, so there's no "unfixed" entry
			if self.pred['used'] is None: return None
			else: return self.pred['class'], (self.pred['score'], False, self.pred['info'])
		else:
			return None
	
	def get_id(self) -> int:
		if hasattr(self, 'pred'):
			return self.pred['_id']
		elif hasattr(self, 'gt'):
			return self.gt['_id']
		else:
			return -1
	
	
	def show(self, dataset, out_path:str=None,
<<<<<<< HEAD
		pred_color:tuple=(0, 255, 255), gt_color:tuple=(255, 0, 0),
		font=cv2.FONT_HERSHEY_COMPLEX_SMALL,
			 val2017='/Users/wuhan/tide/examples/val2017/'):
		if not os.path.exists(out_path):
			os.mkdir(out_path)
		pred = self.pred if hasattr(self, 'pred') else self.gt
		# print(pred.keys())
		img_path = os.path.join(val2017,str(pred['image_id']).zfill(12)+'.jpg')
		img = cv2.imread(img_path)
		# print(img.shape)
		if hasattr(self, 'gt'):
			img = cv2.rectangle(img, *f.points(self.gt['bbox']), gt_color, 2)
			img = cv2.putText(img, str(self.gt['class']),
=======
		pred_color:tuple=(43, 12, 183), gt_color:tuple=(43, 183, 12),
		font=cv2.FONT_HERSHEY_SIMPLEX):
		
		pred = self.pred if hasattr(self, 'pred') else self.gt
		img = dataset.get_img_with_anns(pred['image_id'])

		
		if hasattr(self, 'gt'):
			img = cv2.rectangle(img, *f.points(self.gt['bbox']), gt_color, 2)
			img = cv2.putText(img, dataset.cat_name(self.gt['category_id']),
>>>>>>> 49a5d2a4aeb56795e93a3ed7cc7e6d25757bb4c1
				(100, 200), font, 1, gt_color, 2, cv2.LINE_AA, False)
	
		if hasattr(self, 'pred'):
			img = cv2.rectangle(img, *f.points(pred['bbox']), pred_color, 2)
<<<<<<< HEAD
			img = cv2.putText(img, '%s (%.2f)' % (str(pred['class']), pred['score']),
				(100, 100), font, 0.7, pred_color, 2, cv2.LINE_AA, False)
=======
			img = cv2.putText(img, '%s (%.2f)' % (dataset.cat_name(pred['category_id']), pred['score']),
				(100, 100), font, 1, pred_color, 2, cv2.LINE_AA, False)
>>>>>>> 49a5d2a4aeb56795e93a3ed7cc7e6d25757bb4c1

		if out_path is None:
			cv2.imshow(self.short_name, img)
			cv2.moveWindow(self.short_name, 100, 100)

			cv2.waitKey()
			cv2.destroyAllWindows()
		else:
<<<<<<< HEAD
			cv2.imwrite(os.path.join(out_path,str(pred['image_id']).zfill(12)+'.jpg'), img)
			print('img done', os.path.join(out_path,str(pred['image_id']).zfill(12)+'.jpg'))
=======
			cv2.imwrite(out_path, img)
	
>>>>>>> 49a5d2a4aeb56795e93a3ed7cc7e6d25757bb4c1
	def get_info(self, dataset):
		info = {}
		info['type'] = self.short_name

		if hasattr(self, 'gt'):
			info['gt']   = self.gt
		if hasattr(self, 'pred'):
			info['pred'] = self.pred
		
		img_id = (self.pred if hasattr(self, 'pred') else self.gt)['image_id']
		info['all_gt'] = dataset.get(img_id)
		info['img']    = dataset.get_img(img_id)

		return info








class BestGTMatch:
	"""
	Some errors are fixed by changing false positives to true positives.
	The issue with fixing these errors naively is that you might have
	multiple errors attempting to fix the same GT. In that case, we need
	to select which error actually gets fixed, and which others just get
	suppressed (since we can only fix one error per GT).

	To address this, this class finds the prediction with the hiighest
	score and then uses that as the error to fix, while suppressing all
	other errors caused by the same GT.
	"""

	def __init__(self, pred, gt):
		self.pred = pred
		self.gt = gt

		if self.gt['used']:
			self.suppress = True
		else:
			self.suppress = False
			self.gt['usable'] = True

			score = self.pred['score']

			if not 'best_score' in self.gt:
				self.gt['best_score'] = -1

			if self.gt['best_score'] < score:
				self.gt['best_score'] = score
				self.gt['best_id'] = self.pred['_id']
		
	def fix(self):
		if self.suppress or self.gt['best_id'] != self.pred['_id']:
			return None
		else:
			return (self.pred['score'], True, self.pred['info'])
