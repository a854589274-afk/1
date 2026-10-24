const pptxgen = require("pptxgenjs");
const { applyTheme } = require("/root/.claude/skills/synced/3ebecd3a-4e08-4c8e-8b9e-b267b9c7dbba_81a1e534-1d85-4e04-b869-41720bd654b3/pptx/scripts/apply_theme.js");
const THEME = { name: "Hospital940", headFontFace: "Microsoft YaHei", bodyFontFace: "Microsoft YaHei",
 colors: { dk1:"1B2A41", lt1:"FFFFFF", dk2:"1F4E79", lt2:"EEF2F6", accent1:"1F4E79", accent2:"B3202A", accent3:"2E8B9A", accent4:"D9A441", accent5:"5B7C99", accent6:"7A8CA3", hlink:"1F4E79", folHlink:"5B7C99" } };
const pres = new pptxgen(); pres.layout = "LAYOUT_WIDE"; pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "检验医学科专业基地迎接国家住培基地检查汇报";
const C = pres.SchemeColor;
pres.defineSlideMaster({ title: "CONTENT", background: { color: "FFFFFF" },
 objects: [
  { text: { text: "联勤保障部队第九四〇医院 · 检验医学科住培基地", options: { x: 0.6, y: 7.0, w: 8, h: 0.3, fontSize: 10, color: "7A8CA3", margin: 0 } } } ],
 slideNumber: { x: 12.2, y: 7.0, w: 0.6, h: 0.3, fontSize: 10, color: "7A8CA3" } });
pres.defineSlideMaster({ title: "DARK", background: { color: "1B2A41" } });

function head(s, no, title, sub) {
  s.addShape(pres.ShapeType.ellipse, { x: 0.6, y: 0.45, w: 0.7, h: 0.7, fill: { color: "B3202A" }, objectName: "badge" });
  s.addText(no, { x: 0.6, y: 0.45, w: 0.7, h: 0.7, align: "center", valign: "middle", fontSize: 18, bold: true, color: "FFFFFF", margin: 0, isTextBox: true });
  s.addText(title, { x: 1.5, y: 0.4, w: 8, h: 0.8, fontSize: 32, bold: true, color: "1B2A41", valign: "middle", margin: 0, isTextBox: true });
  if (sub) s.addText(sub, { x: 8.6, y: 0.5, w: 4.1, h: 0.6, fontSize: 12, color: "7A8CA3", align: "right", valign: "middle", margin: 0, isTextBox: true });
}
function card(s, x, y, w, h, title, lines, fill) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.1, fill: { color: fill || "EEF2F6" }, line: { color: fill || "EEF2F6" } });
  s.addText(title, { x: x + 0.25, y: y + 0.15, w: w - 0.5, h: 0.5, fontSize: 20, bold: true, color: "1F4E79", margin: 0, valign: "middle", isTextBox: true });
  s.addText(lines.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < lines.length - 1 } })),
    { x: x + 0.25, y: y + 0.75, w: w - 0.5, h: h - 0.9, fontSize: 14, color: "1B2A41", valign: "top", paraSpaceAfter: 6, margin: 0, isTextBox: true });
}
function stat(s, x, y, w, num, label) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h: 1.5, rectRadius: 0.1, fill: { color: "1F4E79" } });
  s.addText(num, { x, y: y + 0.12, w, h: 0.8, align: "center", valign: "middle", fontSize: 40, bold: true, color: "FFFFFF", margin: 0, isTextBox: true });
  s.addText(label, { x, y: y + 0.9, w, h: 0.45, align: "center", valign: "middle", fontSize: 14, color: "CADCFC", margin: 0, isTextBox: true });
}
const mk = (n) => { const s = pres.addSlide({ masterName: "CONTENT" }); return s; };
const NOTE = "【数据为示例，汇报前请按本基地实际情况替换】";

