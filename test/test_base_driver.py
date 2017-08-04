import unittest
from mock import patch, MagicMock
from dorm.database import models
from dorm.database.drivers.base import BaseDriver

class BaseDriverTestCase(unittest.TestCase):
    
    def setUp(self):
        
        self.stub_connection = MagicMock()
        