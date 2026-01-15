def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(x)))


class PortraitScore:
    """
    人像得分：只做“分数聚合”，不再对 image 做分析
    输入来自本库其它节点的 FLOAT 输出。
    """

    # 固定权重（人像）
    W_SHARPNESS = 0.35
    W_CLIPPING = 0.25
    W_NOISE = 0.20
    W_CAST = 0.12
    W_CONTRAST = 0.08
    SHARPNESS_NORM_MAX = 0.10
    NOISE_NORM_MAX = 2000.0
    CAST_NORM_MAX = 0.25
    CONTRAST_NORM_MAX = 80.0

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "sharpness_score": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001}),
                "clipping_score": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.0001}),
                "noise_score": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 100000.0, "step": 1.0}),
                "cast_score": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.0001}),
                "contrast_score": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1000.0, "step": 0.1}),

            }
        }

    RETURN_TYPES = ("FLOAT", "STRING", "STRING")
    RETURN_NAMES = ("portrait_quality_score", "portrait_quality_level", "debug_breakdown")
    FUNCTION = "score"
    CATEGORY = "Image Analysis"

    def _level(self, s: float) -> str:
        if s <= 0.40:
            return "Reject (0.00–0.40)"
        if s <= 0.65:
            return "Acceptable (0.41–0.65)"
        if s <= 0.80:
            return "Good (0.66–0.80)"
        return "Excellent (0.81–1.00)"

    def score(
        self,
        sharpness_score: float,
        clipping_score: float,
        noise_score: float,
        cast_score: float,
        contrast_score: float,

    ):
        # Sharpness：节点输出通常集中在 0~0.1 左右，所以先内部归一化到 0~1
        sharp_q = _clamp(sharpness_score / self.SHARPNESS_NORM_MAX, 0.0, 1.0)

        clip_q = 1.0 - _clamp(clipping_score, 0.0, 1.0)

        nmax = max(1e-6, float(self.NOISE_NORM_MAX))
        noise_q = 1.0 - _clamp(noise_score / nmax, 0.0, 1.0)

        cmax = max(1e-6, float(self.CAST_NORM_MAX))
        cast_q = 1.0 - _clamp(cast_score / cmax, 0.0, 1.0)

        tmax = max(1e-6, float(self.CONTRAST_NORM_MAX))
        contrast_q = _clamp(contrast_score / tmax, 0.0, 1.0)

        score = (
                self.W_SHARPNESS * sharp_q
                + self.W_CLIPPING * clip_q
                + self.W_NOISE * noise_q
                + self.W_CAST * cast_q
                + self.W_CONTRAST * contrast_q
        )
        score = _clamp(score, 0.0, 1.0)

        # 人像对焦门槛：对焦差直接重罚
        if sharp_q < 0.20:
            score *= (sharp_q / 0.20)

        score = _clamp(score, 0.0, 1.0)

        level = self._level(score)
        debug = (
            f"S:{sharp_q:.3f}(w{self.W_SHARPNESS}) | "
            f"Clip:{clip_q:.3f}(w{self.W_CLIPPING}) | "
            f"Noise:{noise_q:.3f}(w{self.W_NOISE}) | "
            f"Cast:{cast_q:.3f}(w{self.W_CAST}) | "
            f"Con:{contrast_q:.3f}(w{self.W_CONTRAST}) "
            f"=> {score:.3f}"
        )

        return float(score), level, debug
