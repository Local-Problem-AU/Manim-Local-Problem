# onb_5.py
# 실행 예:
# 1) 빠른 테스트: manim -pql onb_5.py Intro
# 2) 본편 실행   : manim -pql onb_5.py OnboardingFlow

from manim import *

# ===== Config & Brand =====
config.pixel_width  = 1400
config.pixel_height = 800
config.frame_width  = 14
config.frame_height = 8

BRAND_PRIMARY = "#FFD54F"  # 강조색
BRAND_TEXT    = "#FFFFFF"
BRAND_ACCENT  = "#4FC3F7"
BRAND_BG      = "#1E1E1E"

# OS에 따라 존재하는 한글 폰트로 바꿔 쓰세요 (Windows 기본: Malgun Gothic)
FONT = "Malgun Gothic"

# ===== Data (필요시 여기만 편집) =====
HR_DATA = {
    "company_name": "노바텍 (NOVATEK)",
    "mission": "우리의 기술로 산업 현장의 효율과 안전을 높입니다.",
    "values": ["고객집착", "주인의식", "협업", "지속성장"],
    "flow": [
        {"id": "입사",           "desc": "첫날 환영 · 계정 발급 · 팀/멘토 배정"},
        {"id": "교육",           "desc": "보안/제품/안전/업무툴 온보딩"},
        {"id": "고객 가치 창출",  "desc": "현장 문제해결 · 개선 제안 · 피드백 루프"},
        {"id": "성장",           "desc": "역량개발 · 커리어 프레임 · 분기 리뷰"},
    ],
    "cta": "지금 팀에 질문하고, 첫 주 목표를 공유하세요.",
    "legal": "ⓒ NOVATEK. 내부용. 무단배포 금지.",
    "locale": "ko",
}

# ===== Helpers =====
def make_box(p1, p2, **kw):
    (x1, y1), (x2, y2) = p1, p2
    w, h = (x2 - x1), (y2 - y1)
    center = ((x1 + x2) / 2, (y1 + y2) / 2, 0)
    rect = Rectangle(width=w, height=h, **kw)
    rect.move_to(center)
    return rect

def fit_to_width(mobj: Mobject, max_w: float):
    if mobj.width > max_w:
        mobj.scale(max_w / mobj.width)
    return mobj

# ===== Quick sanity-check Scene =====
class Intro(Scene):
    def construct(self):
        self.camera.background_color = BRAND_BG
        title = Text("NOVATEK Onboarding", font=FONT, color=BRAND_TEXT).scale(0.9)
        subtitle = Text("테스트 렌더씬 (Intro)", font=FONT, color=BRAND_ACCENT).scale(0.6)
        subtitle.next_to(title, DOWN, buff=0.4)
        g = VGroup(title, subtitle).move_to(ORIGIN)
        self.play(FadeIn(g, shift=0.3*UP), run_time=0.8)
        self.wait(0.5)

