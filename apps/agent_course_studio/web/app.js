const state = {
  data: null,
  currentLessonId: null,
  currentTab: "overview",
  done: new Set(JSON.parse(localStorage.getItem("agentCourseDone") || "[]")),
  runnerEnabled: false,
  docCache: new Map(),
};

const els = {
  lessonNav: document.querySelector("#lessonNav"),
  globalSearch: document.querySelector("#globalSearch"),
  courseTitle: document.querySelector("#courseTitle"),
  courseDescription: document.querySelector("#courseDescription"),
  courseStats: document.querySelector("#courseStats"),
  lessonCode: document.querySelector("#lessonCode"),
  lessonTitle: document.querySelector("#lessonTitle"),
  lessonIntro: document.querySelector("#lessonIntro"),
  topicPills: document.querySelector("#topicPills"),
  tabContent: document.querySelector("#tabContent"),
  toggleDone: document.querySelector("#toggleDone"),
  copyCommand: document.querySelector("#copyCommand"),
  askButton: document.querySelector("#askButton"),
  assistantQuestion: document.querySelector("#assistantQuestion"),
  assistantAnswer: document.querySelector("#assistantAnswer"),
  searchResults: document.querySelector("#searchResults"),
  searchCount: document.querySelector("#searchCount"),
  runnerStatus: document.querySelector("#runnerStatus"),
  runLesson: document.querySelector("#runLesson"),
  runOutput: document.querySelector("#runOutput"),
  toast: document.querySelector("#toast"),
};

const FLOW_LIBRARY = {
  L01: {
    title: "从聊天到 Agent 的最小闭环",
    nodes: ["用户目标", "LLM 理解", "规划步骤", "调用工具", "记忆沉淀", "返回结果"],
    checks: ["能区分 ChatBot 与 Agent", "能解释 LLM / Planning / Tools / Memory", "能跑通最小 LLM 调用"],
  },
  L02: {
    title: "Prompt 控制 Agent 行为",
    nodes: ["角色边界", "任务规则", "示例约束", "输出格式", "回归测试", "迭代优化"],
    checks: ["System Prompt 有职责和边界", "输出结构可解析", "Prompt 有测试集而不是凭感觉"],
  },
  L03: {
    title: "Function Calling 工具调用循环",
    nodes: ["用户问题", "工具选择", "参数生成", "工具执行", "结果回填", "最终回答"],
    checks: ["工具 schema 清晰", "失败有分类处理", "并发调用有边界和观测"],
  },
  L04: {
    title: "LangChain 快速组装 Agent",
    nodes: ["Model", "Prompt", "Tool", "Memory", "Agent Loop", "应用调用"],
    checks: ["能把手写循环映射到框架组件", "知道 LangChain 与 LangGraph 边界", "工具注释和 schema 足够清楚"],
  },
  L05: {
    title: "RAG 开卷问答链路",
    nodes: ["文档解析", "清洗切分", "索引构建", "问题检索", "上下文增强", "带引用回答"],
    checks: ["知道 chunk 与 overlap 的取舍", "知道 BM25/向量/重排的角色", "答案必须可追溯"],
  },
  L06: {
    title: "LCEL 管道化数据流",
    nodes: ["输入", "Prompt", "LLM", "Parser", "Retriever", "Callback"],
    checks: ["能解释 Runnable 组合", "能处理结构化输出", "能通过 Callback 观察链路"],
  },
  L07: {
    title: "记忆系统读写闭环",
    nodes: ["短期上下文", "摘要压缩", "长期存储", "相关召回", "冲突处理", "隐私治理"],
    checks: ["不同记忆层职责清楚", "记忆可遗忘可更新", "敏感偏好不乱写入"],
  },
  L08: {
    title: "Agent 模式与多 Agent 协作",
    nodes: ["任务分类", "模式选择", "多步推理", "跨源检索", "监督整合", "成本控制"],
    checks: ["能选择 RAG/ReAct/Multi-Agent", "知道何时不该多 Agent", "路由和分库策略明确"],
  },
  L09: {
    title: "MCP 标准化工具接入",
    nodes: ["Client", "Server", "Tools", "Resources", "Prompts", "Sampling 审核"],
    checks: ["能区分 MCP 与 Function Calling", "Root/权限/审计有边界", "Sampling 不绕过用户授权"],
  },
  L10: {
    title: "Skill 能力工程化",
    nodes: ["触发意图", "Skill 载入", "工具编排", "授权校验", "观测评测", "版本回滚"],
    checks: ["Tool/Skill/MCP 分层清楚", "高风险动作有确认", "重试预算和回滚策略明确"],
  },
  L11: {
    title: "评测部署生产闭环",
    nodes: ["评测集", "自动评分", "失败归因", "API 服务", "流式前端", "监控护栏"],
    checks: ["上线前有评测门禁", "成本和延迟可观察", "Prompt 注入和越权有防护"],
  },
  L12: {
    title: "智能客服 Agent 毕业项目闭环",
    nodes: ["需求验收", "LangGraph 状态机", "RAG 知识库", "工单工具", "FastAPI 展示", "答辩复盘"],
    checks: ["覆盖老师硬性要求", "测试和评测可复现", "项目亮点能转成面试表达"],
  },
};

