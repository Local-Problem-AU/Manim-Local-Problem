# -*- coding: utf-8 -*-
# Manim Community 0.19.x / Onboarding Scene for Samkwang Chemical (삼광케미칼)

from manim import *
import numpy as np

# ===== 환경/버전 & 폰트 가이드 =====
MANIM_VERSION = "0.19.x"
FONT = "Malgun Gothic"
TITLE_FONT = FONT
BODY_FONT = FONT

# ===== 브랜딩/레이아웃 설정 =====
BRAND_PRIMARY = "#FFD54F"
BRAND_TEXT    = "#FFFFFF"
BRAND_ACCENT  = "#4FC3F7"
BRAND_BG      = "#1E1E1E"
NEUTRAL_FILL  = "#252525"
NEUTRAL_STROKE= "#3A3A3A"
DIMMED_FILL   = "#1A1A1A"

config.pixel_width  = 1400
config.pixel_height = 800
config.frame_width  = 14
config.frame_height = 8

# 씬 탐색 보조 (있어도 무방, 있으면 더 확실)
__all__ = ["OnboardingFlow"]

# ===== HR 데이터 =====
HR_DATA = {
    "company_name": "삼광케미칼",
    "mission": "경영이념 요약 한 줄을 입력하세요.",
    "values": ["핵심가치1", "핵심가치2", "핵심가치3", "핵심가치4"],
    "flow": [
        {"id": "입사",         "desc": "첫날 환영 · 계정/장비 발급 · 필수 서류"},
        {"id": "교육",         "desc": "안전/품질/제품/보안/문화 교육"},
        {"id": "고객 가치 창출", "desc": "현장 문제해결 · 피드백 루프 운영"},
        {"id": "성장",         "desc": "역량 개발 · 커리어 프레임 · 멘토십"},
    ],
    "growth_support": [
        "품질/안전 우선 원칙과 표준 프로세스",
        "협업 도구 · 멘토링 · 교육비 지원",
        "목표-성과-피드백의 반복(Quarterly)",
    ],
    "cta": "지금 팀 채널에 첫 주 목표를 공유하고, 궁금한 점을 질문하세요.",
    "legal": "ⓒ Samkwang Chemical. 내부용 온보딩 영상. 무단배포 금지.",
    "locale": "ko",
}

