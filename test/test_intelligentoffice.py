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

    @patch.object(GPIO, "input")
    def test_check_quadrant_occupancy_should_raise_error(self, mock_sensor: Mock):
        mock_sensor.return_value = True

        i = IntelligentOffice()

        self.assertRaises(IntelligentOfficeError, i.check_quadrant_occupancy, i.LED_PIN)

    @patch.object(SDL_DS3231, "read_datetime")
    @patch.object(GPIO, "output")
    def test_manage_blinds_based_on_time_blinds_fully_opened(self, mock_blinds: Mock, mock_datetime: Mock):
        mock_datetime.return_value = datetime(2024, 11, 27, 8, 00, 00)
        i = IntelligentOffice()
        i.manage_blinds_based_on_time()

        mock_blinds.assert_called_once_with(i.SERVO_PIN, GPIO.HIGH)

    @patch.object(SDL_DS3231, "read_datetime")
    @patch.object(GPIO, "output")
    def test_manage_blinds_based_on_time_blinds_fully_closed(self, mock_blinds: Mock, mock_datetime: Mock):
        mock_datetime.return_value = datetime(2024, 11, 27, 20, 00, 00)
        i = IntelligentOffice()
        i.manage_blinds_based_on_time()

        mock_blinds.assert_called_once_with(i.SERVO_PIN, GPIO.LOW)

    @patch.object(SDL_DS3231, "read_datetime")
    @patch.object(GPIO, "output")
    def test_manage_blinds_based_on_time_blinds_do_nothing_on_weekend(self, mock_blinds: Mock, mock_datetime: Mock):
        mock_datetime.return_value = datetime(2024, 11, 23, 8, 00, 00)
        i = IntelligentOffice()
        i.manage_blinds_based_on_time()

        mock_blinds.assert_not_called()