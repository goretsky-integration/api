import pathlib

import models
from core.config import ROOT_PATH
from services.parsers.html import BeingLateCertificatesParser

HTML_FILES_PATH = pathlib.Path.joinpath(ROOT_PATH, 'tests', 'test_parsers', 'html')


def test_multiple_units_being_late_certificates():
    with open(HTML_FILES_PATH / 'multiple_being_late_certificates.html', encoding='utf-8') as file:
        html = file.read()
    result: list[models.UnitBeingLateCertificates] = BeingLateCertificatesParser(html).parse()
    expected = {
        'Москва 4-18': 12,
        'Москва 4-7': 1,
        'Москва 4-17': 9,
        'Москва 4-15': 1,
        'Москва 4-4': 1,
        'Москва 4-1': 1,
    }
    for unit in result:
        assert expected[unit.unit_name] == unit.being_late_certificates_count


def test_single_unit_being_late_certificates():
    with open(HTML_FILES_PATH / 'single_unit_being_late_certificates.html', encoding='utf-8') as file:
        html = file.read()
    result: models.SingleUnitBeingLateCertificates = BeingLateCertificatesParser(html).parse()
    assert result.being_late_certificates_count == 9


def test_no_being_late_certificates():
    with open(HTML_FILES_PATH / 'no_being_late_certificates.html', encoding='utf-8') as file:
        html = file.read()
    result: list = BeingLateCertificatesParser(html).parse()
    assert result == []