class OnboardingFlow(Scene):
    def construct(self):
        self.camera.background_color = BRAND_BG

        # ===== 영역 박스 유틸 =====
        def make_box(p1, p2, stroke=0, color="#000000", fill_opacity=0.0):
            w = abs(p2[0] - p1[0])
            h = abs(p2[1] - p1[1])
            c = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, 0)
            r = Rectangle(
                width=w, height=h,
                stroke_width=stroke, stroke_color=color,
                fill_color="#000000", fill_opacity=fill_opacity,
            )
            r.move_to(c)
            return r

        # ===== 레이아웃 프레임 =====
        header_area = make_box(np.array([-7, 4, 0]),  np.array([7, 3, 0]))
        left_flow   = make_box(np.array([-7, 3, 0]),  np.array([1.2, -4, 0]))
        right_notes = make_box(np.array([1.2, 3, 0]), np.array([7, -4, 0]))
        for b in [header_area, left_flow, right_notes]:
            b.set_stroke(width=0).set_fill(opacity=0)
            self.add(b)

        # ===== 헤더 업데이트 =====
        header_label = VGroup()
        def update_step(label):
            nonlocal header_label
            new_label = Text(str(label), font=TITLE_FONT, weight="BOLD", color=BRAND_TEXT)
            new_label.scale_to_fit_height(0.6 * header_area.height)
            new_label.move_to(header_area.get_center())
            if len(header_label) > 0:
                self.play(FadeOut(header_label, run_time=0.35))
            header_label = VGroup(new_label)
            self.play(FadeIn(header_label, run_time=0.35))

        # ===== 우측 스택 관리 =====
        right_stack = []
        RIGHT_BASE_SCALE = 0.6

        def clear_right():
            nonlocal right_stack
            if right_stack:
                self.play(*[FadeOut(m, run_time=0.3) for m in right_stack])
                right_stack = []

        def push_right(mobj):
            nonlocal right_stack
            m = mobj
            m.scale(RIGHT_BASE_SCALE)
            m.set_color(BRAND_TEXT)
            # ✅ set_max_width 대신
            max_w = right_notes.width - 0.6
            if m.width > max_w:
                m.scale_to_fit_width(max_w)
            origin = right_notes.get_center()
            m.move_to(origin).align_to(right_notes.get_left(), LEFT)
            if right_stack:
                prev = right_stack[-1]
                m.next_to(prev, DOWN, buff=0.35).align_to(right_notes.get_left(), LEFT)
            right_stack.append(m)
            if len(right_stack) > 5:
                old = right_stack.pop(0)
                self.play(FadeOut(old, run_time=0.25))
                self.play(*[mob.animate.shift(UP * 0.4) for mob in right_stack], run_time=0.25)
            self.add(m)

        # ===== 좌측 노드/엣지 생성 =====
        def make_node(label):
            box = RoundedRectangle(
                corner_radius=0.25, width=3.4, height=1.1,
                stroke_color=NEUTRAL_STROKE, stroke_width=2,
                fill_color=NEUTRAL_FILL, fill_opacity=1.0,
            )
            txt = Text(str(label), font=BODY_FONT, weight="BOLD", color=BRAND_TEXT)
            txt.scale_to_fit_height(0.45 * box.height)
            grp = VGroup(box, txt).arrange(DOWN, buff=0.0)
            txt.move_to(box.get_center())
            return grp

        def make_edge(n1, n2, label=None):
            a = Arrow(n1.get_right(), n2.get_left(), stroke_width=2.5, buff=0.25)
            if label:
                t = Text(str(label), font=BODY_FONT, weight="MEDIUM", color=BRAND_TEXT).scale(0.35)
                t.next_to(a, UP, buff=0.1)
                return VGroup(a, t)
            return a

        left_nodes = VGroup(*[make_node(step["id"]) for step in HR_DATA["flow"]]).arrange(RIGHT, buff=0.6)
        left_edges = VGroup(*[
            make_edge(left_nodes[i], left_nodes[i + 1]) for i in range(len(left_nodes) - 1)
        ])
        left_group = VGroup(left_nodes, left_edges)
        s = min((left_flow.width * 0.97) / left_group.width, (left_flow.height * 0.97) / left_group.height)
        left_group.scale(s).move_to(left_flow.get_center())
        self.play(GrowFromCenter(left_nodes), run_time=0.6)
        self.play(*[Create(e) for e in left_edges], run_time=0.6)

        def link_left(idx):
            for i, grp in enumerate(left_nodes):
                box = grp[0]
                if i < idx:
                    box.set_stroke(color=NEUTRAL_STROKE, width=2.0)
                    box.set_fill(color=NEUTRAL_FILL, opacity=1.0)
                elif i == idx:
                    box.set_stroke(color=BRAND_PRIMARY, width=4.0)
                    box.set_fill(color=NEUTRAL_FILL, opacity=1.0)
                    self.play(Wiggle(grp, scale_value=1.02), run_time=0.35)
                else:
                    box.set_stroke(color=NEUTRAL_STROKE, width=1.5)
                    box.set_fill(color=DIMMED_FILL, opacity=1.0)

        # ===== Intro =====
        try: self.next_section("Intro")
        except Exception: pass
        update_step(HR_DATA["company_name"])
        intro_line = Text(HR_DATA["mission"], font=BODY_FONT, weight="MEDIUM", color=BRAND_TEXT)
        push_right(intro_line)
        self.wait(0.2)

        # ===== Values =====
        try: self.next_section("Values")
        except Exception: pass
        update_step("핵심가치")
        clear_right()
        for v in HR_DATA["values"]:
            line = Text(str(v), font=BODY_FONT, weight="BOLD", color=BRAND_TEXT)
            bullet = Text("•", font=BODY_FONT, weight="BOLD", color=BRAND_PRIMARY).scale(0.65)
            group = VGroup(bullet, line).arrange(RIGHT, buff=0.25)
            push_right(group)
            self.wait(0.2)

        # ===== Flow =====
        try: self.next_section("Flow")
        except Exception: pass
        update_step("온보딩 흐름")
        clear_right()
        for idx, step in enumerate(HR_DATA["flow"]):
            link_left(idx)
            push_right(Text(f"[{step['id']}]", font=BODY_FONT, weight="BOLD", color=BRAND_PRIMARY))
            desc = Text(step["desc"], font=BODY_FONT, weight="MEDIUM", color=BRAND_TEXT)
            push_right(desc)
            self.wait(0.6)

        # ===== Growth & Support =====
        try: self.next_section("Growth & Support")
        except Exception: pass
        update_step("성장 & 지원")
        clear_right()
        for line in HR_DATA.get("growth_support", []):
            push_right(Text(line, font=BODY_FONT, weight="MEDIUM", color=BRAND_TEXT))
            self.wait(0.2)

        # 보조노드(점선) — ✅ DashedVMobject 사용
        last_node = left_nodes[-1]
        sub1 = RoundedRectangle(
            corner_radius=0.2, width=2.8, height=0.8,
            stroke_color=BRAND_ACCENT, stroke_width=2,
            fill_color=NEUTRAL_FILL, fill_opacity=1.0,
        )
        sub2 = sub1.copy()
        t1 = Text("멘토십", font=BODY_FONT, weight="MEDIUM", color=BRAND_TEXT).scale_to_fit_height(0.4 * sub1.height)
        t2 = Text("교육/자격", font=BODY_FONT, weight="MEDIUM", color=BRAND_TEXT).scale_to_fit_height(0.4 * sub2.height)
        t1.move_to(sub1.get_center())
        t2.move_to(sub2.get_center())

        # 점선 외곽선을 위해 박스만 래핑
        dsub1 = DashedVMobject(sub1, num_dashes=24, dashed_ratio=0.6)
        dsub2 = DashedVMobject(sub2, num_dashes=24, dashed_ratio=0.6)
        g1 = VGroup(dsub1, t1)
        g2 = VGroup(dsub2, t2)
        sub_g = VGroup(g1, g2).arrange(DOWN, buff=0.2)
        sub_g.next_to(last_node, DOWN, buff=0.3).align_to(last_node, LEFT)

        self.play(FadeIn(sub_g, run_time=0.5))
        self.wait(0.3)

        # ===== CTA =====
        try: self.next_section("CTA")
        except Exception: pass
        update_step("첫 주, 이렇게 시작하세요")
        clear_right()
        cta = Text(HR_DATA["cta"], font=BODY_FONT, weight="BOLD", color=BRAND_TEXT)
        max_w = right_notes.width - 0.6
        if cta.width > max_w:
            cta.scale_to_fit_width(max_w)
        push_right(cta)

        self.play(*[grp[0].animate.set_stroke(color=BRAND_PRIMARY, width=3.5) for grp in left_nodes], run_time=0.5)
        self.play(left_nodes[-1][0].animate.set_stroke(color=BRAND_ACCENT, width=5.0), run_time=0.5)
        self.wait(1.0)

        # ===== 법무 엔드카드 =====
        legal = Text(HR_DATA["legal"], font=BODY_FONT, weight="MEDIUM", color=BRAND_TEXT).scale(0.35)
        legal.move_to(np.array([right_notes.get_right()[0] - 0.1, -3.7, 0])).align_to(right_notes.get_right(), RIGHT)
        self.play(FadeIn(legal), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(legal), run_time=0.6)