const PHASES = [
  { label: "Foundation", range: "L01-L03", accent: "coral", text: "认知、Prompt、工具调用" },
  { label: "Framework", range: "L04-L06", accent: "teal", text: "LangChain、RAG、LCEL" },
  { label: "Systems", range: "L07-L09", accent: "blue", text: "Memory、模式、MCP" },
  { label: "Production", range: "L10-L12", accent: "amber", text: "Skill、评测部署、项目" },
];

const COVERAGE = [
  ["Prompt", 92],
  ["Tools", 94],
  ["RAG", 91],
  ["Memory", 86],
  ["MCP", 84],
  ["Skill", 95],
  ["Eval", 88],
  ["Deploy", 86],
];

document.addEventListener("DOMContentLoaded", init);

async function init() {
  animateCanvas();
  state.data = window.AGENT_COURSE_DATA || (await loadCourseData());
  applyHashRoute();
  state.currentLessonId = state.currentLessonId || state.data.lessons[0]?.id;
  renderShell();
  bindEvents();
  checkRunner();
  window.addEventListener("hashchange", () => {
    applyHashRoute();
    renderNav();
    renderLesson();
    syncTabs();
  });
}

function bindEvents() {
  document.querySelectorAll(".tab").forEach((button) => {
    button.addEventListener("click", () => {
      state.currentTab = button.dataset.tab;
      syncTabs();
      updateHash();
      renderLesson();
    });
  });

  els.globalSearch.addEventListener("input", () => renderSearch(els.globalSearch.value));
  els.toggleDone.addEventListener("click", toggleDone);
  els.copyCommand.addEventListener("click", copyCurrentCommand);
  els.askButton.addEventListener("click", answerQuestion);
  els.runLesson.addEventListener("click", runCurrentLesson);
}

function renderShell() {
  const { course, stats } = state.data;
  els.courseTitle.textContent = course.name;
  els.courseDescription.textContent = course.description;
  els.courseStats.innerHTML = [
    ["章节", stats.lessonCount],
    ["实践文件", stats.practiceCount],
    ["资源材料", stats.resourceCount],
    ["课程文件", stats.fileCount],
  ]
    .map(([label, value]) => `<div class="stat"><strong>${value}</strong><span>${label}</span></div>`)
    .join("");
  document.querySelector("#phaseStrip").innerHTML = PHASES.map(
    (phase) => `
      <div class="phase-card ${phase.accent}">
        <span>${escapeHtml(phase.range)}</span>
        <strong>${escapeHtml(phase.label)}</strong>
        <small>${escapeHtml(phase.text)}</small>
      </div>
    `
  ).join("");
  document.querySelector("#coverageBars").innerHTML = COVERAGE.map(
    ([label, value]) => `
      <div class="coverage-row">
        <span>${escapeHtml(label)}</span>
        <div class="coverage-track"><i style="width:${value}%"></i></div>
        <em>${value}</em>
      </div>
    `
  ).join("");
  renderNav();
  renderLesson();
  renderSearch("");
}

