CREATE_CARD_MUTATION = """
mutation CreateCard($pipe_id: ID!, $fields: [FieldValueInput]!) {
  createCard(
    input: {
      pipe_id: $pipe_id
      fields_attributes: $fields
    }
  ) {
    card {
      id
      title
    }
  }
}
"""

UPDATE_CARD_MUTATION = """
mutation UpdateCardField($card_id: ID!, $field_id: String!, $new_value: String!) {
  updateCardField(
    input: {
      card_id: $card_id
      field_id: $field_id
      new_value: $new_value
    }
  ) {
    card {
      id
    }
  }
}
"""