# Cara publish dataset ke github.com/neimasilk/llm-se-benchmark

Folder `release/` sudah siap-push (data + scripts + README + LICENSE).
URL ini sudah ditulis permanen di paper (`06_conclusion.tex`, `references.bib`),
jadi nama repo harus persis **`llm-se-benchmark`** di akun **`neimasilk`**.

## Langkah (sekali jalan)

1. Buat repo kosong **public** di GitHub: `neimasilk/llm-se-benchmark`
   (jangan centang "Add README" — sudah ada di `release/`).

2. Dari folder ini, push isi `release/`:

   ```powershell
   cd D:\documents\zrb\llm-challenges\experiment\release
   git init
   git add .
   git commit -m "Initial release: LLM SE benchmark dataset and analysis"
   git branch -M main
   git remote add origin https://github.com/neimasilk/llm-se-benchmark.git
   git push -u origin main
   ```

3. (Opsional, untuk path Q1/EMSE) buat arsip ber-DOI:
   - Zenodo > New Upload, hubungkan ke repo GitHub, terbitkan rilis `v1.0`.
   - Tambahkan DOI badge ke README dan sitasi DOI di paper jika perlu.

## Verifikasi reprodusibilitas (sebelum push)

```powershell
cd release
pip install matplotlib seaborn numpy scipy pandas
python analyze_efficiency.py   # harus regenerate efficiency_data.json tanpa error
python generate_figures.py     # harus hasilkan figures/*.pdf
```

> Catatan: `release/` adalah salinan rilis. File sumber kanonik tetap di
> `llm-challenges/experiment/`. Kalau data/skrip di-update, jalankan ulang
> penyalinan atau edit langsung di `release/` sebelum push.