# ===== Main Scene =====
class OnboardingFlow(Scene):
    def construct(self):
        self.camera.background_color = BRAND_BG

        # --- Layout guides (invisible) ---
        header_area    = make_box((-7, 3),     (7, 4),     stroke_opacity=0, fill_opacity=0)
        left_flow_area = make_box((-7, -4),    (1.2, 3),   stroke_opacity=0, fill_opacity=0)
        right_notes    = make_box((1.2, -4),   (7, 3),     stroke_opacity=0, fill_opacity=0)

        # State
        self.right_stack = VGroup()
        self.header_label = None

        # ---- Header updater ----
        def update_step(label):
            new_h = Text(label, font=FONT, weight="BOLD", color=BRAND_TEXT)
            new_h.scale_to_fit_height(0.6)
            new_h.move_to(header_area.get_center()).align_to(header_area.get_left(), LEFT)
            if self.header_label is None:
                self.header_label = new_h
                self.play(FadeIn(self.header_label), run_time=0.7)
            else:
                old = self.header_label
                self.header_label = new_h
                self.play(FadeOut(old), FadeIn(self.header_label), run_time=0.7)

        # ---- Right column helpers ----
        RIGHT_BASE_SCALE = 0.6

        def clear_right():
            if len(self.right_stack) > 0:
                self.play(*[FadeOut(m) for m in self.right_stack], run_time=0.4)
            self.right_stack = VGroup()

        def push_right(mobj: Mobject):
            if isinstance(mobj, Text):
                mobj.set_color(BRAND_TEXT)
            mobj.scale(RIGHT_BASE_SCALE)
            fit_to_width(mobj, right_notes.width - 0.6)

            if len(self.right_stack) == 0:
                mobj.move_to(right_notes.get_center()).align_to(right_notes.get_left(), LEFT)
                self.right_stack.add(mobj)
                self.add(mobj)
                self.play(Write(mobj), run_time=0.5)
            else:
                last = self.right_stack[-1]
                mobj.next_to(last, DOWN, buff=0.35).align_to(right_notes.get_left(), LEFT)
                # keep at most 5 lines visible
                if len(self.right_stack) >= 5:
                    oldest = self.right_stack[0]
                    self.right_stack.remove(oldest)
                    self.play(FadeOut(oldest), *[m.animate.shift(0.4 * UP) for m in self.right_stack], run_time=0.25)
                self.right_stack.add(mobj)
                self.add(mobj)
                self.play(Write(mobj), run_time=0.5)

        # ---- Left flow (nodes + edges) ----
        def make_node(label_text):
            label = Text(label_text, font=FONT, color=BRAND_TEXT, weight="BOLD").scale(0.5)
            pad = 0.4
            rr = RoundedRectangle(corner_radius=0.2, width=label.width + 1.0, height=label.height + pad)
            rr.set_stroke(color="#5A5A5A", width=2)
            rr.set_fill(color="#000000", opacity=0.15)
            g = VGroup(rr, label)
            label.move_to(rr.get_center())
            return g

        nodes = VGroup(*[make_node(step["id"]) for step in HR_DATA["flow"]]).arrange(RIGHT, buff=0.8)

        # fit into left area
        s = min((left_flow_area.width * 0.97) / nodes.width, (left_flow_area.height * 0.97) / nodes.height)
        nodes.scale(s).move_to(left_flow_area.get_center())

        # edges
        edges = VGroup()
        for i in range(len(nodes) - 1):
            a = nodes[i][0].get_right() + 0.05 * RIGHT
            b = nodes[i + 1][0].get_left() - 0.05 * RIGHT
            arr = Arrow(a, b, buff=0.1, stroke_width=3,
                        max_tip_length_to_length_ratio=0.08, color="#6E6E6E")
            edges.add(arr)

        # show left flow
        self.play(GrowFromCenter(nodes), run_time=0.7)
        self.play(*[Create(e) for e in edges], run_time=0.7)

        # left focus helper
        def link_left(idx: int):
            for i, n in enumerate(nodes):
                box, lab = n[0], n[1]
                if i < idx:
                    box.set_stroke(color="#9AA0A6", width=2)
                    box.set_fill(color="#000000", opacity=0.18)
                    lab.set_opacity(1.0)
                elif i == idx:
                    box.set_stroke(color=BRAND_PRIMARY, width=4)
                    box.set_fill(color="#000000", opacity=0.30)
                    lab.set_opacity(1.0)
                else:
                    box.set_stroke(color="#444444", width=1.5)
                    box.set_fill(color="#000000", opacity=0.10)
                    lab.set_opacity(0.6)
            for j, e in enumerate(edges):
                if j < idx:
                    e.set_stroke(color=BRAND_PRIMARY, width=4, opacity=1.0)
                else:
                    e.set_stroke(color="#6E6E6E", width=3, opacity=0.7)
            self.play(Wiggle(nodes[idx], scale_value=1.02), run_time=0.6)

        # ===== Sequence =====
        # Intro
        update_step(HR_DATA["company_name"])
        clear_right()
        intro_line = Text(HR_DATA["mission"], font=FONT, color=BRAND_TEXT)
        push_right(intro_line)

        # Values
        update_step("핵심가치")
        for v in HR_DATA["values"]:
            t = Text(v, font=FONT, color=BRAND_TEXT, weight="BOLD")
            push_right(t)

        # Flow walkthrough
        update_step("온보딩 흐름")
        clear_right()
        for i, step in enumerate(HR_DATA["flow"]):
            msg = Text(f"{step['id']}: {step['desc']}", font=FONT, color=BRAND_TEXT)
            push_right(msg)
            link_left(i)
            self.wait(0.2)

        # Growth & Support
        update_step("성장 & 지원")
        clear_right()
        for m in [
            "멘토십 · 피어 러닝 · 정기 피드백",
            "업무툴/보안정책 준수로 품질과 안전 강화",
            "커리어 프레임 기반 역량 성장",
        ]:
            t = Text(m, font=FONT, color=BRAND_TEXT)
            push_right(t)

        # CTA
        update_step("시작하기")
        clear_right()
        cta = Text(HR_DATA["cta"], font=FONT, color=BRAND_TEXT, weight="BOLD")
        fit_to_width(cta, right_notes.width - 0.6)
        push_right(cta)

        # Left flow highlight & final node focus
        self.play(*[n[0].animate.set_stroke(color=BRAND_ACCENT, width=2) for n in nodes], run_time=0.5)
        link_left(len(HR_DATA["flow"]) - 1)

        # Legal (end card)
        legal = Text(HR_DATA["legal"], font=FONT, color="#BDBDBD").scale(0.35)
        legal.to_edge(DOWN).to_edge(RIGHT)
        self.play(FadeIn(legal), run_time=0.6)
        self.wait(0.5)
