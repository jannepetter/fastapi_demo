from utils.tokens import make_tokens, make_token_payloads


async def generate_auth_headers(user):

    role_data, user_data = await make_token_payloads(user)

    access_token, _ = make_tokens(user_data, role_data)

    return {"Authorization": f"Bearer {access_token}"}
