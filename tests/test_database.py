import uuid
import pytest

from bookstore_orders.components.models.book_order import BookOrder
from bookstore_orders.components.business.order import ABook
from bookstore_orders.components.utils.database.service import DatabaseService


def test_database_connection():
    # Testa se a conexão com o banco de dados é estabelecida corretamente
    try:
        DatabaseService()
    except Exception as e:
        pytest.fail(f"Erro ao conectar ao banco de dados: {e}")


@pytest.fixture
def mock_database_service(mocker):
    # Cria uma instância mock de DatabaseService
    mock_db_service = mocker.patch("bookstore_orders.components.utils.database.service.DatabaseService").return_value
    # Configura o retorno do método query() do mock
    mock_query = mock_db_service.query.return_value
    # Configura o retorno do método filter() do mock_query
    mock_query.filter.return_value.one.return_value = BookOrder(
        order_id=uuid.UUID("554e7cce-d7fa-4e5b-bd83-929f66f071fa"),
        book_id="123",
        user_id="456",
        quantity=2,
        order_date_time="2024-05-08 10:27:40.951007",
        order_status="pending",
        delivery_address="Rua dos Bobos, 123",
        payment_method="credit_card",
        total_amount=50.0,
        order_notes="Por favor, entregue antes das 18:00",
        major_category="Ficção",
        minor_category="Romance"
    )
    return mock_db_service


def test_get_book_order_method_returns_expected_data_for_specific_category(mock_database_service):
    # Cria uma instância de Order
    book_order_instance = ABook(user_id="456")
    # Define a conexão com o banco de dados para a instância mock
    book_order_instance.conn = mock_database_service

    # Chama a função get_book_order
    book_order_data = book_order_instance.get_book_order(major="Ficção", minor="Romance")

    # Verifica se a função retorna os dados corretos
    assert book_order_data == {
        "order_id": uuid.UUID("554e7cce-d7fa-4e5b-bd83-929f66f071fa"),
        "book_id": "123",
        "user_id": "456",
        "quantity": 2,
        "order_date_time": "2024-05-08 10:27:40.951007",
        "order_status": "pending",
        "delivery_address": "Rua dos Bobos, 123",
        "payment_method": "credit_card",
        "total_amount": 50.0,
        "order_notes": "Por favor, entregue antes das 18:00",
        "major_category": "Ficção",
        "minor_category": "Romance"
    }
