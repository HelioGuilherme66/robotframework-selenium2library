import unittest
import os
from collections import namedtuple

from mockito import mock, verifyStubbedInvocationsAreUsed, when, unstub, verify
from robot.utils import JYTHON
from selenium.webdriver.common.keys import Keys
try:
    from approvaltests.approvals import verify_all
    from approvaltests.reporters.generic_diff_reporter_factory import GenericDiffReporterFactory
except ImportError:
    if JYTHON:
        verify = None
        GenericDiffReporterFactory = None
    else:
        raise

from SeleniumLibrary.keywords import ElementKeywords


class ElementKeywordsPessKeys(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ctx = mock()
        cls.element_keywords = ElementKeywords(ctx)

    def setUp(self):
        path = os.path.dirname(__file__)
        reporter_json = os.path.abspath(os.path.join(path, '..', 'approvals_reporters.json'))
        factory = GenericDiffReporterFactory()
        factory.load(reporter_json)
        self.reporter = factory.get_first_working()

    def tearDown(self):
        unstub()

    def test_press_keys_with_locator(self):
        element = mock()
        when(self.element_keywords).find_element('id:tidii', required=False).thenReturn(element)
        self.element_keywords.press_keys('id:tidii', 'A', 'B', 'C')
        verifyStubbedInvocationsAreUsed()

    def test_press_keys_no_locator(self):
        when(self.element_keywords).find_element('id:tidii', required=False).thenReturn(None)
        self.element_keywords.press_keys('None', 'A', 'B', 'C')
        verify(self.element_keywords, times=0).find_element('None', required=False)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_parse_keys(self):
        results = []
        results.append(self.element_keywords._parse_keys('A', 'B', 'C'))
        results.append(self.element_keywords._parse_keys('AAA', 'CONTROL', 'C'))
        results.append(self.element_keywords._parse_keys('AAA', 'CONTROL+B', 'C'))
        results.append(self.element_keywords._parse_keys('CONTROL+A', 'ALT+B'))
        results.append(self.element_keywords._parse_keys('CONTROL+ALT+b'))
        verify_all('index', results, reporter=self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_parse_keys_aliases(self):
        results = []
        results.append(self.element_keywords._parse_aliases('CTRL'))
        results.append(self.element_keywords._parse_aliases('ESC'))
        results.append(self.element_keywords._parse_aliases('CONTROL'))
        results.append(self.element_keywords._parse_aliases('BB'))
        verify_all('Alias testing', results, reporter=self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_separate_key(self):
        results = []
        results.append(self.element_keywords._separate_key('BB'))
        results.append(self.element_keywords._separate_key('ALT+B'))
        results.append(self.element_keywords._separate_key('A+B+C'))
        results.append(self.element_keywords._separate_key('A++'))
        results.append(self.element_keywords._separate_key('A+++'))
        results.append(self.element_keywords._separate_key('A+++C'))
        verify_all('Separate key', results, reporter=self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_convert_key(self):
        results = []
        results.append(self.element_keywords._convert_special_keys(['B']))
        results.append(self.element_keywords._convert_special_keys(['AA', 'CCC']))
        results.append(self.element_keywords._convert_special_keys(['ALT', 'B']))
        results.append(self.element_keywords._convert_special_keys(['ALT', 'CTRL']))
        verify_all('To Selenium Special Keys', results, reporter=self.reporter)
