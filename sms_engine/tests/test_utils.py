from django.test import TestCase

from sms_engine.sms import create as create_sms
from sms_engine.utils import get_sms_usage

from freezegun import freeze_time


@freeze_time("2020-11-05")
class UtilsTest(TestCase):

    def test_get_sms_usage(self):
        create_sms(to="+62800000000001", message="Test", backend='dummy', scheduled_time="2020-11-06")
        sms_usage = get_sms_usage("2020-11-01", "2020-11-15")
        self.assertEqual(sms_usage["dummy"]["total"], 1)
