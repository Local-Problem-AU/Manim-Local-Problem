# -*- coding: utf-8 -*-
# Manim Community 0.19.x
# 파일명 예: hdhi_report_2025H1.py
# 실행 예: manim -pqh hdhi_report_2025H1.py HDHI_Report_2025H1

from manim import *
import numpy as np
import math

# ===== 폰트/테마 =====
FONT = "Malgun Gothic"  # mac/Linux는 Noto Sans CJK KR 등으로 교체
BG = "#0F1226"
FG = "#FFFFFF"
MUTED = "#8A8FA6"
GRID = "#1B1F3B"
PRIMARY = "#FFD54F"
ACCENT = "#4FC3F7"
ACCENT2 = "#9AFFDF"
ACCENT3 = "#7A83C6"

# ===== 데이터 (보고서 원문 기반, 단위: 백만원 / 일부 표시는 조원 환산) =====
DATA = {
    "period": "2025년 상반기(6월 30일 기준)",
    "company": "HD현대중공업",
    "sales_total": 7_969_641,
    "operating_profit": 905_190,
    "export_sales": 7_501_697,
    "domestic_sales": 467_944,
    "segment_sales": [
        {"label": "조선", "value": 5_592_961, "ratio": 70.18},
        {"label": "엔진기계", "value": 1_929_974, "ratio": 24.22},
        {"label": "해양플랜트", "value": 405_071, "ratio": 5.08},
        {"label": "기타", "value": 41_635, "ratio": 0.52},
    ],
    "backlog_total": 46_344_247,
    "backlog_by_item": [
        {"label": "조선", "value": 33_261_399},
        {"label": "해양플랜트", "value": 3_019_810},
        {"label": "기타", "value": 10_063_038},
    ],
    "rd_expense": 53_986,
    "rd_ratio_pct": 0.66,
    "debt_ratio_pct": 219.30,
    "cash_like": 2_835_973,
    "borrowings": 822_657,
    "interest_coverage": 17.08,
    "capacity": [
        {"label": "선박", "value": "5,000천 GT"},
        {"label": "대형/중형 엔진(본사)", "value": "8,000천 BHP"},
        {"label": "중형 엔진(HD현대엔진)", "value": "489천 BHP"},
        {"label": "해양플랜트", "value": "*Note (H-Dock 선박 Max. 1,200천 GT/년)"},
    ],
    "raw_material_prices": {
        "years": ["2023", "2024", "2025H1"],
        "steel_plate": [1_130_000, 958_500, 913_000],
        "h_beam": [1_021_000, 878_000, 846_000],
        "unit": "원/TON",
        "note": "스틸데일리 공시(SS275 20T / 앵글 SS400) 평균"
    },
    "highlights": [
        "매출 7.97조원(+수출 94% 비중) · 영업이익 0.91조원",
        "수주잔고 46.3조원(조선 33.3조/기타 10.1조/해양 3.0조)",
        "R&D 539.9억원, 매출 대비 0.66%",
        "부채비율 219.3%, 현금성 2.84조 vs 차입금 0.82조",
        "이자보상배율 17.08배로 안정적",
        "친환경 DF엔진·해상풍력·SMR 등 포트폴리오 확장"
    ],
}

# ===== 유틸 =====
def fmt_krw_billion(x_million: int) -> str:
    jo = x_million / 1_000_000
    if jo >= 1:
        return f"{jo:.2f}조원"
    uk = x_million / 10_000
    return f"{uk:.1f}억원"

def make_kpi_box(title, value, subtitle=None, width=3.6, height=1.6):
    box = RoundedRectangle(
        corner_radius=0.2, width=width, height=height,
        stroke_color=GRID, stroke_width=2,
        fill_color="#161A33", fill_opacity=1.0
    )
    t1 = Text(title, font=FONT, weight="MEDIUM", color=MUTED).scale(0.36)
    t1.move_to(box.get_top()).shift(DOWN * 0.35)
    t2 = Text(value, font=FONT, weight="BOLD", color=PRIMARY).scale(0.6)
    t2.next_to(t1, DOWN, buff=0.15).align_to(t1, LEFT)
    if subtitle:
        t3 = Text(subtitle, font=FONT, weight="MEDIUM", color=FG).scale(0.32)
        t3.next_to(t2, DOWN, buff=0.1).align_to(t1, LEFT)
        grp = VGroup(box, t1, t2, t3)
    else:
        grp = VGroup(box, t1, t2)
    grp[0].set_z_index(1)
    for m in grp[1:]:
        m.set_z_index(2)
    return grp

