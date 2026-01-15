☃️ ComfyUI-Portrait-Score
ComfyUI-Portrait-Score is a custom ComfyUI node designed to quantitatively evaluate portrait image quality and enable automatic image filtering, ranking, and decision-making in portrait-centric generation pipelines.
Instead of relying on subjective visual inspection, this node aggregates multiple low-level image quality metrics into a single normalized portrait quality score, making it suitable for automation, gating, and conditional execution in complex workflows.

---
🚀 Why Portrait Score?
In portrait-focused ComfyUI workflows (e.g. AI influencers, character LoRAs, face-centric pipelines):
- Large numbers of images are generated per batch
- Many outputs are blurred, noisy, poorly exposed, or color-shifted
- Expensive downstream nodes (FaceDetailer, upscalers, refiners) are often applied blindly
👉 Portrait-Score solves this by acting as a quality gate.
It allows you to:
- Automatically reject unusable portraits
- Only upscale / refine high-quality images
- Avoid wasted compute on bad generations
- Build fully automated, quality-aware pipelines

---
🧠 How It Works
The node does no image analysis itself.
 Instead, it aggregates outputs from existing image-analysis nodes into a single score.
Input Metrics (5 Core Signals)
暂时无法在飞书文档外展示此内容
Each metric is normalized and direction-corrected (higher = better), then combined using empirically tuned weights optimized for portrait usability.

---
📊 Output
The node produces three outputs:
- portrait_quality_score
 A float value in range 0.0 – 1.0
- portrait_quality_level
 Human-readable classification:
  - Reject (0.00–0.40)
  - Acceptable (0.41–0.70)
  - Good (0.71–0.85)
  - Excellent (0.86–1.00)
- debug_breakdown
 Weighted contribution of each metric for debugging and tuning

---
🧪 Example Results
❌ Low-Quality Portrait (Rejected)
Blurry, low-focus portrait correctly classified as Reject:
[图片]

---
✅ High-Quality Portrait (Excellent)
Sharp, well-lit portrait classified as Excellent and suitable for production use:
[图片]

---
🧩 Typical Use Cases
- Automated image filtering before upscaling
- Conditional execution of FaceDetailer / refinement nodes
- Batch ranking of portrait generations
- Quality-aware dataset curation
- Compute cost reduction in large pipelines

---
📦 Installation
3486. Copy or clone this repository into your ComfyUI custom nodes directory:
cd ComfyUI/custom_nodes
git clone https://github.com/<YOUR_GITHUB_USERNAME>/ComfyUI-Portrait-Score.git
2. Restart ComfyUI
The node will appear as:
☃️ Portrait_Score

---
🧱 Dependencies
This project relies on standard scientific Python libraries commonly used in ComfyUI environments:
- numpy
- opencv-python
- torch
(Exact requirements are listed in requirements.txt / pyproject.toml.)

---
📚 Credits & Acknowledgement
This project was developed as an independent extension built on top of an existing image analysis toolkit ecosystem for ComfyUI.
The original toolkit provides a rich set of low-level image quality metrics, which made it possible to design higher-level scoring and automation logic focused specifically on portrait usability.

---
📄 License
MIT License

---
🧠 Author Notes
This node was built for real-world production workflows, not academic scoring.
 All weights and thresholds were tuned using actual portrait generation failures vs usable outputs, with the goal of maximizing automation reliability and compute efficiency.
