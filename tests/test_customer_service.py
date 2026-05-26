from app.modules.customer.dto.create_customer_dto import CreateCustomerDto
from app.modules.customer.service.customer_service import CustomerService
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
import pytest


@pytest.fixture
def mock_repo():
    repo = MagicMock()
    repo.find_customer_by_email = AsyncMock()
    repo.create = AsyncMock()
    repo.update_priority = AsyncMock()
    return repo


@pytest.fixture
def mock_pipefy():
    client = MagicMock()
    client.create_card = AsyncMock()         
    client.update_card_priority = AsyncMock()
    return client


@pytest.fixture
def service(mock_repo, mock_pipefy):
    return CustomerService(repo=mock_repo, pipefy_client=mock_pipefy)


def make_fake_customer(**overrides):
    customer = MagicMock()
    customer.id = 1
    customer.cliente_nome = "João"
    customer.cliente_email = "joao@email.com"
    customer.tipo_solicitacao = "Atualização cadastral"
    customer.valor_patrimonio = 10000.0
    customer.status = "ativo"
    for key, value in overrides.items():
        setattr(customer, key, value)
    return customer

@pytest.mark.asyncio
async def test_create_customer_success(service, mock_repo, mock_pipefy):
    """Deve criar cliente e chamar o pipefy quando email não existe"""
    mock_repo.find_customer_by_email.return_value = None
    fake_customer = make_fake_customer()
    mock_repo.create.return_value = fake_customer

    dto = CreateCustomerDto(
        cliente_email="joao@email.com",
        cliente_nome="João",
        tipo_solicitacao="Atualização cadastral",
        valor_patrimonio=10000
    )

    result = await service.create_customer(dto)

    mock_repo.find_customer_by_email.assert_called_once_with(dto.cliente_email)
    mock_repo.create.assert_called_once_with(dto)
    mock_pipefy.create_card.assert_called_once_with(fake_customer)

    assert result.id == fake_customer.id
    assert result.cliente_email == fake_customer.cliente_email
    assert result.cliente_nome == fake_customer.cliente_nome
    assert result.status == fake_customer.status
    assert result.valor_patrimonio == fake_customer.valor_patrimonio

@pytest.mark.asyncio
async def test_create_customer_raises_conflict_if_email_exists(service, mock_repo, mock_pipefy):
    """Deve lançar 409 e não chamar create nem pipefy quando email já existe"""
    mock_repo.find_customer_by_email.return_value = make_fake_customer()  # email ocupado

    dto = CreateCustomerDto(
        cliente_email="existente@email.com",
        cliente_nome="Maria",
        tipo_solicitacao="Atualização cadastral",
        valor_patrimonio=10000
    )

    with pytest.raises(HTTPException) as exc:
        await service.create_customer(dto)

    assert exc.value.status_code == 409
    mock_repo.create.assert_not_called()
    mock_pipefy.create_card.assert_not_called()