// 1 title
let s = pres.addSlide({ masterName: "DARK" });
s.addShape(pres.ShapeType.ellipse, { x: 9.8, y: -1.5, w: 5.5, h: 5.5, fill: { color: "B3202A", transparency: 75 } });
s.addShape(pres.ShapeType.ellipse, { x: 11.2, y: 4.8, w: 3.6, h: 3.6, fill: { color: "2E8B9A", transparency: 80 } });
s.addText("联勤保障部队第九四〇医院", { x: 0.9, y: 0.7, w: 9, h: 0.6, fontSize: 22, color: "CADCFC", margin: 0, isTextBox: true });
s.addText("2026年度国家住培评估迎检汇报", { x: 0.9, y: 1.3, w: 9, h: 0.5, fontSize: 16, color: "CADCFC", margin: 0, isTextBox: true });
s.addText("检验医学科专业基地\n迎接国家住培基地检查汇报", { x: 0.9, y: 2.4, w: 11, h: 2, fontSize: 44, bold: true, color: "FFFFFF", margin: 0, valign: "top", isTextBox: true });
s.addText([{ text: "汇报人：哈小琴", options: { breakLine: true } }, { text: "科　室：检验科", options: { breakLine: true } }, { text: "汇报日期：2026年10月28日" }],
 { x: 0.9, y: 5.2, w: 6, h: 1.4, fontSize: 18, color: "FFFFFF", paraSpaceAfter: 4, margin: 0, valign: "top", isTextBox: true });

// 2 contents
s = mk(); 
s.addText("目录", { x: 0.6, y: 0.4, w: 4, h: 0.8, fontSize: 36, bold: true, color: "1B2A41", margin: 0, isTextBox: true });
s.addText("CONTENTS", { x: 0.6, y: 1.1, w: 4, h: 0.4, fontSize: 14, color: "7A8CA3", charSpacing: 4, margin: 0, isTextBox: true });
const toc = [["01","基地概况","基地条件 · 师资结构 · 学员规模 · 结业情况"],["02","教学管理","教学小组 · 会议 · 出科考核 · 管理制度"],["03","师资队伍","带教分配 · 培训考核 · 激励 · 退出机制"],["04","轮转管理","轮转计划 · 入科教育 · 出科考核 · 交叉印证"],["05","教学活动","教学查房 · 病例讨论 · 小讲课 · 技能训练"],["06","考核与病历管理","考核资料 · 报告规范 · 技能训练 · 抽考准备"],["07","学员权益保障","待遇保障 · 合理排班 · 投诉反馈 · 宣教"],["08","持续改进与展望","问题整改 · 不足 · 改进计划 · 发展目标"]];
toc.forEach((t, i) => { const col = i % 2, row = Math.floor(i / 2); const x = 0.6 + col * 6.2, y = 1.8 + row * 1.2;
  s.addShape(pres.ShapeType.roundRect, { x, y, w: 5.9, h: 1.0, rectRadius: 0.08, fill: { color: "EEF2F6" } });
  s.addText(t[0], { x: x + 0.15, y, w: 0.9, h: 1.0, fontSize: 30, bold: true, color: i % 2 ? "2E8B9A" : "1F4E79", valign: "middle", margin: 0, isTextBox: true });
  s.addText(t[1], { x: x + 1.1, y: y + 0.1, w: 4.7, h: 0.45, fontSize: 20, bold: true, color: "1B2A41", valign: "middle", margin: 0, isTextBox: true });
  s.addText(t[2], { x: x + 1.1, y: y + 0.55, w: 4.7, h: 0.35, fontSize: 12, color: "5B7C99", valign: "middle", margin: 0, isTextBox: true }); });

// 3 base conditions
s = mk(); head(s, "01", "基地概况：基地条件", "基地条件 · 师资结构 · 学员规模 · 结业情况");
stat(s, 0.6, 1.6, 2.8, "XX", "年检测标本量（万份）"); stat(s, 3.6, 1.6, 2.8, "XX", "开展检测项目（项）");
stat(s, 6.6, 1.6, 2.8, "XX", "实验室面积（㎡）"); stat(s, 9.6, 1.6, 3.1, "XX", "核定住培容量（人）");
card(s, 0.6, 3.5, 6.0, 3.2, "专业设置与布局", ["临床体液血液、临床生化、临床免疫、临床微生物、分子诊断五大专业组", "设置学员示教室、技能训练室、电子阅览与资料室", "配备显微镜互动教学系统与教学数据库"]);
card(s, 6.8, 3.5, 5.9, 3.2, "设备与质量保障", ["拥有全自动生化免疫流水线、血球及凝血、微生物质谱与自动培养系统", "通过实验室质量管理体系认证，室内质控与室间质评持续合格", "满足住培学员全流程操作与结果分析需求"], "E6F1F3");
s.addNotes("基地条件：数据为占位，请按实际替换。" );

