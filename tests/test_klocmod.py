from klocmod import LocalizationsContainer, InvalidLocalizationFileError
import pytest


def load_file(filename: str) -> LocalizationsContainer:
    return LocalizationsContainer.from_file("tests/" + filename, default_lang='ru')


@pytest.fixture(params=['language-phrases.json', 'phrase-languages.json', 'language-phrases.ini'])
def localization(request, caplog) -> LocalizationsContainer:
    lc = load_file(request.param)
    assert "The 'fr-ca' key is found, but 'fr' is missing!" in caplog.text
    return lc


def test_reading_from_file(localization: LocalizationsContainer) -> None:
    assert isinstance(localization, LocalizationsContainer)


def test_language_retrieval(localization: LocalizationsContainer) -> None:
    assert localization.get_lang("en-US") == localization.get_lang("en_US")
    assert localization.get_lang("en-US") != localization.get_lang("en")
    assert localization.get_lang() == localization.get_lang("ru")   # default language
    assert localization.get_lang() == localization.get_lang("de")   # non-existing language
    assert localization.get_lang() != localization.get_lang("en")
    assert localization.get_lang().name == "ru"
    assert localization.get_lang("en-US").name == "en-us"
    assert localization.get_lang("en").name == "en"


def test_phrase_retrieval(localization: LocalizationsContainer) -> None:
    assert localization.get_lang()['color'] == "цвет"
    assert localization.get_lang("en-US")['color'] == "color"
    assert localization.get_lang("en")['color'] == "colour"
    assert localization.get_phrase("ru", "mood") == "настроение"
    assert localization["ru-RU"]["mood"] == "настроение"


def test_key_as_fallback_value(localization: LocalizationsContainer):
    assert localization.get_phrase("en", "blue") == localization.get_phrase("ru", "blue") == "blue"


@pytest.mark.parametrize("filename,message", [('plain.txt', 'Not supported file type: .txt'),
                                              ('invalid-format.json', 'Invalid JSON file.'),
                                              ('invalid.ini', 'Invalid INI file.')])
def test_exceptions_with_other_invalid_files(filename, message):
    with pytest.raises(InvalidLocalizationFileError, message=message):
        load_file(filename)


def test_non_existing_file():
    with pytest.raises(FileNotFoundError):
        load_file("foo.bar")
