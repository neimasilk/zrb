# Reformat ke Template ASE-J (Springer "Automated Software Engineering")

Status venue: **dipilih ASE-J** (Springer, Q2). Gratis (subscription, no APC
wajib), Scopus, terima arXiv preprint. Median first-decision ~16 hari, scope
2025 eksplisit memanggil "generative AI & LLM-enabled approaches".

Konten paper **single-source**: section `01_intro..06_conclusion.tex` dipakai
oleh build IEEE (`main.tex`) maupun Springer (`main_snj.tex`). Reformat =
mengganti wrapper + ekspansi isi, bukan rewrite.

---

> **UPDATE 2026-05-25:** Template Springer Nature **versi Desember 2024**
> sudah diunduh & dipasang lokal di `paper/` (`sn-jnl.cls` + `sn-mathphys-num.bst`
> dkk). **`main_snj.tex` sudah compile bersih: 24 halaman, 0 error, 0 undefined
> citation.** File template di-gitignore (jangan redistribusi file Springer).
> Build: `pdflatex main_snj && bibtex main_snj && pdflatex main_snj x2`.
> Jadi langkah 1–3 di bawah sebagian besar SUDAH selesai; sisanya kosmetik +
> single-file untuk submission (lihat §6a).

## 1. Dapatkan template Springer Nature (prasyarat, ~10 menit) — SUDAH DILAKUKAN

`sn-jnl.cls` + file `.bst` TIDAK ada di repo (lisensi Springer). Ambil dari:
- https://www.springernature.com/gp/authors/campaigns/latex-author-support, atau
- Overleaf: cari template **"Springer Nature LaTeX Template"** (paling mudah —
  langsung bisa compile).

Taruh `sn-jnl.cls` dan `sn-mathphys-num.bst` di folder `paper/`, lalu:
```
pdflatex main_snj
bibtex   main_snj
pdflatex main_snj
pdflatex main_snj
```
`main_snj.tex` sudah saya siapkan (title block, abstract, keywords,
declarations, data-availability) — tinggal isi affiliation.

---

## 2. Isi yang masih TODO di `main_snj.tex`

- [ ] **Affiliation** kedua author (ditandai `[... TODO]`). Wajib untuk ASE-J:
      nama institusi legal lengkap (UBHINUS = ?), departemen, kota, negara.
      Go Frendi: konfirmasi afiliasi (State Alchemists / independen?).
- [ ] **Corresponding author** sudah di-set ke Mukhlis (`\author*`). Ubah jika
      perlu.
- [ ] **ORCID** (opsional tapi disukai): tambah `\orcid{...}` per author.

---

## 3. Konversi layout IEEE two-column → Springer single-column

Yang perlu diubah di `04_results.tex` (semua figure ada di sini):

| Lokasi | IEEE | Springer single-column |
|---|---|---|
| `04_results.tex:45,57,140` | `\begin{figure*}` (span 2 kolom) | ganti ke `\begin{figure}` |
| width figure* | `0.75\textwidth` | `\linewidth` (atau `0.8\linewidth`) |
| `04_results.tex:159,173,234,251` | `\includegraphics[width=\columnwidth]` | ganti `\columnwidth` → `\linewidth` |
| Tabel `[htbp]` | OK apa adanya | OK |

> Catatan: `figure*` secara teknis tetap compile di single-column (jadi
> full-width), tapi konversi eksplisit lebih rapi dan menghindari warning float.

**Saran:** lakukan konversi ini di section files HANYA jika sudah yakin tidak
balik ke build IEEE. Kalau mau pertahankan dua build paralel, gunakan makro
kondisional atau copy `04_results.tex` ke `04_results_snj.tex`.

---

## 4. Ekspansi konten — TERNYATA TIDAK PERLU

