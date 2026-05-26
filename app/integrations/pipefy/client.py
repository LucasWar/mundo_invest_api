from app.integrations.pipefy.mutations import (
    CREATE_CARD_MUTATION,
    UPDATE_CARD_MUTATION
)

class PipefyClient:

    PIPE_ID = 123456

    async def create_card(self, customer):

        variables = {
            "pipe_id": self.PIPE_ID,
            "fields": [
                {
                    "field_id": "nome",
                    "field_value": customer.cliente_nome
                },
                {
                    "field_id": "email",
                    "field_value": customer.cliente_email
                },
                {
                    "field_id": "tipo_de_solicitacao",
                    "field_value": customer.tipo_solicitacao
                },
                {
                    "field_id": "patrimonio",
                    "field_value": str(customer.valor_patrimonio)
                }
            ]
        }

        payload = {
            "query": CREATE_CARD_MUTATION,
            "variables": variables
        }

        print("PIPEFY CREATE CARD")
        print(payload)

        return payload

    async def update_card_priority(
        self,
        card_id: str,
        prioridade: str
    ):

        payload = {
            "query": UPDATE_CARD_MUTATION,
            "variables": {
                "card_id": card_id,
                "field_id": "prioridade",
                "new_value": prioridade
            }
        }

        print("PIPEFY UPDATE CARD")
        print(payload)

        return payload