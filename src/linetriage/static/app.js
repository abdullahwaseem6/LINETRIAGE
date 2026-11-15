  const ROUTES = {
    safety_alert: "Safety alert",
    human_review: "Human review",
    escalate_quality: "Escalate to quality",
    auto_ticket: "Auto ticket",
  };
  const FIELDS = [
    ["station_id", "Station"],
    ["fault_type", "Fault type"],
    ["downtime_minutes", "Downtime"],
    ["recurring", "Recurring"],
    ["safety_involved", "Safety risk"],
    ["affected_part", "Affected part"],
    ["language", "Language"],
  ];
  const LANGUAGES = { en: "English", hu: "Hungarian", de: "German", mixed: "Mixed" };
  const $ = (id) => document.getElementById(id);
  const text = $("text"), submit = $("submit");
  const stages = [$("st1"), $("st2"), $("st3")];
  let ticketNo = 1000 + Math.floor(Math.random() * 9000);


  // Pipeline boxes: a light that follows the mouse, and blue sparks drifting out and fading.
  const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
  stages.forEach((stage) => {
    stage.addEventListener("pointermove", (e) => {
      const r = stage.getBoundingClientRect();
      stage.style.setProperty("--mx", `${e.clientX - r.left}px`);
      stage.style.setProperty("--my", `${e.clientY - r.top}px`);
    });
    stage.addEventListener("pointerleave", () => {
      stage.style.setProperty("--mx", "50%");
      stage.style.setProperty("--my", "50%");
    });
  });

  function spark(stage) {
    const r = stage.getBoundingClientRect();
    const el = document.createElement("span");
    el.className = "spark";
    // Start somewhere on the box's edge and drift outwards.
    const edge = Math.floor(Math.random() * 4);
    let x = Math.random() * r.width, y = Math.random() * r.height, dx = (Math.random() - 0.5) * 30, dy = (Math.random() - 0.5) * 30;
    if (edge === 0) { y = 0; dy = -(20 + Math.random() * 40); }
    if (edge === 1) { x = r.width; dx = 20 + Math.random() * 40; }
    if (edge === 2) { y = r.height; dy = 20 + Math.random() * 30; }
    if (edge === 3) { x = 0; dx = -(20 + Math.random() * 40); }
    el.style.left = `${x - 2}px`;
    el.style.top = `${y - 2}px`;
    el.style.setProperty("--dx", `${dx}px`);
    el.style.setProperty("--dy", `${dy}px`);
    el.style.setProperty("--life", `${1.4 + Math.random() * 1.6}s`);
    el.addEventListener("animationend", () => el.remove());
    stage.append(el);
  }

  if (!calm) {
    setInterval(() => {
      if (document.hidden) return;
      stages.forEach((stage) => {
        const busy = stage.matches(":hover") || stage.classList.contains("active");
        const chance = busy ? 0.95 : 0.22;
        if (Math.random() < chance) spark(stage);
        if (busy && Math.random() < 0.6) spark(stage);
      });
    }, 160);
  }

  const updateCount = () => { $("count").textContent = `${text.value.length} / 2000`; };
  text.addEventListener("input", updateCount);
  // Access: guests can run the free samples; an access code unlocks your own notes.
  let accessCode = "";
  let role = "guest";
  try { accessCode = localStorage.getItem("linetriage-code") || ""; } catch (e) {}

  function setRole(next) {
    role = next;
    const badge = $("role");
    badge.textContent = { owner: "Owner", member: "Member", open: "Open access", guest: "Guest" }[role];
    badge.className = "role " + (role === "owner" ? "owner" : role === "member" ? "member" : "");
    const unlocked = role !== "guest";
    $("access").classList.toggle("unlocked", unlocked);
    $("access-label").textContent = unlocked
      ? (role === "open" ? "Open access: any note can be triaged" : `Unlocked as ${role}: triage any note`)
      : "Your own notes need an access code";
    text.readOnly = !unlocked;
    text.placeholder = unlocked ? "Paste an operator's shift note…" : "Pick a free sample below, or unlock with an access code";
  }

  async function checkCode(code) {
    try {
      const r = await fetch("/access", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ code }) });
      return (await r.json()).role;
    } catch (e) { return "guest"; }
  }

  $("unlock").addEventListener("click", async () => {
    const code = $("code").value.trim();
    const found = await checkCode(code);
    if (found === "guest") { $("error").textContent = "That access code isn't valid."; return; }
    accessCode = code;
    try { localStorage.setItem("linetriage-code", code); } catch (e) {}
    $("error").textContent = "";
    setRole(found);
  });
  $("code").addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); $("unlock").click(); } });

  fetch("/samples").then((r) => r.json()).then((samples) => {
    const box = $("chips");
    for (const s of samples) {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = "chip";
      const tag = document.createElement("span");
      tag.className = "tag";
      tag.textContent = s.tag;
      const label = document.createElement("span");
      label.textContent = s.text;
      chip.append(tag, label);
      chip.addEventListener("click", () => {
        box.querySelectorAll(".chip").forEach((c) => c.classList.remove("active"));
        chip.classList.add("active");
        text.value = s.text;
        updateCount();
      });
      box.append(chip);
    }
  });

  checkCode(accessCode).then(setRole);

  function setStage(i) {
    stages.forEach((s, j) => {
      s.classList.toggle("active", j === i);
      s.classList.toggle("done", j < i);
    });
  }

  function show(key, value) {
    if (value === null || value === undefined) return null;
    if (typeof value === "boolean") return value ? "Yes" : "No";
    if (key === "downtime_minutes") return value === 0 ? "0 min (running)" : `${value} min`;
    if (key === "language") return LANGUAGES[value] || value;
    return String(value);
  }

  function render(data) {
    const route = $("route");
    route.className = "route " + data.route;
    $("route-name").textContent = ROUTES[data.route] || data.route;
    $("route-reason").textContent = data.reason;
    $("summary").textContent = data.facts.summary;
    $("ticket").textContent = `#${ticketNo++}`;

    const facts = $("facts");
    facts.replaceChildren();
    for (const [key, label] of FIELDS) {
      const value = show(key, data.facts[key]);
      const box = document.createElement("div");
      const dt = document.createElement("dt");
      const dd = document.createElement("dd");
      dt.textContent = label;
      dd.textContent = value ?? "Unknown";
      if (value === null) dd.className = "none";
      if (key === "safety_involved" && data.facts[key]) dd.className = "warn";
      box.append(dt, dd);
      facts.append(box);
    }

    const op = data.second_opinion;
    const second = $("second");
    second.hidden = !op;
    if (op) {
      $("second-meta").textContent = `Own model · ${op.milliseconds} ms · $0`;
      $("tick").style.left = `${op.threshold * 100}%`;
      $("fill").style.width = "0";
      requestAnimationFrame(() => requestAnimationFrame(() => { $("fill").style.width = `${Math.max(2, op.danger_score * 100)}%`; }));
      const verdict = $("verdict");
      verdict.replaceChildren();
      const score = document.createElement("span");
      score.textContent = `Danger score ${op.danger_score.toFixed(2)}`;
      const pill = document.createElement("span");
      pill.className = "pill " + (op.dangerous ? "danger" : "ok");
      pill.textContent = op.dangerous ? "Dangerous" : "Safe";
      const llmSafe = data.facts.safety_involved;
      const agree = document.createElement("span");
      if (op.dangerous === llmSafe) {
        agree.className = "pill agree";
        agree.textContent = "Agrees with the LLM";
      } else if (op.dangerous) {
        agree.className = "pill check";
        agree.textContent = "Possible risk the LLM missed: please check";
      } else {
        agree.className = "pill agree";
        agree.textContent = "The LLM is more cautious";
      }
      verdict.append(score, pill, agree);
    }

    $("review-note").textContent = "Awaiting your decision";
    $("empty").hidden = true;
    $("result").hidden = false;
  }

  $("form").addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!text.value.trim()) return;
    submit.disabled = true;
    $("submit-label").textContent = "Analysing…";
    $("error").textContent = "";
    setStage(0);
    const timer = setTimeout(() => setStage(1), 900);
    try {
      const response = await fetch("/triage", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-Access-Code": accessCode },
        body: JSON.stringify({ text: text.value }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(typeof data.detail === "string" ? data.detail : "Invalid request.");
      clearTimeout(timer);
      setStage(1);
      await new Promise((r) => setTimeout(r, 250));
      setStage(2);
      render(data);
    } catch (err) {
      clearTimeout(timer);
      setStage(-1);
      $("error").textContent = err.message || "Something went wrong.";
    } finally {
      submit.disabled = false;
      $("submit-label").textContent = "Run triage";
    }
  });

  document.querySelectorAll("[data-decision]").forEach((button) =>
    button.addEventListener("click", () => {
      const when = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
      $("review-note").textContent = `${button.dataset.decision} at ${when} · not saved yet`;
      setStage(3);
    })
  );