def donut(values, labels, colors, inner_ratio=0.55, r=1.6):
    total = sum(values)
    start = -PI / 2
    arcs = VGroup()
    lbls = VGroup()
    for i, v in enumerate(values):
        angle = (v / total) * TAU
        arc = AnnularSector(
            inner_radius=r * inner_ratio, outer_radius=r,
            start_angle=start, angle=angle,
            color=colors[i], fill_opacity=1.0, stroke_width=0
        )
        arcs.add(arc)
        mid = start + angle / 2
        p_in = np.array([math.cos(mid), math.sin(mid), 0.0]) * r * 0.92
        p_out = np.array([math.cos(mid), math.sin(mid), 0.0]) * (r + 0.3)
        line = Line(p_in, p_out, color=colors[i], stroke_width=2)
        percent = v / total * 100.0
        lab = Text(f"{labels[i]} {percent:.1f}%", font=FONT, weight="BOLD", color=FG).scale(0.36)
        if math.cos(mid) >= 0:
            lab.next_to(p_out, RIGHT, buff=0.08).align_to(p_out, UP)
        else:
            lab.next_to(p_out, LEFT, buff=0.08).align_to(p_out, UP)
        lbls.add(VGroup(line, lab))
        start += angle
    return VGroup(arcs, lbls)

def hor_bar(values, labels, width=4.6, bar_h=0.28, colors=None):
    max_v = max(values)
    bars = VGroup()
    h = bar_h
    gap = 0.16
    y = 0.0
    for i, v in enumerate(values):
        w = (v / max_v) * width
        c = colors[i] if colors else ACCENT
        bg = Rectangle(width=width, height=h, stroke_width=1, stroke_color=GRID, fill_color="#11142B", fill_opacity=1.0)
        fg = Rectangle(width=w, height=h, stroke_width=0, fill_color=c, fill_opacity=1.0).align_to(bg, LEFT)
        row = VGroup(bg, fg)
        lab = Text(labels[i], font=FONT, weight="MEDIUM", color=MUTED).scale(0.34)
        lab.next_to(row, LEFT, buff=0.28)
        val = Text(fmt_krw_billion(v), font=FONT, weight="BOLD", color=FG).scale(0.34)
        val.next_to(row, RIGHT, buff=0.15)
        grp = VGroup(row, lab, val)
        grp.move_to(np.array([0.0, -y, 0.0]))
        y += (h + gap)
        bars.add(grp)
    bars.shift(UP * ((bars.height) / 2 - bar_h / 2))
    return bars

def price_axes(title, xlabels, xmin=0, xmax=2, ymin=800_000, ymax=1_200_000, width=5.6, height=3.0):
    ax = Axes(
        x_range=[xmin, xmax, 1], y_range=[ymin, ymax, 100_000],
        x_length=width, y_length=height,
        axis_config={"include_numbers": False, "stroke_color": GRID, "stroke_width": 2},
        tips=False
    )
    xlabs = VGroup()
    for i, s in enumerate(xlabels):
        tx = Text(s, font=FONT, weight="MEDIUM", color=MUTED).scale(0.3)
        tx.next_to(ax.c2p(i, ymin), DOWN, buff=0.15)
        xlabs.add(tx)
    ylabs = VGroup()
    for val in range(ymin, ymax + 1, 100_000):
        ty = Text(f"{val//1000}k", font=FONT, weight="MEDIUM", color=GRID).scale(0.26)
        ty.next_to(ax.c2p(xmin, val), LEFT, buff=0.15)
        ylabs.add(ty)
    title_text = Text(title, font=FONT, weight="BOLD", color=FG).scale(0.4)
    return ax, xlabs, ylabs, title_text

