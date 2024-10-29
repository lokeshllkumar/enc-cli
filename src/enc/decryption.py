from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from ..metadata import read_metadata
import os, gzip

def dec_aes_key_with_rsa(encrypted_key, private_key_path):
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(), password = None, backend = default_backend()
        )
    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(mgf = padding.MGF1(algorithm = hashes.SHA256()), algorithm = hashes.SHA256(), label = None)
    )

    return aes_key

def dec_file(input_file, output_file, private_key_path):
    with open(input_file, "rb") as f_in:
        key_length = int.from_bytes(f_in.read(2), 'big')
        encrypted_key = f_in.read(key_length)
        iv = f_in.read(12)
        tag = f_in.read(16)
        salt = f_in.read(16)
        metadata = read_metadata(f_in)

        aes_key = dec_aes_key_with_rsa(encrypted_key, private_key_path)

        cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv, tag), backend = default_backend())
        decryptor = cipher.decryptor()

        with gzip.open(f_in, "rb") as gz_in, open(output_file, "wb") as f_out:
            for chunk in iter(lambda: gz_in.read(1024), b""):
                f_out.write(decryptor.update(chunk))
            f_out.write(decryptor.finalize())