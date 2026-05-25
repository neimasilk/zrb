# Handoff — LLM Benchmark Paper Publication

**Tanggal update:** 2026-05-25
**Status:** Venue **dipilih: ASE-J** (Springer Q2). De-anonymize + citation
gap + dataset bundle + scaffold Springer + penguatan rigor empiris **selesai**.
Sisa: tugas yang butuh akun/aksi manual Mukhlis + ekspansi konten ke panjang
jurnal + submit.

---

## 1. Konteks & Scope Lock

**Paper:** "Comprehensive Evaluation of Large Language Models on Software
Engineering Tasks: A Multi-Task Benchmark"
**Authors:** Go Frendi Gunawan (first), Mukhlis Amien (second, corresponding —
UBHINUS Malang, `amien@ubhinus.ac.id`)
**arXiv:** v1 (arXiv:2602.07079), Feb 2026
**Working dir:** `D:\documents\zrb\llm-challenges\experiment\`
**Branch kerja:** `paper/ase-j-submission` (di-fork ke `neimasilk/zrb`)

**SCOPE LOCK:** hanya subtree `llm-challenges/experiment/`. JANGAN edit
`src/zrb/` / framework Zrb. JANGAN full-pull dari origin (623 commit framework,
tidak relevan & paper tidak ada di origin).

**Goal:** Submission low-effort ke ASE-J. Gratis (no-APC), Scopus, Q bebas.

---

## 2. Keputusan yang Sudah Diambil

- **Venue: ASE-J** (Automated Software Engineering, Springer, Q2). Median
  decision ~16 hari, scope 2025 eksplisit LLM-enabled SE.
- **Dataset host: repo GitHub baru** `github.com/neimasilk/llm-se-benchmark`
  (URL sudah ditulis permanen di paper).
- **Funding: tidak ada** ("no specific grant ...").

---

## 3. Yang SUDAH Dikerjakan (sesi 2026-05-25, branch `paper/ase-j-submission`)

| Commit | Isi |
|---|---|
| `a13574a5` | Checkpoint edit paper sesi lalu (+206/−68) + artefak sumber |
| `499c62d2` | De-anonymize semua placeholder; referensi **16 → 30** (14 baru, metadata diverifikasi web); fix duplikasi Acknowledgments |
| `cc8c1603` | Bundle dataset `release/` siap-push + `DATASET_RELEASE.md` |
| `6c841dcc` | Scaffold Springer `main_snj.tex` + `REFORMAT_ASE-J.md` |
| `cd675488` | Rigor: metrik jadi persamaan bernomor, Threats to Validity dikonsolidasi (4 kategori), 95% CI [−0.20,0.34] ke korelasi, model-selection table, affiliation UBHINUS |

**State paper:** IEEE build (`main.tex`) compile bersih, 10 hal, 0 undefined
citation, 30 ref. Semua placeholder anonim hilang. Tidak ada sisa "13 model".

---

## 4. Sisa Pekerjaan

### A. Butuh aksi Mukhlis (tidak bisa diotomatiskan)
1. ~~Buat repo `neimasilk/llm-se-benchmark` + push `release/`.~~ **SELESAI
   2026-05-25** — repo live di `github.com/neimasilk/llm-se-benchmark`
   (commit `e1b7fb7`, branch `main`). URL data-availability di paper resolve.
   (Opsional: Zenodo DOI untuk reproducibility lebih kuat.)
2. **Ambil `sn-jnl.cls`** (Overleaf/Springer, gratis) → `paper/`, compile
   `main_snj.tex`. Isi yang TODO: department UBHINUS, afiliasi Go Frendi, ORCID.
   Detail: `REFORMAT_ASE-J.md`.

### B. Bisa lanjut (ekspansi konten — opsional, judgment call)
3. **Ekspansi ke 15–25 hal single-column.** CATATAN: paper sekarang padat &
   konsisten; ASE-J tidak mewajibkan 25 hal. Ekspansi sebaiknya substantif
   (perdalam Related Work, narasi figure, harness detail) — hindari padding.
4. Konversi `figure*` → `figure` di `04_results.tex` (opsional; `figure*` tetap
   compile di single-column, jadi tidak wajib).

### C. Submit
5. Editorial Manager ASE (https://www.editorialmanager.com/ause/). Cover letter
   draft siap di `COVER_LETTER_ASE-J.md`. Deklarasi arXiv preprint.

---

## 5. File Penting

- Paper source: `paper/01..06_*.tex`, `paper/main.tex` (IEEE), `paper/main_snj.tex` (Springer)
- Referensi: `paper/references.bib` (30 entry)
- Data/scripts: `results.json` (55 run), `efficiency_data.json`, `analyze_*.py`,
  `generate_figures.py`, `analysis/*`, `compute_ci.py`
- Rilis: `release/` (siap-push)
- Panduan: `DATASET_RELEASE.md`, `REFORMAT_ASE-J.md`, `COVER_LETTER_ASE-J.md`

---

## 6. Data Inti (verified dari `results.json`)

11 model × 5 task = 55 run. Pass rate 98.2% (54/55). Korelasi tool-usage vs
score: r=0.077, 95% CI [−0.20, 0.34], n=54 (lihat `compute_ci.py`). Variance
antar perfect-scorer: 22× waktu, 49× tool, 53× cost. Anomali: Gemini-3 Flash
917 tool calls; Qwen3-VL inference lambat; Kimi-K2.5 gagal (malformed tool call).

---

## 7. Preferensi Kolaborasi Mukhlis

Bahasa Indonesia, ringkas, tabel kalau bisa. Minta rekomendasi + alasan.
Disiplin scope-lock. Suka mode otonom: kerjakan sebisanya, sisakan yang butuh
dia dengan instruksi jelas.
