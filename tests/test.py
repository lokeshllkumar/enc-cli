from ..src.enc import enc_file, dec_file

def test():
    enc_file('test.txt', 'test.enc', 'password', 'keys/public_key.pem')
    dec_file('test.enc', 'test_decrypted.txt', 'keys/private_key.pem')
    assert open('test.txt', 'rb').read() == open('test_decrypted.txt', 'rb').read()