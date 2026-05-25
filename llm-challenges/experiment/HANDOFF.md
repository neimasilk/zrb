# Handoff — LLM Benchmark Paper Publication

**Tanggal:** 2026-04-22
**Status:** Triage selesai, memo jurnal selesai. Belum ada edit ke paper. Menunggu keputusan venue dari Mukhlis.

---

## 1. Konteks & Scope Lock

**Paper:** "Comprehensive Evaluation of Large Language Models on Software Engineering Tasks: A Multi-Task Benchmark"
**Authors:** Go Frendi Gunawan (first), Mukhlis Amien (second — dosen UBHINUS, pemilik sesi ini)
**arXiv:** v1 published 6 Feb 2026 (arXiv:2602.07079), idle 2.5 bulan, **belum submit ke jurnal manapun**
**Working dir paper:** `D:\documents\zrb\llm-challenges\experiment\` (semua aset paper di subtree ini)

**SCOPE LOCK — jangan dilanggar:**
- HANYA sentuh subtree `llm-challenges/experiment/`
- JANGAN edit `src/zrb/` atau framework Zrb (out-of-scope; itu proyek Go Frendi / State Alchemists)
- JANGAN rewrite paper dari scratch — hanya polish existing
- Abaikan `CLAUDE.md` dan `AGENTS.md` di root (mereka describe framework Zrb, bukan paper)

**Goal:** Low-effort submission ke jurnal Scopus. BUKAN major expansion, BUKAN refactor.

---

## 2. Syarat Publikasi (Final)

Dikonfirmasi Mukhlis:
1. **Gratis — no APC wajib** (subscription model OK; Gold OA opsional OK; wajib-bayar OA OUT)
2. **Scopus indexed**
3. **Quartile bebas** (Q1–Q4 semua diterima)
4. (Implisit) Menerima paper yang sudah di arXiv

---

## 3. State Paper Saat Ini

### Struktur
- 10 halaman IEEE conference two-column (build terakhir: `paper/main_v2.pdf`)
- Semua section lengkap: Abstract, Intro, Related Work, Methodology, Results, Discussion, Conclusion
- 16 references (FINAL_REPORT menargetkan 30 — gap 14)
- Bahasa EN, belum ada co-author selain Go Frendi & Mukhlis

### Data & reproducibility
- `results.json`: **55 run = 11 model × 5 task** (bukan 13 model seperti yang sempat disebut awal)
- 11 model: GPT-4o/5.1/5.2, Gemini 2.5 Flash/Pro + 3 Flash/Pro preview, Deepseek-Chat, Ollama-cloud (GLM-4.7, Kimi-K2.5, Qwen3-VL)
- **Anthropic Claude tidak ada** — sudah di-acknowledge sebagai limitation di `05_discussion.tex:67`
- Scripts siap: `analyze_anomaly.py`, `analyze_efficiency.py`, `generate_figures.py`, `analysis/process_data.py`, `stat_tests.py`, `visualizations.py`
- Figures: 7 PDF + PNG di `paper/figures/` dan `experiment/figures/`

### Hook findings paper
- Tool-usage tidak korelasi success (Pearson r=0.077, p=0.575)
- 22×–53× variance di model perfect-score (completion time, tool calls, cost)
- 2 pola inefficiency: loop (Gemini-3 Flash 917 tool calls) + inference (Qwen3-VL slow tokens)
- Research task paling challenging (90.9% success), coding tasks 100%

### Placeholder/TODO yang BELUM dibereskan
- `06_conclusion.tex:53` — URL `https://github.com/[anonymous]/llm-challenge-experiment` masih placeholder
- `06_conclusion.tex:68` — "[anonymous funding sources]" di Acknowledgments
- `references.bib:106-111` — entry `our_dataset` masih "Anonymous Authors"
- **Duplikasi Acknowledgments**: ada di `main.tex:50-51` DAN `06_conclusion.tex:68` — perlu pilih salah satu

---

## 4. Memo Jurnal (Hasil Research Agent)

Lima kandidat dibandingkan, semua lolos 3 syarat (no APC wajib, Scopus, Q bebas). Semua hybrid publisher — subscription = gratis, Gold OA murni opsional. arXiv preprint aman di semua.

| Jurnal | Scopus Q | APC wajib | Avg first-decision | Fit |
|---|---|---|---|---|
| JSS (Elsevier) | Q1 | Tidak | ~3–5 bln (tidak resmi) | Kuat |
| IST (Elsevier) | Q1 | Tidak | ~217 hari (~7 bln) | Kuat |
| JSEP (Wiley) | Q2 | Tidak | 6–12 minggu | Sedang — scope miss |
| EMSE (Springer) | Q1 | Tidak | **24 hari** median | Sangat kuat |
| ASE-J (Springer) | Q2 | Tidak | **16 hari** median | Sangat kuat — scope 2025 eksplisit LLM |

