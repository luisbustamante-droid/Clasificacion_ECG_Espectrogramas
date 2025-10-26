import torch
from utils.utils_models import build_model
from utils.utils_spectrograms import signal_to_spec_img
from utils.utils_ecg import (
    load_record_from_wfdb_zip,
    validate_wfdb_zip_structure,
    get_aami_distribution_from_base
)

 
# 1. Test de inicialización del modelo
def test_inference_initialization():
    model = build_model("mobilenetv3_large", num_classes=5)
    model.eval()
    assert callable(model.forward), "El modelo no tiene método forward"

 
# 2. Test de pipeline de inferencia
def test_inference_pipeline():
    model = build_model("efficientnet_v2_b0", num_classes=5)
    model.eval()
    x = torch.randn(1, 3, 224, 224)
    with torch.no_grad():
        out = model(x)
        pred = torch.argmax(out, dim=1).item()
    assert 0 <= pred <= 4, "Predicción fuera de rango de clases AAMI"

 
# 3. Test de validación de ZIPs de registros WFDB (app clínica)
def test_validate_wfdb_zip(tmp_path):
    dummy_zip = tmp_path / "sample.zip"
    dummy_zip.write_bytes(b"")
    result = validate_wfdb_zip_structure(dummy_zip)
    assert isinstance(result, bool)

 
# 4. Test de distribución AAMI simulada
def test_aami_distribution_from_base():
    dist = get_aami_distribution_from_base("mitdb")
    assert isinstance(dist, dict)
    assert all(k in ["N", "S", "V", "F", "Q"] for k in dist.keys())
