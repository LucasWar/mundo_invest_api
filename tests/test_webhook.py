from app.modules.webhook.services.webhook_service import WebhookService
from app.modules.webhook.dto.update_card import UpdateCardDto
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
import pytest


@pytest.fixture
def mock_customer_service():
    service = MagicMock()
    service.find_customer_by_email = AsyncMock()
    service.update_priority_record = AsyncMock()
    return service

@pytest.fixture
def mock_card_repo():
    repo = MagicMock()
    repo.find_event_by_id = AsyncMock()
    repo.create = AsyncMock()
    return repo

@pytest.fixture
def webhook_service(mock_customer_service, mock_card_repo):
    return WebhookService(
        customer_service=mock_customer_service,
        card_repo=mock_card_repo
    )

def make_fake_dto(**overrides):
    dto = MagicMock(spec=UpdateCardDto)
    dto.event_id = "evt_001"
    dto.cliente_email = "joao@email.com"
    for key, value in overrides.items():
        setattr(dto, key, value)
    return dto


def make_fake_customer(valor_patrimonio: float):
    customer = MagicMock()
    customer.valor_patrimonio = valor_patrimonio
    customer.cliente_email = "joao@email.com"
    return customer

@pytest.mark.asyncio
@pytest.mark.parametrize("patrimonio,prioridade_esperada", [
    (100000, "prioridade_normal"),
    (200000, "prioridade_alta"),
    (500000, "prioridade_alta"),
])
async def test_card_update_aplica_prioridade_correta(
    webhook_service,
    mock_customer_service,
    mock_card_repo,
    patrimonio,
    prioridade_esperada
):
    """Deve calcular a prioridade correta baseada no valor do patrimônio"""

    mock_card_repo.find_event_by_id.return_value = None

    mock_customer_service.find_customer_by_email.return_value = make_fake_customer(patrimonio)

    dto = make_fake_dto()


    await webhook_service.card_update(dto)

    mock_card_repo.find_event_by_id.assert_called_once_with(dto.event_id)

    mock_customer_service.find_customer_by_email.assert_called_once_with(dto.cliente_email)

    mock_customer_service.update_priority_record.assert_called_once_with(
        dto.cliente_email,
        prioridade_esperada 
    )

    mock_card_repo.create.assert_called_once_with(dto)

@pytest.mark.asyncio
async def test_card_update_bloqueia_evento_duplicado(
    webhook_service,
    mock_customer_service,
    mock_card_repo
):
    """Deve lançar HTTP 200 e interromper o fluxo se o event_id já foi processado"""

    mock_card_repo.find_event_by_id.return_value = MagicMock()

    dto = make_fake_dto()

    with pytest.raises(HTTPException) as exc:
        await webhook_service.card_update(dto)

    assert exc.value.status_code == 200

    mock_customer_service.find_customer_by_email.assert_not_called()
    mock_customer_service.update_priority_record.assert_not_called()
    mock_card_repo.create.assert_not_called()