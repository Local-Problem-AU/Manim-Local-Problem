from manim import *
import numpy as np

# ===== Config & Brand =====
config.pixel_width  = 1400
config.pixel_height = 800
config.frame_width  = 14
config.frame_height = 8

BRAND_PRIMARY = "#FFD54F"  # focus/accent
BRAND_TEXT    = "#FFFFFF"
BRAND_ACCENT  = "#4FC3F7"
BRAND_BG      = "#1E1E1E"

FONT = "Malgun Gothic"  # mac: "Apple SD Gothic Neo", fallback: "Noto Sans CJK KR", "NanumGothic"


# ===== Data =====
HR_DATA = {
    "company_name": "경동도시가스",
    "mission": "미션/비전 문장 한 줄로 요약해 주세요.",  # 예: "안전하고 편리한 에너지로 삶의 질을 높입니다."
    "values": ["고객집착", "주인의식", "협업", "성장"],
    "flow": [
        {"id": "입사",           "desc": "첫날 환영 · 계정 발급 · 필수 서류 완료"},
        {"id": "교육",           "desc": "안전/보안 · 제품/서비스 · 조직문화 교육"},
        {"id": "고객 가치 창출",  "desc": "현장/민원/운영 이슈 해결 · 피드백 루프"},
        {"id": "성장",           "desc": "멘토링 · 역량개발 · 커리어 프레임 설정"},
    ],
    "cta": "지금 팀에 질문하고, 첫 주 목표를 공유하세요.",
    "legal": "ⓒ Kyungdong City Gas. 내부용. 무단배포 금지.",
    "locale": "ko",
}


