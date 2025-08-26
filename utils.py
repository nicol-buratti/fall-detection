import math
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.tree import _tree

WINDOW_SIZE = 20


def preprocess_df(df):
	df['acceleration'] = np.sqrt(
		df['accel_x_list'] ** 2 + df['accel_y_list'] ** 2 + df['accel_z_list'] ** 2
	)
	df['rotationrate'] = np.sqrt(
		df['gyro_x_list'] ** 2 + df['gyro_y_list'] ** 2 + df['gyro_z_list'] ** 2
	)

	df['acceleration'] = df['acceleration'].rolling(window=WINDOW_SIZE).mean()
	df['rotationrate'] = df['rotationrate'].rolling(window=WINDOW_SIZE).mean()

	df['pitch'] = np.atan2(
		-df['accel_x_list'], np.sqrt(df['accel_y_list'] ** 2 + df['accel_z_list'] ** 2)
	) * (180 / np.pi)

	df['gyro_integration'] = df['gyro_y_list'] * (1 / 50)
	alpha = 0.98
	angle_pitch = 0.0
	angles = []
	for gyro_angle_change, p in zip(df['gyro_integration'], df['pitch']):
		angle_pitch = alpha * (angle_pitch + gyro_angle_change) + (1 - alpha) * p
		angles.append(angle_pitch)

	df['angle_pitch'] = angles

	df = df.filter(
		items=[
			'accel_time_list',
			'gyro_time_list',
			'acceleration',
			'rotationrate',
			'angle_pitch',
			'label',
		]
	)
	return df


def get_fall_dataset(dataset):
	falls_path = Path('WEDA-FALL/dataset/fall_timestamps.csv')
	falls_df = pd.read_csv(falls_path)

	p_accel = (f for f in dataset.glob('F*/*_accel.csv') if 'vertical' not in f.name)
	p_gyro = dataset.glob('F*/*_gyro.csv')

	df_list = []
	for acc, gyro in zip(p_accel, p_gyro):
		df1 = pd.read_csv(acc)
		df2 = pd.read_csv(gyro)
		df = pd.concat([df1, df2], axis=1)

		split = acc.stem.split('_')
		filename = str(acc.parent.name + '/' + split[0] + '_' + split[1])
		falls_df[falls_df['filename'] == filename]
		_, start, end = falls_df[falls_df['filename'] == filename].iloc[0]

		df['label'] = np.where(
			(df['accel_time_list'] > start)
			& (df['accel_time_list'] < end)
			& (df['gyro_time_list'] > start)
			& (df['gyro_time_list'] < end),
			'fall',
			'ADL',
		)

		df = preprocess_df(df).dropna()
		df_list.append(df)
	df = pd.concat(df_list)

	return df


def tree_to_rules(clf, feature_names):
	tree_ = clf.tree_
	feature_name = [
		feature_names[i] if i != _tree.TREE_UNDEFINED else 'undefined!' for i in tree_.feature
	]
	c_features = defaultdict(list)

	# The tuple is min, max
	d = defaultdict(lambda: (float('-inf'), float('inf')))

	def recurse(node, d):
		if tree_.feature[node] != _tree.TREE_UNDEFINED:
			name = feature_name[node]
			threshold = tree_.threshold[node]
			threshold = float(threshold)

			d_copy = d.copy()

			# Left child
			# The new upper bound for the feature is the threshold
			d[name] = (d_copy[name][0], threshold)
			recurse(tree_.children_left[node], d)

			# Right child
			# The new lower bound for the feature is the threshold
			d[name] = (threshold, d_copy[name][1])
			recurse(tree_.children_right[node], d)
		else:
			# Leaf node
			value = tree_.value[node]
			class_id = value.argmax()
			class_name = clf.classes_[class_id]
			c_features[class_name].append(d.copy())

	recurse(0, d)
	return c_features


def format_rules(class_rules):
	rule_strings = []
	for rule in class_rules:
		conditions = []
		for feature, (min_val, max_val) in rule.items():
			# Check for lower bound condition
			if min_val > -math.inf:
				conditions.append(f'{feature} > {min_val:.2f}')

			# Check for upper bound condition
			if max_val < math.inf:
				conditions.append(f'{feature} <= {max_val:.2f}')

		# Join all conditions for a single rule with " and "
		if conditions:
			rule_strings.append(' and '.join(conditions))
	return rule_strings


def print_rules(c_features):
	for class_id, rules in c_features.items():
		print(f'Rules for class {class_id}:')
		formatted = format_rules(rules)
		for rule_string in formatted:
			print(f'  - {rule_string}')
		print()