# ===== 메인 씬 =====
class HDHI_Report_2025H1(Scene):
    def construct(self):
        config.frame_width = 14
        config.frame_height = 8
        self.camera.background_color = BG

        header = Text(
            f"{DATA['company']} — {DATA['period']} 주요 재무지표 & 사업내용",
            font=FONT, weight="BOLD", color=FG
        ).scale(0.6).to_edge(UP).shift(DOWN * 0.2)
        sub = Text("단위: 백만원(₩) · 표시는 조원 환산", font=FONT, weight="MEDIUM", color=MUTED).scale(0.32)
        sub.next_to(header, DOWN, buff=0.12)
        line = Line(LEFT * 6.4, RIGHT * 6.4, color=GRID, stroke_width=2).next_to(sub, DOWN, buff=0.18)
        self.play(FadeIn(header, shift=UP * 0.2), FadeIn(sub), Create(line), run_time=0.9)

        k1 = make_kpi_box("매출액", fmt_krw_billion(DATA["sales_total"]), f"수출 {DATA['export_sales']/DATA['sales_total']*100:.1f}%")
        k2 = make_kpi_box("영업이익", fmt_krw_billion(DATA["operating_profit"]), f"이자보상배율 {DATA['interest_coverage']:.2f}배")
        k3 = make_kpi_box("수주잔고", fmt_krw_billion(DATA["backlog_total"]), "중장기 물량 안정")
        k4 = make_kpi_box("R&D", fmt_krw_billion(DATA["rd_expense"]), f"매출 대비 {DATA['rd_ratio_pct']:.2f}%")
        k1.to_corner(UL).shift(DOWN * 0.7 + RIGHT * 0.2)
        k2.next_to(k1, RIGHT, buff=0.3)
        k3.next_to(k2, RIGHT, buff=0.3)
        k4.next_to(k3, RIGHT, buff=0.3)
        self.play(*[FadeIn(k, shift=UP * 0.2) for k in [k1, k2, k3, k4]], run_time=1.0)

        seg_values = [s["value"] for s in DATA["segment_sales"]]
        seg_labels = [s["label"] for s in DATA["segment_sales"]]
        seg_colors = [PRIMARY, ACCENT, ACCENT2, ACCENT3]
        d = donut(seg_values, seg_labels, seg_colors, inner_ratio=0.60, r=1.8)
        d_title = Text("사업부문별 매출 구성", font=FONT, weight="BOLD", color=FG).scale(0.4)
        d_grp = VGroup(d_title, d).arrange(DOWN, buff=0.25).move_to(np.array([-4.4, -0.6, 0.0]))
        self.play(GrowFromCenter(d[0]), run_time=0.9)
        for i in range(len(seg_values)):
            self.play(Write(d[1][i][1]), run_time=0.2)
        self.add(d_title)

        reg_values = [DATA["export_sales"], DATA["domestic_sales"]]
        reg_labels = ["수출", "국내"]
        bars = hor_bar(reg_values, reg_labels, width=4.2, bar_h=0.26, colors=[ACCENT, ACCENT3])
        bars_title = Text("지역별 매출", font=FONT, weight="BOLD", color=FG).scale(0.4).next_to(bars, UP, buff=0.25)
        bars_grp = VGroup(bars_title, bars).move_to(np.array([-4.4, -2.8, 0.0]))
        self.play(FadeIn(bars_title, shift=UP * 0.2))
        for row in bars:
            self.play(GrowFromEdge(row[0][1], LEFT), FadeIn(row[1]), FadeIn(row[2]), run_time=0.25)

        bl_values = [b["value"] for b in DATA["backlog_by_item"]]
        bl_labels = [b["label"] for b in DATA["backlog_by_item"]]
        bl_bars = hor_bar(bl_values, bl_labels, width=5.3, bar_h=0.24, colors=[PRIMARY, ACCENT, ACCENT3])
        bl_title = Text("수주잔고 구성", font=FONT, weight="BOLD", color=FG).scale(0.4).next_to(bl_bars, UP, buff=0.22)
        bl_note = Text(f"합계: {fmt_krw_billion(DATA['backlog_total'])}", font=FONT, weight="MEDIUM", color=MUTED).scale(0.34)
        bl_note.next_to(bl_bars, DOWN, buff=0.18)
        right_top = VGroup(bl_title, bl_bars, bl_note).move_to(np.array([3.9, 0.4, 0.0]))
        self.play(FadeIn(bl_title), *[GrowFromEdge(r[0][1], LEFT) for r in bl_bars], run_time=0.6)
        self.play(FadeIn(bl_note), run_time=0.3)

        bullets = VGroup(*[
            VGroup(Dot(radius=0.04, color=PRIMARY), Text(s, font=FONT, weight="MEDIUM", color=FG).scale(0.36)).arrange(RIGHT, buff=0.18)
            for s in DATA["highlights"]
        ])
        bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        bullets_title = Text("사업 하이라이트", font=FONT, weight="BOLD", color=FG).scale(0.4).next_to(bullets, UP, buff=0.2)
        right_mid = VGroup(bullets_title, bullets).move_to(np.array([3.9, -1.7, 0.0]))
        self.play(FadeIn(bullets_title, shift=UP * 0.2))
        for row in bullets:
            self.play(FadeIn(row[0]), Write(row[1]), run_time=0.16)

        cap_box = RoundedRectangle(
            corner_radius=0.15, width=5.6, height=1.8, stroke_color=GRID, stroke_width=2,
            fill_color="#161A33", fill_opacity=1.0
        )
        cap_title = Text("생산능력(2025H1)", font=FONT, weight="BOLD", color=FG).scale(0.36)
        cap_title.move_to(cap_box.get_top()).shift(DOWN * 0.35)
        cap_lines = VGroup()
        for c in DATA["capacity"]:
            t = Text(f"{c['label']}: {c['value']}", font=FONT, weight="MEDIUM", color=FG).scale(0.32)
            cap_lines.add(t)
        cap_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.10).next_to(cap_title, DOWN, buff=0.12)
        cap_lines.align_to(cap_box.get_left(), LEFT).shift(RIGHT * 0.35)
        cap_grp = VGroup(cap_box, cap_title, cap_lines).move_to(np.array([3.9, -3.5, 0.0]))
        self.play(FadeIn(cap_box), Write(cap_title), *[Write(t) for t in cap_lines], run_time=0.8)

        ax, xlabs, ylabs, ax_title = price_axes(
            "원재료 가격변동(평균)", DATA["raw_material_prices"]["years"],
            xmin=0, xmax=2, ymin=800_000, ymax=1_200_000, width=5.8, height=3.0
        )
        ax_title.scale(0.4).move_to(np.array([-0.2, 2.2, 0]))
        ax_group = VGroup(ax, xlabs, ylabs, ax_title).scale(0.75).move_to(np.array([-0.1, 2.1, 0]))
        self.play(FadeIn(ax), FadeIn(xlabs), FadeIn(ylabs), Write(ax_title), run_time=0.6)

        sp = DATA["raw_material_prices"]["steel_plate"]
        hb = DATA["raw_material_prices"]["h_beam"]
        steel_graph = ax.plot_line_graph(
            x_values=[0, 1, 2], y_values=sp, add_vertex_dots=True, stroke_width=3
        )
        hbeam_graph = ax.plot_line_graph(
            x_values=[0, 1, 2], y_values=hb, add_vertex_dots=True, stroke_width=3
        )
        steel_lbl = Text("후판(SS275 20T)", font=FONT, weight="BOLD", color=FG).scale(0.28)
        hbeam_lbl = Text("형강(앵글 SS400)", font=FONT, weight="BOLD", color=FG).scale(0.28)
        steel_lbl.next_to(ax, UP, buff=0.05).align_to(ax.get_left(), LEFT)
        hbeam_lbl.next_to(steel_lbl, RIGHT, buff=0.5)
        note = Text(DATA["raw_material_prices"]["note"], font=FONT, color=MUTED).scale(0.26)
        note.next_to(ax, DOWN, buff=0.05).align_to(ax.get_left(), LEFT)

        self.play(Create(steel_graph), run_time=0.6)
        self.play(Create(hbeam_graph), run_time=0.6)
        self.play(FadeIn(steel_lbl), FadeIn(hbeam_lbl), FadeIn(note), run_time=0.4)

        safety = VGroup(
            Text("재무 스냅샷", font=FONT, weight="BOLD", color=FG).scale(0.36),
            Text(
                f"부채비율 {DATA['debt_ratio_pct']:.2f}% | 현금성 {fmt_krw_billion(DATA['cash_like'])} "
                f"vs 차입금 {fmt_krw_billion(DATA['borrowings'])} | 이자보상배율 {DATA['interest_coverage']:.2f}배",
                font=FONT, weight="MEDIUM", color=MUTED
            ).scale(0.32),
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).to_edge(DOWN).shift(UP * 0.35 + LEFT * 0.2)
        self.play(FadeIn(safety), run_time=0.4)

        focus_arc = donut(seg_values, seg_labels, seg_colors, inner_ratio=0.60, r=1.8)[0][0]
        self.play(Indicate(focus_arc, color=PRIMARY, scale_factor=1.03), run_time=0.8)

        foot = Text("ⓒ HD현대중공업 2025H1 사업보고서 기반 요약 시각화(내부 참고용)", font=FONT, weight="MEDIUM", color=MUTED).scale(0.28)
        foot.to_edge(DOWN).shift(UP * 0.08)
        self.play(FadeIn(foot), run_time=0.4)
        self.wait(1.0)
