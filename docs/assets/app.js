const state = {
  index: null, months: [], selectedMonth: null,
  sources: new Set(["WIRED","The Economist","Scientific American","The Atlantic","The New York Times","The Wall Street Journal"]),
  cache: {}, query: ""
};

async function loadIndex(){
  const r = await fetch("./data/index.json", {cache:"no-store"});
  if(!r.ok) throw new Error("index.json not found");
  state.index = await r.json();
  state.months = state.index.months || [];
  state.selectedMonth = state.months[state.months.length - 1];
  renderMonthOptions();
}

function renderMonthOptions(){
  const sel = document.getElementById("monthSelect");
  sel.innerHTML = "";
  state.months.forEach(m=>{
    const opt = document.createElement("option");
    opt.value = m; opt.textContent = `${m} (${state.index.counts[m]||0})`;
    sel.appendChild(opt);
  });
  if(state.selectedMonth) sel.value = state.selectedMonth;
  sel.onchange = ()=>{ state.selectedMonth = sel.value; renderList(); };
}

async function loadMonthData(monthKey){
  if(state.cache[monthKey]) return state.cache[monthKey];
  const [y,m] = monthKey.split("-");
  const r = await fetch(`./data/${y}/${m}.json`, {cache:"no-store"});
  const data = r.ok ? await r.json() : [];
  state.cache[monthKey] = data;
  return data;
}

function fmtDate(iso){
  if(!iso) return "";
  const d = new Date(iso);
  try { return d.toLocaleString("zh-CN",{hour12:false,timeZone:"Asia/Shanghai"}); }
  catch { return d.toLocaleString("zh-CN",{hour12:false}); }
}
function escapeHtml(s){ return (s||"").replace(/[&<>"']/g, m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m])); }

function card(it){
  const div = document.createElement("div");
  div.className = "card";
  const by = it.author ? `<span class="byline">${escapeHtml(it.author)}</span>` : "";
  const meta = `${by}${by?" · ":""}${escapeHtml(fmtDate(it.published_at))} · ${escapeHtml(it.source)}`;
  const canReadHere = !!it.can_publish_fulltext && (it.content_text || it.content_html);
  const readBtn = canReadHere ? `<a href="#" class="button primary" data-read-id="${it.id}">阅读</a>` : "";
  const giftBtn = it.gift_url ? `<a class="button" href="${it.gift_url}" target="_blank" rel="noopener noreferrer">礼物链接</a>` : "";
  const openBtn = `<a class="button" href="${it.url}" target="_blank" rel="noopener noreferrer">原文</a>`;
  div.innerHTML = `
    <h3><a href="${it.url}" target="_blank" rel="noopener noreferrer">${escapeHtml(it.title)}</a></h3>
    <div class="meta">${meta}</div>
    <div class="summary">${escapeHtml(it.summary||"")}</div>
    <div class="actions" style="margin-top:10px">${readBtn} ${giftBtn} ${openBtn}</div>
  `;
  // 绑定阅读
  if(canReadHere){
    const a = div.querySelector(`[data-read-id="${it.id}"]`);
    a.addEventListener("click", (ev)=>{ ev.preventDefault(); openReader(it); });
  }
  return div;
}

async function renderList(){
  const list = document.getElementById("list");
  list.innerHTML = `<div class="card"><div class="meta">加载中…</div></div>`;
  const data = await loadMonthData(state.selectedMonth);
  const q = (state.query||"").trim().toLowerCase();
  const filtered = data.filter(it=>state.sources.has(it.source)).filter(it=>{
    if(!q) return true;
    const hay = (it.title+" "+(it.summary||"")+" "+(it.author||"")).toLowerCase();
    return hay.includes(q);
  });
  list.innerHTML = "";
  if(filtered.length === 0){
    list.innerHTML = `<div class="card"><div class="meta">没有匹配结果</div></div>`;
    return;
  }
  filtered.forEach(it=>list.appendChild(card(it)));
}

function bindControls(){
  document.querySelectorAll(".src").forEach(cb=>{
    cb.addEventListener("change", ()=>{
      if(cb.checked) state.sources.add(cb.value); else state.sources.delete(cb.value);
      renderList();
    });
  });
  document.getElementById("q").addEventListener("input", e=>{
    state.query = e.target.value || ""; renderList();
  });
  // 阅读器关闭
  const reader = document.getElementById("reader");
  reader.querySelector(".reader__backdrop").addEventListener("click", closeReader);
  reader.querySelector(".reader__close").addEventListener("click", closeReader);
}

function closeReader(){
  const r = document.getElementById("reader");
  r.classList.add("hidden");
  document.body.style.overflow = "";
}

function openReader(it){
  const r = document.getElementById("reader");
  r.classList.remove("hidden");
  document.body.style.overflow = "hidden";
  document.getElementById("rd-title").textContent = it.title || "";
  document.getElementById("rd-meta").textContent = `${it.author?it.author+" · ":""}${fmtDate(it.published_at)} · ${it.source}`;
  const actions = document.getElementById("rd-actions");
  actions.innerHTML = `
    <a class="button" href="${it.url}" target="_blank" rel="noopener noreferrer">原文</a>
    ${it.gift_url ? `<a class="button" href="${it.gift_url}" target="_blank" rel="noopener noreferrer">礼物链接</a>` : ""}
  `;
  const body = document.getElementById("rd-body");
  body.innerHTML = "";
  if(it.content_html){
    // 简单净化：移除 script/style
    const tmp = document.createElement("div");
    tmp.innerHTML = it.content_html;
    tmp.querySelectorAll("script,style,noscript,iframe").forEach(n=>n.remove());
    body.appendChild(tmp);
  } else if(it.content_text){
    it.content_text.split(/\n{2,}/).forEach(p=>{
      const el = document.createElement("p"); el.textContent = p.trim(); body.appendChild(el);
    });
  } else {
    body.innerHTML = `<p class="meta">该来源未提供公开可展示的全文，请点击原文阅读。</p>`;
  }
}

(async function(){
  bindControls();
  try { await loadIndex(); await renderList(); }
  catch(e){ document.getElementById("list").innerHTML = `<div class="card"><div class="meta">数据尚未生成。请在 Actions 运行一次工作流。</div></div>`; }
})();
