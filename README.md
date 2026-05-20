# Car : Mini Game

Game mobil arcade sederhana berbasis Python + Pygame. Pemain menghindari kendaraan dan rintangan di jalan 5 jalur, sambil melewati siklus siang-malam, lampu jalan, efek senter, jumpscare hantu, dan tampilan menu/game over bernuansa retro.

## Fitur Game

- Jalan 5 jalur dengan obstacle acak.
- Musuh berupa mobil, cone, truck, bus, van, compact car, dan hantu saat malam.
- Mobil musuh tertentu bisa berpindah jalur.
- Siklus siang dan malam.
- Efek senter mobil saat malam.
- Lampu pinggir jalan yang membuka area gelap seperti penglihatan siang.
- Hantu tidak langsung game over, tetapi menghalangi pandangan dengan jumpscare singkat.
- UI start screen dan game over bergaya retro arcade.
- High score dan score saat game over.
- Sound effect untuk move, crash, score, jumpscare, restart, dan game over.

## Cara Memainkan

Kontrol saat bermain:

| Tombol | Fungsi |
| --- | --- |
| `A` atau `LEFT` | Pindah ke jalur kiri |
| `D` atau `RIGHT` | Pindah ke jalur kanan |
| `SPACE` di menu awal | Mulai game |
| `R` saat game over | Langsung mulai ulang |
| `SPACE` saat game over | Kembali ke menu awal |

Tujuan game adalah bertahan selama mungkin dan menghindari obstacle. Score bertambah selama game berjalan.

## Cara Menjalankan dari GitHub

1. Clone repository:

   ```bash
   git clone <url-repository-github>
   cd game_car
   ```

2. Pastikan Python sudah terpasang. Disarankan memakai Python 3.10 atau lebih baru.

3. Install dependency:

   ```bash
   pip install pygame
   ```

4. Jalankan game:

   ```bash
   python main.py
   ```

## Struktur File Penting

| File | Keterangan |
| --- | --- |
| `main.py` | Source code utama game |
| `move.wav` | SFX pindah jalur |
| `crash.wav` | SFX tabrakan |
| `score.wav` | SFX milestone score |
| `jumpscare.wav` | SFX saat terkena hantu |
| `cihuy.wav` | SFX restart dengan tombol `R` |
| `gameover.wav` | SFX game over |
| `image_0.png` | Asset opsional untuk mobil pemain |

Jika `image_0.png` tidak ada, game otomatis membuat mobil pemain dari bentuk Pygame sederhana.

## Informasi Asset

### Visual

Sebagian besar asset visual dibuat langsung di dalam `main.py` menggunakan primitive Pygame, seperti:

- mobil pemain fallback,
- mobil obstacle,
- truck, bus, van, compact car,
- cone,
- hantu,
- pohon oak, pohon pine, bush,
- lampu pinggir jalan,
- efek jumpscare,
- overlay malam, senter, scanline, dan UI retro.

Asset gambar eksternal yang didukung:

- `image_0.png`: gambar mobil pemain. File ini opsional dan akan di-scale otomatis mengikuti ukuran jalur.

### Audio

Asset audio yang dipakai game:

- `move.wav`: SFX move retro.
- `jumpscare.wav`: SFX jumpscare retro.
- `gameover.wav`: menggunakan SFX **Game Over Sound (Old School)** dari OpenGameArt, lisensi CC0.
  Source: https://opengameart.org/content/game-over-soundold-school
- `crash.wav`, `score.wav`, dan `cihuy.wav`: asset audio lokal di folder project.

Catatan: jika salah satu file audio tidak ada, game tetap berjalan karena loader SFX akan mengembalikan `None` dan suara tersebut tidak diputar.

## Spesifikasi Teknis

| Item | Detail |
| --- | --- |
| Bahasa | Python |
| Library utama | Pygame |
| Resolusi window | 480 x 640 |
| FPS target | 60 FPS |
| Jumlah jalur | 5 |
| Mode tampilan | Windowed |
| Audio | Pygame mixer |

## Gameplay State

Game memiliki beberapa state utama:

- `START`: tampilan awal retro arcade.
- `PLAYING`: gameplay utama.
- `GAMEOVER`: tampilan akhir dengan score, tombol restart, dan menu.
- `JUMPSCARE`: state lama masih ada di kode, tetapi hantu saat ini memakai overlay jumpscare sementara tanpa mengakhiri game.

## Catatan Pengembangan

- Semua konfigurasi utama ada di `main.py`.
- Ukuran mobil menyesuaikan lebar jalur.
- Obstacle dibuat secara acak dengan bobot tertentu.
- Saat malam, hantu lebih sering muncul.
- Difficulty meningkat perlahan melalui `scroll_speed` dan `obstacle_frequency`.

