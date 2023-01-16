import unittest
from bot_app import screenshot
from datetime import datetime
from mock import patch


class TestScreenshot(unittest.TestCase):

    def test_get_status_code_1(self):
        with patch('requests.get') as mock_request:
            url = 'https://www.yandex.ru'
            mock_request.return_value.status_code = 302
            self.assertEqual(screenshot.get_status_code(url), mock_request.return_value.status_code)

    def test_get_status_code_2(self):
        with patch('requests.get') as mock_request:
            url = 'http://google.com/nonexistingurl'
            mock_request.return_value.status_code = 404
            self.assertEqual(screenshot.get_status_code(url), mock_request.return_value.status_code)

    def test_get_file_name(self):
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
        self.assertEqual(screenshot.get_file_name("https://www.yandex.ru"),
                                                  f'./screens/{current_time}_httpswwwyandexru.jpg')


if __name__ == "__main__":
    unittest.main()