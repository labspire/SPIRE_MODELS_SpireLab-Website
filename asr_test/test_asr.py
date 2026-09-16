from espnet2.bin.asr_inference import Speech2Text
import soundfile as sf

print("Model download ho raha hai, thoda time lagega...")

speech2text = Speech2Text.from_pretrained(
    "SpireLab/spire_respin_baselines_espnet"
)

print("Model load ho gaya! Ab test audio se try karte hain...")

# Test ke liye koi bhi .wav file ka path daalo (16kHz mono recommended)
speech, rate = sf.read("test_audio.wav")
result = speech2text(speech)
text, *_ = result[0]

print("Transcription:", text)