﻿from unittest import TestCase
import unittest
from multiprocessing import Process
import time
import pinpointPy


class TestUnderProcessMode(TestCase):

    def tearDown(self):
        pinpointPy.force_flush_trace(4)

    def _test_api_flow(self):
        self.assertTrue(pinpointPy.set_collector(collector_host='unix:/tmp/unexist.sock'))
        # self.assertTrue(pinpointPy.enable_debug(None))

        while True:
            pinpointPy.set_special_key('sid','12345678')
            self.assertEqual(pinpointPy.start_trace(),1)
            pinpointPy.add_clue("key","value3")
            pinpointPy.add_clues("key","value3")
            value = pinpointPy.get_special_key('sid')
            self.assertEqual(value,'12345678')
            self.assertEqual(pinpointPy.end_trace(),0)

    def test_process(self):
        p1 = Process(target=self._test_api_flow)
        p1.start()
        p2 = Process(target=self._test_api_flow)
        p2.start()
        p3 = Process(target=self._test_api_flow)
        p3.start()
        time.sleep(3)
        p1.terminate()
        p2.terminate()
        p3.terminate()
        p1.join()
        p2.join()
        p3.join()

if __name__ == '__main__':
    unittest.main()