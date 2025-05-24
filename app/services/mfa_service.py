import pyotp

def generate_mfa_secret():
    return pyotp.random_base32()

def get_qr_url(email, secret, issuer="SecurePassManager"):
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=email, issuer_name=issuer)

def verify_mfa_code(secret, code):
    totp = pyotp.TOTP(secret)
    return totp.verify(code)
