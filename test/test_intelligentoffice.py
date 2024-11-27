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

    @patch.object(GPIO, "output")
    @patch.object(VEML7700, 'lux', new_callable = PropertyMock)
    def test_manage_light_level_lights_turned_on(self, mock_lux: Mock, mock_output: Mock):
        mock_lux.return_value = 499

        i = IntelligentOffice()
        i.manage_light_level()
        mock_output.assert_called_once_with(i.LED_PIN, GPIO.HIGH)

    @patch.object(GPIO, "output")
    @patch.object(VEML7700, 'lux', new_callable = PropertyMock)
    def test_manage_light_level_lights_turned_off(self, mock_lux: Mock, mock_output: Mock):
        mock_lux.return_value = 551
        i = IntelligentOffice()
        i.light_on = True
        i.manage_light_level()
        mock_output.assert_called_once_with(i.LED_PIN, GPIO.LOW)

    @patch.object(GPIO, "input")
    @patch.object(GPIO, "output")
    @patch.object(VEML7700, 'lux', new_callable = PropertyMock)
    def test_manage_light_level_lights_last_worker_leaves(self, mock_lux, mock_output: Mock, mock_input: Mock):
        mock_input.return_value = False
        mock_lux.return_value = 501
        i = IntelligentOffice()
        i.manage_light_level()
        mock_output.assert_called_once_with(i.LED_PIN, GPIO.LOW)

    @patch.object(GPIO, "input")
    @patch.object(GPIO, "output")
    @patch.object(VEML7700, 'lux', new_callable = PropertyMock)
    def test_manage_light_level_lights_first_worker_steps_in(self, mock_lux, mock_output: Mock, mock_input: Mock):
        mock_input.return_value = True
        mock_lux.return_value = 501
        i = IntelligentOffice()
        i.manage_light_level()
        mock_output.assert_called_once_with(i.LED_PIN, GPIO.HIGH)