function renderNav() {
  els.lessonNav.innerHTML = state.data.lessons
    .map((lesson) => {
      const active = lesson.id === state.currentLessonId ? "active" : "";
      const done = state.done.has(lesson.id) ? "done" : "";
      return `
        <button class="lesson-link ${active} ${done}" data-lesson="${escapeAttr(lesson.id)}" type="button">
          <span class="lesson-code">${escapeHtml(lesson.code)}</span>
          <span class="lesson-name">${escapeHtml(trimTitle(lesson.title))}</span>
          <span class="done-dot" aria-hidden="true"></span>
        </button>
      `;
    })
    .join("");

  els.lessonNav.querySelectorAll(".lesson-link").forEach((button) => {
    button.addEventListener("click", () => {
      state.currentLessonId = button.dataset.lesson;
      state.currentTab = "overview";
      syncTabs();
      updateHash();
      renderNav();
      renderLesson();
    });
  });
}

function currentLesson() {
  return state.data.lessons.find((lesson) => lesson.id === state.currentLessonId);
}

async function loadCourseData() {
  try {
    const res = await fetch("/api/course");
    if (res.ok) return await res.json();
  } catch {
    // Static hosting mode falls back to the generated JSON file.
  }
  const res = await fetch("./data/course.json");
  return res.json();
}

async function renderLesson() {
  const lesson = currentLesson();
  if (!lesson) return;

  els.lessonCode.textContent = lesson.code;
  els.lessonTitle.textContent = lesson.title;
  els.lessonIntro.textContent = lesson.intro;
  els.toggleDone.textContent = state.done.has(lesson.id) ? "已完成" : "标记完成";
  els.topicPills.innerHTML = lesson.topics.map((topic) => `<span class="pill">${escapeHtml(topic)}</span>`).join("");

  const renderers = {
    overview: renderOverview,
    lecture: renderLecture,
    practice: renderPractice,
    trace: renderTrace,
    interview: renderInterview,
    resources: renderResources,
  };
  const lessonIdAtStart = lesson.id;
  els.tabContent.innerHTML = `<div class="empty">正在加载章节内容...</div>`;
  const html = await renderers[state.currentTab](lesson);
  if (currentLesson()?.id === lessonIdAtStart) {
    els.tabContent.innerHTML = html;
  }
  bindDynamicButtons();
}

function renderOverview(lesson) {
  return `
    <div class="content-grid">
      <section class="content-block">
        <h3>学习目标</h3>
        ${renderList(lesson.goals)}
      </section>
      <section class="content-block">
        <h3>交付物</h3>
        ${renderList(lesson.deliverables)}
      </section>
      <section class="content-block">
        <h3>文件地图</h3>
        <ul>
          <li>讲义与总结：${countDocs(lesson, ["lecture", "summary"])} 份</li>
          <li>实践文件：${lesson.practiceFiles.length} 个</li>
          <li>材料文件：${lesson.materialFiles.length} 个</li>
          <li>资源文件：${lesson.resourceFiles.length} 个</li>
        </ul>
      </section>
      <section class="content-block">
        <h3>一键学习命令</h3>
        ${renderCommand(lesson.preclassCommand || "本章暂无一键脚本")}
      </section>
    </div>
  `;
}

async function renderLecture(lesson) {
  const doc = findDoc(lesson, "lecture") || findDoc(lesson, "summary") || findDoc(lesson, "readme");
  return doc ? renderMarkdownDoc(doc, await loadDocContent(doc)) : empty("本章暂无讲义内容。");
}

async function renderPractice(lesson) {
  return `
    <section class="content-block">
      <h3>实验入口</h3>
      <p class="muted">建议先复制命令在本地终端运行；如服务端显式开启 runner，也可以在右侧实验区执行白名单脚本。</p>
      ${renderCommand(lesson.preclassCommand || "本章暂无一键脚本")}
    </section>
    <section class="file-list" style="margin-top:12px">
      ${renderFiles(lesson.practiceFiles)}
    </section>
  `;
}

