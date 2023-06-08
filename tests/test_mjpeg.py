from contextlib import AbstractContextManager
from re import L
from unittest import TestCase

import cv2
from mjpegazer.core import MJPEGFrames
import numpy as np
from mjpegazer.utils.constants import HEALTH_THRESHOLD

MOCK_IMAGE = np.random.randint(0, 256, (100, 100), dtype=np.uint8)


class VideoCaptureMock:
    _yields: int

    def __init__(self, *args, **kwargs):
        self._yields = 0

    def read(self):
        return True, MOCK_IMAGE

    def isOpened(self):
        self._yields += 1
        return self._yields < 10


class ContextManager(AbstractContextManager):
    def __init__(self):
        pass

    def __enter__(self) -> VideoCaptureMock:
        return VideoCaptureMock()

    def __exit__(self, *_) -> bool:
        return False


class TestMJPEG(TestCase):
    def setUp(self):
        video_context_manager = ContextManager()
        self.mjpeg = MJPEGFrames(video_context_manager)
        self.mjpeg._failures = 0

    def test_health(self):
        mjpeg_object = self.mjpeg

        self.assertTrue(mjpeg_object.healthy)

        mjpeg_object._failures = HEALTH_THRESHOLD
        self.assertFalse(mjpeg_object.healthy)

        mjpeg_object._failures = 0
        self.assertTrue(mjpeg_object.healthy)

    def test_iterator(self):
        mjpeg_object = self.mjpeg

        mock: np.ndarray[int, np.generic]
        success, mock = cv2.imencode(".jpg", MOCK_IMAGE)
        if not success:
            raise Exception("The test is broken, is cv2 installed?")
        for i in mjpeg_object:
            self.assertIn(mock.tobytes(), i)