// 4 faculty
s = mk(); head(s, "01", "基地概况：师资结构", "示例数据，汇报前替换");
s.addChart(pres.charts.PIE, [{ name: "职称", labels: ["正高", "副高", "中级", "初级"], values: [3, 5, 8, 4] }],
 { x: 0.6, y: 1.5, w: 5.6, h: 5.2, chartColors: ["1F4E79", "2E8B9A", "D9A441", "B3202A"], showLegend: true, legendPos: "b", legendFontSize: 14, legendFontFace: "+mn-lt", showPercent: false, showValue: true, dataLabelColor: "FFFFFF", dataLabelFontSize: 16, dataLabelFontFace: "+mn-lt", showTitle: true, title: "带教师资职称构成（人）", titleFontSize: 16, titleFontFace: "+mn-lt", titleColor: "1B2A41" });
card(s, 6.6, 1.6, 6.1, 2.4, "师资配置", ["基地主任 1 名、教学主任 1 名、教学秘书 1 名", "带教师资均具备中级及以上职称，从事检验工作 5 年以上", "高级职称带教比例 XX%，硕博学历占比 XX%"]);
card(s, 6.6, 4.2, 6.1, 2.5, "师资资质", ["全部带教师资取得省级及以上师资培训合格证书", "师生比 1 : X，满足国家基地标准要求", "近三年承担院级以上教学课题 X 项"], "E6F1F3");

