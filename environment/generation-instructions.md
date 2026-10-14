# Candidate-A / Paper A — Full Pipeline Reproduction Runbook (Tier 2 Documented Reference)

This runbook documents the complete end-to-end execution pipeline from raw image generation to facial identity measurement. Executing this pipeline requires specialized GPU hardware and external weights.

## 1. System Requirements
- **OS:** Linux (Ubuntu 20.04/22.04 LTS x86_64) or Windows WSL2.
- **GPU:** NVIDIA GPU with $\ge 16$ GB VRAM (RTX 3090, 4090, A100, or V100).
- **CUDA:** 11.8 with cuDNN 8.x.
- **Python Environment:** Conda environment with Python 3.9.25, PyTorch 2.1.2+cu118, Diffusers 0.27.2.

## 2. Upstream Checkpoints & Benchmark Acquisition
1. **Stable Diffusion v1.5:**
   - Clone or download `runwayml/stable-diffusion-v1-5` from Hugging Face Hub.
2. **UniPortrait:**
   - Upstream repository: `https://github.com/junjiehe96/UniPortrait.git` (Commit: `a4deff2b48e3f67c8466905f27b5a662fc9e912e`).
   - Download the official pretrained attention adapter checkpoint into `models/uniportrait/`.
3. **InsightFace Buffalo_L:**
   - Download the official Antelopev2 / Buffalo_L ONNX models (`w600k_r50.onnx`, `det_10g.onnx`, `2d106det.onnx`) into `~/.insightface/models/buffalo_l/`.
4. **MultiHuman-Testbench Dataset:**
   - Clone `https://github.com/Qualcomm-AI-research/MultiHuman-Testbench.git` (Commit: `ff9f1209a8d90d9ac42db87c7c319e8ee6a1d0db`).
   - Acquire reference portraits from official benchmark instructions (FFHQ, SFHQ, CelebA-HQ).

## 3. Step-by-Step Pipeline Execution
1. **PRE Baseline Generation:**
   ```bash
   python tools/candidate_a_confirmatory/run_pre_accrual.py --seed 101 --steps 25
   ```
2. **Study 1 POST Generation (Action A1 & Action A0):**
   ```bash
   python tools/candidate_a_confirmatory/run_confirmatory_post_generation.py --action a1
   python tools/candidate_a_confirmatory/run_confirmatory_post_generation.py --action a0
   ```
3. **Study 2 POST Generation (Action A2 Native Dual-ID):**
   ```bash
   python tools/candidate_a_study2_a2/run_a2_generation.py --seeds 1101,2202,3303
   ```
4. **Distance-IoU (DIoU) Structural Correspondence:**
   ```bash
   python tools/candidate_a_confirmatory/run_a1_structural_correspondence.py
   python tools/candidate_a_study2_a2/run_a2_structural_correspondence.py
   ```
5. **Buffalo_L Identity Measurement:**
   ```bash
   python tools/candidate_a_confirmatory/run_confirmatory_identity_measurement.py
   python tools/candidate_a_study2_a2/run_a2_identity_measurement.py
   ```
