import pytest
from utils.tokens import make_tokens, decode_token


@pytest.mark.anyio
async def test_tokens():
    user_data = {"id": 1, "roles": "jeps"}
    data = {1: ["juu", "jaa"]}

    access, refresh = make_tokens(user_data, data)

    assert (
        access
        == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoxLCJyb2xlcyI6ImplcHMifSwiZGF0YSI6eyIxIjpbImp1dSIsImphYSJdfSwiZXhwIjoxNzU1OTUxMzAwfQ.vSlJhmN4xKtehwgcyLRvgybV1jjlSH_pL_yR9d_VZ7I"
    )
    assert len(access) == 183
    assert len(refresh) == 147

    dec_acc = decode_token(access)

    assert dec_acc == {
        "user": {"id": 1, "roles": "jeps"},
        "data": {"1": ["juu", "jaa"]},
        "exp": 1755951300,
    }
