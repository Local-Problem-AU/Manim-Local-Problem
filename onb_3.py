from manim import *
import os

# ============================================================
# MANIM_VERSION: 0.19.x (Community)
# Windows 폰트 권장: "Malgun Gothic" (Noto Sans CJK KR 설치 시 교체 가능)
# 실행 예: manim -pqh .\onb_ecocab.py ECOCAP_Onboarding
# ============================================================

# ---------- Canvas ----------
config.pixel_width  = 1400
config.pixel_height = 800
config.frame_width  = 14
config.frame_height = 8

# ---------- Brand Tokens (에코캡 톤앤매너: 네이비/시안/그린) ----------
BRAND_BG       = "#0C1424"  # 다크 네이비
BRAND_PANEL    = "#121A2D"  # 패널
BRAND_PRIMARY  = "#33C1E3"  # 시안 포인트
BRAND_ACCENT   = "#2ECC71"  # 그린 포인트
BRAND_TEXT     = "#EAF0FB"  # 본문 텍스트
BRAND_MUTED    = "#A7B5D6"  # 보조 텍스트
BRAND_STROKE   = "#314366"  # 보더

# ---------- Font ----------
FONT = "Malgun Gothic"  # 필요 시 "Noto Sans CJK KR"로 변경

# ---------- Optional: 홈페이지/브로슈어 스크린샷(연출용 배경) ----------
# PNG/JPG 권장 (PDF 직접 로드는 불가)
ASSET_HERO = r"assets\ecocab_hero.png"  # 사용자 환경에 맞게 교체

# ---------- HR 텍스트만 교체하면 재활용 가능 ----------
HR = {
    "company_name": "에코캡 (ECOCAB)",
    "mission": "스마트 전장 배선과 커넥터로 안전하고 신뢰성 높은 e-모빌리티를 실현합니다.",
    "values": ["안전", "품질", "지속가능성", "고객신뢰", "협력과 성장"],
    "onboarding_flow": [
        {"id": "입사",   "desc": "첫날 환영 · 계정/보호구 발급 · 정보보안 서약"},
        {"id": "교육",   "desc": "안전/보건 · 품질기준 · 하네스/커넥터 공정 · ESG"},
        {"id": "현장적응", "desc": "라인 투어 · 표준작업(SOP) · 불량 예방·개선 활동"},
        {"id": "고객가치", "desc": "e-모빌리티 전장 솔루션 · 납기/품질 신뢰 확보"},
        {"id": "성장",   "desc": "멘토링 · 교육포털 · 직무역량/커리어 프레임"}
    ],
    "rnd_highlights": [
        "와이어 하네스 설계/번들링 최적화",
        "커넥터/단자 신뢰성 평가·환경시험",
        "전장 간섭/전기적 특성(EMC) 검토",
        "e-모빌리티 모듈/배선 아키텍처"
    ],
    "site_focus": [
        "안전 수칙: 보호구, 설비 Lockout-Tagout, 화기/전기 안전",
        "품질 기준: 공정 표준, 트레이서빌리티, 불량 제로 챌린지",
        "보안/윤리: 정보보안, 협력사 공정거래, 내부자 신고 채널"
    ],
    "talent_points": [
        "문제해결형 Kaizen 제안",
        "멘토 1:1 온보딩 & 주간 리캡",
        "교육포털(표준작업·품질·ESG) 러닝패스"
    ],
    "members": [
        "HYUNDAI·KIA", "GM", "Renault", "Nissan",
        "Volkswagen Group", "Mercedes-Benz", "Audi",
        "Volvo", "Jaguar Land Rover", "현대모비스"
    ],
    "cta": "첫 주 안전·품질 체크리스트를 완료하고, 멘토와 1:1 목표를 공유하세요.",
    "legal": "ⓒ ECOCAB. 내부 교육용. 무단 배포 금지."
}


