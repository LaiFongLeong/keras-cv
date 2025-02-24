# Copyright 2022 Waymo LLC.
#
# Licensed under the terms in https://github.com/keras-team/keras-cv/blob/master/keras_cv/layers/preprocessing_3d/waymo/LICENSE  # noqa: E501

import numpy as np
import pytest

from keras_cv.backend.config import keras_3
from keras_cv.layers.preprocessing_3d import base_augmentation_layer_3d
from keras_cv.layers.preprocessing_3d.waymo.global_random_flip import (
    GlobalRandomFlip,
)
from keras_cv.tests.test_case import TestCase

POINT_CLOUDS = base_augmentation_layer_3d.POINT_CLOUDS
BOUNDING_BOXES = base_augmentation_layer_3d.BOUNDING_BOXES


@pytest.mark.skipif(keras_3(), reason="Not implemented in Keras 3")
class GlobalRandomFlipTest(TestCase):
    def test_augment_random_point_clouds_and_bounding_boxes(self):
        add_layer = GlobalRandomFlip()
        point_clouds = np.random.random(size=(2, 50, 10)).astype("float32")
        bounding_boxes = np.random.random(size=(2, 10, 7)).astype("float32")
        inputs = {POINT_CLOUDS: point_clouds, BOUNDING_BOXES: bounding_boxes}
        outputs = add_layer(inputs)
        self.assertNotAllClose(inputs, outputs)

    def test_augment_specific_random_point_clouds_and_bounding_boxes(self):
        add_layer = GlobalRandomFlip()
        point_clouds = np.array(
            [[[1, 1, 2, 3, 4, 5, 6, 7, 8, 9]] * 2] * 2
        ).astype("float32")
        bounding_boxes = np.array([[[1, 1, 2, 3, 4, 5, 1]] * 2] * 2).astype(
            "float32"
        )

        inputs = {POINT_CLOUDS: point_clouds, BOUNDING_BOXES: bounding_boxes}
        outputs = add_layer(inputs)
        flipped_point_clouds = np.array(
            [[[1, -1, 2, 3, 4, 5, 6, 7, 8, 9]] * 2] * 2
        ).astype("float32")
        flipped_bounding_boxes = np.array(
            [[[1, -1, 2, 3, 4, 5, -1]] * 2] * 2
        ).astype("float32")
        self.assertAllClose(outputs[POINT_CLOUDS], flipped_point_clouds)
        self.assertAllClose(outputs[BOUNDING_BOXES], flipped_bounding_boxes)

    def test_augment_batch_point_clouds_and_bounding_boxes(self):
        add_layer = GlobalRandomFlip()
        point_clouds = np.random.random(size=(3, 2, 50, 10)).astype("float32")
        bounding_boxes = np.random.random(size=(3, 2, 10, 7)).astype("float32")
        inputs = {POINT_CLOUDS: point_clouds, BOUNDING_BOXES: bounding_boxes}
        outputs = add_layer(inputs)
        self.assertNotAllClose(inputs, outputs)

    def test_noop_raises_error(self):
        with self.assertRaisesRegexp(
            ValueError, "must flip over at least 1 axis"
        ):
            _ = GlobalRandomFlip(flip_x=False, flip_y=False, flip_z=False)

    def test_flip_x_or_z_raises_error(self):
        with self.assertRaisesRegexp(
            ValueError, "only supports flipping over the Y"
        ):
            _ = GlobalRandomFlip(flip_x=True, flip_y=False, flip_z=False)

        with self.assertRaisesRegexp(
            ValueError, "only supports flipping over the Y"
        ):
            _ = GlobalRandomFlip(flip_x=False, flip_y=False, flip_z=True)