// 5 trainees
s = mk(); head(s, "01", "基地概况：学员规模与结业情况", "示例数据，汇报前替换");
s.addChart(pres.charts.BAR, [{ name: "在培学员", labels: ["2022级", "2023级", "2024级", "2025级"], values: [3, 4, 4, 5] }, { name: "结业学员", labels: ["2022级", "2023级", "2024级", "2025级"], values: [3, 4, 0, 0] }],
 { x: 0.6, y: 1.5, w: 7.2, h: 5.2, barDir: "col", barGrouping: "clustered", chartColors: ["1F4E79", "D9A441"], showLegend: true, legendPos: "b", legendFontSize: 14, legendFontFace: "+mn-lt", showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 14, dataLabelColor: "1B2A41", dataLabelFontFace: "+mn-lt", catAxisLabelColor: "1B2A41", valAxisLabelColor: "1B2A41", catAxisLabelFontSize: 14, valAxisLabelFontSize: 12, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", valGridLine: { color: "DDE3EA", size: 0.5 }, catGridLine: { style: "none" }, showTitle: true, title: "各年级学员人数（人）", titleFontSize: 16, titleFontFace: "+mn-lt", titleColor: "1B2A41" });
stat(s, 8.2, 1.6, 2.2, "XX", "在培学员（人）"); stat(s, 10.6, 1.6, 2.1, "100%", "结业考核通过率");
card(s, 8.2, 3.4, 4.5, 3.3, "结业去向", ["本院及军队医院检验岗位", "继续攻读专业型硕博士", "学员满意度 XX%，岗位胜任力评价良好"], "E6F1F3");

// 6 teaching mgmt structure
s = mk(); head(s, "02", "教学管理：组织架构", "教学小组 · 会议 · 出科考核 · 管理制度");
s.addShape(pres.ShapeType.roundRect, { x: 4.9, y: 1.5, w: 3.5, h: 0.9, rectRadius: 0.08, fill: { color: "B3202A" } });
s.addText("科室教学管理小组\n组长：科主任", { x: 4.9, y: 1.5, w: 3.5, h: 0.9, align: "center", valign: "middle", fontSize: 16, bold: true, color: "FFFFFF", margin: 0, isTextBox: true });
s.addShape(pres.ShapeType.line, { x: 6.65, y: 2.4, w: 0, h: 0.4, line: { color: "7A8CA3", width: 1.5 } });
s.addShape(pres.ShapeType.line, { x: 2.15, y: 2.8, w: 8.9, h: 0, line: { color: "7A8CA3", width: 1.5 } });
[["教学主任","统筹培养方案与质量控制"],["教学秘书","日常管理、档案资料、排班"],["专业组带教组长","各亚专业带教落实"],["考核与督导员","出科考核与过程督导"]].forEach((t, i) => { const x = 0.6 + i * 3.1;
  s.addShape(pres.ShapeType.line, { x: x + 1.55, y: 2.8, w: 0, h: 0.4, line: { color: "7A8CA3", width: 1.5 } });
  s.addShape(pres.ShapeType.roundRect, { x, y: 3.2, w: 2.9, h: 1.0, rectRadius: 0.08, fill: { color: "1F4E79" } });
  s.addText(t[0], { x, y: 3.2, w: 2.9, h: 1.0, align: "center", valign: "middle", fontSize: 18, bold: true, color: "FFFFFF", margin: 0, isTextBox: true });
  s.addShape(pres.ShapeType.roundRect, { x, y: 4.35, w: 2.9, h: 1.3, rectRadius: 0.08, fill: { color: "EEF2F6" } });
  s.addText(t[1], { x: x + 0.15, y: 4.35, w: 2.6, h: 1.3, align: "left", valign: "middle", fontSize: 14, color: "1B2A41", margin: 0, isTextBox: true }); });
s.addText("职责明确、分工到人，形成“科主任负总责—教学主任抓落实—带教组长管过程”的三级管理链条", { x: 0.6, y: 5.95, w: 12.1, h: 0.7, fontSize: 16, bold: true, color: "1F4E79", margin: 0, valign: "middle", isTextBox: true });

// 7 system and meetings
s = mk(); head(s, "02", "教学管理：会议与制度", "教学小组 · 会议 · 出科考核 · 管理制度");
card(s, 0.6, 1.6, 4.0, 5.0, "教学例会", ["每月召开教学小组会议，总结培训进展", "每季度召开师生座谈会，收集意见", "会议记录完整、问题闭环、持续跟踪"]);
card(s, 4.7, 1.6, 4.0, 5.0, "出科考核", ["理论 + 操作技能 + 综合评价三位一体", "出科考核由带教组长与教学主任共同评定", "结果及时反馈学员并归档"], "E6F1F3");
card(s, 8.8, 1.6, 3.9, 5.0, "管理制度", ["住院医师规范化培训实施细则", "带教师资管理与考核办法", "轮转、请假、考勤与考核管理规定", "教学档案与质量控制制度"]);

// 8 faculty assign
s = mk(); head(s, "03", "师资队伍：带教分配与培训考核", "带教分配 · 培训考核 · 激励 · 退出机制");
const steps = [["选拔","满足职称、工龄、教学能力条件，个人申请、科室推荐、医院审定"],["分配","按专业组实行“一对一”或“一对二”带教，明确责任导师"],["培训","参加院级、省级及国家级师资培训，定期开展教学法与教学评价培训"],["考核","学员评教、同行评议、教学督导、教学成果综合评价"]];
steps.forEach((t, i) => { const x = 0.6 + i * 3.1;
  s.addShape(pres.ShapeType.ellipse, { x: x + 0.1, y: 1.7, w: 0.9, h: 0.9, fill: { color: i % 2 ? "2E8B9A" : "1F4E79" } });
  s.addText(String(i + 1), { x: x + 0.1, y: 1.7, w: 0.9, h: 0.9, align: "center", valign: "middle", fontSize: 24, bold: true, color: "FFFFFF", margin: 0, isTextBox: true });
  s.addText(t[0], { x: x + 1.15, y: 1.7, w: 1.7, h: 0.9, fontSize: 22, bold: true, color: "1B2A41", valign: "middle", margin: 0, isTextBox: true });
  s.addShape(pres.ShapeType.roundRect, { x, y: 2.9, w: 2.9, h: 2.4, rectRadius: 0.08, fill: { color: "EEF2F6" } });
  s.addText(t[1], { x: x + 0.2, y: 3.0, w: 2.5, h: 2.2, fontSize: 14, color: "1B2A41", valign: "top", margin: 0, isTextBox: true }); });
s.addText("全程可追溯：师资档案、培训证书、带教记录与考核结果均纳入教学档案管理", { x: 0.6, y: 5.7, w: 12.1, h: 0.8, fontSize: 16, bold: true, color: "1F4E79", valign: "middle", margin: 0, isTextBox: true });

// 9 incentive & exit
s = mk(); head(s, "03", "师资队伍：激励与退出机制", "带教分配 · 培训考核 · 激励 · 退出机制");
card(s, 0.6, 1.6, 6.0, 5.0, "激励机制", ["设立带教津贴，按带教人数与质量核发", "教学成果纳入职称晋升、评优评先和绩效考核", "每年评选“优秀带教老师”，予以表彰奖励", "支持师资外出进修、参加教学竞赛与学术交流"]);
card(s, 6.8, 1.6, 5.9, 5.0, "退出机制", ["学员评教或教学督导连续不达标者，暂停带教资格", "无故缺席教学活动、教学档案不完整者，限期整改", "整改后仍不合格者，取消带教资格并重新培训考核", "动态调整师资库，保证带教质量"], "FBEDEE");

// 10 rotation plan
s = mk(); head(s, "04", "轮转管理：轮转计划", "轮转计划 · 入科教育 · 出科考核 · 交叉印证");
const rot = [["临床体液血液","2个月"],["临床生化","2个月"],["临床免疫","2个月"],["临床微生物","3个月"],["分子诊断","1个月"],["质量管理与综合","2个月"]];
rot.forEach((t, i) => { const x = 0.6 + i * 2.05;
  s.addShape(pres.ShapeType.roundRect, { x, y: 2.0, w: 1.9, h: 1.6, rectRadius: 0.08, fill: { color: i % 2 ? "2E8B9A" : "1F4E79" } });
  s.addText(t[0], { x, y: 2.1, w: 1.9, h: 0.9, align: "center", valign: "middle", fontSize: 16, bold: true, color: "FFFFFF", margin: 0, isTextBox: true });
  s.addText(t[1], { x, y: 3.0, w: 1.9, h: 0.5, align: "center", valign: "middle", fontSize: 14, color: "FFFFFF", margin: 0, isTextBox: true }); });
s.addText("以上为示例轮转时长，请按本基地《培养方案》调整", { x: 0.6, y: 3.7, w: 12, h: 0.35, fontSize: 12, color: "7A8CA3", margin: 0, isTextBox: true });
card(s, 0.6, 4.2, 6.0, 2.5, "制定原则", ["严格依据国家《住院医师规范化培训内容与标准（检验医学科）》", "个性化轮转表，保证各专业组学习时长与病种、技能要求"]);
card(s, 6.8, 4.2, 5.9, 2.5, "执行与调整", ["轮转计划提前公示，轮转变更须经教学主任审批备案", "教学秘书全程跟踪，轮转手册随时查阅"], "E6F1F3");

// 11 intake / exit / cross verification
s = mk(); head(s, "04", "轮转管理：入科、出科与交叉印证", "轮转计划 · 入科教育 · 出科考核 · 交叉印证");
const flow = [["入科教育","生物安全、医院感染、实验室规章、培训目标与考核要求"],["过程带教","专业组带教老师按轮转大纲实施，登记轮转手册"],["出科考核","理论考试 + 操作技能 + 病例分析，形成书面评价"],["交叉印证","轮转手册、考核成绩、操作登记、学员访谈相互印证"]];
flow.forEach((t, i) => { const x = 0.6 + i * 3.1;
  s.addShape(pres.ShapeType.homePlate || pres.ShapeType.rightArrow, { x, y: 1.7, w: 3.0, h: 1.0, fill: { color: i === 3 ? "B3202A" : "1F4E79" } });
  s.addText(t[0], { x: x + 0.1, y: 1.7, w: 2.5, h: 1.0, align: "center", valign: "middle", fontSize: 18, bold: true, color: "FFFFFF", margin: 0, isTextBox: true });
  s.addShape(pres.ShapeType.roundRect, { x, y: 2.95, w: 2.9, h: 2.0, rectRadius: 0.08, fill: { color: "EEF2F6" } });
  s.addText(t[1], { x: x + 0.2, y: 3.05, w: 2.5, h: 1.8, fontSize: 14, color: "1B2A41", valign: "top", margin: 0, isTextBox: true }); });
s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 5.25, w: 12.1, h: 1.35, rectRadius: 0.08, fill: { color: "E6F1F3" } });
s.addText("交叉印证要点：学员自述记录 ↔ 带教老师签字 ↔ LIS 系统操作痕迹 ↔ 出科成绩，保证“记录真实、过程可溯、结果可信”", { x: 0.9, y: 5.25, w: 11.5, h: 1.35, fontSize: 16, bold: true, color: "1F4E79", valign: "middle", margin: 0, isTextBox: true });

