# Handoff — LLM Benchmark Paper Publication

**Update terakhir:** 2026-05-25
**Status singkat:** Paper **praktis siap submit** ke ASE-J. Semua polish, rigor,
dataset publik, dan build Springer (24 hal, compile bersih) sudah beres. Yang
tersisa hanya aksi yang butuh login/keputusan Mukhlis (submit) + beberapa item
opsional kecil.

---

## 1. Konteks & Scope Lock

**Paper:** "Comprehensive Evaluation of Large Language Models on Software
Engineering Tasks: A Multi-Task Benchmark"
**Authors:** Go Frendi Gunawan & Mukhlis Amien — **keduanya UBHINUS**
(Universitas Bhinneka Nusantara, Malang). Corresponding: Mukhlis
(`amien@ubhinus.ac.id`). GitHub Mukhlis: `neimasilk`.
**arXiv:** v1 (arXiv:2602.07079), Feb 2026.
**Working dir:** `D:\documents\zrb\llm-challenges\experiment\`
**Branch kerja:** `paper/ase-j-submission` (ter-backup di fork `neimasilk/zrb`).

**SCOPE-LOCK:** hanya subtree `llm-challenges/experiment/`. JANGAN edit `src/zrb/`
/ framework Zrb. JANGAN full-pull dari `origin` (623 commit framework, paper tidak
ada di sana; paper murni lokal + di fork).

**Goal:** submission low-effort. Gratis (no-APC), Scopus, Q bebas.

---

## 2. Keputusan Terkunci

| Aspek | Nilai |
|---|---|
| Venue | **ASE-J** (Automated Software Engineering, Springer, Q2) |
| Biaya | **GRATIS** — verified resmi: jurnal "does not charge a submission fee or publication fee" |
| Portal submit | **`https://submission.nature.com/new-submission/10515/3`** (Springer Nature; BUKAN Editorial Manager) |
| Dataset repo | **`github.com/neimasilk/llm-se-benchmark`** (live) |
| Funding | tidak ada |
| Open access | opsional (Open Choice berbayar) — default subscription = gratis |

---

## 3. Status File Paper

- **Dua build, satu sumber konten** (section `01..06_*.tex` dipakai keduanya):
  - `paper/main.tex` — IEEE two-column, 10 hal (untuk arXiv). Compile bersih.
  - `paper/main_snj.tex` — **Springer sn-jnl, 24 hal**. Compile bersih, 0 error,
    0 undefined citation. Target submission ASE-J.
- **Referensi:** `paper/references.bib`, **30 entry**, semua tersitasi & metadata
  diverifikasi.
- **Template Springer:** `sn-jnl.cls` + `sn-mathphys-num.bst` dkk (versi Des 2024)
  terpasang lokal di `paper/` tapi **gitignored** (hak cipta Springer). Untuk
  rebuild di mesin lain: download ulang dari
  springernature.com/gp/authors/campaigns/latex-author-support.
- **Build Springer:** `cd paper && pdflatex main_snj && bibtex main_snj &&
  pdflatex main_snj && pdflatex main_snj`.
- Placeholder anonim: **nihil**. Konsistensi angka: **bersih** (tidak ada sisa
  "13 model", dll).

---

## 4. Yang SUDAH Dikerjakan (branch `paper/ase-j-submission`, 9 commit)

1. `a13574a5` Checkpoint edit paper sesi lalu (+206/−68) + artefak sumber.
2. `499c62d2` De-anonymize placeholder; referensi **16 → 30**; fix Acknowledgments dobel.
3. `cc8c1603` Bundle dataset `release/` + `DATASET_RELEASE.md`.
4. `6c841dcc` Scaffold Springer `main_snj.tex` + `REFORMAT_ASE-J.md`.
5. `cd675488` Rigor: persamaan metrik bernomor, Threats to Validity dikonsolidasi
   (4 kategori), **95% CI [−0.20, 0.34] dari data**, model-selection table.
6. `7e5037c0` Cover letter ASE-J + handoff.
7. `16526908` Tandai dataset repo published.
8. `29c09041` **Build Springer jalan (24 hal)** dengan template resmi Des 2024;
   affiliation UBHINUS kedua author.
9. `76115b5c` Koreksi portal (submission.nature.com) + konfirmasi gratis.

**Dataset repo** `neimasilk/llm-se-benchmark` sudah live (commit `e1b7fb7`, main).
**Branch** sudah di fork `neimasilk/zrb`.

---

## 5. Sisa Pekerjaan

### Wajib (butuh Mukhlis — tidak bisa diotomatiskan)
- **Submit** di `https://submission.nature.com/new-submission/10515/3`: login,
  upload manuskrip, tempel cover letter (`COVER_LETTER_ASE-J.md`), setujui
  deklarasi etika/authorship, kirim. Aksi tak bisa dibatalkan → review final dulu.

### Opsional / kecil
- Gabung section jadi **satu `main_flat.tex`** (Springer sarankan single-file).
  Portal biasanya juga terima zip multi-file. (Bisa diminta ke Claude.)
- Tambah `\orcid{...}` + `\orgdiv{department}` di `main_snj.tex`.
- Konversi `figure*` → `figure` di `04_results.tex` (kosmetik; sudah compile).
- (Opsional) Zenodo DOI untuk dataset (reproducibility lebih kuat).

---

## 6. Panduan & File Penting

- `REFORMAT_ASE-J.md` — checklist reformat + submit (sudah update: template done).
- `COVER_LETTER_ASE-J.md` — draft cover letter (portal sudah benar).
- `DATASET_RELEASE.md` — cara publish dataset (sudah dilakukan).
- Source: `paper/01..06_*.tex`, `paper/main.tex`, `paper/main_snj.tex`, `paper/references.bib`.
- Data/scripts: `results.json` (55 run), `efficiency_data.json`, `analyze_*.py`,
  `generate_figures.py`, `analysis/*`, `compute_ci.py`.
- Rilis publik: `release/` (mirror repo `llm-se-benchmark`).

---

## 7. Data Inti (verified dari `results.json`)

11 model × 5 task = 55 run. Pass rate 98.2% (54/55). Korelasi tool-usage vs score:
r=0.077, 95% CI [−0.20, 0.34], n=54 (`compute_ci.py`). Variance antar
perfect-scorer: 22× waktu, 49× tool, 53× cost. Anomali: Gemini-3 Flash 917 tool
calls; Qwen3-VL inference lambat; Kimi-K2.5 gagal (malformed tool call).

---

## 8. Preferensi Kolaborasi Mukhlis

Bahasa Indonesia, ringkas, tabel kalau bisa. Minta rekomendasi + alasan. Disiplin
scope-lock. Suka **mode otonom**: kerjakan sebisanya, sisakan yang butuh dia
dengan instruksi jelas. Jangan submit/aksi tak-bisa-dibatalkan tanpa konfirmasi.
