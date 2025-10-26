import pytest
import numpy as np
import torch
from utils.utils_ecg import (
    load_record, get_rpeaks, extract_windows_from_rpeaks, WindowCfg
)
from utils.utils_spectrograms import signal_to_spec_img, SpecCfg
from utils.dataset import ECGSpecDataset

 
# 1. Test de carga y preprocesamiento de señales ECG 
def test_load_record_shape():
    signal, fs = load_record("100", db="mitdb")
    assert signal.ndim == 2, "La señal debe tener dos canales"
    assert fs in [360, 128], "Frecuencia de muestreo inesperada"

def test_rpeaks_detection():
    signal, fs = load_record("100", db="mitdb")
    rpeaks = get_rpeaks(signal, fs)
    assert len(rpeaks) > 0, "No se detectaron R-peaks"
    assert all(isinstance(r, int) for r in rpeaks), "R-peaks deben ser enteros"

 
# 2. Test de extracción de ventanas centradas en R-peaks
def test_window_extraction():
    signal, fs = load_record("100", db="mitdb")
    rpeaks = get_rpeaks(signal, fs)
    cfg = WindowCfg(window_sec=2.5, stride_sec=0.5)
    windows = extract_windows_from_rpeaks(signal, fs, rpeaks, cfg)
    assert isinstance(windows, list)
    assert windows[0].shape[0] == int(fs * cfg.window_sec)

 
# 3. Test de generación de espectrogramas STFT
def test_spectrogram_generation():
    signal = np.random.randn(900)
    spec = signal_to_spec_img(signal, fs=360)
    assert spec.shape == (224, 224, 3), "El espectrograma debe ser 224x224 RGB"
    assert not np.isnan(spec).any(), "El espectrograma contiene NaN"

 
# 4. Test de Dataset y caching
def test_dataset_output_shapes():
    ds = ECGSpecDataset(split="val")
    x, y = ds[0]
    assert isinstance(x, torch.Tensor)
    assert x.shape[-1] == 224
    assert isinstance(y, int)
