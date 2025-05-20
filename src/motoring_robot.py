import tkinter as tk
from tkinter import ttk, messagebox
import serial

class MonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Monitor")
        self.root.geometry("900x480")
        self.root.configure(bg="#E8EEF5")

        self.judul = ["Motor Speed", "Servo Angle"]
        self.entries = []
        self.sensor_labels = []
        self.sensor_bars = []

        # Status Navigasi
        self.status_var = tk.StringVar()
        self.status_var.set("Status: Diam")
        self.status_label = tk.Label(self.root, textvariable=self.status_var, font=("Segoe UI", 12, "bold"), fg="#0078D7", bg="#E8EEF5")
        self.status_label.pack(pady=(0, 10))

        # Untuk tracking gerak lingkaran
        self.moving_direction = None  # None, "up", "down", "left", "right"
        self.move_speed = 20          # Jarak per langkah (akan diatur sesuai PWM)
        self.move_interval = 100      # ms, interval update gerak (bisa juga diatur sesuai PWM)

        # Buat style untuk 5 progress bar sensor
        self.pb_styles = []
        for i in range(5):
            style = ttk.Style()
            style_name = f"SensorPB{i}.Horizontal.TProgressbar"
            style.theme_use('default')
            style.configure(style_name, troughcolor="#D3D3D3", background="#D3D3D3")
            self.pb_styles.append(style_name)

        # Inisialisasi koneksi serial ke COM5
        try:
            self.serial_conn = serial.Serial('COM5', 115200, timeout=1)
        except serial.SerialException as e:
            messagebox.showerror("Error", f"Tidak bisa membuka port COM5.\n{e}")
            self.serial_conn = None

        # Judul utama GUI
        tk.Label(self.root, text="SISTEM MONITOR", font=("Segoe UI", 18, "bold"),
                 fg="#0078D7", bg="#E8EEF5").pack(pady=20)

        # Buat layout kiri dan kanan
        main_frame = tk.Frame(self.root, bg="#E8EEF5")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        main_frame.columnconfigure(0, weight=1, uniform='a')
        main_frame.columnconfigure(1, weight=1, uniform='a')
        main_frame.rowconfigure(0, weight=1)

        self.left_frame = tk.Frame(main_frame, bg="#E8EEF5")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0,15))
        self.right_frame = tk.Frame(main_frame, bg="#E8EEF5")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(15,0))

        separator = ttk.Separator(main_frame, orient='vertical')
        separator.place(relx=0.5, rely=0, relheight=1)

        # Panggil fungsi untuk bagian kiri dan kanan
        self.create_left_side()
        self.create_right_side()
        self.read_serial_loop()

    def __del__(self):
        # Tutup koneksi serial saat objek dihancurkan
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()

    def create_left_side(self):
        # Input manual Motor dan Servo
        input_frame = tk.LabelFrame(self.left_frame, text="Kontrol Motor & Servo", 
                                   font=("Segoe UI", 14, "bold"), fg="#0078D7", bg="#E8EEF5", padx=15, pady=15)
        input_frame.pack(fill="x")

        for i, label_text in enumerate(self.judul):
            lbl = tk.Label(input_frame, text=f"{label_text}", font=("Segoe UI", 13), bg="#E8EEF5")
            lbl.grid(row=i, column=0, sticky="w", pady=8, padx=(0,10))

            entry = tk.Entry(input_frame, font=("Segoe UI", 12), width=12, relief="groove", bd=2)
            entry.grid(row=i, column=1, pady=8, padx=(0,10))
            self.entries.append(entry)

            # Tombol OK untuk kirim nilai
            btn = tk.Button(input_frame, text="OK", font=("Segoe UI", 11, "bold"),
                            bg="#0078D7", fg="white", width=5,
                            command=lambda e=entry, l=label_text: self.submit(e, l))
            btn.grid(row=i, column=2, pady=8)

        # =Kontrol arah robot (panah dan STOP)
        control_frame = tk.LabelFrame(self.left_frame, text="Kontrol Arah", 
                                      font=("Segoe UI", 14, "bold"), fg="#0078D7", bg="#E8EEF5", padx=15, pady=15)
        control_frame.pack(pady=20, fill="both", expand=True)

        btn_opts = {"width": 5, "height": 2, "bg": "#0078D7", "fg": "white", "font": ("Segoe UI", 14, "bold"), "relief": "raised"}

        btn_frame = tk.Frame(control_frame, bg="#E8EEF5")
        btn_frame.pack()

        tk.Button(btn_frame, text="↑", command=self.move_forward, **btn_opts).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(btn_frame, text="←", command=self.turn_left, **btn_opts).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(btn_frame, text="↓", command=self.move_backward, **btn_opts).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(btn_frame, text="→", command=self.turn_right, **btn_opts).grid(row=1, column=2, padx=10, pady=5)
        tk.Button(btn_frame, text="STOP", command=self.stop_motor, **btn_opts).grid(row=2, column=1, pady=10)

    def create_right_side(self):
        # Frame sensor garis (dengan 5 progress bar)
        sensor_frame = tk.LabelFrame(self.right_frame, text="Sensor Garis", 
                                     font=("Segoe UI", 14, "bold"), fg="#0078D7", bg="#E8EEF5", padx=20, pady=15)
        sensor_frame.pack(fill="both", expand=True, pady=10)

        for i in range(5):
            row_frame = tk.Frame(sensor_frame, bg="#E8EEF5")
            row_frame.pack(fill="x", pady=6, padx=10)

            sensor_label = tk.Label(row_frame, text=f"Sensor {i+1}: -",
                                    font=("Segoe UI", 13), fg="#333", bg="#E8EEF5", anchor="w", width=15)
            sensor_label.pack(side="left")
            self.sensor_labels.append(sensor_label)

            bar = ttk.Progressbar(row_frame, orient="horizontal", length=120, mode="determinate", maximum=1, style=self.pb_styles[i])
            bar.pack(side="left", padx=10)
            bar["value"] = 0
            self.sensor_bars.append(bar)

        # Tracking Canvas
        tracking_frame = tk.LabelFrame(self.right_frame, text="Tracking Navigasi", 
                                      font=("Segoe UI", 14, "bold"), fg="#0078D7", bg="#E8EEF5", padx=20, pady=15)
        tracking_frame.pack(fill="both", expand=True, pady=10)

        self.tracking_canvas = tk.Canvas(tracking_frame, width=200, height=200, bg="#fff", highlightthickness=1, highlightbackground="#0078D7")
        self.tracking_canvas.pack(pady=10)
        # Titik awal di tengah
        self.circle_radius = 15
        self.circle_x = 100
        self.circle_y = 100
        self.tracking_circle = self.tracking_canvas.create_oval(
            self.circle_x - self.circle_radius, self.circle_y - self.circle_radius,
            self.circle_x + self.circle_radius, self.circle_y + self.circle_radius,
            fill="#0078D7"
        )

    def move_tracking_circle(self, dx, dy):
        # Update posisi lingkaran
        new_x = self.circle_x + dx
        new_y = self.circle_y + dy
        # Batas canvas
        min_pos = self.circle_radius
        max_pos = 200 - self.circle_radius
        self.circle_x = max(min_pos, min(new_x, max_pos))
        self.circle_y = max(min_pos, min(new_y, max_pos))
        self.tracking_canvas.coords(
            self.tracking_circle,
            self.circle_x - self.circle_radius, self.circle_y - self.circle_radius,
            self.circle_x + self.circle_radius, self.circle_y + self.circle_radius
        )

    def move_tracking_circle_continuous(self):
        if self.moving_direction == "up":
            self.move_tracking_circle(0, -self.move_speed)
        elif self.moving_direction == "down":
            self.move_tracking_circle(0, self.move_speed)
        elif self.moving_direction == "left":
            self.move_tracking_circle(-self.move_speed, 0)
        elif self.moving_direction == "right":
            self.move_tracking_circle(self.move_speed, 0)
        # Lanjutkan jika masih bergerak
        if self.moving_direction:
            self.root.after(self.move_interval, self.move_tracking_circle_continuous)

    def get_pwm_value(self):
        # Ambil nilai PWM dari entry "Motor Speed", default 150 jika kosong/tidak valid
        try:
            val = int(self.entries[0].get())
            if 0 <= val <= 255:
                return val
        except Exception:
            pass
        return 150  # Default PWM

    def update_move_speed(self):
        pwm = self.get_pwm_value()
        # Skala kecepatan: minimal 2, maksimal 25 (bisa disesuaikan)
        self.move_speed = max(2, int(pwm / 10))

    def update_sensor_value(self, index, value):
        # Update progress bar dan label sensor sesuai nilai
        if 0 <= index < len(self.sensor_labels):
            self.sensor_labels[index].config(text=f"Sensor {index+1}: {value}")
            try:
                v = int(value)
                self.sensor_bars[index]["value"] = v
                style = ttk.Style()
                if v == 1:
                    style.configure(self.pb_styles[index], background="#4CAF50", troughcolor="#D3D3D3")
                else:
                    style.configure(self.pb_styles[index], background="#D3D3D3", troughcolor="#D3D3D3")
            except Exception:
                self.sensor_bars[index]["value"] = 0

    def read_serial_loop(self):
        # Kirim permintaan sensor ke Arduino dan baca respons
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write("GETSENSOR\n".encode())
            except serial.SerialException:
                pass

        if self.serial_conn and self.serial_conn.in_waiting:
            try:
                data = self.serial_conn.readline().decode(errors='ignore').strip()
                if data.startswith("SENSORS:"):
                    parts = data.replace("SENSORS:", "").split(",")
                    for i, val in enumerate(parts):
                        self.update_sensor_value(i, val)
                else:
                    print("Arduino:", data)
            except Exception as e:
                print("Error reading serial:", e)

        # Panggil ulang fungsi setiap 200ms
        self.root.after(200, self.read_serial_loop)

    def send_motor_command(self, speed, action):
        # Kirim perintah motor dengan format M:<speed>:<action>
        if self.serial_conn and self.serial_conn.is_open:
            try:
                command = f"M:{speed}:{action}\n"
                self.serial_conn.write(command.encode())
            except serial.SerialException:
                messagebox.showerror("Error", "Gagal mengirim data ke perangkat Serial.")
        else:
            messagebox.showwarning("Warning", "Serial belum terkoneksi.")

    # Fungsi-fungsi arah motor
    def stop_motor(self):
        self.send_motor_command(0, "S")
        self.status_var.set("Status: Diam")
        self.moving_direction = None  # Hentikan gerak lingkaran

    def move_forward(self):
        pwm = self.get_pwm_value()
        self.send_motor_command(pwm, "F")
        self.status_var.set("Status: Maju")
        self.update_move_speed()
        self.moving_direction = "up"
        self.move_tracking_circle_continuous()

    def move_backward(self):
        pwm = self.get_pwm_value()
        self.send_motor_command(pwm, "B")
        self.status_var.set("Status: Mundur")
        self.update_move_speed()
        self.moving_direction = "down"
        self.move_tracking_circle_continuous()

    def turn_left(self):
        pwm = self.get_pwm_value()
        self.send_motor_command(pwm, "L")
        self.status_var.set("Status: Kiri")
        self.update_move_speed()
        self.moving_direction = "left"
        self.move_tracking_circle_continuous()

    def turn_right(self):
        pwm = self.get_pwm_value()
        self.send_motor_command(pwm, "R")
        self.status_var.set("Status: Kanan")
        self.update_move_speed()
        self.moving_direction = "right"
        self.move_tracking_circle_continuous()

    def submit(self, entry, label):
        val = entry.get()
        if label == "Motor Speed":
            # Validasi dan kirim perintah motor speed manual
            if val.isdigit() and 0 <= int(val) <= 255:
                if self.serial_conn and self.serial_conn.is_open:
                    try:
                        self.serial_conn.write(f"M:{val}:F\n".encode())
                        messagebox.showinfo("Sukses", f"Perintah motor speed {val} terkirim!")
                    except serial.SerialException:
                        messagebox.showerror("Error", "Gagal mengirim data ke perangkat Serial.")
            else:
                messagebox.showwarning("Input Error", "Input Motor Speed harus angka antara 0 sampai 255.")
        elif label == "Servo Angle":
            # Validasi dan kirim perintah servo
            if val.isdigit() and 0 <= int(val) <= 180:
                if self.serial_conn and self.serial_conn.is_open:
                    try:
                        self.serial_conn.write(f"S:{val}\n".encode())
                        messagebox.showinfo("Sukses", f"Perintah servo angle {val} terkirim!")
                    except serial.SerialException:
                        messagebox.showerror("Error", "Gagal mengirim data ke perangkat Serial.")
            else:
                messagebox.showwarning("Input Error", "Input Servo Angle harus angka antara 0 sampai 180.")

# Jalankan GUI utama
if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorApp(root)
    root.mainloop()