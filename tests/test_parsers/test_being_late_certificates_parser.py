import json
import pathlib

import pytest
from pydantic import parse_obj_as

import models
from core.config import ROOT_PATH
from services.parsers.html import BeingLateCertificatesParser

HTML_FILES_PATH = pathlib.Path.joinpath(ROOT_PATH, 'tests', 'test_parsers', 'html')
UNITS_PATH = pathlib.Path.joinpath(ROOT_PATH, 'tests', 'units.json')


@pytest.fixture
def units() -> list[models.UnitIdAndName]:
    with open(UNITS_PATH, encoding='utf-8') as file:
        return parse_obj_as(list[models.UnitIdAndName], json.load(file))


def test_multiple_units_being_late_certificates(units):
    with open(HTML_FILES_PATH / 'multiple_being_late_certificates.html', encoding='utf-8') as file:
        html = file.read()
    result = BeingLateCertificatesParser(html, None, units).parse()
    assert sum([i.being_late_certificates_count for i in result]) == 9


def test_single_unit_being_late_certificates():
    with open(HTML_FILES_PATH / 'single_unit_being_late_certificates.html', encoding='utf-8') as file:
        html = file.read()
    unit_ids_and_names = parse_obj_as(list[models.UnitIdAndName], [
        {
            'id': 389,
            'name': 'Москва 4-1',
        },
    ])
    result = BeingLateCertificatesParser(html, 389, unit_ids_and_names).parse()
    assert result[0].being_late_certificates_count == 2


def test_no_being_late_certificates(units):
    with open(HTML_FILES_PATH / 'no_being_late_certificates.html', encoding='utf-8') as file:
        html = file.read()
    result: list = BeingLateCertificatesParser(html, None, units).parse()
    assert result == []
