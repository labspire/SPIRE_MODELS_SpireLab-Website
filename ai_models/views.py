from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, Http404
import requests

# 1. Main Dashboard/Home Page View
def home_view(request):
    return render(request, 'home.html')

# 2. Complete Languages Directory Portal
def languages_page(request):
    return render(request, 'Language.html')

# 3. Models Central Hub Landing View
def models_page(request):
    return render(request, 'Models.html')

# 4. ASR Pipeline Portal (Connected to local Flask ASR inference server)
def model_detail_asr(request):
    transcript = None
    error = None
    selected_language = None

    if request.method == 'POST' and request.FILES.get('audio_file'):
        uploaded_file = request.FILES['audio_file']
        selected_language = request.POST.get('language', 'hi')

        try:
            files = {'audio': (uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)}
            data = {'language': selected_language}

            response = requests.post(
                'http://127.0.0.1:5001/transcribe',
                files=files,
                data=data,
                timeout=120
            )

            result = response.json()

            if result.get('success'):
                transcript = result.get('transcription')
            else:
                error = result.get('error', 'Unknown error from ASR server')

        except requests.exceptions.ConnectionError:
            error = "Could not connect to the ASR server. Is it running? (127.0.0.1:5001)"
        except Exception as e:
            error = str(e)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'transcript': transcript,
                'error': error,
                'selected_language': selected_language,
            })

    return render(request, 'model_asr.html', {
        'transcript': transcript,
        'error': error,
        'selected_language': selected_language,
    })

# 5. Language Identification (LID) Portal View
def model_detail_lid(request):
    return render(request, 'model_lid.html')

# 6. Dialect Identification Portal View
def model_detail_dialect(request):
    return render(request, 'model_dialect.html')

# 7. Model Performance Benchmarks Ledger View
LANG_COLUMNS = [
    ("bh", "Bhojpuri"), ("bn", "Bengali"), ("ch", "Chhattisgarhi"), ("hi", "Hindi"),
    ("kn", "Kannada"), ("mg", "Magahi"), ("mr", "Marathi"), ("mt", "Maithili"), ("te", "Telugu"),
]

