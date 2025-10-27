# -*- coding: utf-8 -*-
# Manim Community 0.19.x
# 빠른 미리보기:  manim -pqh hhi_overview.py OnboardingFlow

from manim import *

config.pixel_width = 1400
config.pixel_height = 800
config.frame_width = 14
config.frame_height = 8

FONT = "Malgun Gothic"

BRAND_PRIMARY = "#FFD54F"  # 포커스/강조
BRAND_TEXT = "#FFFFFF"
BRAND_ACCENT = "#4FC3F7"
BRAND_BG = "#1E1E1E"

HR_DATA = {
    "company_name": "HD현대중공업㈜ (HD HYUNDAI HEAVY INDUSTRIES CO., LTD.)",
    "mission": "조선·해양·엔진 분야에서 안전하고 친환경적인 미래를 설계합니다.",
    "values": ["안전·품질 최우선", "친환경·연료전환(수소·암모니아)", "고객가치/납기 준수", "기술혁신/성장"],
    "flow": [
        {"id": "설립(2019-06-01)", "desc": "현대중공업에서 물적분할 신규 설립"},
        {"id": "상장(2021-09-17)", "desc": "유가증권시장 상장(HHI)"},
        {"id": "주요사업", "desc": "조선 70%, 해양플랜트 5%, 엔진기계 24%"},
        {"id": "신용등급", "desc": "회사채 A→A+ (2025년 상향)"},
    ],
    "cta": "첫 주: 팀에 미션/가치를 질문하고, 본인 업무목표 1가지를 공유하세요.",
    "legal": "ⓒ HD현대중공업. 내부용. 무단배포 금지.",
    "locale": "ko",
    "address": "울산광역시 동구 방어진순환도로 1000 (전하동) | 052-202-2114 | www.hhi.co.kr",
    "subs": "연결대상 종속회사 3사(비상장), 주요 종속 1사 / 당반기 신설: HD현대엠엔에스㈜",
}