// 12 teaching activities
s = mk(); head(s, "05", "教学活动", "教学查房 · 病例讨论 · 小讲课 · 技能训练");
card(s, 0.6, 1.6, 6.0, 2.45, "教学查房", ["每月 1–2 次，结合临床科室疑难检验结果", "学员汇报、带教点评、检验与临床联合"]);
card(s, 6.8, 1.6, 5.9, 2.45, "病例讨论", ["每月 1 次检验—临床联合病例讨论", "围绕危急值、异常结果与项目选择解读"], "E6F1F3");
card(s, 0.6, 4.25, 6.0, 2.45, "小讲课", ["每周 1 次，涵盖标准、质控、新技术与前沿进展", "学员轮流主讲，带教老师点评并记录"], "E6F1F3");
card(s, 6.8, 4.25, 5.9, 2.45, "技能训练", ["显微镜镜检、血涂片、细菌鉴定、标本前处理", "技能训练室定期开放，操作考核留痕"]);

// 13 assessment & records
s = mk(); head(s, "06", "考核与病历管理", "考核资料 · 报告规范 · 技能训练 · 抽考准备");
card(s, 0.6, 1.6, 4.0, 3.2, "考核资料", ["理论考试、操作考核、过程考核试题库", "考核结果统一归档，一人一档"]);
card(s, 4.7, 1.6, 4.0, 3.2, "报告规范", ["检验报告书写规范、结果审核与危急值记录", "学员报告须经带教老师审核签发"], "E6F1F3");
card(s, 8.8, 1.6, 3.9, 3.2, "技能训练", ["必备操作项目清单与例数要求", "操作登记、带教签字、定期核查"]);
s.addShape(pres.ShapeType.roundRect, { x: 0.6, y: 5.0, w: 12.1, h: 1.7, rectRadius: 0.1, fill: { color: "1F4E79" } });
s.addText([{ text: "抽考准备", options: { bold: true, fontSize: 20, breakLine: true } }, { text: "组织模拟抽考与技能演练，学员熟悉国家标准要求；资料、记录、示范操作三项提前预检，查缺补漏。", options: { fontSize: 15 } }],
 { x: 0.9, y: 5.05, w: 11.5, h: 1.6, color: "FFFFFF", valign: "middle", margin: 0, isTextBox: true });

