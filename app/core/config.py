import ast
import torch

# =========================
# Paths & Model Configuration
# =========================

DATA_PATH = r"data/sales_dataset.xlsx"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

MAX_NEW_TOKENS = 128

MODEL_NAME = "qwen-plus"
API_KEY_ENV_VAR = "DASHSCOPE_API_KEY"
BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

MAX_RETRIES = 5