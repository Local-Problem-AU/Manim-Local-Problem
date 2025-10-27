# -*- coding: utf-8 -*-
# Manim Community 0.19.x
# 파일명 예: hhi_kpi_overview.py
# 실행 예: manim -pqh hhi_kpi_overview.py OnboardingFlow
#
# OS 폰트 가이드(한글):
# - Windows: "Malgun Gothic"
# - macOS: "Apple SD Gothic Neo"
# - 공용 대체: "Noto Sans CJK KR", "NanumGothic"
# 글꼴이 없으면 다른 한글 폰트로 대체될 수 있음.

from manim import *

# ===== Manim 전역 해상도 및 프레임 =====
config.pixel_width = 1400
config.pixel_height = 800
config.frame_width = 14
config.frame_height = 8

# ===== 브랜드/색상/폰트 =====
BRAND_PRIMARY = "#FFD54F"  # 포커스/강조
BRAND_TEXT = "#FFFFFF"
BRAND_ACCENT = "#4FC3F7"
BRAND_BG = "#1E1E1E"
FONT = "Malgun Gothic"

# ===== 데이터(보고서 기반 + 가용정보 위주 반영) =====
HR_DATA = {
    "company_name": "HD현대중공업",
    "mission": "첨단 조선·해양 기술로 안전하고 효율적인 에너지·물류 생태계를 만든다.",
    "values": ["안전 최우선", "고객 신뢰", "현장 중심 혁신", "지속가능성"],
    "flow": [
        {"id": "재무지표", "desc": "핵심 KPI로 현재 위치 점검"},
        {"id": "사업부문", "desc": "조선 · 해양플랜트 · 엔진기계"},
        {"id": "보수/거버넌스", "desc": "이사/감사 보수 및 기준 공개"},
        {"id": "성장과제", "desc": "수주, 품질, 생산성, 안전"}
    ],
    "cta": "부문별 KPI 점검 → 이번 분기 실행과제와 책임자를 명확히 합의하세요.",
    "legal": "ⓒ HD현대중공업. 내부 교육용. 무단배포 금지.",
    "locale": "ko"
}

# 가용 텍스트 기반 KPI/부문 요약(숫자는 천원/백만원 단위 표기 주의)
FIN_DATA = {
    "kpis": [
        "이사·감사 전체 보수총액: 986,344천원 (5인, 1인당 평균 197,269천원)",
        "주주총회 승인 한도: 4,000,000천원",
        "등기이사 보수: 860,344천원 (2인, 1인당 430,172천원)",
        "감사위원회 위원 보수: 126,000천원 (3인, 1인당 42,000천원)",
        "5억원(=500,000천원) 이상 수령 이사/감사/임직원: 해당 없음"
    ],
    "segments": [
        "조선: 매출 5,592,961백만원 (비율 70.18%)",
        "해양플랜트: 매출 405,071백만원 (비율 5.08%)",
        "엔진기계: (보고서 일부 발췌 기반, 상세 수치 미기재)"
    ],
    "governance": [
        "이사(사내): 기본연봉(기본급+직책급) + 성과연봉",
        "성과연봉 지표: 매출·수주·영업이익 등 계량 + 리더십/전문성 등 비계량",
        "감사위원회: 독립성 보장을 위해 기본연봉 정액 지급",
        "주식매수선택권: 이사·감사, 미등기임원 모두 당반기말 기준 부여 없음"
    ],
    "growth_tasks": [
        "수주 믹스 고도화(LNG, 컨테이너, 특수선)",
        "생산성·원가개선(블록·의장 표준화, 공정 디지털화)",
        "품질/안전(Zero Harm) 및 납기 신뢰 향상",
        "엔진·친환경 추진체계 기술경쟁력 강화"
    ]
}

