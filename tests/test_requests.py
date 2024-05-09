from unittest.mock import patch

import pytest
import requests


@pytest.fixture
def bearer_token():
    return ("Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0NTYsImV4cCI6MTYyMDg2NzQ0MH0"
            ".5tgyzzz1wRwtiN9XKkQmw2-2vQk2HN8K8Oh24zD-v3w")


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


def test_get_orders_request_fails_without_authentication(base_url):
    # URL completa
    url = f"{base_url}/orders/book/Ficção/Romance"

    # Realizando a requisição GET para /orders/book/{major}/{minor} sem o token de autenticação
    response = requests.get(url)

    # Verificando se a resposta possui o status code 401 (Unauthorized)
    assert response.status_code == 401


def test_get_orders_request_fails_with_invalid_authentication(base_url):
    # URL completa
    url = f"{base_url}/orders/book/Ficção/Romance"

    # Token de autenticação inválido
    invalid_token = "Bearer invalid_token"

    # Realizando a requisição GET para /orders/book/{major}/{minor} com token de autenticação inválido
    response = requests.get(url, headers={"Authorization": invalid_token})

    # Verificando se a resposta possui o status code 401 (Unauthorized)
    assert response.status_code == 401


@patch('your_application.verify_token')
def test_get_orders_request_returns_expected_data_for_specific_book_category_with_token_verify(mock_verify_token, base_url, expected_data):
    # Configure o retorno do mock_verify_token para indicar uma autenticação bem-sucedida
    mock_verify_token.return_value = True

    # URL completa
    url = f"{base_url}/orders/book/Ficção/Romance"

    # Realizando a requisição GET para /orders/book/{major}/{minor} com o bearer token no cabeçalho de autorização
    response = requests.get(url, headers={"Authorization": "Bearer your_access_token"})

    # Verificando se a resposta possui o status code 200
    assert response.status_code == 200

    # Verificando se os dados retornados na resposta são iguais aos dados esperados
    assert response.json() == expected_data
