import pytest
import requests
from json.decoder import JSONDecodeError


class TestUserAgentCheck:
    arg_names = 'user_agent, expected_platform, expected_browse, expected_device'
    arg_values = [
        (
            "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "Mobile",
            "No",
            "Android"
        ),
        (
            "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
            "Mobile",
            "Chrome",
            "iOS"
        ),
        (
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Googlebot",
            "Unknown",
            "Unknown"
        ),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
            "Web",
            "Chrome",
            "No"
        ),
        (
            "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            "Mobile",
            "No",
            "iPhone"
        ),
    ]

    @pytest.mark.parametrize(arg_names, arg_values)
    def test_1(self, user_agent, expected_platform, expected_browse, expected_device):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        headers = {"user-agent": user_agent}
        response = requests.get(url, headers=headers)

        try:
            response_dict = response.json()
        except JSONDecodeError:
            print("Response is not a JSON format")

        assert "platform" in response_dict, "There is no field 'platform' in the response"
        assert "browser" in response_dict, "There is no field 'browser' in the response"
        assert "device" in response_dict, "There is no field 'device' in the response"

        actual_platform = response_dict["platform"]
        actual_browser = response_dict["browser"]
        actual_device = response_dict["device"]

        assert actual_platform == expected_platform, f"Expected_platform is different from actual_platform: {actual_platform}, user_agent: {user_agent}"
        assert actual_browser == expected_browse, f"Expected_browser is different from actual_browser: {actual_browser}, user_agent: {user_agent}"
        assert actual_device == expected_device, f"Expected_device is different from actual_device: {actual_device}, user_agent: {user_agent}"