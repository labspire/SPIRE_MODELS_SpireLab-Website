from flask import Flask, request, jsonify
from espnet2.bin.asr_inference import Speech2Text
import librosa
import numpy as np
import os

app = Flask(__name__)

MODEL_BASE = r"C:\hfcache\models--SpireLab--spire_respin_baselines_espnet\snapshots\39a0707aaff9cfc39eea585dac443de0b4b50030\exp_small"

# Language code -> model folder/file mapping (from meta.yaml)
LANGUAGE_CONFIG = {
    "hi": {"folder": "exp_hi", "prefix": "asr_hi_ebf_size256_mlp1024_lin1024_e8_mactrue_bs6M_gacc1", "weight": "valid.acc.ave_5best.pth"},
    "bn": {"folder": "exp_bn", "prefix": "asr_bn_ebf_size256_mlp1024_lin1024_e8_mactrue_bs6M_gacc1", "weight": "valid.acc.ave_5best.pth"},
    "bh": {"folder": "exp_bh", "prefix": "asr_bh_ebf_size256_mlp1024_lin1024_e8_mactrue_bs6M_gacc1", "weight": "valid.acc.ave_5best.pth"},
    "ch": {"folder": "exp_ch", "prefix": "asr_ch_ebf_size256_mlp1024_lin1024_e8_mactrue_bs6M_gacc1", "weight": "valid.acc.ave_5best.pth"},
    "kn": {"folder": "exp_kn", "prefix": "asr_kn_ebf_size256_mlp1024_lin1024_e8_mactrue_bs6M_gacc1", "weight": "valid.acc.ave_5best.pth"},
    "mg": {"folder": "exp_mg", "prefix": "asr_mg_ebf_size256_mlp1024_lin1024_e8_mactrue_bs6M_gacc1", "weight": "valid.acc.ave_5best.pth"},
    "mr": {"folder": "exp_mr", "prefix": "asr_mr_ebf_size256_mlp1024_lin1024_e8_mactrue_bs6M_gacc1", "weight": "valid.acc.ave_5best.pth"},
    "mt": {"folder": "exp_mt", "prefix": "asr_mt_ebf_size256_mlp1024_lin1024_e8_mactrue_bs6M_gacc1", "weight": "valid.acc.ave_10best.pth"},
    "te": {"folder": "exp_te", "prefix": "asr_te_ebf_size256_mlp1024_lin1024_e8_mactrue_bs6M_gacc1", "weight": "valid.acc.ave_5best.pth"},
}

# Loaded models are cached here (lazy loading: loaded only on first use per language)
loaded_models = {}


def get_model(lang_code):
    """Load a language model if it isn't already loaded, and return it."""
    if lang_code not in LANGUAGE_CONFIG:
        raise ValueError(f"Unsupported language: {lang_code}")

    if lang_code not in loaded_models:
        cfg = LANGUAGE_CONFIG[lang_code]
        model_dir = os.path.join(MODEL_BASE, cfg["folder"], cfg["prefix"])
        print(f"[Loading] loading model for language: {lang_code} ...")
        loaded_models[lang_code] = Speech2Text(
            asr_train_config=os.path.join(model_dir, "config.yaml"),
            asr_model_file=os.path.join(model_dir, cfg["weight"]),
        )
        print(f"[Loaded] model ready for language: {lang_code}")

    return loaded_models[lang_code]


@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file received"}), 400

    lang_code = request.form.get("language", "hi")
    audio_file = request.files["audio"]

    # Keep the original file extension so the decoder can detect the format correctly
    original_name = audio_file.filename or "upload.wav"
    ext = os.path.splitext(original_name)[1] or ".wav"
    temp_path = f"temp_upload{ext}"
    audio_file.save(temp_path)

    try:
        # librosa can decode mp3, m4a, wav, etc. and resamples straight to 16kHz mono
        speech, rate = librosa.load(temp_path, sr=16000, mono=True)

        model = get_model(lang_code)
        result = model(speech)
        text, *_ = result[0]

        return jsonify({"success": True, "language": lang_code, "transcription": text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ASR server is running", "loaded_languages": list(loaded_models.keys())})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)