from django.conf import settings


def get_backend(alias='default'):
    return get_available_backends()[alias]


def get_available_backends():
    backends = get_config().get('BACKENDS', {})

    if backends:
        return backends

    backends['default'] = 'sms_engine.backends.DummyBackend'

    return backends


def get_config():
    """
    Returns SMS Engines's configuration in dictionary format. e.g:
    SMS_ENGINE = {
        'BACKENDS': {
            'twilio': sms_engine.backends.TwilioBackend
        }
    }
    """
    return getattr(settings, 'SMS_ENGINE', {})


def get_default_priority():
    return get_config().get('DEFAULT_PRIORITY', 'medium')


def get_log_level():
    return get_config().get('LOG_LEVEL', 1)
