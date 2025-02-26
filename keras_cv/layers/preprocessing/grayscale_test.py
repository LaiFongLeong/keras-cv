# Copyright 2022 The KerasCV Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import tensorflow as tf

from keras_cv.layers import preprocessing
from keras_cv.tests.test_case import TestCase


class GrayscaleTest(TestCase):
    def test_return_shapes(self):
        xs = tf.ones((2, 52, 24, 3))

        layer = preprocessing.Grayscale(
            output_channels=1,
        )
        xs1 = layer(xs, training=True)

        layer = preprocessing.Grayscale(
            output_channels=3,
        )
        xs2 = layer(xs, training=True)

        self.assertEqual(xs1.shape, [2, 52, 24, 1])
        self.assertEqual(xs2.shape, [2, 52, 24, 3])

    def test_in_tf_function(self):
        xs = tf.cast(
            tf.stack([2 * tf.ones((10, 10, 3)), tf.ones((10, 10, 3))], axis=0),
            tf.float32,
        )

        # test 1
        layer = preprocessing.Grayscale(
            output_channels=1,
        )

        @tf.function
        def augment(x):
            return layer(x, training=True)

        xs1 = augment(xs)

        # test 2
        layer = preprocessing.Grayscale(
            output_channels=3,
        )

        @tf.function
        def augment(x):
            return layer(x, training=True)

        xs2 = augment(xs)

        self.assertEqual(xs1.shape, [2, 10, 10, 1])
        self.assertEqual(xs2.shape, [2, 10, 10, 3])

    def test_non_square_image(self):
        xs = tf.cast(
            tf.stack([2 * tf.ones((52, 24, 3)), tf.ones((52, 24, 3))], axis=0),
            tf.float32,
        )

        layer = preprocessing.Grayscale(
            output_channels=1,
        )
        xs1 = layer(xs, training=True)

        layer = preprocessing.Grayscale(
            output_channels=3,
        )
        xs2 = layer(xs, training=True)

        self.assertEqual(xs1.shape, [2, 52, 24, 1])
        self.assertEqual(xs2.shape, [2, 52, 24, 3])

    def test_in_single_image(self):
        xs = tf.cast(
            tf.ones((52, 24, 3)),
            dtype=tf.float32,
        )

        layer = preprocessing.Grayscale(
            output_channels=1,
        )
        xs1 = layer(xs, training=True)

        layer = preprocessing.Grayscale(
            output_channels=3,
        )
        xs2 = layer(xs, training=True)

        self.assertEqual(xs1.shape, [52, 24, 1])
        self.assertEqual(xs2.shape, [52, 24, 3])