class OnboardingFlow(Scene):
    def construct(self):
        self.camera.background_color = BRAND_BG

        # 레이아웃 박스
        self.header_area = self.make_box([-7, 3, 0], [7, 4, 0], stroke_opacity=0)
        self.left_flow = self.make_box([-7, -4, 0], [1.2, 3, 0], stroke_opacity=0)
        self.right_notes = self.make_box([1.2, -4, 0], [7, 3, 0], stroke_opacity=0)

        # 내부 상태
        self._header = None
        self._right_stack = VGroup()

        # 좌측 흐름도
        nodes, edges, graph = self._build_flow([s["id"] for s in HR_DATA["flow"]])
        self.fit_left_flow(graph)

        # 인트로
        self.update_step(HR_DATA["company_name"])
        intro_msg = Text(HR_DATA["mission"], font=FONT, color=BRAND_TEXT)
        self.push_right(intro_msg)
        addr = Text(HR_DATA["address"], font=FONT, color=BRAND_ACCENT).scale(0.55)
        self.push_right(addr)
        subs = Text(HR_DATA["subs"], font=FONT, color=BRAND_TEXT).scale(0.55)
        self.push_right(subs)

        self.play(
            LaggedStart(*[FadeIn(n[0], scale=0.9) for n in nodes], lag_ratio=0.1, run_time=0.7),
            LaggedStart(*[Write(n[1]) for n in nodes], lag_ratio=0.1, run_time=0.7),
        )
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.15, run_time=0.7))
        self.wait(0.2)

        # Values
        self.update_step("핵심가치")
        for v in HR_DATA["values"]:
            msg = Text(v, font=FONT, color=BRAND_TEXT)
            if ("친환경" in v) or ("혁신" in v) or ("안전" in v) or ("품질" in v) or ("고객" in v):
                msg.set_color(BRAND_PRIMARY)
            self.push_right(msg)
            self.wait(0.1)

        # Flow 단계별 포커스
        self.update_step("회사 흐름")
        for idx, step in enumerate(HR_DATA["flow"]):
            self.link_left(nodes, edges, idx)
            desc = Text(step["desc"], font=FONT, color=BRAND_TEXT)
            self.push_right(desc)
            self.wait(0.1)

        # 사업 요약 + 신용평가
        self.update_step("성장 & 지원")
        g1 = Text("조선: 일반상선·가스선·해양/군함·수소·암모니아 추진선 개발", font=FONT, color=BRAND_TEXT).scale(0.6)
        g2 = Text("해양플랜트: 원유 생산·저장설비, 발전/화공플랜트 프로젝트", font=FONT, color=BRAND_TEXT).scale(0.6)
        g3 = Text("엔진기계: 대형/힘센엔진·발전설비 공급, 친환경 제품 자체개발", font=FONT, color=BRAND_TEXT).scale(0.6)
        self.push_right(g1)
        self.push_right(g2)
        self.push_right(g3)
        credit = Text("신용등급(회사채): 2025년 A+ (정기평가 상향)", font=FONT, color=BRAND_PRIMARY).scale(0.62)
        self.push_right(credit)

        # CTA
        self.update_step("Start Here")
        cta = Text(HR_DATA["cta"], font=FONT, color=BRAND_PRIMARY).scale(0.7)
        self.push_right(cta)
        self._pulse_all(nodes)
        self.wait(0.6)

        # 엔드 카드(법무)
        legal = Text(HR_DATA["legal"], font=FONT, color=BRAND_TEXT).scale(0.45)
        legal.to_corner(DR).shift(0.3 * UP + 0.3 * LEFT)
        self.play(FadeIn(legal), run_time=0.6)
        self.wait(0.6)
        self.play(FadeOut(legal), run_time=0.6)

    # ===== 헬퍼 =====
    def make_box(self, p1, p2, **kw):
        width = abs(p2[0] - p1[0])
        height = abs(p2[1] - p1[1])
        rect = Rectangle(width=width, height=height, color="#000000", **kw)
        cx = (p1[0] + p2[0]) / 2.0
        cy = (p1[1] + p2[1]) / 2.0
        rect.move_to([cx, cy, 0])
        self.add(rect)
        return rect

    def fit_left_flow(self, obj):
        box = self.left_flow
        s = min((box.width * 0.97) / obj.width, (box.height * 0.97) / obj.height)
        obj.scale(s)
        obj.move_to(box.get_center())

    def _build_flow(self, labels):
        nodes = []
        for label in labels:
            n = self.make_node(label)
            nodes.append(n)
        g_nodes = VGroup(*[VGroup(r, t) for (r, t) in nodes])
        g_nodes.arrange(RIGHT, buff=0.9)
        edges = []
        for i in range(len(nodes) - 1):
            a = self.make_edge(nodes[i][0], nodes[i + 1][0])
            edges.append(a)
        graph = VGroup(g_nodes, *edges)
        self.add(graph)
        return nodes, edges, graph

    def make_node(self, label):
        box = RoundedRectangle(
            corner_radius=0.3,
            width=3.4,
            height=1.4,
            stroke_color=BRAND_TEXT,
            fill_color="#000000",
            fill_opacity=0.0,
        )
        text = Text(label, font=FONT, color=BRAND_TEXT).scale(0.6)
        group = VGroup(box, text)
        text.move_to(box.get_center())
        return (box, text)

    def make_edge(self, n1_box, n2_box, label=None):
        a = Arrow(
            n1_box.get_right(),
            n2_box.get_left(),
            buff=0.2,
            stroke_color=BRAND_TEXT,
            max_tip_length_to_length_ratio=0.12,
        )
        if label:
            t = Text(label, font=FONT, color=BRAND_TEXT).scale(0.45)
            t.next_to(a, UP, buff=0.1)
            return VGroup(a, t)
        return a

    def update_step(self, label):
        new_header = Text(label, font=FONT, color=BRAND_TEXT, weight="BOLD")
        new_header.scale_to_fit_height(0.6 * self.header_area.height)
        new_header.move_to(self.header_area.get_center()).align_to(self.header_area, LEFT).shift(0.2 * RIGHT)
        if self._header is None:
            self._header = new_header
            self.play(FadeIn(self._header), run_time=0.7)
        else:
            old = self._header
            self._header = new_header
            self.play(FadeOut(old), FadeIn(self._header), run_time=0.7)
        self.clear_right()

    def clear_right(self):
        if len(self._right_stack) > 0:
            self.play(FadeOut(self._right_stack), run_time=0.3)
        self.remove(self._right_stack)
        self._right_stack = VGroup()

    def push_right(self, mobj):
        RIGHT_BASE_SCALE = 0.6
        mobj.scale(RIGHT_BASE_SCALE)
        max_w = self.right_notes.width - 0.6
        if mobj.width > max_w:
            mobj.set_max_width(max_w)
        origin = self.right_notes.get_center()
        if len(self._right_stack) == 0:
            mobj.move_to(origin).align_to(self.right_notes.get_left(), LEFT)
            self._right_stack.add(mobj)
            self.add(mobj)
            self.play(FadeIn(mobj, shift=0.1 * UP), run_time=0.4)
        else:
            prev = self._right_stack[-1]
            mobj.next_to(prev, DOWN, buff=0.35).align_to(self.right_notes.get_left(), LEFT)
            self._right_stack.add(mobj)
            self.add(mobj)
            self.play(FadeIn(mobj, shift=0.1 * UP), run_time=0.4)
        if len(self._right_stack) > 5:
            first = self._right_stack[0]
            self._right_stack.remove(first)
            self.play(FadeOut(first), self._right_stack.animate.shift(0.4 * UP), run_time=0.3)

    def link_left(self, nodes, edges, idx):
        for i, (box, txt) in enumerate(nodes):
            if i < idx:
                box.set_stroke(color=BRAND_TEXT, width=2.0, opacity=1.0)
                txt.set_color(BRAND_TEXT)
                box.set_fill("#000000", opacity=0.0)
            elif i == idx:
                box.set_stroke(color=BRAND_PRIMARY, width=4.0, opacity=1.0)
                txt.set_color(BRAND_PRIMARY)
                box.set_fill(BRAND_PRIMARY, opacity=0.1)
            else:
                box.set_stroke(color=BRAND_TEXT, width=1.0, opacity=0.5)
                txt.set_color(BRAND_TEXT)
                box.set_fill("#000000", opacity=0.0)
        for i, e in enumerate(edges):
            if i < idx:
                if isinstance(e, VGroup):
                    e[0].set_stroke(color=BRAND_TEXT, opacity=1.0, width=2.0)
                else:
                    e.set_stroke(color=BRAND_TEXT, opacity=1.0, width=2.0)
            elif i == idx - 1:
                if isinstance(e, VGroup):
                    e[0].set_stroke(color=BRAND_PRIMARY, opacity=1.0, width=3.0)
                else:
                    e.set_stroke(color=BRAND_PRIMARY, opacity=1.0, width=3.0)
            else:
                if isinstance(e, VGroup):
                    e[0].set_stroke(color=BRAND_TEXT, opacity=0.4, width=1.0)
                else:
                    e.set_stroke(color=BRAND_TEXT, opacity=0.4, width=1.0)
        self.play(Wiggle(nodes[idx][0], scale_value=1.02), run_time=0.6)

    def _pulse_all(self, nodes):
        anims = []
        for (box, _) in nodes:
            anims.append(Indicate(box, color=BRAND_PRIMARY, scale_factor=1.02))
        self.play(LaggedStart(*anims, lag_ratio=0.1, run_time=0.8))