### Rekomendasi agent
- **Pilih: ASE-J** — scope 2025 eksplisit panggil "generative AI & LLM-enabled approaches", median decision 16 hari tercepat, effort reformat manageable.
- **Runner-up: EMSE** — kalau mau Q1, siap review cycle lebih ketat (perlu beef up empirical rigor: power analysis, CI, replication package).
- **Skip: JSEP** — scope miss, Q2 tanpa kompensasi speed.
- **Hold: IST, JSS** — cadangan kalau reject.

### Risk flags
1. **Reformat effort common untuk semua 5**: IEEE two-column 10 hal → single-column journal template (~15–25 hal). Budget 1–2 minggu.
2. **EMSE risk**: Dengan N=11 dan r=0.077, framing harus kuat ke empirical rigor (effect size, CI, threats to validity, replication package di Zenodo/Figshare). Sekadar "leaderboard" → desk reject.

---

## 5. Keputusan yang BELUM Diambil

Mukhlis belum commit ke venue spesifik. Pilihan di atas meja:
- (a) Ambil rekomendasi agent: **ASE-J** sebagai primary target
- (b) Go Q1: **EMSE** dengan effort tambahan di empirical rigor
- (c) Opsi lain yang belum dipertimbangkan

---

## 6. Action Konkret Tersisa (Low-Effort, 1–2 Jam/Sesi)

Dari triage awal, masih relevan:

1. **De-anonymize + release dataset** (~1–2 jam, zero-regret apa pun venue-nya)
   - Bikin repo GitHub public: `results.json`, `efficiency_data.json`, `analysis/`, `generate_figures.py`
   - Update `06_conclusion.tex:53` dan `references.bib:106-111` dengan URL real + author names
   - Fix duplikasi Acknowledgments (`main.tex:50` vs `06_conclusion.tex:68`)
   - **Prerequisite untuk semua venue** — kalau ada, zero-regret
   - Pertimbangkan Zenodo DOI paralel dengan GitHub (untuk EMSE path, ini hampir wajib)

2. **Citation gap fill** (~1–2 jam, zero-regret)
   - Tambah 14 reference ke target 30 (FINAL_REPORT target)
   - Kandidat wajib: SWE-bench Verified, LiveCodeBench, ToolBench 2024/25, Anthropic Claude paper (jastifikasi absence), ICSE/FSE 2024–25 empirical LLM-SE studies
   - Edit hanya `references.bib` + beberapa sitasi di `02_related.tex` — tidak ubah argumen

3. **Reformat ke template venue** (~1–2 minggu, decision-locked)
   - Hanya start setelah venue dipilih
   - IEEE two-column → Springer SVJour3 (ASE-J/EMSE) atau elsarticle (JSS/IST) atau Wiley (JSEP)
   - Expand ke ~15–25 halaman single-column (terutama Related Work & Threats to Validity)

4. **(Kondisional, EMSE only) Beef up statistical rigor** (~3–5 jam)
   - Tambah effect size + CI + power analysis ke Results
   - Perkuat Threats to Validity dengan replication discussion
   - Skip kalau pilih ASE-J

---

## 7. File Referensi Penting

- Paper source: `paper/01_intro.tex`, `02_related.tex`, `03_methodology.tex`, `04_results.tex`, `05_discussion.tex`, `06_conclusion.tex`, `main.tex`
- Build terakhir: `paper/main_v2.pdf` (10 hal)
- References: `paper/references.bib`
- Data: `results.json`, `efficiency_data.json`
- Scripts: `analyze_*.py`, `generate_figures.py`, `analysis/*.py`
- Planning docs existing: `PAPER_PLAN.md`, `FINAL_REPORT.md`, `CONTINUATION.md`, `TASKS.md`, `REPORT.md`, `ANOMALY_ANALYSIS.md`, `EFFICIENCY_ANALYSIS.md`, `PROGRESS_REPORT.md`
- Sesi ini: tidak ada edit ke paper; semua temuan tercatat di sini

---

## 8. Preferensi Kolaborasi Mukhlis (Dari Sesi Ini)

- Bahasa: **Indonesia**
- Format: ringkas, punchy, tabel kalau bisa
- Decision style: minta rekomendasi + alasan, bukan menu panjang; siap revisi asumsi kalau salah (awal bilang "13 model" padahal data 11, diterima begitu saja saat aku koreksi)
- Scope discipline: eksplisit soal scope lock — jangan slip ke Zrb framework