// 14 trainee rights
s = mk(); head(s, "07", "学员权益保障", "待遇保障 · 合理排班 · 投诉反馈 · 宣教");
[["待遇保障","按规定足额发放工资、津贴及社保公积金，落实各项福利"],["合理排班","严格执行工作时间规定，夜班值班与休息合理安排"],["投诉反馈","设立意见箱与投诉渠道，教学秘书限时受理、答复"],["宣教","入科宣讲学员权利义务，公示规章制度与培训标准"]].forEach((t, i) => { const x = 0.6 + i * 3.1;
  s.addShape(pres.ShapeType.roundRect, { x, y: 1.8, w: 2.9, h: 4.6, rectRadius: 0.1, fill: { color: i % 2 ? "E6F1F3" : "EEF2F6" } });
  s.addShape(pres.ShapeType.ellipse, { x: x + 0.95, y: 2.1, w: 1.0, h: 1.0, fill: { color: i % 2 ? "2E8B9A" : "1F4E79" } });
  s.addText(String(i + 1), { x: x + 0.95, y: 2.1, w: 1.0, h: 1.0, align: "center", valign: "middle", fontSize: 26, bold: true, color: "FFFFFF", margin: 0, isTextBox: true });
  s.addText(t[0], { x, y: 3.3, w: 2.9, h: 0.6, align: "center", valign: "middle", fontSize: 22, bold: true, color: "1B2A41", margin: 0, isTextBox: true });
  s.addText(t[1], { x: x + 0.25, y: 4.0, w: 2.4, h: 2.2, fontSize: 14, color: "1B2A41", valign: "top", margin: 0, isTextBox: true }); });

