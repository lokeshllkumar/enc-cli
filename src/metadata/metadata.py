import json
import time

def write_metadata(f_out, original_filename):
    metadata = {
        "filename": original_filename,
        "timestamp": time.time()
    }
    f_out.write(json.dumps(metadata).encode() + b'\n')

def read_metadata(f_in):
    metadata = f_in.readline().decode()
    return json.loads(metadata)