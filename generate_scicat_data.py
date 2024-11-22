#!/bin/python


import json
import random
import string
from datetime import datetime, timedelta, timezone
import sys

def random_date(start, end):
    """
    This function returns a random datetime between two datetime 
    objects, including timezone information.
    """
    delta = end - start
    int_delta = int(delta.total_seconds())
    random_second = random.randint(0, int_delta)
    random_datetime = start + timedelta(seconds=random_second)
    # Make the datetime timezone-aware (UTC)
    return random_datetime.replace(tzinfo=timezone.utc)

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_scientific_metadata(metadata_count):
    metadata_fields = []
    # Typical metadata fields for X-ray tomography experiments
    possible_fields = [
        'beamEnergy', 'exposureTime', 'detectorDistance', 'sampleRotation', 'cameraPixelSize',
        'effectivePixelSize', 'scanMode', 'filterMaterial', 'monochromatorType', 'flux',
        'beamCurrent', 'beamSize', 'numberOfProjections', 'detectorType', 'opticalMagnification',
        'radiationDose', 'photonEnergy', 'ringCurrent', 'undulatorGap', 'detectorResolution',
        'temperature', 'pressure', 'humidity', 'experimentDuration', 'dataAcquisitionDate'
    ]
    for i in range(metadata_count):
        field_name = possible_fields[i % len(possible_fields)] + f"_{i+1}"  # Ensure unique field names
        metadata_fields.append({
            field_name: {
                "value": round(random.uniform(1, 100), 2),
                "unit": random.choice(["keV", "s", "mm", "degrees", "um", "mrad", "Gy", "Hz", "A"]),
                "valueSI": round(random.uniform(1e-15, 1e-14), 16),
                "unitSI": random.choice(["(kg m^2) / s^2", "s", "m", "rad", "Gy", "s^-1", "A"])
            }
        })
    return {k: v for d in metadata_fields for k, v in d.items()}

def generate_record(index, metadata_count):
    return {
        "_id": f"PID.SAMPLE.PREFIX/{random_string(5)}_{index}",
        "owner": f"{random.choice(['Oleksandr Yefanov', 'Stephen Collins', 'Doru Constantin'])}",
        "ownerEmail": f"{random_string(5).lower()}@example.com",
        "orcidOfOwner": "0000-0001-8676-" + str(random.randint(1000, 9999)),
        "contactEmail": f"{random_string(5).lower()}@example.com",
        "sourceFolder": "https://example.com/data/" + random_string(10),
        "sourceFolderHost": "https://example.com/" + random_string(5),
        "size": random.randint(1000, 5000000000),
        "packedSize": random.randint(0, 4000),
        "numberOfFiles": random.randint(1, 100),
        "numberOfFilesArchived": random.randint(1, 100),
        "creationTime": {
            "$date": random_date(
                datetime(2010, 1, 1, tzinfo=timezone.utc),
                datetime(2023, 12, 31, tzinfo=timezone.utc)
            ).isoformat()
        },
        "type": random.choice(["raw", "derived"]),
        "description": random_string(50),
        "datasetName": random_string(8),
        "classification": "IN=medium,AV=low,CO=low",
        "license": "",
        "version": "3.1.0",
        "isPublished": random.choice([True, False]),
        "ownerGroup": "aGroup",
        "accessGroups": [],
        "createdBy": "ingestor",
        "history": [],
        "datasetlifecycle": {
            "archivable": random.choice([True, False]),
            "retrievable": random.choice([True, False]),
            "publishable": random.choice([True, False]),
            "archiveRetentionTime": {
                "$date": random_date(
                    datetime(2030, 1, 1, tzinfo=timezone.utc),
                    datetime(2040, 12, 31, tzinfo=timezone.utc)
                ).isoformat()
            },
            "dateOfPublishing": {
                "$date": random_date(
                    datetime(2022, 1, 1, tzinfo=timezone.utc),
                    datetime(2025, 12, 31, tzinfo=timezone.utc)
                ).isoformat()
            },
            "isOnCentralDisk": random.choice([True, False]),
            "archiveStatusMessage": "datasetCreated",
            "retrieveStatusMessage": "",
            "retrieveIntegrityCheck": random.choice([True, False])
        },
        "createdAt": {
            "$date": random_date(
                datetime(2020, 1, 1, tzinfo=timezone.utc),
                datetime(2023, 12, 31, tzinfo=timezone.utc)
            ).isoformat()
        },
        "updatedAt": {
            "$date": random_date(
                datetime(2020, 1, 1, tzinfo=timezone.utc),
                datetime(2023, 12, 31, tzinfo=timezone.utc)
            ).isoformat()
        },
        "techniques": [
            {
                "pid": "PaNET" + str(random.randint(10000, 99999)),
                "name": random_string(100)
            }
        ],
        "principalInvestigator": random.choice(["Principal Investigator", "Investigator"]),
        "scientificMetadata": generate_scientific_metadata(metadata_count),
        "sampleId": random_string(7),
        "instrumentId": random_string(10)
    }

def generate_data(records_count, metadata_count):
    return [generate_record(i, metadata_count) for i in range(records_count)]

def save_data_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_mongo_data.py <number_of_records> <scientific_metadata_count>")
        sys.exit(1)
    
    # Number of records and metadata fields to generate
    records_count = int(sys.argv[1])
    metadata_count = int(sys.argv[2])
    
    data = generate_data(records_count, metadata_count)
    filename = f"generated_data_{records_count}_{metadata_count}_metadata.json"
    save_data_to_file(data, "Dataset.json")
    print(f"Data saved to {filename}")