> **UPDATE:** Setelah reformat ke single-column Springer, `main_snj.tex`
> **sudah 24 halaman** — pas di rentang target 15–25 hal **tanpa padding**.
> Jadi ekspansi besar TIDAK diperlukan. Konten cukup. Kalau reviewer minta
> elaborasi spesifik nanti, prioritas (tanpa data baru) di bawah ini.

Prioritas elaborasi opsional (kalau diminta reviewer):

1. **Related Work** — perdalam tiap subsection; sekarang sudah 30 ref (cukup).
   Tambah paragraf posisi vs SWE-bench Verified, LiveCodeBench, agentic eval.
2. **Methodology** — detailkan verification harness per task, definisi metrik
   (TER, time-efficiency, cost model) dengan rumus eksplisit + contoh.
3. **Results** — narasikan tiap figure lebih panjang; tambah analisis
   per-provider dan per-task.
4. **Threats to Validity** — sudah ada kerangka; perluas (internal/external/
   construct/conclusion validity) — penting untuk reviewer empiris.
5. **Discussion** — implikasi praktis + "model selection framework" jadi
   subsection tersendiri.

---

## 5. Catatan empiris (N=11, N=1 per sel)

ASE-J lebih toleran ke studi observasional dibanding EMSE, TAPI reviewer tetap
akan menyoroti **N=1 per model-task** dan **r=0.077 (n kecil)**. Mitigasi murah:
- Bingkai sebagai *exploratory/characterization study*, bukan klaim kausal.
- Laporkan correlation dengan CI + caveat eksplisit di Results.
- Tegaskan replication package (repo `llm-se-benchmark`) di Data Availability —
  sudah saya taruh di `main_snj.tex`.

(Kalau mau, upgrade opsional: tambah effect size + CI di `04_results.tex` —
~3–5 jam. Tidak wajib untuk ASE-J.)

---

## 6. Submission ASE-J (saat siap)

- Portal: Springer Nature submission system — https://submission.nature.com/new-submission/10515/3
  (ASE-J kini pakai ini, BUKAN Editorial Manager). Konfirmasi resmi: jurnal
  **"does not charge a submission fee or publication fee"** (gratis).
- Cek "Submission Guidelines" untuk: struktur, declarations (sudah disiapkan),
  format referensi (sn-mathphys-num OK).
- Cover letter: sebut novelty (efficiency-first, 22–53× variance, no
  tool-success correlation) + relevansi scope LLM-enabled SE.
- Deklarasikan arXiv preprint (arXiv:2602.07079) — diizinkan Springer.

---

## 6a. Submission butuh SATU file .tex (catatan Springer)

Springer menyarankan submit **satu file `.tex`** (jangan `\input`). `main_snj.tex`
sekarang pakai `\input{01_intro}` dkk untuk preview. Sebelum submit, gabung jadi
satu file: salin isi tiap `0X_*.tex` menggantikan baris `\input{...}` (atau pakai
`latexpand main_snj.tex > main_flat.tex` kalau punya perl). Portal Springer
Nature umumnya juga menerima upload zip berisi `.tex` + `.bib` + figures + `.bbl`.

## Ringkasan status

- [x] De-anonymize (URL, funding, dataset author) — selesai
- [x] Referensi 16 → 30 — selesai
- [x] Bundle dataset (`release/`) + push ke GitHub — **selesai & live**
- [x] Wrapper Springer `main_snj.tex` — selesai
- [x] **Template sn-jnl.cls (Des 2024) terpasang; build 24 hal, 0 error** — selesai
- [x] Affiliation UBHINUS (kedua author) — selesai
- [x] Ekspansi konten — tidak perlu (sudah 24 hal)
- [ ] (opsional) ORCID + department di `main_snj.tex`
- [ ] (opsional) Konversi `figure*` → `figure` (kosmetik; sudah compile)
- [ ] Gabung jadi satu `.tex` untuk submission (§6a)
- [ ] Submit via portal Springer Nature (login + review final oleh Mukhlis)
