from django.core.cache import cache
from django.test import TestCase

from sms_engine.models import SMS, SMSTag, STATUS


class ModelsTest(TestCase):

    def test_dispatch(self):
        sms = SMS.objects.create(
            to='+6280000000000', message='test', backend_alias='dummy'
        )
        sms.dispatch(log_level=2)
        sms = SMS.objects.latest('id')
        self.assertEqual(sms.to, '+6280000000000')
        self.assertEqual(sms.status, STATUS.sent)
        self.assertEqual(sms.logs.first().status, STATUS.sent)

        SMS.objects.all().delete()

        sms = SMS.objects.create(
            to='+6280000000000', message='test', backend_alias='dummy'
        )
        sms.dispatch(log_level=0)
        self.assertEqual(sms.status, STATUS.sent)
        self.assertFalse(sms.logs.exists())

        SMS.objects.all().delete()

        sms = SMS.objects.create(
            to='+6280000000000', message='test', backend_alias='error'
        )
        sms.dispatch()

        self.assertEqual(sms.status, STATUS.failed)

        log = sms.logs.first()
        self.assertEqual(log.message, 'SMS sending error')
        self.assertEqual(log.exception_type, 'SendSMSError')

    def test_tag(self):
        self.assertIsNone(SMSTag.get('mytag'))

        # make sure tag object is cached
        tag = SMSTag.objects.create(name='mytag')
        self.assertEqual(SMSTag.get('mytag'), tag)
        self.assertEqual(cache.get("sms-tag:mytag"), tag)

        # if tag name is changed, the old cached object should be cleared
        # and create a new one
        tag.name = 'newtag'
        tag.save()

        self.assertIsNone(SMSTag.get('mytag'))
        self.assertEqual(SMSTag.get('newtag'), tag)
        self.assertEqual(cache.get('sms-tag:newtag'), tag)

        # if tag is deleted, it should remove the cached object
        tag.delete()
        self.assertIsNone(cache.get('sms-tag:newtag'))
