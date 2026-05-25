# Prompt Kickoff Sesi Berikutnya

Besok, di sesi baru, **copy-paste blok di bawah ini** sebagai pesan pertama
(atau cukup tunjuk file ini dan bilang "lanjut").

---

```
Halo, saya Mukhlis Amien (second author). Lanjutkan publikasi paper benchmark LLM.

BACA DULU: D:\documents\zrb\llm-challenges\experiment\HANDOFF.md
— itu berisi status lengkap, keputusan terkunci, dan sisa pekerjaan.

Aturan:
- Scope-lock: HANYA sentuh subtree llm-challenges/experiment/. JANGAN edit
  framework Zrb di src/. JANGAN full-pull dari origin.
- Kerja di branch paper/ase-j-submission (ter-backup di fork neimasilk/zrb).
- Bahasa Indonesia, ringkas. Mode otonom: kerjakan sebisanya, sisakan yang
  butuh saya dengan instruksi jelas. JANGAN submit/aksi tak-bisa-dibatalkan
  tanpa konfirmasi saya.

Konteks singkat: paper PRAKTIS SIAP SUBMIT ke ASE-J (Springer Q2, GRATIS).
Build Springer paper/main_snj.tex compile bersih 24 hal. Dataset sudah live di
github.com/neimasilk/llm-se-benchmark. Portal submit: submission.nature.com.

Tanya saya dulu mau lanjut ke yang mana sebelum eksekusi:
(a) gabungkan section jadi satu main_flat.tex untuk submission single-file,
(b) tambah ORCID + department di main_snj.tex,
(c) bantu proses upload/submit (saya yang login & pencet kirim),
(d) hal lain.
```

---

## Catatan untuk diri-sendiri (Mukhlis)

- Semua sudah ter-commit & ter-push. Tidak ada kerja yang hilang.
- Kalau Claude sesi baru "lupa" konteks: tunjuk `HANDOFF.md`, itu sumber kebenaran.
- Langkah terakhir yang HANYA bisa Anda lakukan: **login ke
  `submission.nature.com/new-submission/10515/3` dan submit** (review final +
  setujui deklarasi etika dulu).
- Bahan submit: `paper/main_snj.tex` + `references.bib` + `figures/` + `main_snj.bbl`
  (atau minta Claude gabungkan jadi satu `.tex`). Cover letter: `COVER_LETTER_ASE-J.md`.
- Template Springer (`sn-jnl.cls` dkk) di-gitignore — kalau pindah mesin,
  download ulang dari springernature.com/.../latex-author-support.
