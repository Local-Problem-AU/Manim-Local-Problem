from manim import *
import os

# ---------- Brand Colors ----------
BRAND_BG       = "#0E1526"  # 다크 네이비
BRAND_PANEL    = "#141B2E"  # 패널
BRAND_PRIMARY  = "#3BB4E6"  # 시안 포인트
BRAND_ACCENT   = "#E84545"  # 레드 포인트
BRAND_TEXT     = "#E9EEF7"  # 본문 텍스트
BRAND_MUTED    = "#AAB6CF"  # 보조 텍스트
BRAND_STROKE   = "#334066"  # 보더

# ---------- Font ----------
FONT = "Malgun Gothic"  # Windows 권장 (Noto Sans CJK KR 설치 시 변경 가능)

# ---------- Data ----------
ASSET_HERO = "성우하이텍.png"  # 홈페이지 캡처 이미지 경로

HR = {
    "company_name": "성우하이텍 (Sungwoo Hitech)",
    "mission": "경량·고강도 차체로 안전하고 지속가능한 이동을 만듭니다.",
    "values": ["안전", "품질", "지속가능성", "협력", "성장"],
    "onboarding_flow": [
        {"id":"입사", "desc":"첫날 환영 · 계정/보호구 발급 · 보안서약"},
        {"id":"교육", "desc":"안전/보건, 품질기준, 차체·프레스·용접 공정, ESG"},
        {"id":"고객가치", "desc":"경량화·충돌안전 솔루션, 불량 제로 도전"},
        {"id":"성장", "desc":"멘토링 · 교육포털 · 직무역량 · 커리어 프레임"}
    ],
    "rnd_highlights": [
        "차체 구조해석/경량 설계",
        "충돌/강성/진동 해석",
        "용접·접합 기술",
        "신소재·성형 공정"
    ],
    "news_examples": [
        "지역 협력 투자·상생 사례",
        "공정거래/윤리경영 활동",
        "국제 행사·지역 사회 공헌"
    ],
    "talent_points": [
        "문제 해결형 실무 러닝",
        "멘토 1:1 온보딩 동행",
        "개선제안 · 품질·안전 활동"
    ],
    "members": ["HYUNDAI", "KIA", "GM", "Volkswagen", "Mercedes-Benz",
                "Audi", "Nissan", "Jaguar", "Chevrolet", "Samsung 전장"],
    "cta": "첫 주 안전·품질 체크리스트 완료 → 멘토와 1:1 목표 공유",
    "legal": "ⓒ Sungwoo Hitech. 내부 교육용. 무단 배포 금지."
}


