import json
import random
import string
import uuid
from datetime import datetime
import argparse

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_datafile_entry():
    now = datetime.utcnow()
    return {
        "path": f"{generate_random_string(8)}.dat",
        "size": random.randint(1000, 1000000),
        "time": now.isoformat() + "Z",
        "chk": generate_random_string(64),
        "uid": "user123",
        "gid": "group123",
        "perm": "rw-r--r--"
    }

def generate_datablock(output_file: str, num_entries: int):
    with open(output_file, "w") as f:
#        f.write('{"_id": "' + str(uuid.uuid4()) + '",\n')
        f.write('{\n')
        f.write('"archiveId": "' + str(uuid.uuid4()) + '",\n')
        f.write('"size": 0,\n"packedSize": 0,\n')
        f.write('"chkAlg": "sha256",\n"version": "v1.0",\n')
        f.write('"dataFileList": [\n')

        for i in range(num_entries):
            if i > 0:
                f.write(",\n")
            json.dump(generate_datafile_entry(), f)

        f.write("\n]}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Datablock with DataFiles for SciCat ingestion.")
    parser.add_argument("--entries", type=int, default=1000000, help="Number of DataFile entries to generate")
    parser.add_argument("--output", type=str, default="datablock_upload.json", help="Output file path")

    args = parser.parse_args()
    generate_datablock(args.output, args.entries)
