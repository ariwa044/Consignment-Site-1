
import unittest
from unittest.mock import patch, MagicMock
import requests
import sys
import os
import django
from django.conf import settings

# Add the project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure minimal Django settings
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=['consignment'],
        SECRET_KEY='test_secret_key',
    )
    django.setup()

from consignment.utils import geocode

class TestGeocodeResilience(unittest.TestCase):
    @patch('consignment.utils.requests.get')
    def test_geocode_connection_error(self, mock_get):
        # Simulate a connection error
        mock_get.side_effect = requests.exceptions.ConnectionError("Network is unreachable")
        
        # Call geocode
        lat, lon = geocode("Coventry")
        
        # Verify it returns None, None instead of raising exception
        self.assertIsNone(lat)
        self.assertIsNone(lon)
        print("Test passed: Geocode handled ConnectionError gracefully.")

    @patch('consignment.utils.requests.get')
    def test_geocode_timeout(self, mock_get):
        # Simulate a timeout
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        
        # Call geocode
        lat, lon = geocode("Coventry")
        
        # Verify it returns None, None
        self.assertIsNone(lat)
        self.assertIsNone(lon)
        print("Test passed: Geocode handled Timeout gracefully.")
        
    @patch('consignment.utils.requests.get')
    def test_geocode_500_error(self, mock_get):
        # Simulate a 500 error
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
        mock_get.return_value = mock_response
        
        # Call geocode
        lat, lon = geocode("Coventry")
        
        # Verify it returns None, None
        self.assertIsNone(lat)
        self.assertIsNone(lon)
        print("Test passed: Geocode handled HTTPError gracefully.")

if __name__ == '__main__':
    unittest.main()