async function renderTrace(lesson) {
  const flow = FLOW_LIBRARY[lesson.code] || FLOW_LIBRARY.L01;
  const nodes = flow.nodes
    .map(
      (node, index) => `
        <div class="flow-node">
          <span>${String(index + 1).padStart(2, "0")}</span>
          <strong>${escapeHtml(node)}</strong>
        </div>
      `
    )
    .join("");
  return `
    <section class="flow-board">
      <div>
        <p class="eyebrow">${escapeHtml(lesson.code)} · Agent 开发图谱</p>
        <h3>${escapeHtml(flow.title)}</h3>
        <p class="muted">这张图用于课堂讲解和复盘：先抓住本章主链路，再回到讲义与代码里看每一步怎么落地。</p>
      </div>
      <div class="flow-lane">${nodes}</div>
    </section>
    <div class="content-grid" style="margin-top:12px">
      <section class="content-block">
        <h3>验收检查</h3>
        ${renderList(flow.checks)}
      </section>
      <section class="content-block">
        <h3>建议演示顺序</h3>
        ${renderList([
          "先讲清图谱中的主链路和失败点。",
          "再打开“实战”页复制或运行本章脚本。",
          "最后切到“面试”页，把工程判断整理成可表达答案。",
        ])}
      </section>
    </div>
  `;
}

async function renderInterview(lesson) {
  const doc = findDoc(lesson, "interview");
  if (!doc) return empty("本章暂未整理独立面试题，建议查看章节总结和拓展作业。");
  return renderMarkdownDoc(doc, await loadDocContent(doc));
}

async function renderResources(lesson) {
  const resourceDocs = lesson.docs.filter((doc) => doc.key.startsWith("resource:"));
  const support = state.data.supportDocs || [];
  const html = [
    `<section class="content-block"><h3>本章资源</h3>${renderFiles(lesson.resourceFiles)}</section>`,
    `<section class="content-block" style="margin-top:12px"><h3>教辅资料</h3>${renderSupportDocs(support)}</section>`,
  ];
  if (resourceDocs.length) {
    html.push(
      `<section class="content-block" style="margin-top:12px"><h3>资源摘要</h3>${resourceDocs
        .map((doc) => `<p><strong>${escapeHtml(doc.label)}</strong><br><span class="muted">${escapeHtml(doc.excerpt)}</span></p>`)
        .join("")}</section>`
    );
  }
  return html.join("");
}