MODELS_DATA = [
    {
        "model": "SeamlessM4T-v2-Large", "category": "Pretrained Models (fine-tuned on non-RESPIN public data)",
        "hf_link": "https://huggingface.co/facebook/seamless-m4t-v2-large",
        "cer": {"bh": 29.09, "bn": 17.54, "ch": 33.20, "hi": 15.34, "kn": 18.91, "mg": 30.07, "mr": 14.44, "mt": 27.15, "te": 14.33, "avg": 22.23},
        "wer": {"bh": 56.77, "bn": 45.56, "ch": 71.86, "hi": 25.43, "kn": 55.38, "mg": 56.49, "mr": 42.09, "mt": 66.64, "te": 46.11, "avg": 51.81},
    },
    {
        "model": "IndicW2V", "category": "Pretrained Models (fine-tuned on non-RESPIN public data)",
        "hf_link": "https://github.com/AI4Bharat/IndicWav2Vec",
        "cer": {"bh": 17.08, "bn": 14.27, "ch": 22.77, "hi": 11.02, "kn": 10.37, "mg": 19.64, "mr": 15.09, "mt": 23.30, "te": 8.61, "avg": 15.80},
        "wer": {"bh": 51.61, "bn": 42.83, "ch": 65.98, "hi": 28.34, "kn": 42.37, "mg": 54.32, "mr": 53.91, "mt": 66.10, "te": 37.82, "avg": 49.25},
    },
    {
        "model": "SPRING-W2V2", "category": "Pretrained Models (fine-tuned on non-RESPIN public data)",
        "hf_link": "https://asr.iitm.ac.in/models",
        "cer": {"bh": 15.10, "bn": 12.50, "ch": 20.81, "hi": 8.80, "kn": 11.43, "mg": 16.35, "mr": 7.56, "mt": 20.12, "te": 6.97, "avg": 13.29},
        "wer": {"bh": 41.32, "bn": 25.93, "ch": 55.42, "hi": 22.99, "kn": 44.35, "mg": 42.09, "mr": 34.15, "mt": 53.69, "te": 36.32, "avg": 39.58},
    },
    {
        "model": "SPRING-Data2Vec-AQC", "category": "Pretrained Models (fine-tuned on non-RESPIN public data)",
        "hf_link": "https://asr.iitm.ac.in/models",
        "cer": {"bh": 15.02, "bn": 11.94, "ch": 21.26, "hi": 7.20, "kn": 10.78, "mg": 15.81, "mr": 7.49, "mt": 19.91, "te": 6.53, "avg": 12.88},
        "wer": {"bh": 42.35, "bn": 23.69, "ch": 56.17, "hi": 20.93, "kn": 42.79, "mg": 42.47, "mr": 33.40, "mt": 53.65, "te": 33.98, "avg": 38.83},
    },
    {
        "model": "TDNN-HMM", "category": "Traditional Models (trained from scratch on RESPIN subset)",
        "hf_link": "https://github.com/labspire/respin_baselines",
        "cer": {"bh": 5.67, "bn": 5.22, "ch": 4.45, "hi": 3.25, "kn": 4.88, "mg": 7.69, "mr": 3.30, "mt": 6.53, "te": 3.94, "avg": 4.99},
        "wer": {"bh": 17.57, "bn": 16.87, "ch": 12.69, "hi": 8.72, "kn": 23.01, "mg": 22.33, "mr": 13.40, "mt": 20.13, "te": 20.81, "avg": 17.28},
    },
    {
        "model": "E-Branchformer", "category": "Traditional Models (trained from scratch on RESPIN subset)",
        "hf_link": "https://huggingface.co/SpireLab/spire_respin_baselines_espnet",
        "cer": {"bh": 4.95, "bn": 4.33, "ch": 3.63, "hi": 3.52, "kn": 4.62, "mg": 6.68, "mr": 3.19, "mt": 5.75, "te": 3.97, "avg": 4.52},
        "wer": {"bh": 15.21, "bn": 14.96, "ch": 10.59, "hi": 9.94, "kn": 24.50, "mg": 20.38, "mr": 14.48, "mt": 17.95, "te": 21.64, "avg": 16.63},
    },
    {
        "model": "Whisper-Tiny", "category": "Fine-tuned Models (fine-tuned on RESPIN subset)",
        "hf_link": "https://github.com/labspire/respin_baselines",
        "cer": {"bh": 9.62, "bn": 11.60, "ch": 7.13, "hi": 9.69, "kn": 12.62, "mg": 13.98, "mr": 9.15, "mt": 10.73, "te": 11.43, "avg": 10.66},
        "wer": {"bh": 27.45, "bn": 32.51, "ch": 20.81, "hi": 21.71, "kn": 48.54, "mg": 36.40, "mr": 30.93, "mt": 31.96, "te": 41.61, "avg": 32.44},
    },
    {
        "model": "Whisper-Base", "category": "Fine-tuned Models (fine-tuned on RESPIN subset)",
        "hf_link": "https://github.com/labspire/respin_baselines",
        "cer": {"bh": 7.15, "bn": 7.69, "ch": 5.36, "hi": 5.80, "kn": 8.10, "mg": 10.44, "mr": 6.23, "mt": 7.51, "te": 7.51, "avg": 7.31},
        "wer": {"bh": 22.51, "bn": 24.71, "ch": 16.67, "hi": 15.19, "kn": 36.52, "mg": 30.54, "mr": 24.28, "mt": 24.80, "te": 32.99, "avg": 25.36},
    },
    {
        "model": "Whisper-Small", "category": "Fine-tuned Models (fine-tuned on RESPIN subset)",
        "hf_link": "https://github.com/labspire/respin_baselines",
        "cer": {"bh": 7.90, "bn": 5.46, "ch": 3.85, "hi": 4.16, "kn": 6.00, "mg": 7.46, "mr": 3.93, "mt": 5.94, "te": 6.54, "avg": 5.69},
        "wer": {"bh": 19.02, "bn": 18.91, "ch": 12.36, "hi": 11.78, "kn": 29.66, "mg": 23.94, "mr": 16.95, "mt": 20.28, "te": 27.82, "avg": 20.08},
    },
    {
        "model": "IndicW2V (fine-tuned)", "category": "Fine-tuned Models (fine-tuned on RESPIN subset)",
        "hf_link": "https://github.com/labspire/respin_baselines",
        "cer": {"bh": 4.42, "bn": 4.28, "ch": 3.24, "hi": 3.16, "kn": 4.68, "mg": 6.02, "mr": 3.19, "mt": 5.19, "te": 4.54, "avg": 4.30},
        "wer": {"bh": 16.07, "bn": 16.65, "ch": 11.36, "hi": 10.47, "kn": 24.86, "mg": 21.51, "mr": 15.13, "mt": 19.19, "te": 24.03, "avg": 17.69},
    },
    {
        "model": "SPRING-W2V2 (fine-tuned)", "category": "Fine-tuned Models (fine-tuned on RESPIN subset)",
        "hf_link": "https://github.com/labspire/respin_baselines",
        "cer": {"bh": 3.92, "bn": 3.86, "ch": 2.99, "hi": 2.37, "kn": 4.30, "mg": 5.20, "mr": 2.49, "mt": 4.37, "te": 3.85, "avg": 3.71},
        "wer": {"bh": 14.61, "bn": 15.12, "ch": 10.74, "hi": 8.22, "kn": 23.90, "mg": 19.40, "mr": 12.75, "mt": 16.64, "te": 21.92, "avg": 15.92},
    },
    {
        "model": "SPRING-Data2Vec-AQC (fine-tuned)", "category": "Fine-tuned Models (fine-tuned on RESPIN subset)",
        "hf_link": "https://github.com/labspire/respin_baselines",
        "cer": {"bh": 3.95, "bn": 3.63, "ch": 2.84, "hi": 2.27, "kn": 4.11, "mg": 4.98, "mr": 2.38, "mt": 4.30, "te": 3.72, "avg": 3.58},
        "wer": {"bh": 14.84, "bn": 14.15, "ch": 10.25, "hi": 7.91, "kn": 23.13, "mg": 18.50, "mr": 12.28, "mt": 16.41, "te": 21.17, "avg": 15.40},
    },
]


