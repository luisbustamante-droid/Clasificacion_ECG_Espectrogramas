import pytest
import torch
from utils.utils_models import build_model

MODEL_PATHS = {
    "mobilenetv3_large": "models/mobilenet_v3_large_best_ema.pt",
    "efficientnet_v2_b0": "models/efficientnet_v2_b0_best_ema.pt",
    "resnet50": "models/resnet50_best_ema.pt",
}

 
# 1. Test de construcción de arquitecturas
@pytest.mark.parametrize("arch", ["mobilenetv3_large", "efficientnet_v2_b0", "resnet50"])
def test_model_build_and_output_shape(arch):
    model = build_model(arch, num_classes=5)
    x = torch.randn(2, 3, 224, 224)
    out = model(x)
    assert out.shape == (2, 5), f"Salida incorrecta para {arch}"

 
# 2. Test de carga de checkpoints
@pytest.mark.parametrize("arch,path", MODEL_PATHS.items())
def test_model_load_weights(arch, path):
    model = build_model(arch, num_classes=5)
    state = torch.load(path, map_location="cpu")
    model.load_state_dict(state)
    model.eval()
    assert all(param.requires_grad for param in model.parameters())
    assert isinstance(state, dict)

 
# 3. Test de salida de probabilidades normalizadas
def test_model_softmax_probabilities():
    model = build_model("mobilenetv3_large", num_classes=5)
    x = torch.randn(1, 3, 224, 224)
    with torch.no_grad():
        y = torch.nn.functional.softmax(model(x), dim=1)
    assert torch.isclose(y.sum(), torch.tensor(1.0), atol=1e-5)