function renderList(items) {
  if (!items || !items.length) return `<p class="muted">暂无结构化条目，请查看讲义正文。</p>`;
  return `<ul>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
}

function renderFiles(files) {
  if (!files || !files.length) return `<div class="empty">暂无文件。</div>`;
  return files
    .map(
      (file) => `
        <div class="file-row">
          <div>
            <strong>${escapeHtml(file.name)}</strong><br />
            <small>${escapeHtml(file.path)}</small>
          </div>
          <small>${escapeHtml(file.size || "")}</small>
        </div>
      `
    )
    .join("");
}

function renderSupportDocs(docs) {
  if (!docs.length) return `<div class="empty">暂无教辅资料。</div>`;
  return docs
    .map(
      (doc) => `
        <div class="file-row">
          <div>
            <strong>${escapeHtml(doc.title)}</strong><br />
            <small>${escapeHtml(doc.path)}</small>
          </div>
        </div>
      `
    )
    .join("");
}

function renderCommand(command) {
  return `
    <div class="command-box">
      <pre><code>${escapeHtml(command)}</code></pre>
      <button class="secondary-action copy-inline" data-copy="${escapeAttr(command)}" type="button">复制这条命令</button>
    </div>
  `;
}

async function loadDocContent(doc) {
  if (!doc?.contentPath) return doc?.excerpt || "";
  if (state.docCache.has(doc.contentPath)) return state.docCache.get(doc.contentPath);
  const res = await fetch(doc.contentPath);
  const text = res.ok ? await res.text() : doc.excerpt || "";
  state.docCache.set(doc.contentPath, text);
  return text;
}

function renderMarkdownDoc(doc, content) {
  return `
    <article class="markdown-view">
      <p class="eyebrow">${escapeHtml(doc.label)} · ${escapeHtml(doc.path)}</p>
      ${markdownToHtml(content)}
    </article>
  `;
}

function empty(message) {
  return `<div class="empty">${escapeHtml(message)}</div>`;
}

function bindDynamicButtons() {
  document.querySelectorAll(".copy-inline").forEach((button) => {
    button.addEventListener("click", () => copyText(button.dataset.copy || ""));
  });
}

function findDoc(lesson, key) {
  return lesson.docs.find((doc) => doc.key === key);
}

function countDocs(lesson, keys) {
  return lesson.docs.filter((doc) => keys.includes(doc.key)).length;
}

function renderSearch(query) {
  const hits = search(query);
  els.searchCount.textContent = hits.length;
  els.searchResults.innerHTML =
    hits.length === 0
      ? `<div class="empty">输入关键词后显示匹配章节。</div>`
      : hits
          .slice(0, 8)
          .map(
            (hit) => `
              <div class="search-hit">
                <button data-lesson="${escapeAttr(hit.lesson.id)}" type="button">${escapeHtml(hit.lesson.code)} · ${escapeHtml(trimTitle(hit.lesson.title))}</button>
                <p>${escapeHtml(hit.reason)}</p>
              </div>
            `
          )
          .join("");

  els.searchResults.querySelectorAll("button[data-lesson]").forEach((button) => {
    button.addEventListener("click", () => {
      state.currentLessonId = button.dataset.lesson;
      updateHash();
      renderNav();
      renderLesson();
    });
  });
}

function search(query) {
  const q = normalize(query);
  if (!q) return [];
  const terms = q.split(/\s+/).filter(Boolean);
  return state.data.lessons
    .map((lesson) => {
      const corpus = normalize([lesson.title, lesson.intro, lesson.topics.join(" "), lesson.searchText].join(" "));
      let score = 0;
      terms.forEach((term) => {
        if (corpus.includes(term)) score += term.length > 2 ? 3 : 1;
        if (normalize(lesson.title).includes(term)) score += 5;
        if (lesson.topics.some((topic) => normalize(topic).includes(term))) score += 4;
      });
      return {
        lesson,
        score,
        reason: lesson.searchText || lesson.intro,
      };
    })
    .filter((hit) => hit.score > 0)
    .sort((a, b) => b.score - a.score);
}

function answerQuestion() {
  const query = els.assistantQuestion.value.trim();
  if (!query) {
    showToast("先输入一个课程问题");
    return;
  }
  const hits = search(query).slice(0, 5);
  if (!hits.length) {
    els.assistantAnswer.innerHTML = "没有在本地课程索引中找到足够证据。建议换一个关键词，或直接查看左侧课程地图。";
    return;
  }
  const refs = hits
    .map((hit) => {
      const doc = findBestDoc(hit.lesson, query);
      return `<li><button data-lesson="${escapeAttr(hit.lesson.id)}" type="button">${escapeHtml(hit.lesson.code)} · ${escapeHtml(trimTitle(hit.lesson.title))}</button><br><span class="muted">${escapeHtml(doc?.path || hit.lesson.id)}</span><p>${escapeHtml(doc?.excerpt || hit.lesson.intro)}</p></li>`;
    })
    .join("");
  const focus = hits[0].lesson.topics.slice(0, 4).join("、");
  const route = suggestLearningRoute(hits[0].lesson, query);
  els.assistantAnswer.innerHTML = `
    <strong>建议先看 ${escapeHtml(hits[0].lesson.code)}。</strong>
    <p>从本地索引看，你的问题和 ${escapeHtml(focus || hits[0].lesson.title)} 关系最强。可以先读匹配章节的讲义和总结，再进入实战脚本验证。</p>
    <p><strong>学习动作</strong></p>
    <ol>${route.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ol>
    <p><strong>引用来源</strong></p>
    <ol>${refs}</ol>
  `;
  els.assistantAnswer.querySelectorAll("button[data-lesson]").forEach((button) => {
    button.addEventListener("click", () => {
      state.currentLessonId = button.dataset.lesson;
      state.currentTab = "overview";
      syncTabs();
      updateHash();
      renderNav();
      renderLesson();
    });
  });
}

function suggestLearningRoute(lesson, query) {
  const q = normalize(query);
  if (q.includes("面试")) {
    return ["先打开本章“面试”页建立回答框架。", "回到“讲义”页补概念定义。", "用“实战”页命令验证代码路径。"];
  }
  if (q.includes("代码") || q.includes("运行") || q.includes("demo")) {
    return ["先打开“实战”页复制本章命令。", "运行前确认 `.env` 和 conda 环境。", "运行后回到“图谱”页复盘链路。"];
  }
  if (q.includes("架构") || q.includes("设计")) {
    return ["先看“图谱”页抓住主流程。", "再读资源文档里的工程专题。", "最后整理成本章交付物或答辩表达。"];
  }
  return [`先读 ${lesson.code} 的讲义和总结。`, "再看图谱，把主流程用自己的话复述一遍。", "最后进入实战页运行或阅读关键脚本。"];
}

function findBestDoc(lesson, query) {
  const terms = normalize(query).split(/\s+/).filter(Boolean);
  return lesson.docs
    .map((doc) => {
      const corpus = normalize([doc.label, doc.path, doc.excerpt].join(" "));
      return {
        doc,
        score: terms.reduce((sum, term) => sum + (corpus.includes(term) ? 1 : 0), 0),
      };
    })
    .sort((a, b) => b.score - a.score)[0]?.doc;
}

function toggleDone() {
  const lesson = currentLesson();
  if (!lesson) return;
  if (state.done.has(lesson.id)) {
    state.done.delete(lesson.id);
  } else {
    state.done.add(lesson.id);
  }
  localStorage.setItem("agentCourseDone", JSON.stringify([...state.done]));
  renderNav();
  renderLesson();
}

function copyCurrentCommand() {
  const lesson = currentLesson();
  copyText(lesson?.preclassCommand || "");
}

function copyText(text) {
  if (!text) return;
  navigator.clipboard.writeText(text).then(() => showToast("已复制"));
}

async function checkRunner() {
  if (window.AGENT_COURSE_STATIC_EXPORT) {
    state.runnerEnabled = false;
    els.runnerStatus.textContent = "静态模式";
    return;
  }
  try {
    const res = await fetch("/api/health");
    if (!res.ok) throw new Error("static mode");
    const data = await res.json();
    state.runnerEnabled = Boolean(data.runnerEnabled);
    els.runnerStatus.textContent = state.runnerEnabled ? "已启用" : "默认关闭";
  } catch {
    state.runnerEnabled = false;
    els.runnerStatus.textContent = "静态模式";
  }
}

async function runCurrentLesson() {
  const lesson = currentLesson();
  if (!lesson) return;
  els.runOutput.textContent = "正在请求本地服务...";
  try {
    const res = await fetch("/api/runs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ lessonId: lesson.id }),
    });
    const data = await res.json();
    els.runOutput.textContent = data.output || data.message || JSON.stringify(data, null, 2);
    if (!res.ok) showToast("真实执行未开启，已显示安全提示");
  } catch (err) {
    els.runOutput.textContent = `当前是静态模式，不能直接运行脚本。\n\n请在终端执行：\n${lesson.preclassCommand}`;
  }
}

function markdownToHtml(markdown) {
  const lines = markdown.split("\n");
  let html = "";
  let inCode = false;
  let inList = false;
  let inTable = false;
  let tableRows = [];

  const flushList = () => {
    if (inList) {
      html += "</ul>";
      inList = false;
    }
  };

  const flushTable = () => {
    if (!inTable) return;
    const rows = tableRows.filter((row) => !/^\|\s*-+/.test(row));
    html += "<table>";
    rows.forEach((row, idx) => {
      const cells = row
        .split("|")
        .slice(1, -1)
        .map((cell) => cell.trim());
      const tag = idx === 0 ? "th" : "td";
      html += `<tr>${cells.map((cell) => `<${tag}>${inlineMarkdown(cell)}</${tag}>`).join("")}</tr>`;
    });
    html += "</table>";
    tableRows = [];
    inTable = false;
  };

  lines.forEach((raw) => {
    const line = raw.replace(/\r$/, "");
    if (line.startsWith("```")) {
      flushList();
      flushTable();
      if (!inCode) {
        inCode = true;
        html += "<pre><code>";
      } else {
        inCode = false;
        html += "</code></pre>";
      }
      return;
    }
    if (inCode) {
      html += `${escapeHtml(line)}\n`;
      return;
    }
    if (line.trim().startsWith("|") && line.trim().endsWith("|")) {
      flushList();
      inTable = true;
      tableRows.push(line.trim());
      return;
    }
    flushTable();
    const trimmed = line.trim();
    if (!trimmed) {
      flushList();
      return;
    }
    if (trimmed.startsWith("# ")) {
      flushList();
      html += `<h1>${inlineMarkdown(trimmed.slice(2))}</h1>`;
    } else if (trimmed.startsWith("## ")) {
      flushList();
      html += `<h2>${inlineMarkdown(trimmed.slice(3))}</h2>`;
    } else if (trimmed.startsWith("### ")) {
      flushList();
      html += `<h3>${inlineMarkdown(trimmed.slice(4))}</h3>`;
    } else if (trimmed.startsWith("- ")) {
      if (!inList) {
        html += "<ul>";
        inList = true;
      }
      html += `<li>${inlineMarkdown(trimmed.slice(2))}</li>`;
    } else if (/^\d+\.\s/.test(trimmed)) {
      flushList();
      html += `<p>${inlineMarkdown(trimmed)}</p>`;
    } else {
      flushList();
      html += `<p>${inlineMarkdown(trimmed)}</p>`;
    }
  });
  flushList();
  flushTable();
  return html;
}

