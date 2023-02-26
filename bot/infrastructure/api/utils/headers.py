def bearer_authorization(access_token) -> dict:
    return {"Authorization": "Bearer " + access_token}