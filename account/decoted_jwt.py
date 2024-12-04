import jwt


def decode_jwt_token(token:str, token_secret):

    try:
        decoded_payload = jwt.decode(token, token_secret, algorithms=["HS256"])
        # print("Verified payload:", decoded_payload)
        return str(decoded_payload['user_id'])
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None

