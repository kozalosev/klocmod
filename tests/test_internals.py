from klocmod.internals import swap_keys, check_missing_non_regional_languages


def test_swap_keys():
    given = {
        'test': {
            'en': "test",
            'ru-RU': "тест"
        }
    }
    expected = {
        'en': {
            'test': "test"
        },
        'ru-RU': {
            'test': "тест"
        }
    }
    assert swap_keys(given) == expected


def test_check_missing_non_regional_languages(caplog):
    check_missing_non_regional_languages({
        'en': {
            'test': "test",
        },
        'ru-RU': {
            'test': "тест",
        }
    })
    assert "The 'ru-RU' key is found, but 'ru' is missing!" in caplog.text