function inlineMarkdown(text) {
  return escapeHtml(text)
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<span title="$2">$1</span>');
}

function animateCanvas() {
  const canvas = document.querySelector("#flowCanvas");
  const ctx = canvas.getContext("2d");
  const nodes = Array.from({ length: 34 }, (_, i) => ({
    x: Math.random(),
    y: Math.random(),
    vx: (Math.random() - 0.5) * 0.0007,
    vy: (Math.random() - 0.5) * 0.0007,
    r: i % 7 === 0 ? 2.4 : 1.5,
  }));

  const resize = () => {
    canvas.width = window.innerWidth * window.devicePixelRatio;
    canvas.height = window.innerHeight * window.devicePixelRatio;
  };
  window.addEventListener("resize", resize);
  resize();

  const tick = () => {
    const w = canvas.width;
    const h = canvas.height;
    ctx.clearRect(0, 0, w, h);
    nodes.forEach((node) => {
      node.x += node.vx;
      node.y += node.vy;
      if (node.x < 0 || node.x > 1) node.vx *= -1;
      if (node.y < 0 || node.y > 1) node.vy *= -1;
    });

    ctx.lineWidth = 1 * window.devicePixelRatio;
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const a = nodes[i];
        const b = nodes[j];
        const dx = (a.x - b.x) * w;
        const dy = (a.y - b.y) * h;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 190 * window.devicePixelRatio) {
          ctx.strokeStyle = `rgba(15, 118, 110, ${0.14 * (1 - dist / (190 * window.devicePixelRatio))})`;
          ctx.beginPath();
          ctx.moveTo(a.x * w, a.y * h);
          ctx.lineTo(b.x * w, b.y * h);
          ctx.stroke();
        }
      }
    }
    nodes.forEach((node) => {
      ctx.fillStyle = "rgba(23, 32, 42, 0.32)";
      ctx.beginPath();
      ctx.arc(node.x * w, node.y * h, node.r * window.devicePixelRatio, 0, Math.PI * 2);
      ctx.fill();
    });
    requestAnimationFrame(tick);
  };
  tick();
}

