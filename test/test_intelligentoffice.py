import unittest
from datetime import datetime
from unittest.mock import patch, Mock, PropertyMock
import mock.GPIO as GPIO
from mock.SDL_DS3231 import SDL_DS3231
from mock.adafruit_veml7700 import VEML7700
from src.intelligentoffice import IntelligentOffice, IntelligentOfficeError


class TestIntelligentOffice(unittest.TestCase):

    @patch.object(GPIO, "input")
    def test_check_quadrant_occupancy_return_True(self, mock_sensor: Mock):
        mock_sensor.return_value = True

        i = IntelligentOffice()

        self.assertTrue(i.check_quadrant_occupancy(i.INFRARED_PIN1))