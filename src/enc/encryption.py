from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from ..metadata import write_metadata
import os, gzip


def gen_aes_key():
    key = os.urandom(32)
    iv = os.urandom(12)
    return key, iv

def enc_aes_key_with_rsa(aes_key, public_key_path):
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_der_public_key(
            key_file.read(), backend = default_backend()
        )
    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(mgf = padding.MGF1(algorithm = hashes.SHA256()), algorithm = hashes.SHA256(), label = None)
    )
    return encrypted_key
    

def enc_file(input_file, output_file, public_key_path):
    aes_key, iv = gen_aes_key()
    salt = os.urandom(16)
    encrypted_key = enc_aes_key_with_rsa(aes_key, public_key_path)

    with open(output_file, "wb") as f_out:
        f_out.write(len(encrypted_key).to_bytes(2, 'big'))
        f_out.write(encrypted_key)
        f_out.write(iv)
        f_out.write(salt)
        write_metadata(f_out, os.path.basename(input_file))

        with open(input_file, "rb") as f_in, gzip.open(f_out, 'wb') as gz_out:
            cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv), backend = default_backend())
            encryptor = cipher.encryptor()
            for chunk in iter(lambda: f_in.read(1024), b""):
                gz_out.write(encryptor.update(chunk))
            gz_out.write(encryptor.finalize())
            gz_out.write(encryptor.tag)