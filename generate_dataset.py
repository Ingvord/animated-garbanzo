import json
import uuid
import datetime
import argparse

def generate_scicat_dataset(metadata_count):
    """Generates a SciCat-compatible dataset record with a specified number of metadata fields."""

    dataset = {
        "ownerGroup": "testGroup",
        "accessGroups": ["public"],
        "instrumentGroup": "defaultGroup",
        "owner": "John Doe",
        "ownerEmail": "john.doe@example.com",
        "orcidOfOwner": "0000-0002-1825-0097",
        "contactEmail": "contact@example.com",
        "sourceFolder": "/data/source",
        "sourceFolderHost": "host.example.com",
        "size": 1024,
        "packedSize": 512,
        "numberOfFiles": 10,
        "numberOfFilesArchived": 5,
        "creationTime": datetime.datetime.utcnow().isoformat(),
        "validationStatus": "valid",
        "keywords": ["test", "benchmark", "SciCat"],
        "description": "Benchmark dataset for SciCat ingestion performance testing.",
        "datasetName": f"Test Dataset {metadata_count} fields",
        "classification": "experiment",
        "license": "CC-BY-4.0",
        "isPublished": False,
        "sharedWith": [],
        "relationships": [],
        "datasetlifecycle": {},
        "scientificMetadata": {},
        "comment": "Automated dataset generation for ingestion performance testing.",
        "dataQualityMetrics": 95.5,
        "principalInvestigator": "Dr. John Smith",
        "startTime": datetime.datetime.utcnow().isoformat(),
        "endTime": datetime.datetime.utcnow().isoformat(),
        "creationLocation": "Test Facility",
        "dataFormat": "HDF5",
        "inputDatasets": [],
        "usedSoftware": ["SciCat Ingestor"],
        "jobParameters": {},
        "jobLogData": "Successful ingestion",
        "runNumber": "42",
        "type": "raw"  # Ensuring it's explicitly set as "raw"
    }    

    # Generate metadata fields dynamically
    for i in range(1, metadata_count + 1):
        dataset["scientificMetadata"][f"field_{i}"] = {"value": f"Sample data {i}", "unit": "unit"}

    return dataset

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate SciCat dataset with a specified number of metadata fields.")
    parser.add_argument("metadata_count", type=int, help="Number of metadata fields to include in the dataset.")

    args = parser.parse_args()
    
    dataset = generate_scicat_dataset(args.metadata_count)
    
    with open("upload.json", "w") as f:
        json.dump(dataset, f, indent=4)

    print(f"SciCat dataset with {args.metadata_count} metadata fields saved to upload.json")