def leaderboard_page(request):
    metric = request.GET.get('metric', 'both')
    if metric not in ('both', 'wer', 'cer'):
        metric = 'both'

    valid_lang_codes = [c for c, _ in LANG_COLUMNS]
    language = request.GET.get('language', valid_lang_codes[0])
    if language not in valid_lang_codes:
        language = valid_lang_codes[0]

    sort_key = request.GET.get('sort', 'wer_avg')
    order = request.GET.get('order', 'asc')

    valid_metric_cols = [f"cer_{c}" for c, _ in LANG_COLUMNS] + ["cer_avg"] + \
                         [f"wer_{c}" for c, _ in LANG_COLUMNS] + ["wer_avg"]
    valid_keys = valid_metric_cols + ["model"]
    if sort_key not in valid_keys:
        sort_key = 'wer_avg'

    rows = list(MODELS_DATA)

    def sort_value(m):
        if sort_key == 'model':
            return m['model'].lower()
        met, col = sort_key.split('_', 1)
        val = m[met].get(col)
        return val if val is not None else float('inf')

    rows = sorted(rows, key=sort_value, reverse=(order == 'desc'))

    display_rows = []
    for i, m in enumerate(rows, start=1):
        cer_cells = [{"code": code, "val": m["cer"].get(code)} for code, _ in LANG_COLUMNS]
        wer_cells = [{"code": code, "val": m["wer"].get(code)} for code, _ in LANG_COLUMNS]
        display_rows.append({
            "rank": i,
            "model": m["model"],
            "hf_link": m.get("hf_link", ""),
            "category": m["category"],
            "cer_cells": cer_cells,
            "wer_cells": wer_cells,
            "cer_avg": m["cer"]["avg"],
            "wer_avg": m["wer"]["avg"],
        })

    lang_name_map = dict(LANG_COLUMNS)
    current_language_name = lang_name_map.get(language, language)
    metric_labels = {
        "both": "Both (CER & WER)",
        "wer": "WER (Word Error Rate)",
        "cer": "CER (Character Error Rate)",
    }
    current_metric_label = metric_labels.get(metric, "Both (CER & WER)")

    context = {
        "rows": display_rows,
        "lang_columns": LANG_COLUMNS,
        "current_sort": sort_key,
        "current_order": order,
        "current_metric": metric,
        "current_metric_label": current_metric_label,
        "current_language": language,
        "current_language_name": current_language_name,
    }

    # If this request came from JavaScript (AJAX), return JSON instead of a full page reload
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(context)

    return render(request, 'leaderboard.html', context)

