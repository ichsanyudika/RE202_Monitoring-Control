# 📡 Monitoring & Control GUI Robot Wireless

Proyek ini merupakan tugas dari mata kuliah RE-202 Pemrograman Berorientasi Objek (OOP) yang bertujuan membangun sistem monitoring dan kontrol robot berbasis GUI menggunakan Python (Tkinter) yang terhubung secara wireless dengan mikrokontroler. GUI ini dapat mengontrol kecepatan motor, sudut servo, arah gerak robot, serta memonitor status sensor garis secara real-time.

## 🛠️ Fitur Utama

- Kontrol kecepatan motor (motor kiri dan kanan) dan sudut servo secara wireless dari GUI Python

- Kendali arah robot: Maju, Mundur, Belok Kiri, Belok Kanan, dan Stop

- Monitoring status sensor garis (line sensor) secara real-time melalui GUI dengan indikator progress bar

- Komunikasi dua arah antara Python dan ESP32 via jaringan WiFi

- Sistem command serial berbasis protokol sederhana (misal: M:<nilai> untuk motor, S:<nilai> untuk servo)

- GUI responsif menggunakan Tkinter dengan thread terpisah untuk komunikasi agar tidak blocking

- Pengaturan parameter kontrol dan monitoring secara intuitif dan mudah digunakan

- Penggunaan WiFiManager (ESP32 version) untuk konfigurasi jaringan WiFi secara mudah tanpa perlu hardcode SSID dan password

## ⚙️ Komponen yang Digunakan

### Hardware

- ESP32 Dev Board sebagai mikrokontroler utama

- Motor DC (2 buah)

- Driver motor (misal L298N)

- Servo SG90 untuk kontrol sudut

- Sensor garis (5 channel digital)

- Modul WiFi internal ESP32 untuk komunikasi wireless

- Power supply sesuai kebutuhan robot

### Software

- Python 3.x

- Tkinter (GUI Python built-in)

- Modul socket Python untuk komunikasi TCP/IP

- Modul threading Python untuk concurrency

- Arduino IDE dengan library ESP32 dan WiFiManager for ESP32

- ESP32 program menangani parsing perintah kontrol motor dan servo serta pembacaan sensor

## 📋 Penjelasan Kode

- ESP32 Firmware (Server TCP/IP + WiFiManager) Menggunakan WiFiManager library versi ESP32 untuk konfigurasi WiFi secara mudah:

- Saat pertama kali dijalankan atau gagal koneksi WiFi, ESP32 membuat access point (AP) sendiri dengan portal captive untuk memasukkan SSID & password WiFi.

- Setelah konfigurasi selesai, ESP32 otomatis terhubung ke jaringan WiFi yang dipilih tanpa perlu upload ulang firmware.

- Membuat server TCP/IP socket di port 80

- Menerima koneksi dari client (GUI Python)

- Menerima perintah dalam format string, misal: M:<nilai> untuk mengatur kecepatan motor (nilai 0-255), S:<nilai> untuk mengatur sudut servo (nilai 0-180)

- Membaca status sensor garis secara berkala dan mengirim data sensor kembali ke client

- Mengontrol motor dan servo berdasarkan perintah yang diterima

- Menangani multiple koneksi dan komunikasi non-blocking sederhana

### Python GUI Client (Tkinter)

- Membuat jendela GUI dengan slider untuk motor kiri dan kanan, slider servo, dan tombol arah

- Menampilkan status sensor garis dalam progress bar (5 sensor)

- Membuat thread terpisah untuk koneksi socket TCP/IP ke ESP32

- Mengirim perintah sesuai interaksi pengguna ke ESP32 secara real-time

- Menerima data sensor garis dan memperbarui GUI secara berkala tanpa freeze GUI

- Menangani reconnect dan error koneksi

## 🪟 Tampilan GUI

![](asset/gui.png)  

## 🧑‍💻 Tim Pengembang

- Ichsan Fajar Yudika (4222401042)
- Wildan Mahfudh Khoirul Murtadho (4222401046)
- M. Rasyid Prasetyo (4222411048)
- Moh. Abdul Hikmal (4222401032)