# ============================================================
# Main Scene
# ============================================================
class SWH_Onboarding(Scene):
    def construct(self):
        self.camera.background_color = BRAND_BG

        # 레이아웃 박스
        header_box  = self._box([-7,  3, 0], [ 7, 4, 0])  # 헤더
        left_box    = self._box([-7, -4, 0], [ 1.2, 3, 0])  # 좌: 흐름도
        right_box   = self._box([ 1.2,-4, 0], [ 7, 3, 0])  # 우: 본문/패널

        # 배경 연출
        self._maybe_hero_bg()

        # 좌측 온보딩 플로우 그래프
        nodes, edges, graph = self._build_flow([s["id"] for s in HR["onboarding_flow"]])
        self._fit_to_box(graph, left_box, scale_pad=0.96)

        # 헤더 초기화
        self._header = None
        self._right_stack = VGroup()

        # Intro
        self._set_header(header_box, HR["company_name"])
        intro = self._text(HR["mission"], size=46, weight="BOLD",
                           t2c={k:BRAND_PRIMARY for k in ["경량","고강도","안전","지속가능"]})
        self._panel_push(right_box, intro)
        self.play(LaggedStart(*[FadeIn(n, shift=DOWN*0.1) for n in nodes], lag_ratio=0.08), run_time=0.6)
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.08), run_time=0.6)

        # Values
        self._set_header(header_box, "핵심가치")
        self._panel_clear()
        for i, v in enumerate(HR["values"]):
            tag = self._chip(v)
            tag.next_to(nodes[min(i, len(nodes)-1)], DOWN, buff=0.22)
            self.play(GrowFromCenter(tag), run_time=0.25)
        for v in HR["values"]:
            line = self._text(v, size=38, weight="BOLD", t2c={v:BRAND_PRIMARY})
            self._panel_push(right_box, line)

        # R&D CENTER
        self._set_header(header_box, "R&D CENTER")
        self._panel_clear()
        rnd_title = self._text("핵심 연구영역", size=40, weight="BOLD")
        self._panel_push(right_box, rnd_title)
        for h in HR["rnd_highlights"]:
            self._panel_push(right_box, self._bullet(h))

        # ISSUE
        self._set_header(header_box, "ISSUE")
        self._panel_clear()
        news_title = self._text("최근 소식(예시)", size=40, weight="BOLD")
        self._panel_push(right_box, news_title)
        for n in HR["news_examples"]:
            self._panel_push(right_box, self._bullet(n))

        # 인재육성
        self._set_header(header_box, "인재육성")
        self._panel_clear()
        self._panel_push(right_box, self._text("현장 밀착형 성장 지원", size=40, weight="BOLD"))
        for t in HR["talent_points"]:
            self._panel_push(right_box, self._bullet(t))

        # 온보딩 흐름
        self._set_header(header_box, "온보딩 흐름")
        self._panel_clear()
        for idx, step in enumerate(HR["onboarding_flow"]):
            self._link_focus(nodes, edges, idx)
            desc = self._text(f"[{step['id']}] {step['desc']}", size=36, weight="MEDIUM",
                              t2c={step["id"]:BRAND_PRIMARY})
            self._panel_push(right_box, desc)
            self.play(Wiggle(nodes[idx], scale_value=1.02), run_time=0.4)

        # MEMBERS
        self._set_header(header_box, "MEMBERS")
        self._panel_clear()
        self._panel_push(right_box, self._text("함께하는 고객사(텍스트 표기)", size=38, weight="BOLD"))
        chip_row = self._chips(HR["members"])
        self._panel_push(right_box, chip_row, animate=False)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT*0.1) for c in chip_row], lag_ratio=0.05), run_time=0.6)

        # CTA
        self._set_header(header_box, "함께 만드는 안전·품질·성장")
        self._panel_clear()
        cta = self._text(HR["cta"], size=42, weight="BOLD",
                         t2c={"체크리스트":BRAND_PRIMARY,"멘토":BRAND_PRIMARY,"목표":BRAND_PRIMARY})
        self._panel_push(right_box, cta)

        # 좌측 전체 강조
        highlight = SurroundingRectangle(graph, color=BRAND_PRIMARY, stroke_width=3).set_opacity(0.95)
        self.play(Create(highlight), run_time=0.5)
        self.play(Indicate(nodes[-1], color=BRAND_ACCENT, scale_factor=1.05), run_time=0.6)
        self.play(FadeOut(highlight), run_time=0.4)

        # Legal
        legal = Text(HR["legal"], font=FONT, weight="MEDIUM", color=BRAND_MUTED).scale(0.35)
        legal.to_edge(DR, buff=0.3)
        self.play(FadeIn(legal), run_time=0.4)
        self.wait(0.6)


    # ===================== Helpers =====================
    def _maybe_hero_bg(self):
        if os.path.exists(ASSET_HERO):
            try:
                hero = ImageMobject(ASSET_HERO)
                hero.set_opacity(0.10)
                hero.set_width(config.frame_width * 1.05)
                hero.set_z_index(-10)
                self.add(hero)
            except Exception:
                pass

    def _box(self, p1, p2):
        w = abs(p2[0]-p1[0]); h = abs(p2[1]-p1[1])
        c = [(p1[0]+p2[0])/2, (p1[1]+p2[1])/2, 0]
        return Rectangle(width=w, height=h, stroke_width=0, fill_opacity=0).move_to(c)

    def _fit_to_box(self, obj, box, scale_pad=0.95):
        s = min((box.width*scale_pad)/obj.width, (box.height*scale_pad)/obj.height)
        obj.scale(s)
        obj.move_to(box.get_center())

    def _text(self, s, size=36, weight="MEDIUM", color=BRAND_TEXT, t2c=None):
        t = Text(s, font=FONT, weight=weight, color=color, t2c=t2c)
        t.scale(size/36.0)
        return t

    def _bullet(self, s):
        dot = Dot(radius=0.055, color=BRAND_PRIMARY).set_stroke(width=0)
        txt = self._text(s, size=34, weight="MEDIUM", color=BRAND_TEXT)
        g = VGroup(dot, txt).arrange(RIGHT, buff=0.25)
        return g

    def _chip(self, s):
        t = self._text(s, size=28, weight="BOLD", color=BRAND_TEXT)
        rr = RoundedRectangle(corner_radius=0.20, width=t.width+0.45, height=t.height+0.30)
        rr.set_fill(BRAND_PANEL, opacity=1.0).set_stroke(BRAND_STROKE, width=2, opacity=0.95)
        g = VGroup(rr, t)
        t.move_to(rr.get_center())
        return g

    def _chips(self, items, cols=3):
        chips = VGroup(*[self._chip(s) for s in items])
        chips.arrange_in_grid(rows=((len(items)-1)//cols)+1, cols=cols, buff=0.25, cell_alignment=LEFT)
        return chips

    def _panel_clear(self):
        if hasattr(self, "_right_stack") and len(self._right_stack)>0:
            self.play(LaggedStart(*[FadeOut(m, shift=UP*0.12) for m in self._right_stack], lag_ratio=0.10), run_time=0.45)
        self._right_stack = VGroup()
        self.add(self._right_stack)

    def _panel_push(self, right_box, mobj, animate=True):
        # 배경 패널
        if len(self._right_stack)==0:
            panel = RoundedRectangle(corner_radius=0.22, width=right_box.width*0.96, height=right_box.height*0.96)
            panel.set_fill(BRAND_PANEL, opacity=0.92).set_stroke(BRAND_STROKE, width=2, opacity=1.0)
            panel.move_to(right_box.get_center())
            self._right_panel = panel
            self.add(panel)
        # 아이템 배치
        mobj.set_max_width(right_box.width*0.86)
        if len(self._right_stack)==0:
            mobj.move_to(self._right_panel.get_top()).shift(DOWN*0.7).align_to(self._right_panel.get_left(), LEFT).shift(RIGHT*0.5)
        else:
            prev = self._right_stack[-1]
            mobj.next_to(prev, DOWN, buff=0.3).align_to(prev, LEFT)
        self._right_stack.add(mobj)
        if animate:
            self.play(FadeIn(mobj, shift=RIGHT*0.15), run_time=0.32)
        else:
            self.add(mobj)

    def _set_header(self, header_box, label):
        new_h = self._text(label, size=54, weight="BOLD",
                           t2c={"안전":"#FFD54F","품질":"#FFD54F"})
        new_h.move_to(header_box.get_center())
        underline = Line(header_box.get_left()+RIGHT*0.2, header_box.get_right()+LEFT*0.2, stroke_width=3, color=BRAND_STROKE)
        underline.next_to(new_h, DOWN, buff=0.15)
        group = VGroup(new_h, underline)
        if hasattr(self, "_header") and self._header:
            self.play(FadeOut(self._header, shift=UP*0.2), run_time=0.25)
        self._header = group
        self.play(FadeIn(group, shift=DOWN*0.2), run_time=0.35)

    def _build_flow(self, labels):
        nodes = [self._node(l) for l in labels]
        row = VGroup(*nodes).arrange(RIGHT, buff=0.6)
        edges = []
        for i in range(len(nodes)-1):
            a = Arrow(nodes[i].get_right(), nodes[i+1].get_left(), buff=0.22, stroke_width=3, max_tip_length_to_length_ratio=0.06)
            a.set_color(BRAND_STROKE).set_opacity(0.9)
            edges.append(a)
        graph = VGroup(row, *edges)
        return nodes, edges, graph

    def _node(self, label):
        txt = self._text(label, size=34, weight="BOLD")
        padx, pady = 0.6, 0.35
        rect = RoundedRectangle(corner_radius=0.22, width=txt.width+padx, height=txt.height+pady)
        rect.set_fill("#1B2238", opacity=1.0).set_stroke(BRAND_STROKE, width=2)
        return VGroup(rect, txt)

    def _link_focus(self, nodes, edges, idx):
        for i, n in enumerate(nodes):
            rect, txt = n[0], n[1]
            if i < idx:
                rect.set_fill("#1B2238", opacity=1.0).set_stroke("#6C7AAA", width=2)
                txt.set_color(BRAND_MUTED)
                n.set_opacity(0.95)
            elif i == idx:
                rect.set_fill("#222C49", opacity=1.0).set_stroke(BRAND_PRIMARY, width=4)
                txt.set_color(BRAND_TEXT)
                n.set_opacity(1.0)
            else:
                rect.set_fill("#151C30", opacity=0.95).set_stroke(BRAND_STROKE, width=2)
                txt.set_color("#BFC7DA")
                n.set_opacity(0.82)

        for e_i, e in enumerate(edges):
            if e_i < idx-1:
                e.set_color("#7C8CB6").set_stroke(width=3, opacity=0.95)
            elif e_i == idx-1:
                e.set_color(BRAND_PRIMARY).set_stroke(width=4, opacity=1.0)
                self.play(Create(e), run_time=0.28)
            else:
                e.set_color(BRAND_STROKE).set_stroke(width=2, opacity=0.7)
