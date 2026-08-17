"""Generate a synthetic hand X-ray DICOM for pipeline smoke tests.

Writes a single-frame DX study that satisfies the tags DICOMDataLoaderOperator
and the SERIES_RULES selector in hand_osteo/app.py both require. Content is
meaningless; only the metadata matters.

Usage: python tools/make_test_dicom.py [output_dir]
"""

import sys
from pathlib import Path

import numpy as np
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid

OUTPUT_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("input")


def build() -> Dataset:
    ds = Dataset()

    ds.file_meta = FileMetaDataset()
    ds.file_meta.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.1.1.1"
    ds.file_meta.MediaStorageSOPInstanceUID = generate_uid()
    ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    ds.file_meta.ImplementationClassUID = generate_uid()

    ds.SOPClassUID = ds.file_meta.MediaStorageSOPClassUID
    ds.SOPInstanceUID = ds.file_meta.MediaStorageSOPInstanceUID
    ds.StudyInstanceUID = generate_uid()
    ds.SeriesInstanceUID = generate_uid()

    ds.PatientName = "Test^Hand"
    ds.PatientID = "TESTHAND001"
    ds.PatientBirthDate = "19700101"
    ds.PatientSex = "O"

    # Matched by SERIES_RULES in hand_osteo/app.py.
    ds.Modality = "DX"
    ds.BodyPartExamined = "HAND"

    ds.StudyDate = "20260817"
    ds.StudyTime = "100000"
    ds.SeriesDate = ds.StudyDate
    ds.SeriesTime = ds.StudyTime
    ds.ContentDate = ds.StudyDate
    ds.ContentTime = ds.StudyTime
    ds.AccessionNumber = "ACC000001"
    ds.StudyID = "1"
    ds.SeriesNumber = 1
    ds.InstanceNumber = 1
    ds.StudyDescription = "Synthetic hand radiograph"
    ds.SeriesDescription = "Synthetic hand radiograph"

    rows, cols = 256, 256
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.Rows = rows
    ds.Columns = cols
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 15
    ds.PixelRepresentation = 0
    ds.PixelSpacing = [r"0.1", r"0.1"]
    ds.RescaleIntercept = "0"
    ds.RescaleSlope = "1"

    rng = np.random.default_rng(0)
    ds.PixelData = rng.integers(0, 4096, size=(rows, cols), dtype=np.uint16).tobytes()

    return ds


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / "test_hand_xray.dcm"
    build().save_as(path, write_like_original=False)
    print(f"wrote {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
