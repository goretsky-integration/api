import pathlib
import uuid

from services.parsers import OrderByUUIDParser
from models.external_api_responses.shift_manager import OrderByUUID


def test_canceled_order_parser_with_rejecter_and_courier():
    html = pathlib.Path.joinpath(pathlib.Path(__file__).parent.parent.parent.parent, 'api_responses', 'canceled_orders', 'with-courier-and-rejecter.html').read_text(encoding='utf-8')
    order_uuid = uuid.uuid4()
    expected = OrderByUUID(
        unit_name="Калуга-1",
        created_at='06.02.2023 20:23:09',
        receipt_printed_at='06.02.2023 23:30:54',
        number='227 - 1',
        type='Доставка',
        price=889,
        uuid=order_uuid,
        courier_name='СЗ Эгембердиев М.',
        rejected_by_user_name='Байыш Кызы  Мираида',
    )
    actual = OrderByUUIDParser(html, order_type='Доставка', order_price=889, order_uuid=order_uuid).parse()
    assert actual == expected


def test_canceled_order_parser_without_courier():
    html = pathlib.Path.joinpath(pathlib.Path(__file__).parent.parent.parent.parent, 'api_responses', 'canceled_orders', 'without-courier.html').read_text(encoding='utf-8')
    order_uuid = uuid.uuid4()
    expected = OrderByUUID(
        unit_name="Вязьма-1",
        created_at='07.02.2023 13:58:33',
        receipt_printed_at='07.02.2023 14:09:16',
        number='92 - 2',
        type='Доставка',
        price=889,
        uuid=order_uuid,
        courier_name=None,
        rejected_by_user_name='Шайнусова Руфина',
    )
    actual = OrderByUUIDParser(html, order_type='Доставка', order_price=889, order_uuid=order_uuid).parse()
    assert actual == expected


def test_canceled_order_parser_without_courier_and_rejecter():
    html = pathlib.Path.joinpath(pathlib.Path(__file__).parent.parent.parent.parent, 'api_responses', 'canceled_orders', 'without-courier-and-rejecter.html').read_text(encoding='utf-8')
    order_uuid = uuid.uuid4()
    expected = OrderByUUID(
        unit_name="Вязьма-1",
        created_at='07.02.2023 13:58:33',
        receipt_printed_at='07.02.2023 14:09:16',
        number='92 - 2',
        type='Доставка',
        price=889,
        uuid=order_uuid,
        courier_name=None,
        rejected_by_user_name=None,
    )
    actual = OrderByUUIDParser(html, order_type='Доставка', order_price=889, order_uuid=order_uuid).parse()
    assert actual == expected
