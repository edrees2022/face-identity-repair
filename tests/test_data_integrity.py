import pytest
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

EXPECTED_HASHES = {
    "cohort_n119_safe_manifest.json": "71617c7a42854740bb8bc1d3e459a8d3ddd1ebaef010c24aa80e70a78843233a",
    "study1_inference_summary.json": "8b16f23b8ed9e0896d26d649ff3c74e128f136e5e70f292107ed78930af52561",
    "study1_joint_summary.json": "88fb502afae692014132d7b9007786364926fe690802d777ce600123414c08b6",
    "study2_joint_summary.json": "dd2b9a48a9a49e6327928c593539a730b28dde570ccf17db4a961883b4248fe1",
    "study2_master_paired_input.csv": "373c9f1d0600f47eb5a78aa36b2f54306af738d595ae44c9c99d1008b28efa08",
    "validation_summary.json": "b40fc4e074c2000ab70041c4157d1afa4a3e66ae87a0c22f504b0b87d29d21cd"
}

@pytest.mark.parametrize("filename,expected_hash", sorted(EXPECTED_HASHES.items()))
def test_all_six_public_data_hashes(filename, expected_hash):
    p = DATA_DIR / filename
    assert p.exists(), f"File {filename} missing"
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    assert h == expected_hash, f"Hash mismatch for {filename}"
