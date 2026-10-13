"""Native chart helpers: column chart with a dashed threshold line on hidden secondary axes."""
import copy
from lxml import etree
from pptx.util import Inches, Pt
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.oxml.ns import qn
from decklib import _set_fonts, TEAL, NAVY, ORANGE, MUTED, RULE, INK

C = "http://schemas.openxmlformats.org/drawingml/2006/chart"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"


def _el(tag, val=None, **attrs):
    ns, name = tag.split(":")
    el = etree.Element(qn(tag))
    if val is not None:
        el.set("val", str(val))
    for k, v in attrs.items():
        el.set(k, str(v))
    return el


def _font_txpr(parent_tag, size, color, bold=False):
    txPr = etree.Element(qn(parent_tag))
    bp = etree.SubElement(txPr, qn("a:bodyPr"))
    etree.SubElement(txPr, qn("a:lstStyle"))
    p = etree.SubElement(txPr, qn("a:p"))
    pPr = etree.SubElement(p, qn("a:pPr"))
    d = etree.SubElement(pPr, qn("a:defRPr"))
    d.set("sz", str(int(size * 100))); d.set("b", "1" if bold else "0")
    sf = etree.SubElement(d, qn("a:solidFill")); etree.SubElement(sf, qn("a:srgbClr")).set("val", str(color))
    _set_fonts(d)
    etree.SubElement(p, qn("a:endParaRPr")).set("lang", "zh-CN")
    return txPr


def bar_with_threshold(slide, x, y, w, h, categories, values, threshold, vmax,
                       series_name="比对偏差R", threshold_name="判定标准",
                       value_fmt='0.00"%"', axis_fmt='0"%"', plot_box=(0.12, 0.06, 0.84, 0.76),
                       threshold_label_fmt='"判定标准 "0"%"'):
    """Column chart + dashed threshold line, both data-bound on the SAME axes.
    One blank padding category on each side lets the line run past the bars
    (renders identically in PowerPoint and LibreOffice; no secondary axes)."""
    cats = [" "] + list(categories) + ["  "]
    bar_vals = [None] + list(values) + [None]
    cd = CategoryChartData()
    cd.categories = cats
    cd.add_series(series_name, bar_vals)
    cd.add_series(threshold_name, [threshold] * len(cats))
    gf = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    gf.name = "R柱状图(原生)"
    chart = gf.chart
    chart.has_legend = False
    chart.has_title = False
    plot = chart.plots[0]
    plot.gap_width = 60
    bar = plot.series[0]
    bar.format.fill.solid(); bar.format.fill.fore_color.rgb = TEAL
    bar.invert_if_negative = False
    dl = bar.data_labels
    dl.show_value = True
    dl.number_format = value_fmt
    dl.number_format_is_linked = False
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.font.size = Pt(22); dl.font.bold = True; dl.font.color.rgb = ORANGE

    va = chart.value_axis
    va.minimum_scale = 0; va.maximum_scale = vmax; va.major_unit = 1
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = RULE
    va.major_gridlines.format.line.width = Pt(0.75)
    va.tick_labels.number_format = axis_fmt
    va.tick_labels.number_format_is_linked = False
    va.format.line.fill.background()
    ca = chart.category_axis
    ca.format.line.color.rgb = RULE
    ca.has_major_gridlines = False

    cs = chart._chartSpace
    plotArea = cs.find(".//" + qn("c:plotArea"))
    layout = plotArea.find(qn("c:layout"))
    if layout is None:
        layout = etree.Element(qn("c:layout")); plotArea.insert(0, layout)
    for ch in list(layout):
        layout.remove(ch)
    ml = etree.SubElement(layout, qn("c:manualLayout"))
    for tag, v in (("c:layoutTarget", "inner"), ("c:xMode", "edge"), ("c:yMode", "edge"),
                   ("c:x", plot_box[0]), ("c:y", plot_box[1]), ("c:w", plot_box[2]), ("c:h", plot_box[3])):
        ml.append(_el(tag, v))

    barChart = plotArea.find(qn("c:barChart"))
    ax_ids = [e.get("val") for e in barChart.findall(qn("c:axId"))]
    line_ser = barChart.findall(qn("c:ser"))[1]
    barChart.remove(line_ser)
    for t in ("c:invertIfNegative", "c:dLbls", "c:spPr"):
        for e in line_ser.findall(qn(t)):
            line_ser.remove(e)
    spPr = etree.Element(qn("c:spPr"))
    ln = etree.SubElement(spPr, qn("a:ln")); ln.set("w", "28575"); ln.set("cap", "rnd")
    sf = etree.SubElement(ln, qn("a:solidFill")); etree.SubElement(sf, qn("a:srgbClr")).set("val", str(NAVY))
    etree.SubElement(ln, qn("a:prstDash")).set("val", "dash")
    etree.SubElement(ln, qn("a:round"))
    line_ser.find(qn("c:tx")).addnext(spPr)
    marker = etree.Element(qn("c:marker")); marker.append(_el("c:symbol", "none"))
    spPr.addnext(marker)
    # data label only on the last point: "判定标准 6%"
    dLbls = etree.Element(qn("c:dLbls"))
    d = etree.SubElement(dLbls, qn("c:dLbl"))
    d.append(_el("c:idx", len(cats) - 1))
    nf = etree.SubElement(d, qn("c:numFmt")); nf.set("formatCode", threshold_label_fmt); nf.set("sourceLinked", "0")
    sp = etree.SubElement(d, qn("c:spPr")); etree.SubElement(sp, qn("a:noFill")); l2 = etree.SubElement(sp, qn("a:ln")); etree.SubElement(l2, qn("a:noFill"))
    d.append(_font_txpr("c:txPr", 15, NAVY, bold=True))
    for tag, v in (("c:dLblPos", "t"), ("c:showLegendKey", 0), ("c:showVal", 1), ("c:showCatName", 0),
                   ("c:showSerName", 0), ("c:showPercent", 0), ("c:showBubbleSize", 0)):
        d.append(_el(tag, v))
    for tag, v in (("c:showLegendKey", 0), ("c:showVal", 0), ("c:showCatName", 0), ("c:showSerName", 0),
                   ("c:showPercent", 0), ("c:showBubbleSize", 0)):
        dLbls.append(_el(tag, v))
    marker.addnext(dLbls)
    line_ser.append(_el("c:smooth", 0))

    lineChart = etree.Element(qn("c:lineChart"))
    lineChart.append(_el("c:grouping", "standard"))
    lineChart.append(_el("c:varyColors", 0))
    lineChart.append(line_ser)
    lineChart.append(_el("c:marker", 1))
    for a in ax_ids:
        lineChart.append(_el("c:axId", a))
    barChart.addnext(lineChart)

    for ax_tag, size in (("c:catAx", 16), ("c:valAx", 14)):
        ax = plotArea.find(qn(ax_tag))
        old = ax.find(qn("c:txPr"))
        if old is not None:
            ax.remove(old)
        txPr = _font_txpr("c:txPr", size, MUTED if ax_tag == "c:valAx" else INK)
        ax.find(qn("c:crossAx")).addprevious(txPr)
        mt = ax.find(qn("c:majorTickMark"))
        if mt is not None:
            mt.set("val", "none")
    for dd in cs.iter(qn("a:defRPr")):
        if dd.find(qn("a:ea")) is None:
            _set_fonts(dd)
    return gf, plot_box