# ============================================================
# Main Scene
# ============================================================
class ECOCAP_Onboarding(Scene):
    def construct(self):
        self.camera.background_color = BRAND_BG

        # 레이아웃 박스
        header_box = self._box([-7,  3, 0], [ 7, 4, 0])   # 헤더
        left_box   = self._box([-7, -4, 0], [ 1.3, 3, 0]) # 좌: 플로우
        right_box  = self._box([ 1.3,-4, 0], [ 7, 3, 0])  # 우: 본문 패널

        # 배경 연출(있으면 활용)
        self._maybe_hero_bg()

        # 좌측 온보딩 플로우 그래프
        nodes, edges, graph = self._build_flow([s["id"] for s in HR["onboarding_flow"]])
        self._fit_to_box(graph, left_box, scale_pad=0.96)

        # 상태
        self._header = None
        self._right_stack = VGroup()

        # ===== Intro =====
        self._set_header(header_box, HR["company_name"])
        intro = self._text(
            HR["mission"],
            size=46, weight="BOLD",
            t2c={k: BRAND_PRIMARY for k in ["전장", "커넥터", "e-모빌리티", "신뢰성", "안전"]}
        )
        self._panel_push(right_box, intro)
        self.play(LaggedStart(*[FadeIn(n, shift=DOWN*0.1) for n in nodes], lag_ratio=0.08), run_time=0.6)
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.08), run_time=0.6)

        # ===== Values =====
        self._set_header(header_box, "핵심가치")
        self._panel_clear()
        for i, v in enumerate(HR["values"]):
            tag = self._chip(v)
            tag.next_to(nodes[min(i, len(nodes)-1)], DOWN, buff=0.22)
            self.play(GrowFromCenter(tag), run_time=0.25)
        for v in HR["values"]:
            self._panel_push(right_box, self._text(v, size=38, weight="BOLD", t2c={v: BRAND_PRIMARY}))

        # ===== R&D CENTER =====
        self._set_header(header_box, "R&D CENTER")
        self._panel_clear()
        self._panel_push(right_box, self._text("핵심 연구영역", size=40, weight="BOLD"))
        for h in HR["rnd_highlights"]:
            self._panel_push(right_box, self._bullet(h))

        # ===== SITE FOCUS =====
        self._set_header(header_box, "SITE FOCUS")
        self._panel_clear()
        self._panel_push(right_box, self._text("첫 주 꼭 알아두기", size=40, weight="BOLD"))
        for s in HR["site_focus"]:
            self._panel_push(right_box, self._bullet(s))

        # ===== 온보딩 흐름(좌측 단계별 포커스 + 우측 설명) =====
        self._set_header(header_box, "온보딩 흐름")
        self._panel_clear()
        for idx, step in enumerate(HR["onboarding_flow"]):
            self._link_focus(nodes, edges, idx)
            desc = self._text(f"[{step['id']}] {step['desc']}", size=36, weight="MEDIUM",
                              t2c={step['id']: BRAND_PRIMARY, "품질": BRAND_ACCENT, "안전": BRAND_ACCENT})
            self._panel_push(right_box, desc)
            self.play(Wiggle(nodes[idx], scale_value=1.02), run_time=0.4)

        # ===== 고객사(텍스트 칩스) =====
        self._set_header(header_box, "CUSTOMERS")
        self._panel_clear()
        self._panel_push(right_box, self._text("파트너 & 고객사", size=38, weight="BOLD"))
        chips = self._chips(HR["members"])
        self._panel_push(right_box, chips, animate=False)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT*0.1) for c in chips], lag_ratio=0.05), run_time=0.6)

        # ===== CTA =====
        self._set_header(header_box, "함께 만드는 안전·품질·성장")
        self._panel_clear()
        cta = self._text(HR["cta"], size=42, weight="BOLD",
                         t2c={"체크리스트": BRAND_PRIMARY, "멘토": BRAND_PRIMARY, "목표": BRAND_PRIMARY})
        self._panel_push(right_box, cta)

        # 좌측 전체 하이라이트 & 마지막 노드 강조
        hl = SurroundingRectangle(graph, color=BRAND_PRIMARY, stroke_width=3).set_opacity(0.95)
        self.play(Create(hl), run_time=0.5)
        self.play(Indicate(nodes[-1], color=BRAND_ACCENT, scale_factor=1.05), run_time=0.6)
        self.play(FadeOut(hl), run_time=0.4)

        # Legal
        legal = Text(HR["legal"], font=FONT, weight="MEDIUM", color=BRAND_MUTED).scale(0.35)
        legal.to_edge(DR, buff=0.3)
        self.play(FadeIn(legal), run_time=0.4)
        self.wait(0.6)

    # ===================== Helpers =====================
    def _maybe_hero_bg(self):
        if isinstance(ASSET_HERO, str) and os.path.exists(ASSET_HERO):
            try:
                hero = ImageMobject(ASSET_HERO)
                hero.set_opacity(0.10)
                hero.set_width(config.frame_width * 1.05)
                hero.set_z_index(-10)
                self.add(hero)
            except Exception:
                pass

    def _box(self, p1, p2):
        w = abs(p2[0] - p1[0]); h = abs(p2[1] - p1[1])
        c = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, 0]
        return Rectangle(width=w, height=h, stroke_width=0, fill_opacity=0).move_to(c)

    def _fit_to_box(self, obj, box, scale_pad=0.95):
        s = min((box.width * scale_pad) / obj.width, (box.height * scale_pad) / obj.height)
        obj.scale(s)
        obj.move_to(box.get_center())

    def _text(self, s, size=36, weight="MEDIUM", color=BRAND_TEXT, t2c=None):
        t = Text(s, font=FONT, weight=weight, color=color, t2c=t2c)
        t.scale(size / 36.0)
        return t

    def _bullet(self, s):
        dot = Dot(radius=0.055, color=BRAND_PRIMARY).set_stroke(width=0)
        txt = self._text(s, size=34, weight="MEDIUM", color=BRAND_TEXT)
        return VGroup(dot, txt).arrange(RIGHT, buff=0.25)

    def _chip(self, s):
        t = self._text(s, size=28, weight="BOLD", color=BRAND_TEXT)
        rr = RoundedRectangle(corner_radius=0.20, width=t.width + 0.45, height=t.height + 0.30)
        rr.set_fill(BRAND_PANEL, opacity=1.0).set_stroke(BRAND_STROKE, width=2, opacity=0.95)
        g = VGroup(rr, t)
        t.move_to(rr.get_center())
        return g

    def _chips(self, items, cols=3):
        chips = VGroup(*[self._chip(s) for s in items])
        chips.arrange_in_grid(rows=((len(items) - 1) // cols) + 1, cols=cols, buff=0.25, cell_alignment=LEFT)
        return chips

    def _panel_clear(self):
        if hasattr(self, "_right_stack") and len(self._right_stack) > 0:
            self.play(LaggedStart(*[FadeOut(m, shift=UP * 0.12) for m in self._right_stack], lag_ratio=0.10), run_time=0.45)
        self._right_stack = VGroup()
        self.add(self._right_stack)

    def _panel_push(self, right_box, mobj, animate=True):
        # 배경 패널(최초 1회)
        if len(self._right_stack) == 0:
            panel = RoundedRectangle(corner_radius=0.22, width=right_box.width * 0.96, height=right_box.height * 0.96)
            panel.set_fill(BRAND_PANEL, opacity=0.92).set_stroke(BRAND_STROKE, width=2, opacity=1.0)
            panel.move_to(right_box.get_center())
            self._right_panel = panel
            self.add(panel)

        # 아이템 배치
        mobj.set_max_width(right_box.width * 0.86)
        if len(self._right_stack) == 0:
            mobj.move_to(self._right_panel.get_top()).shift(DOWN * 0.7).align_to(self._right_panel.get_left(), LEFT).shift(RIGHT * 0.5)
        else:
            prev = self._right_stack[-1]
            mobj.next_to(prev, DOWN, buff=0.3).align_to(prev, LEFT)
        self._right_stack.add(mobj)

        if animate:
            self.play(FadeIn(mobj, shift=RIGHT * 0.15), run_time=0.32)
        else:
            self.add(mobj)

    def _set_header(self, header_box, label):
        new_h = self._text(label, size=54, weight="BOLD",
                           t2c={"안전": "#FFD54F", "품질": "#FFD54F"})
        new_h.move_to(header_box.get_center())
        underline = Line(header_box.get_left() + RIGHT * 0.2,
                         header_box.get_right() + LEFT * 0.2,
                         stroke_width=3, color=BRAND_STROKE)
        underline.next_to(new_h, DOWN, buff=0.15)
        group = VGroup(new_h, underline)
        if hasattr(self, "_header") and self._header:
            self.play(FadeOut(self._header, shift=UP * 0.2), run_time=0.25)
        self._header = group
        self.play(FadeIn(group, shift=DOWN * 0.2), run_time=0.35)

    def _build_flow(self, labels):
        nodes = [self._node(l) for l in labels]
        row = VGroup(*nodes).arrange(RIGHT, buff=0.6)
        edges = []
        for i in range(len(nodes) - 1):
            a = Arrow(nodes[i].get_right(), nodes[i + 1].get_left(),
                      buff=0.22, stroke_width=3, max_tip_length_to_length_ratio=0.06)
            a.set_color(BRAND_STROKE).set_opacity(0.9)
            edges.append(a)
        graph = VGroup(row, *edges)
        return nodes, edges, graph

    def _node(self, label):
        txt = self._text(label, size=34, weight="BOLD")
        padx, pady = 0.6, 0.35
        rect = RoundedRectangle(corner_radius=0.22, width=txt.width + padx, height=txt.height + pady)
        rect.set_fill("#182340", opacity=1.0).set_stroke(BRAND_STROKE, width=2)
        return VGroup(rect, txt)

    def _link_focus(self, nodes, edges, idx):
        # 노드 상태
        for i, n in enumerate(nodes):
            rect, txt = n[0], n[1]
            if i < idx:
                rect.set_fill("#182340", opacity=1.0).set_stroke("#6F7FA7", width=2)
                txt.set_color(BRAND_MUTED)
                n.set_opacity(0.95)
            elif i == idx:
                rect.set_fill("#1F2B4D", opacity=1.0).set_stroke(BRAND_PRIMARY, width=4)
                txt.set_color(BRAND_TEXT)
                n.set_opacity(1.0)
            else:
                rect.set_fill("#141C32", opacity=0.95).set_stroke(BRAND_STROKE, width=2)
                txt.set_color("#C7D2EA")
                n.set_opacity(0.82)

        # 엣지 상태
        for e_i, e in enumerate(edges):
            if e_i < idx - 1:
                e.set_color("#7F8EB8").set_stroke(width=3, opacity=0.95)
            elif e_i == idx - 1:
                e.set_color(BRAND_PRIMARY).set_stroke(width=4, opacity=1.0)
                self.play(Create(e), run_time=0.28)
            else:
                e.set_color(BRAND_STROKE).set_stroke(width=2, opacity=0.7)