# 8. Cross-Verification Comparison Console View
def compare_page(request):
    return render(request, 'compare.html')

# 9. Developer Cryptographic API Access View
def api_keys_page(request):
    return render(request, 'api_keys.html')

# 10. Research Publications Archive View
PUBLICATIONS = [
    {
        "slug": "dialect-id-multimodal-asr-2025",
        "title": "Improving Dialect Identification in Indian Languages Using Multimodal Features from Dialect Informed ASR",
        "authors": "Amartyaveer, Saurabh Kumar, Sumit Sharma, Sathvik Udupa, Sandhya Badiger, Abhayjeet Singh, Deekshitha G, Jesuraja Bandekar, Savitha Murthy, Prasanta Kumar Ghosh",
        "venue": "Accepted in ICASSP 2025",
        "year": 2025,
        "doi": "https://doi.org/10.1109/ICASSP49660.2025.10889099",
        "abstract": "Dialect identification (DID) addresses the challenge of recognizing regional variations within a language. The current deep learning approaches focus on audio-only, text-only, or multi-task setups combining automatic speech recognition (ASR) with DID. This work introduces a novel multimodal architecture that leverages speech and text features to enhance DID performance. Our method integrates ASR-generated speech representations with text embeddings derived from ASR hypotheses using a RoBERTa-based encoder. Additionally, we perform a layer-wise analysis of the IndicWav2Vec model to identify the layers most effective for extracting dialectal features. We evaluate our approach on a subset of the RESPIN dataset featuring eight Indian languages and 33 dialects. Experimental results show that our proposed multimodal DID system achieves an average DID accuracy of 79.81%, consistently outperforming baseline methods. This study is the first to analyse comprehensively DID in Indian languages, providing new insights into their dialectal diversity.",
    },
    {
        "slug": "jointly-improving-dialect-asr-2025",
        "title": "Jointly Improving Dialect Identification and ASR in Indian Languages using Multimodal Feature Fusion",
        "authors": "Saurabh Kumar, Amartyaveer, Prasanta Kumar Ghosh",
        "venue": "INTERSPEECH 2025",
        "year": 2025,
        "doi": "",
        "abstract": "Automatic Speech Recognition (ASR) and Dialect Identification (DID) are crucial for Indian languages, many of which are low-resource and exhibit significant dialectal differences. Existing methods often optimize ASR or DID individually, resulting in performance trade-offs. In this work, we propose a multimodal framework that jointly improves ASR and DID. Our method employs a Bottleneck Encoder to extract dialectal features from Conformer-based speech representations and a RoBERTa encoder to process ASR-generated CTC embeddings. A gating mechanism merges these features, followed by an attention encoder to refine the representations. The learned embeddings are concatenated with Conformer outputs to enhance ASR features. Evaluated on eight Indian languages with thirty-three dialects, our method achieves an average DID accuracy of 81.63% and average CER and WER of 4.65% and 17.73%, respectively. These results highlight the effectiveness of our method for joint ASR-DID modeling.",
    },
    {
        "slug": "madasr-2-0-challenge-2025",
        "title": "MADASR 2.0: Multi-Lingual Multi-Dialect ASR Challenge in 8 Indian Languages",
        "authors": "Saurabh Kumar, Sumit Sharma, Deekshitha G, Abhayjeet Singh, Amartya veer, Sathvik Udupa, Sandhya Badiger, and et. al.",
        "venue": "IEEE ASRU 2025",
        "year": 2025,
        "doi": "",
        "abstract": "We present MADASR 2.0, a challenge at ASRU 2025 aimed at advancing multilingual and multidialectal automatic speech recognition (ASR) in low-resource Indian languages. Building on the 2023 edition, it introduces a subset of the RESPIN corpus, over 1200 hours of read speech across 8 languages and 33 dialects, with test sets including both read and spontaneous speech. The challenge comprises four tracks varying by training data size and external resource usage, and supports auxiliary tasks like language and dialect identification. We detail the dataset, tasks, baselines, and submissions and analyse trends across tracks and speech styles. Results highlight the continued difficulty of spontaneous ASR, the benefits of multitask and transfer learning, and effective strategies for building dialect-aware ASR systems. MADASR 2.0 offers a standardised benchmark to support future research on inclusive and scalable ASR for linguistically diverse populations.",
    },
    {
        "slug": "respin-s1-corpus-2025",
        "title": "RESPIN-S1.0 Corpus: A read speech corpus of 10000+ hours in dialects of nine Indian Languages",
        "authors": "Saurabh Kumar, Abhayjeet Singh, Deekshitha G, Amartyaveer, Jesuraj Bandekar, Savitha Murthy, Sumit Sharma, Sandhya Badiger, Sathvik Udupa, Amala Nagireddi, Srinivasa Raghavan K M, Rohan Saxena, Jai Nanavati",
        "venue": "NeurIPS Datasets & Benchmarks Track 2025",
        "year": 2025,
        "doi": "https://openreview.net/forum?id=qL8M2dOY4L",
        "abstract": "We introduce RESPIN-S1.0, the largest publicly available dialect-rich read speech corpus for Indian languages, comprising over 10,000 hours of validated audio spanning nine major languages -- Bengali, Bhojpuri, Chhattisgarhi, Hindi, Kannada, Magahi, Maithili, Marathi, and Telugu. Indian languages are characterized by high dialectal variation and are spoken by populations that are often digitally underserved. Existing speech corpora typically represent only standard dialects and lack domain relevance. RESPIN-S1.0 fills this critical gap by collecting speech across 38+ dialects and two high-impact domains: agriculture and finance. Text data was carefully composed by native dialect speakers and validated via a robust pipeline involving both automatic and manual checks. Over 200,000 utterances were recorded through a crowdsourced mobile application by native speakers and subsequently categorized into clean, semi-noisy, and noisy slabs based on transcription quality. The clean slab alone exceeds 10,000 hours. RESPIN also provides speaker metadata, phonetic lexicons, and dialect-aware train-dev-test splits to ensure reproducibility. To benchmark performance, we evaluate a range of ASR models -- TDNN-HMM, E-Branchformer, Whisper, IndicWav2Vec2, and SPRING SSL models -- and find that fine-tuning on RESPIN significantly improves recognition accuracy over existing pretrained models. A subset of RESPIN-S1.0 has already supported community efforts through challenges such as the SLT Code Hackathon 2022 and MADASR@ASRU 2023/2025, with over 1200 hours of data released publicly. This resource supports research in dialectal ASR, LID, DID, and speech-related areas, and sets a new standard for inclusive, dialect-rich corpora in multilingual, low-resource settings.",
    },
    {
        "slug": "adapter-pretraining-asr-2024",
        "title": "Adapter pre-training for improved speech recognition in unseen domains using low resource adapter tuning of self-supervised models",
        "authors": "Sathvik Udupa, Jesuraj Bandekar, Saurabh Kumar, Deekshitha G, Sandhya B, Abhayjeet S, Savitha Murthy, Priyanka Pai, Srinivasa Raghavan, Raoul Nanavati, Prasanta Kumar Ghosh",
        "venue": "Accepted in Interspeech 2024",
        "year": 2024,
        "doi": "https://www.isca-archive.org/interspeech_2024/udupa24_interspeech.pdf",
        "abstract": "Adapter tuning is an approach to fine-tune large neural network models on new tasks. These methods can be used to efficiently fine-tune large self-supervised learning (SSL) models for speech recognition tasks. In this work, we aim to perform improved low-resource adaptation of SSL features from source to target domain. Toward this, we experiment with adapter pretraining for Wav2Vec2-based models over different source and target configurations. We experiment over 3 datasets consisting 14 languages, including very low-resource languages. Further, we show the consistency of this method across different adapter dimensions and analyse the feature transformation due to the adapter pre-training process. With the proposed methods, we obtain over 10%-30% relative improvement in WER and CER with Viterbi decoding in 13 languages. Further, we obtain consistent performance gains using LM decoding on many of these languages.",
    },
    {
        "slug": "asr-corpus-chhattisgarhi-2023",
        "title": "An ASR corpus in Chhattisgarhi, a low resource Indian language",
        "authors": "Abhayjeet Singh, Arjun Singh Mehta, Ashish Khuraishi K S, Deekshitha G, Gauri Date, Jai Nanavati, Jesuraja Bandekar, and et. al.",
        "venue": "Springer",
        "year": 2023,
        "doi": "https://link.springer.com/chapter/10.1007/978-3-031-48312-7_14",
        "abstract": "RESPIN is a project that aims to develop a dialect-rich database and some user-friendly voice-technology applications in 9 Indian languages including Chhattisgarhi. The paper elaborates on the entire process of such a low-resource database preparation in a crowd-sourced manner. Through this work we have open-sourced around 250 hours of dialect-rich, domain-rich Chhattisgarhi ASR dataset to popularize the scope of voice technology to the Chhattisgarh population. The paper also describes developing a base model with a WER score of 11.58% on the test set.",
    },
    {
        "slug": "gated-multi-encoders-dialectal-asr-2023",
        "title": "Gated Multi Encoders and Multitask Objectives for Dialectal Speech Recognition in Indian Languages",
        "authors": "Sathvik Udupa, Jesuraja Bandekar, Deekshitha G, Saurabh Kumar, Prasanta Kumar Ghosh, Sandhya Badiger, Abhayjeet Singh, Savitha Murthy, Priyanka Pai, Srinivasa Raghavan, and Raoul Nanavat",
        "venue": "Workshop on Automatic Speech Recognition and Understanding (ASRU) 2023",
        "year": 2023,
        "doi": "https://www.researchgate.net/publication/377548210_Gated_Multi_Encoders_and_Multitask_Objectives_for_Dialectal_Speech_Recognition_in_Indian_Languages",
        "abstract": "In this work, several methods have been proposed towards improving the performance of dialectal automatic speech recognition (ASR). A novel encoder architecture has been introduced that is suited for multi-dialect ASR training. Further, we propose Multi-Task Self-Supervised learning (SSL) fine-tuning using CTC and dialect identification. Additionally, the use of different language models (LM) to improve the performance of dialectal ASR has been investigated. Around 800 hours of Bengali and Bhojpuri data, released as a part of the MADASR ASRU challenge have been used to train these models. The work shows that the proposed multi-encoder ASR observes a relative reduction of 7.5% and 9% in WER in Bhojpuri and Bengali, respectively. Additionally, we also observe a 1-2% WER reduction in fine-tuning SSL, further improving performance in these languages. Moreover, we observe advantages in using dialect-specific LM decoding based on predicted dialect.",
    },
    {
        "slug": "taltech-madasr-2023-challenge",
        "title": "Dialect Adaptation and Data Augmentation for Low-Resource ASR: TalTech Systems for the MADASR 2023 Challenge",
        "authors": "Tanel Alumäe, Jiaming Kong, and Daniil Robnikov",
        "venue": "Workshop on Automatic Speech Recognition and Understanding (ASRU) 2023",
        "year": 2023,
        "doi": "https://synthical.com/article/6b099b42-6e29-45df-acd0-dcc7ef39358f",
        "abstract": "This paper describes Tallinn University of Technology (TalTech) systems developed for the ASRU MADASR 2023 Challenge. The challenge focuses on automatic speech recognition of dialect-rich Indian languages with limited training audio and text data. TalTech participated in two tracks of the challenge: Track 1 that allowed using only the provided training data and Track 3 which allowed using additional audio data. In both tracks, we relied on wav2vec2.0 models. Our methodology diverges from the traditional procedure of finetuning pretrained wav2vec2.0 models in two key points: firstly, through the implementation of the aligned data augmentation technique to enhance the linguistic diversity of the training data, and secondly, via the application of deep prefix tuning for dialect adaptation of wav2vec2.0 models. In both tracks, our approach yielded significant improvements over the provided baselines, achieving the lowest word error rates across all participating teams.",
    },
    {
        "slug": "model-adaptation-asr-low-resource-2023",
        "title": "Model Adaptation for ASR in low-resource Indian Languages",
        "authors": "Abhayjeet Singh, Arjun Singh Mehta, Ashish Khuraishi K S, Deekshitha G, Gauri Date, Jai Nanavati, Jesuraja Bandekar, Karnalius Basumatary, Karthika P, Sandhya Badiger, Sathvik Udupa, Saurabh Kumar, Savitha, Prasanta Kumar Ghosh, and et. al.",
        "venue": "Arxiv Org",
        "year": 2023,
        "doi": "https://arxiv.org/abs/2307.07948",
        "abstract": "Automatic speech recognition (ASR) performance has improved drastically in recent years, mainly enabled by self-supervised learning (SSL) based acoustic models such as wav2vec2 and large-scale multi-lingual training like Whisper. A huge challenge still exists for low-resource languages where the availability of both audio and text is limited. This is further complicated by the presence of multiple dialects like in Indian languages. However, many Indian languages can be grouped into the same families and share the same script and grammatical structure. This is where a lot of adaptation and fine-tuning techniques can be applied to overcome the low-resource nature of the data by utilising well-resourced similar languages.",
    },
]

def publications_page(request):
    years = sorted({pub["year"] for pub in PUBLICATIONS}, reverse=True)

    # Build a short "First Author, et al." version of the author list
    # for the list view, without touching the original full author string.
    publications_by_year = {}
    for year in years:
        year_pubs = []
        for pub in PUBLICATIONS:
            if pub["year"] != year:
                continue
            first_author = pub["authors"].split(",")[0].strip()
            has_more_authors = "," in pub["authors"]
            pub_copy = dict(pub)
            pub_copy["authors_short"] = f"{first_author}, et al." if has_more_authors else first_author
            year_pubs.append(pub_copy)
        publications_by_year[year] = year_pubs

    return render(request, 'publications.html', {
        "years": years,
        "publications_by_year": publications_by_year,
    })

def publication_detail(request, slug):
    pub = next((p for p in PUBLICATIONS if p["slug"] == slug), None)
    if pub is None:
        raise Http404("Publication not found")
    return render(request, 'publication_detail.html', {"pub": pub})