function normalize(text) {
  return String(text || "").toLowerCase().replace(/[^\p{L}\p{N}]+/gu, " ").trim();
}

function trimTitle(title) {
  return String(title || "").replace(/^L\d+\s*/, "").replace(/^第\d+讲[:：]?\s*/, "");
}

function escapeHtml(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttr(value) {
  return escapeHtml(value).replaceAll("\n", " ");
}

function showToast(message) {
  els.toast.textContent = message;
  els.toast.classList.add("show");
  setTimeout(() => els.toast.classList.remove("show"), 1600);
}

function applyHashRoute() {
  const raw = decodeURIComponent(location.hash.replace(/^#/, ""));
  if (!raw) return;
  const [lessonId, tab] = raw.split(/[/:]/);
  if (lessonId && state.data?.lessons?.some((lesson) => lesson.id === lessonId)) {
    state.currentLessonId = lessonId;
  }
  if (tab && ["overview", "lecture", "practice", "trace", "interview", "resources"].includes(tab)) {
    state.currentTab = tab;
  }
}

function updateHash() {
  if (!state.currentLessonId) return;
  const next = `#${state.currentLessonId}/${state.currentTab}`;
  if (location.hash !== next) history.replaceState(null, "", next);
}

function syncTabs() {
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.tab === state.currentTab);
  });
}