// 15 problems
s = mk(); head(s, "08", "持续改进：问题整改与不足", "问题整改 · 不足 · 改进计划 · 发展目标");
card(s, 0.6, 1.6, 6.0, 5.0, "既往问题整改", ["对上一轮督导反馈问题建立台账，逐项整改销号", "完善带教记录与轮转手册填写规范", "增设分子诊断与质量管理轮转内容", "整改措施落实情况已纳入月度教学例会通报"], "E6F1F3");
card(s, 6.8, 1.6, 5.9, 5.0, "当前不足", ["高层次师资比例与教学科研能力有待提升", "信息化教学与过程评价手段仍需完善", "学员临床思维与检验—临床沟通能力培养需加强", "教学资源与学员规模增长之间存在压力"], "FBEDEE");

// 16 plan & goals
s = mk(); head(s, "08", "持续改进：改进计划与发展目标", "问题整改 · 不足 · 改进计划 · 发展目标");
card(s, 0.6, 1.6, 6.0, 3.0, "改进计划", ["建立带教师资梯队，引进与培养并重", "上线住培过程管理信息系统，实现数据化督导", "推进检验—临床联合教学，强化临床思维训练"]);
card(s, 6.8, 1.6, 5.9, 3.0, "发展目标", ["建成国内一流的军队检验医学住培示范基地", "师资全员达到省级及以上培训标准", "学员结业考核通过率保持 100%"], "E6F1F3");
const gl = [["2026","夯实基础，通过国家评估"],["2027","信息化平台上线运行"],["2028","师资梯队建成"],["2030","示范基地目标"]];
gl.forEach((t, i) => { const x = 0.6 + i * 3.1;
  s.addShape(pres.ShapeType.ellipse, { x: x + 0.05, y: 4.95, w: 0.3, h: 0.3, fill: { color: "B3202A" } });
  s.addText(t[0], { x: x + 0.5, y: 4.85, w: 2.3, h: 0.5, fontSize: 20, bold: true, color: "1B2A41", valign: "middle", margin: 0, isTextBox: true });
  s.addText(t[1], { x: x + 0.05, y: 5.5, w: 2.8, h: 0.9, fontSize: 14, color: "1B2A41", valign: "top", margin: 0, isTextBox: true }); });
s.addShape(pres.ShapeType.line, { x: 0.8, y: 5.1, w: 0, h: 0, line: { color: "FFFFFF", width: 0 } });

// 17 thanks
s = pres.addSlide({ masterName: "DARK" });
s.addShape(pres.ShapeType.ellipse, { x: -1.5, y: 4.5, w: 5, h: 5, fill: { color: "B3202A", transparency: 75 } });
s.addShape(pres.ShapeType.ellipse, { x: 10.5, y: -1.2, w: 4.2, h: 4.2, fill: { color: "2E8B9A", transparency: 80 } });
s.addText("恳请各位专家批评指正", { x: 0.9, y: 2.4, w: 11.5, h: 1.2, fontSize: 44, bold: true, color: "FFFFFF", align: "center", margin: 0, isTextBox: true });
s.addText("联勤保障部队第九四〇医院 · 检验医学科", { x: 0.9, y: 3.9, w: 11.5, h: 0.6, fontSize: 20, color: "CADCFC", align: "center", margin: 0, isTextBox: true });

(async () => { await pres.writeFile({ fileName: "检验医学科住培基地迎检汇报.pptx" }); await applyTheme("检验医学科住培基地迎检汇报.pptx", THEME); })();
