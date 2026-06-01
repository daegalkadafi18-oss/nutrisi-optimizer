# 🥗 NutriOpt — Simulasi Optimasi Menu Makanan Harian

Aplikasi web berbasis Flask untuk simulasi optimasi penyusunan menu makanan harian menggunakan algoritma Hill Climbing, Simulated Annealing, dan Genetic Algorithm.

## 📋 Deskripsi

NutriOpt mengoptimasi kombinasi menu harian (sarapan, snack pagi, makan siang, snack sore, makan malam) agar memenuhi kebutuhan nutrisi pengguna berdasarkan profil BMR/TDEE Harris-Benedict, dengan batasan anggaran harian.

**Mata Kuliah:** Kecerdasan Buatan  
**Topik:** Pencarian Lokal dan Optimasi

## 🧠 Algoritma yang Diimplementasikan

| Algoritma | Varian | Keterangan |
|-----------|--------|------------|
| Hill Climbing | Simple, Steepest Ascent, Stochastic | Pencarian lokal deterministik |
| Simulated Annealing | — | Penerimaan solusi buruk via prob. Boltzmann |
| Genetic Algorithm | Tournament + BLX-α + Gaussian Mutation | Evolusi populasi dengan elitisme |

## 🚀 Cara Instalasi & Menjalankan

```bash
# Clone repository
git clone https://github.com/username/nutrisi-optimizer.git
cd nutrisi-optimizer

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
python app.py
```

Buka browser: `http://localhost:5000`

## 📁 Struktur Folder

```
nutrisi-optimizer/
├── app.py              # Flask backend + algoritma optimasi
├── requirements.txt    # Dependencies
├── templates/
│   └── index.html      # Frontend (HTML + JS + Chart.js)
└── README.md
```

## 🎯 Fungsi Fitness

```
fitness = Σ -|nutrisi_aktual[k] - target[k]| / target[k] × 100
          - penalti_budget
          + bonus_variasi × 10
```

## 🌐 Demo

[Link demo setelah deployment]

## 📚 Referensi

- Russell, S. & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach*, 4th Ed.
- Goldberg, D. E. (1989). *Genetic Algorithms in Search, Optimization, and Machine Learning*.
- Kirkpatrick, S. et al. (1983). Optimization by Simulated Annealing. *Science*.
- Harris, J. & Benedict, F. (1918). Biometric Study of Basal Metabolism.