class OnboardingFlow(Scene):
    def construct(self):
        self.camera.background_color = BRAND_BG

        # ===== 레이아웃 영역 =====
        header_area = self.make_box(Rectangle(width=14, height=1), center=ORIGIN).move_to([0, 3.5, 0])
        left_flow_area = self.make_box(Rectangle(width=8.2, height=7), center=ORIGIN).move_to([-3, -0.5, 0])
        right_notes_area = self.make_box(Rectangle(width=5.8, height=7), center=ORIGIN).move_to([4.1, -0.5, 0])

        # ===== 내부 상태 =====
        self._header = None
        self._right_stack = VGroup()
        self._right_origin = right_notes_area.get_center()
        self._right_box = right_notes_area
        self.RIGHT_BASE_SCALE = 0.6

        # ===== 좌측: 플로우 노드 구성 =====
        nodes = []
        labels = []
        for step in HR_DATA["flow"]:
            n = self.make_node(step["id"])
            nodes.append(n)
            labels.append(step["id"])
        graph_group, edges = self.build_flow(nodes)
        self.fit_left_flow(graph_group, left_flow_area)

        # ===== Intro =====
        self.update_step(header_area, HR_DATA["company_name"])
        mission = self.make_text(HR_DATA["mission"], size=0.44, color=BRAND_TEXT)
        self.push_right(mission)
        self.play(FadeIn(graph_group, run_time=0.7))
        self.wait(0.3)

        # ===== Values(핵심가치 → 우측 스택) =====
        self.update_step(header_area, "핵심가치")
        for v in HR_DATA["values"]:
            line = self.make_text(f"• {v}", size=0.42, color=BRAND_TEXT, highlight=True)
            self.push_right(line)
            self.play(Wiggle(graph_group, scale_value=1.02, rotation_angle=0.01, run_time=0.4))
        self.wait(0.2)

        # ===== 재무지표(KPI) 섹션 =====
        self.update_step(header_area, "핵심 재무지표")
        self.clear_right()
        for i, k in enumerate(FIN_DATA["kpis"]):
            t = self.make_text(f"• {k}", size=0.40, color=BRAND_TEXT, highlight=True)
            self.push_right(t)
            if i < len(nodes):
                self.link_left(nodes, edges, labels, i)
            self.play(FadeIn(t, run_time=0.3))
        self.wait(0.4)

        # ===== 사업부문 요약 =====
        self.update_step(header_area, "사업부문")
        self.clear_right()
        for i, s in enumerate(FIN_DATA["segments"]):
            t = self.make_text(f"• {s}", size=0.40, color=BRAND_TEXT, highlight=True)
            self.push_right(t)
            self.play(FadeIn(t, run_time=0.3))
        # 좌측 플로우 포커스(사업부문 단계 인덱스: 1)
        self.link_left(nodes, edges, labels, 1)
        self.wait(0.4)

        # ===== 보수/거버넌스 =====
        self.update_step(header_area, "보수 · 거버넌스")
        self.clear_right()
        for g in FIN_DATA["governance"]:
            t = self.make_text(f"• {g}", size=0.40, color=BRAND_TEXT, highlight=True)
            self.push_right(t)
            self.play(FadeIn(t, run_time=0.25))
        self.link_left(nodes, edges, labels, 2)
        self.wait(0.4)

        # ===== 성장과제 =====
        self.update_step(header_area, "성장과제")
        self.clear_right()
        for z in FIN_DATA["growth_tasks"]:
            t = self.make_text(f"• {z}", size=0.40, color=BRAND_TEXT, highlight=True)
            self.push_right(t)
            self.play(FadeIn(t, run_time=0.25))
        self.link_left(nodes, edges, labels, 3)
        self.wait(0.4)

        # ===== CTA =====
        self.update_step(header_area, "다음 행동")
        self.clear_right()
        cta = self.make_text(HR_DATA["cta"], size=0.46, color=BRAND_PRIMARY)
        self.push_right(cta)
        self.play(FadeIn(cta, run_time=0.7))
        self.play(Wiggle(cta, scale_value=1.02, rotation_angle=0.02, run_time=0.6))
        self.wait(1.0)

        # ===== 법무 엔드카드 =====
        legal = self.make_text(HR_DATA["legal"], size=0.30, color=BRAND_TEXT)
        legal.to_edge(DOWN).to_edge(RIGHT, buff=0.4)
        self.play(FadeIn(legal, run_time=0.6))
        self.wait(0.6)
        self.play(FadeOut(legal, run_time=0.6))

    # ===== 헬퍼들 =====
    def make_text(self, s, size=0.42, color=BRAND_TEXT, highlight=False):
        # 중요 키워드 색 강조(간단 규칙: 숫자/퍼센트/천원/백만원 토큰)
        t = Text(s, font=FONT, weight="MEDIUM", color=color)
        t.set_height(size)
        if highlight:
            # 간단 하이라이트: 숫자/퍼센트/단위 포함 토큰
            try:
                parts = s.split()
                for p in parts:
                    if any(ch.isdigit() for ch in p) or ("%" in p) or ("천원" in p) or ("백만원" in p):
                        t.set_color_by_tex(p, BRAND_PRIMARY)
            except Exception:
                pass
        t.set_stroke(width=0)
        return t

    def make_node(self, label):
        box = RoundedRectangle(
            corner_radius=0.25,
            width=3.0,
            height=1.0,
            stroke_color="#6F6F6F",
            fill_color="#2A2A2A",
            fill_opacity=1.0,
            stroke_width=2
        )
        txt = Text(label, font=FONT, weight="BOLD", color=BRAND_TEXT)
        txt.set_height(0.44)
        g = VGroup(box, txt)
        txt.move_to(box.get_center())
        return g

    def build_flow(self, nodes):
        # 좌→우 균일 배치 후 엣지 연결
        g = VGroup(*nodes).arrange(RIGHT, buff=0.6)
        edges = VGroup()
        for i in range(len(nodes) - 1):
            a = Arrow(
                nodes[i].get_right(),
                nodes[i + 1].get_left(),
                buff=0.25,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.12,
                color="#8A8A8A"
            )
            edges.add(a)
        group = VGroup(g, edges)
        return group, edges

    def fit_left_flow(self, obj, target_box):
        # 단 1회 균등 스케일 후 중심 이동
        ow = obj.width
        oh = obj.height
        tw = target_box.width * 0.97
        th = target_box.height * 0.97
        s = min(tw / ow, th / oh)
        obj.scale(s)
        obj.move_to(target_box.get_center())

    def update_step(self, header_area_box, label):
        new_header = Text(label, font=FONT, weight="BOLD", color=BRAND_TEXT)
        new_header.scale_to_fit_height(0.6)
        new_header.move_to(header_area_box.get_center()).align_to(header_area_box.get_left(), LEFT).shift(RIGHT * 0.3)
        if self._header is None:
            self.play(FadeIn(new_header, run_time=0.7))
        else:
            self.play(FadeOut(self._header, run_time=0.35))
            self.play(FadeIn(new_header, run_time=0.35))
        self._header = new_header

    def clear_right(self):
        if len(self._right_stack) > 0:
            self.play(FadeOut(self._right_stack, run_time=0.3))
        self._right_stack = VGroup()

    def push_right(self, mobj):
        # 우측 스택 규칙
        mobj.scale(self.RIGHT_BASE_SCALE)
        mobj.set_max_width(self._right_box.width - 0.6)
        if len(self._right_stack) == 0:
            mobj.move_to(self._right_origin).align_to(self._right_box.get_left(), LEFT).shift(RIGHT * 0.3)
            self._right_stack.add(mobj)
            self.add(mobj)
            return
        last = self._right_stack[-1]
        mobj.next_to(last, DOWN, buff=0.35).align_to(self._right_box.get_left(), LEFT).shift(RIGHT * 0.3)
        self._right_stack.add(mobj)
        # 최대 5줄 유지
        if len(self._right_stack) > 5:
            oldest = self._right_stack[0]
            self._right_stack.remove(oldest)
            self.play(FadeOut(oldest, run_time=0.2))
            self._right_stack.shift(UP * 0.4)
        self.add(mobj)

    def link_left(self, nodes, edges, labels, idx):
        # 현재 idx 하이라이트, 이전 중립, 다음 희미
        for i, n in enumerate(nodes):
            box = n[0]
            txt = n[1]
            if i < idx:
                box.set_stroke("#5C5C5C", width=2)
                box.set_fill("#242424", opacity=1.0)
                txt.set_color("#CFCFCF")
            elif i == idx:
                box.set_stroke(BRAND_PRIMARY, width=3)
                box.set_fill("#2F2A12", opacity=1.0)
                txt.set_color(BRAND_PRIMARY)
                self.play(Wiggle(n, scale_value=1.02, rotation_angle=0.01, run_time=0.35))
            else:
                box.set_stroke("#3A3A3A", width=1)
                box.set_fill("#1F1F1F", opacity=1.0)
                txt.set_color("#9A9A9A")
        for j, e in enumerate(edges):
            if j < idx:
                e.set_stroke("#8A8A8A", width=3)
            elif j == idx - 1:
                e.set_stroke(BRAND_PRIMARY, width=3)
            else:
                e.set_stroke("#4A4A4A", width=2)

    def make_box(self, rect, center=ORIGIN):
        # 레이아웃 가이드용 객체(실제 표시 안 함)
        rect.set_stroke(width=0)
        rect.set_fill(color="#000000", opacity=0.0)
        rect.move_to(center)
        self.add(rect)
        return rect