class OnboardingFlow(Scene):
    def construct(self):
        # ===== 배경/안내 =====
        self.camera.background_color = BRAND_BG

        # ===== 레이아웃 영역 정의 (좌표 규격 고정) =====
        header_area = self.make_box(np.array([-7,  3, 0]), np.array([ 7,  4, 0]), stroke_width=0)
        left_flow   = self.make_box(np.array([-7, -4, 0]), np.array([ 1.2, 3, 0]), stroke_width=0)
        right_notes = self.make_box(np.array([ 1.2,-4, 0]), np.array([ 7,  3, 0]), stroke_width=0)

        # 내부 상태
        self._header_obj = None
        self.right_stack = VGroup()
        RIGHT_BASE_SCALE = 0.6

        # ===== 회사명/로고 (텍스트 대체) =====
        brand_label = (
            Text(HR_DATA["company_name"], font=FONT, weight="BOLD", color=BRAND_PRIMARY)
            .scale_to_fit_height(0.6)
            .move_to(header_area.get_left() + RIGHT * 0.4)
        )
        self.add(brand_label)

        # ===== 좌측: 노드/엣지 초기 생성 (모든 요소를 먼저 만든 뒤 1회 스케일/배치) =====
        node_labels = [step["id"] for step in HR_DATA["flow"]]
        nodes = VGroup(*[self.make_node(lbl) for lbl in node_labels])
        nodes.arrange(RIGHT, buff=1.0)

        edges = VGroup()
        for i in range(len(nodes) - 1):
            e = self.make_edge(nodes[i], nodes[i + 1])
            edges.add(e)

        # 값 태그(핵심가치 일부를 노드 하단에 매칭)
        tags = VGroup()
        for i, n in enumerate(nodes):
            if i < len(HR_DATA["values"]):
                t = (
                    Text(HR_DATA["values"][i], font=FONT, color=BRAND_ACCENT)
                    .scale(0.35)
                    .next_to(n, DOWN, buff=0.18)
                )
                tags.add(t)
        left_group = VGroup(nodes, edges, tags)

        # 좌측 1회 균등 스케일 & 위치 이동 (재스케일 금지)
        self.fit_left_flow(left_group, left_flow)

        # 초기 가시성 낮춤(인트로에서 은은히 표시)
        for m in left_group:
            m.set_opacity(0.35)
        for n in nodes:
            for c in n:
                c.set_opacity(0.35)

        # ===== 섹션 1: Intro (회사/미션) =====
        self.update_step("회사 소개", header_area)
        self.play(
            FadeIn(nodes, lag_ratio=0.1, run_time=0.7),
            FadeIn(edges, run_time=0.7),
            FadeIn(tags, run_time=0.7),
        )
        self.clear_right(right_notes)
        self.push_right(Text(HR_DATA["mission"], font=FONT, color=BRAND_TEXT), right_notes, RIGHT_BASE_SCALE)

        # ===== 섹션 2: Values (핵심가치) =====
        self.update_step("핵심가치", header_area)
        self.clear_right(right_notes)
        for v in HR_DATA["values"]:
            line = Text(v, font=FONT, color=BRAND_TEXT)
            self.push_right(line, right_notes, RIGHT_BASE_SCALE)
            self.play(line.animate.set_color(BRAND_PRIMARY), run_time=0.2)
            self.play(line.animate.set_color(BRAND_TEXT), run_time=0.2)

        # 노드 하단 태그를 또렷하게
        self.play(*[t.animate.set_opacity(1.0) for t in tags], run_time=0.5)

        # ===== 섹션 3: Flow (입사→교육→고객 가치 창출→성장) =====
        self.update_step("온보딩 흐름", header_area)
        created_edge = set()
        self.play(*[m.animate.set_opacity(1.0) for m in left_group], run_time=0.4)

        for idx, step in enumerate(HR_DATA["flow"]):
            self.push_right(Text(step["desc"], font=FONT, color=BRAND_TEXT), right_notes, RIGHT_BASE_SCALE)
            self.link_left(nodes, edges, idx, created_edge)
            self.wait(0.2)

        # ===== 섹션 4: Growth & Support =====
        self.update_step("성장 & 지원", header_area)
        self.clear_right(right_notes)
        growth_lines = [
            "멘토링 · 1:1 온보딩 체크인",
            "업무 도구: 그룹웨어 · 메신저 · 문서 템플릿",
            "역량개발: 사내교육 · 직무 교육 · 세미나",
        ]
        for g in growth_lines:
            self.push_right(Text(g, font=FONT, color=BRAND_TEXT), right_notes, RIGHT_BASE_SCALE)
            self.wait(0.1)

        # 보조 서브노드(점선)로 마지막 노드 주변 표시
        if len(nodes) > 0:
            last = nodes[-1]
            sub1 = RoundedRectangle(
                corner_radius=0.15, width=1.8, height=0.6,
                stroke_color=BRAND_ACCENT, stroke_opacity=0.8, stroke_width=2
            )
            sub2 = RoundedRectangle(
                corner_radius=0.15, width=1.8, height=0.6,
                stroke_color=BRAND_ACCENT, stroke_opacity=0.8, stroke_width=2
            )
            sub1.set_fill("#000000", opacity=0.0)
            sub2.set_fill("#000000", opacity=0.0)
            sub1.next_to(last, UP + RIGHT, buff=0.25)
            sub2.next_to(last, DOWN + RIGHT, buff=0.25)
            s1t = Text("멘토링", font=FONT, color=BRAND_TEXT).scale(0.35).move_to(sub1.get_center())
            s2t = Text("사내교육", font=FONT, color=BRAND_TEXT).scale(0.35).move_to(sub2.get_center())
            dotted = VGroup(sub1, sub2, s1t, s2t)
            self.play(FadeIn(dotted, run_time=0.5))

        # ===== 섹션 5: CTA =====
        self.update_step("시작할까요?", header_area)
        self.clear_right(right_notes)
        cta = Text(HR_DATA["cta"], font=FONT, color=BRAND_PRIMARY)
        self.push_right(cta, right_notes, RIGHT_BASE_SCALE)
        self.play(*[n[0].animate.set_stroke(color=BRAND_TEXT, width=2) for n in nodes], run_time=0.3)
        if len(nodes) > 0:
            self.play(
                nodes[-1][0].animate.set_stroke(color=BRAND_PRIMARY, width=4),
                Wiggle(nodes[-1][0], scale_value=1.02),
                run_time=0.7,
            )

        # ===== 법무(엔드카드) =====
        legal = Text(HR_DATA["legal"], font=FONT, color="#AAAAAA").scale(0.35)
        legal.to_corner(DR, buff=0.25)
        self.play(FadeIn(legal), run_time=0.6)
        self.wait(0.6)
        self.play(FadeOut(legal), run_time=0.4)

    # ===== 헬퍼들 =====
    def make_box(self, p1, p2, **kw):
        center = (p1 + p2) / 2
        w = abs(p2[0] - p1[0])
        h = abs(p2[1] - p1[1])
        r = Rectangle(width=w, height=h, **kw).move_to(center)
        return r

    def fit_left_flow(self, obj, left_flow):
        # 단 1회 균등 스케일 후 중심 이동 (재스케일 금지)
        s = min((left_flow.width * 0.97) / obj.width, (left_flow.height * 0.97) / obj.height)
        obj.scale(s)
        obj.move_to(left_flow.get_center())

    def make_node(self, label):
        box = RoundedRectangle(
            corner_radius=0.25, width=2.6, height=1.1,
            stroke_color=BRAND_TEXT, stroke_width=2,
            fill_color="#000000", fill_opacity=0.0
        )
        txt = Text(label, font=FONT, color=BRAND_TEXT).scale(0.45)
        grp = VGroup(box, txt).arrange(DOWN, buff=0.0)
        txt.move_to(box.get_center())
        return grp

    def make_edge(self, n1, n2, label=None):
        start = n1[0].get_right()
        end   = n2[0].get_left()
        arr = Arrow(start, end, buff=0.2, stroke_color=BRAND_TEXT, stroke_width=2, max_tip_length_to_length_ratio=0.08)
        if label:
            t = Text(label, font=FONT, color=BRAND_TEXT).scale(0.35)
            t.next_to(arr, UP, buff=0.05)
            return VGroup(arr, t)
        return arr

    def update_step(self, label, header_area):
        new_header = (
            Text(label, font=FONT, weight="BOLD", color=BRAND_TEXT)
            .scale_to_fit_height(0.6)
            .move_to(header_area.get_center())
        )
        if self._header_obj is None:
            self._header_obj = new_header
            self.add(self._header_obj)
            return
        old = self._header_obj
        self.play(FadeOut(old, run_time=0.35))
        self._header_obj = new_header
        self.play(FadeIn(self._header_obj, run_time=0.35))

    def clear_right(self, right_notes):
        if len(self.right_stack) == 0:
            return
        self.play(*[FadeOut(m, run_time=0.25) for m in self.right_stack])
        self.right_stack = VGroup()

    def push_right(self, mobj, right_notes, RIGHT_BASE_SCALE=0.6):
        mobj.scale(RIGHT_BASE_SCALE)
        max_w = right_notes.width - 0.6
        if mobj.width > max_w:
            mobj.scale_to_fit_width(max_w)
        if len(self.right_stack) == 0:
            mobj.move_to(right_notes.get_center()).align_to(right_notes.get_left(), LEFT)
            self.right_stack.add(mobj)
            self.play(FadeIn(mobj, run_time=0.35))
        else:
            prev = self.right_stack[-1]
            mobj.next_to(prev, DOWN, buff=0.35).align_to(right_notes.get_left(), LEFT)
            # 최대 5줄 유지
            if len(self.right_stack) >= 5:
                first = self.right_stack[0]
                self.right_stack.remove(first)
                self.play(FadeOut(first, run_time=0.2))
                for i, it in enumerate(self.right_stack):
                    it.shift(UP * 0.4)
            self.right_stack.add(mobj)
            self.play(FadeIn(mobj, run_time=0.3))

    def link_left(self, nodes, edges, idx, created_edge_set):
        # 이전/다음/현재 스타일
        for i, n in enumerate(nodes):
            box = n[0]
            if i < idx:
                box.set_stroke(color=BRAND_TEXT, width=2)
                n[1].set_color(BRAND_TEXT)
                n.set_opacity(1.0)
            elif i == idx:
                box.set_stroke(color=BRAND_PRIMARY, width=4)
                n[1].set_color(BRAND_TEXT)
                self.play(Wiggle(box, scale_value=1.02), run_time=0.35)
            else:
                box.set_stroke(color="#888888", width=1)
                n[1].set_color("#BBBBBB")
                n.set_opacity(0.9)
        # 해당 엣지 Create
        if idx - 1 >= 0 and (idx - 1) not in created_edge_set:
            created_edge_set.add(idx - 1)
            self.play(Create(edges[idx - 1]), run_time=0.35)
