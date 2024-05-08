import pytest
import requests


@pytest.fixture
def bearer_token():
    return ("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNDU2In0.YkBz8oyHfheCTBsUwR1BJhe8vccyZwFtMZD"
            "-gfZgX2o")


@pytest.fixture
def base_url():
    return "http://localhost:8000"


@pytest.fixture
def expected_data():
    return {
        "order_id": "554e7cce-d7fa-4e5b-bd83-929f66f071fa",
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


def test_get_orders_request_returns_expected_data_for_specific_book_category(bearer_token, base_url, expected_data):
    # URL completa
    url = f"{base_url}/orders/book/Ficção/Romance"

    # Realizando a requisição GET para /orders/book/{major}/{minor} com o bearer token no cabeçalho de autorização
    response = requests.get(url, headers={"Authorization": bearer_token})

    # Verificando se a resposta possui o status code 200
    assert response.status_code == 200

    # Verificando se os dados retornados na resposta são iguais aos dados esperados
    assert response.json() == expected_data
