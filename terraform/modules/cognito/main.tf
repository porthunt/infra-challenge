resource "aws_cognito_user_pool" "cognito_pool" {
    name = var.pool_name
    tags = var.tags

    dynamic "schema" {
        for_each = var.attributes

        content {
            name                     = schema.value.name
            required                 = try(schema.value.required, false)
            attribute_data_type      = schema.value.type
            mutable                  = try(schema.value.mutable, true)

            dynamic "string_attribute_constraints" {
                for_each = schema.value.type == "String" ? [true] : []

                content {
                    min_length = lookup(schema.value, "min_length", 0)
                    max_length = lookup(schema.value, "max_length", 2048)
                }
      }
        }
    }
}

resource "aws_cognito_user_pool_client" "cognito_client" {
  name = var.client_name
  user_pool_id = aws_cognito_user_pool.cognito_pool.id
}
