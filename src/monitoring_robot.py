import tkinter as tk
from tkinter import ttk, messagebox
<<<<<<< HEAD
import socket
import threading
import time

# --- THEME SETUP ---
PALETTE = {
    "bg": "#F6F8FB",
    "frame": "#FFFFFF",
    "accent": "#6C63FF",
    "accent2": "#48C9B0",
    "text": "#22223B",
    "label": "#4B5563",
    "entry_bg": "#F0F1F6",
    "entry_border": "#E0E3EB",
    "button": "#6C63FF",
    "button_hover": "#5548C9",
    "button_text": "#FFFFFF",
    "progress_bg": "#E0E3EB",
    "progress_fg": "#6C63FF",
    "success": "#48C9B0",
}

FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_SUBTITLE = ("Segoe UI", 13, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_ENTRY = ("Segoe UI", 12)
FONT_BUTTON = ("Segoe UI", 12, "bold")

class ModernButton(tk.Button):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self["bg"] = PALETTE["button"]
        self["fg"] = PALETTE["button_text"]
        self["activebackground"] = PALETTE["button_hover"]
        self["activeforeground"] = PALETTE["button_text"]
        self["font"] = FONT_BUTTON
        self["relief"] = "flat"
        self["bd"] = 0
        self["cursor"] = "hand2"
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    def on_enter(self, e):
        self["bg"] = PALETTE["button_hover"]
    def on_leave(self, e):
        self["bg"] = PALETTE["button"]

class ModernEntry(tk.Entry):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self["bg"] = PALETTE["entry_bg"]
        self["fg"] = PALETTE["text"]
        self["font"] = FONT_ENTRY
        self["relief"] = "flat"
        self["bd"] = 2
        self["highlightthickness"] = 1
        self["highlightbackground"] = PALETTE["entry_border"]
        self["highlightcolor"] = PALETTE["accent"]
=======
import serial
>>>>>>> c7cef9e5d201617952badf4591486a0d0f40215a

class MonitorApp:
    def __init__(self, root):
        self.root = root
<<<<<<< HEAD
        self.root.title("Monitor System (TCP/IP)")
        self.root.geometry("950x560")
        self.root.configure(bg=PALETTE["bg"])
=======
        self.root.title("Sistem Monitor")
        self.root.geometry("900x480")
        self.root.configure(bg="#E8EEF5")
>>>>>>> c7cef9e5d201617952badf4591486a0d0f40215a

        self.judul = ["Motor Speed", "Servo Angle"]
        self.entries = []
        self.sensor_labels = []
        self.sensor_bars = []

<<<<<<< HEAD
        self.status_var = tk.StringVar()
        self.status_var.set("Status: Disconnected")
        self.status_label = tk.Label(
            self.root, textvariable=self.status_var,
            font=FONT_LABEL, fg=PALETTE["accent"], bg=PALETTE["bg"], anchor="w", padx=10
        )
        self.status_label.pack(fill="x", pady=(0, 5))

        self.sock = None
        self.is_connected = False
        self.server_ip_var = tk.StringVar(value="192.168.240.127")
        self.server_port_var = tk.StringVar(value="8080")

        header = tk.Label(
            self.root, text="MONITOR SYSTEM", font=FONT_TITLE,
            fg=PALETTE["accent"], bg=PALETTE["bg"], pady=10
        )
        header.pack()

        main_frame = tk.Frame(self.root, bg=PALETTE["bg"])
=======
        # Status Navigasi
        self.status_var = tk.StringVar()
        self.status_var.set("Status: Diam")
        self.status_label = tk.Label(self.root, textvariable=self.status_var, font=("Segoe UI", 12, "bold"), fg="#0078D7", bg="#E8EEF5")
        self.status_label.pack(pady=(0, 10))

        # Untuk tracking gerak lingkaran
        self.moving_direction = None  # None, "up", "down", "left", "right"
        self.move_speed = 20          # Jarak per langkah (akan diatur sesuai PWM)
        self.move_interval = 100      # ms, interval update gerak (bisa juga diatur sesuai PWM)
        self.move_job = None          # Untuk menyimpan after job
        self.last_action = None       # Untuk menyimpan aksi terakhir (F/B/L/R)

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
>>>>>>> c7cef9e5d201617952badf4591486a0d0f40215a
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        main_frame.columnconfigure(0, weight=1, uniform='a')
        main_frame.columnconfigure(1, weight=1, uniform='a')
        main_frame.rowconfigure(0, weight=1)

<<<<<<< HEAD
        self.left_frame = tk.Frame(main_frame, bg=PALETTE["bg"])
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        self.right_frame = tk.Frame(main_frame, bg=PALETTE["bg"])
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(15, 0))

        # --- Progressbar style setup ---
        style = ttk.Style()
        style.theme_use('clam')
        self.pb_styles = []
        for i in range(5):
            style_name = f"ModernPB{i}.Horizontal.TProgressbar"
            style.configure(style_name,
                troughcolor=PALETTE["progress_bg"],
                background=PALETTE["progress_fg"],
                thickness=18,
                bordercolor=PALETTE["progress_bg"],
                lightcolor=PALETTE["progress_fg"],
                darkcolor=PALETTE["progress_fg"],
                borderwidth=0
            )
            self.pb_styles.append(style_name)

        self.create_left_side()
        self.create_right_side()

        conn_frame = tk.Frame(self.root, bg=PALETTE["bg"])
        conn_frame.pack(pady=(0, 10))
        tk.Label(conn_frame, text="ESP32 IP:", font=FONT_LABEL, bg=PALETTE["bg"]).pack(side=tk.LEFT, padx=5)
        self.ip_entry = ModernEntry(conn_frame, textvariable=self.server_ip_var, width=15)
        self.ip_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(conn_frame, text="Port:", font=FONT_LABEL, bg=PALETTE["bg"]).pack(side=tk.LEFT, padx=5)
        self.port_entry = ModernEntry(conn_frame, textvariable=self.server_port_var, width=7)
        self.port_entry.pack(side=tk.LEFT, padx=5)
        self.connect_button = ModernButton(conn_frame, text="Connect", command=self.toggle_connection, width=10)
        self.connect_button.pack(side=tk.LEFT, padx=5)

        self.moving_direction = None
        self.move_speed_factor = 0.1
        self.move_interval = 100
        self.move_job = None

        self.data_thread = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_left_side(self):
        input_frame = tk.Frame(self.left_frame, bg=PALETTE["frame"], bd=0, highlightthickness=0)
        input_frame.pack(fill="x", pady=(0, 20), padx=5, ipady=10, ipadx=5)
        tk.Label(input_frame, text="Motor & Servo Control", font=FONT_SUBTITLE, fg=PALETTE["accent"], bg=PALETTE["frame"]).grid(row=0, column=0, columnspan=3, pady=(5, 10))

        for i, label_text in enumerate(self.judul):
            lbl = tk.Label(input_frame, text=label_text, font=FONT_LABEL, bg=PALETTE["frame"], fg=PALETTE["label"])
            lbl.grid(row=i+1, column=0, sticky="w", pady=8, padx=(0, 10))
            entry = ModernEntry(input_frame, width=12)
            entry.grid(row=i+1, column=1, pady=8, padx=(0, 10))
            self.entries.append(entry)
            btn = ModernButton(input_frame, text="OK", width=5, command=lambda e=entry, l=label_text: self.submit_manual_value(e, l))
            btn.grid(row=i+1, column=2, pady=8)

        control_frame = tk.Frame(self.left_frame, bg=PALETTE["frame"], bd=0, highlightthickness=0)
        control_frame.pack(pady=10, fill="both", expand=True, padx=5, ipady=10, ipadx=5)
        tk.Label(control_frame, text="Direction Control", font=FONT_SUBTITLE, fg=PALETTE["accent"], bg=PALETTE["frame"]).pack(pady=(5, 10))

        btn_opts = {"width": 4, "height": 2}
        btn_frame = tk.Frame(control_frame, bg=PALETTE["frame"])
        btn_frame.pack()
        ModernButton(btn_frame, text="↑", command=self.move_forward, **btn_opts).grid(row=0, column=1, padx=10, pady=5)
        ModernButton(btn_frame, text="←", command=self.turn_left, **btn_opts).grid(row=1, column=0, padx=10, pady=5)
        ModernButton(btn_frame, text="↓", command=self.move_backward, **btn_opts).grid(row=1, column=1, padx=10, pady=5)
        ModernButton(btn_frame, text="→", command=self.turn_right, **btn_opts).grid(row=1, column=2, padx=10, pady=5)
        ModernButton(btn_frame, text="STOP", command=self.stop_motor, width=10, height=1).grid(row=2, column=1, pady=10)

    def create_right_side(self):
        sensor_frame = tk.Frame(self.right_frame, bg=PALETTE["frame"], bd=0, highlightthickness=0)
        sensor_frame.pack(fill="x", pady=(0, 20), padx=5, ipady=10, ipadx=5)
        tk.Label(sensor_frame, text="Line Sensors", font=FONT_SUBTITLE, fg=PALETTE["accent"], bg=PALETTE["frame"]).pack(pady=(5, 10))

        for i in range(5):
            row_frame = tk.Frame(sensor_frame, bg=PALETTE["frame"])
            row_frame.pack(fill="x", pady=6, padx=10)
            sensor_label = tk.Label(row_frame, text=f"Sensor {i+1}: -", font=FONT_LABEL, fg=PALETTE["label"], bg=PALETTE["frame"], anchor="w", width=15)
            sensor_label.pack(side="left")
            self.sensor_labels.append(sensor_label)
            max_val = 4095 if i == 2 else 1
            bar = ttk.Progressbar(row_frame, orient="horizontal", length=140, mode="determinate", maximum=max_val, style=self.pb_styles[i])
            bar.pack(side="left", padx=10, pady=2)
            bar["value"] = 0
            self.sensor_bars.append(bar)

        tracking_frame = tk.Frame(self.right_frame, bg=PALETTE["frame"], bd=0, highlightthickness=0)
        tracking_frame.pack(fill="both", expand=True, pady=10, padx=5, ipady=10, ipadx=5)
        tk.Label(tracking_frame, text="Navigation Tracking", font=FONT_SUBTITLE, fg=PALETTE["accent"], bg=PALETTE["frame"]).pack(pady=(5, 10))
        self.tracking_canvas = tk.Canvas(tracking_frame, width=220, height=220, bg="#F6F8FB", highlightthickness=0)
        self.tracking_canvas.pack(pady=10)
        self.circle_radius = 18
        self.circle_x = 110
        self.circle_y = 110
        self.tracking_circle = self.tracking_canvas.create_oval(
            self.circle_x - self.circle_radius, self.circle_y - self.circle_radius,
            self.circle_x + self.circle_radius, self.circle_y + self.circle_radius,
            fill=PALETTE["accent"], outline=PALETTE["accent2"], width=3
        )

    # --- Connection and TCP communication ---
    def on_closing(self):
        if self.is_connected and self.sock:
            try:
                print("Closing TCP socket...")
                self.sock.close()
            except Exception as e:
                print(f"Error closing socket: {e}")
        self.is_connected = False
        if self.data_thread and self.data_thread.is_alive():
            print("Data thread is alive, attempting to join...")
            self.data_thread.join(timeout=1.0)
            if self.data_thread.is_alive():
                print("Data thread did not terminate gracefully.")
        print("Exiting application.")
        self.root.destroy()

    def toggle_connection(self):
        if not self.is_connected:
            self.connect_to_server()
        else:
            self.disconnect_from_server()

    def connect_to_server(self):
        ip = self.server_ip_var.get()
        port_str = self.server_port_var.get()
        if not ip or not port_str:
            messagebox.showerror("Error", "IP address and port cannot be empty.")
            return
        try:
            port = int(port_str)
        except ValueError:
            messagebox.showerror("Error", "Port must be a number.")
            return

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)
            print(f"Trying to connect to {ip}:{port}...")
            self.sock.connect((ip, port))
            self.sock.settimeout(1)
            self.is_connected = True
            self.status_var.set(f"Status: Connected to {ip}:{port}")
            self.connect_button.config(text="Disconnect", bg=PALETTE["accent2"])
            print(f"Connected to ESP32 at {ip}:{port}")

            if self.data_thread is None or not self.data_thread.is_alive():
                self.data_thread = threading.Thread(target=self.read_data_loop, daemon=True)
                self.data_thread.start()

        except socket.timeout:
            messagebox.showerror("Connection Error", f"Connection to {ip}:{port} timed out.")
            self.is_connected = False
            if self.sock: self.sock.close()
            self.sock = None
        except ConnectionRefusedError:
            messagebox.showerror("Connection Error", f"Connection to {ip}:{port} refused. Make sure ESP32 server is running.")
            self.is_connected = False
            if self.sock: self.sock.close()
            self.sock = None
        except Exception as e:
            messagebox.showerror("Error", f"Cannot connect to {ip}:{port}.\n{e}")
            self.is_connected = False
            if self.sock: self.sock.close()
            self.sock = None
            print(f"Error while connecting: {e}")

    def disconnect_from_server(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception as e:
                print(f"Error closing socket: {e}")
        self.sock = None
        self.is_connected = False
        self.status_var.set("Status: Disconnected")
        self.connect_button.config(text="Connect", bg=PALETTE["button"])
        print("Disconnected from ESP32.")
        for i in range(5):
            self.update_sensor_value(i, "-")
            if i < len(self.sensor_bars):
                self.sensor_bars[i]["value"] = 0
                style = ttk.Style()
                style.configure(self.pb_styles[i], background=PALETTE["progress_bg"])

    # --- Tracking and sensor update ---
    def move_tracking_circle(self, dx, dy):
        new_x = self.circle_x + dx
        new_y = self.circle_y + dy
        min_pos = self.circle_radius
        max_pos_x = self.tracking_canvas.winfo_width() - self.circle_radius
        max_pos_y = self.tracking_canvas.winfo_height() - self.circle_radius
        if max_pos_x < min_pos : max_pos_x = 220 - self.circle_radius
        if max_pos_y < min_pos : max_pos_y = 220 - self.circle_radius
        self.circle_x = max(min_pos, min(new_x, max_pos_x))
        self.circle_y = max(min_pos, min(new_y, max_pos_y))
=======
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
        if hasattr(self, 'serial_conn') and self.serial_conn and self.serial_conn.is_open:
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

            # Tambahkan event Enter pada entry PWM agar update kecepatan saat sedang berjalan
            if label_text == "Motor Speed":
                entry.bind("<Return>", lambda event, e=entry, l=label_text: self.submit(e, l))

            # Tombol OK untuk kirim nilai
            btn = tk.Button(input_frame, text="OK", font=("Segoe UI", 11, "bold"),
                            bg="#0078D7", fg="white", width=5,
                            command=lambda e=entry, l=label_text: self.submit(e, l))
            btn.grid(row=i, column=2, pady=8)

        # Kontrol arah robot (panah dan STOP)
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
        self.circle_radius = 9
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
>>>>>>> c7cef9e5d201617952badf4591486a0d0f40215a
        self.tracking_canvas.coords(
            self.tracking_circle,
            self.circle_x - self.circle_radius, self.circle_y - self.circle_radius,
            self.circle_x + self.circle_radius, self.circle_y + self.circle_radius
        )

    def move_tracking_circle_continuous(self):
<<<<<<< HEAD
        current_move_speed = self.update_move_speed_for_tracking()
        if self.moving_direction == "up":
            self.move_tracking_circle(0, -current_move_speed)
        elif self.moving_direction == "down":
            self.move_tracking_circle(0, current_move_speed)
        elif self.moving_direction == "left":
            self.move_tracking_circle(-current_move_speed, 0)
        elif self.moving_direction == "right":
            self.move_tracking_circle(current_move_speed, 0)
=======
        # Selalu update move_speed sesuai PWM terbaru
        self.update_move_speed()
        if self.moving_direction == "up":
            self.move_tracking_circle(0, -self.move_speed)
        elif self.moving_direction == "down":
            self.move_tracking_circle(0, self.move_speed)
        elif self.moving_direction == "left":
            self.move_tracking_circle(-self.move_speed, 0)
        elif self.moving_direction == "right":
            self.move_tracking_circle(self.move_speed, 0)
        # Lanjutkan jika masih bergerak
>>>>>>> c7cef9e5d201617952badf4591486a0d0f40215a
        if self.moving_direction:
            self.move_job = self.root.after(self.move_interval, self.move_tracking_circle_continuous)
        else:
            self.move_job = None

<<<<<<< HEAD
    def get_pwm_value_from_entry(self):
=======
    def get_pwm_value(self):
        # Ambil nilai PWM dari entry "Motor Speed", default 150 jika kosong/tidak valid
>>>>>>> c7cef9e5d201617952badf4591486a0d0f40215a
        try:
            val = int(self.entries[0].get())
            if 0 <= val <= 255:
                return val
<<<<<<< HEAD
        except (ValueError, IndexError):
            pass
        return 150

    def update_move_speed_for_tracking(self):
        pwm = self.get_pwm_value_from_entry()
        scaled_speed = max(2, int(pwm * self.move_speed_factor))
        return scaled_speed

    def update_sensor_value(self, index, value_str):
        if not (0 <= index < len(self.sensor_labels) and index < len(self.sensor_bars)):
            print(f"Invalid sensor index: {index}")
            return
        self.sensor_labels[index].config(text=f"Sensor {index+1}: {value_str}")
        try:
            v = int(value_str)
            style = ttk.Style()
            if index == 2:
                self.sensor_bars[index]["value"] = v
                if v > 2000:
                    style.configure(self.pb_styles[index], background=PALETTE["success"], troughcolor=PALETTE["progress_bg"])
                else:
                    style.configure(self.pb_styles[index], background=PALETTE["progress_fg"], troughcolor=PALETTE["progress_bg"])
            else:
                self.sensor_bars[index]["value"] = v
                if v == 1:
                    style.configure(self.pb_styles[index], background=PALETTE["success"], troughcolor=PALETTE["progress_bg"])
                else:
                    style.configure(self.pb_styles[index], background=PALETTE["progress_fg"], troughcolor=PALETTE["progress_bg"])
        except ValueError:
            self.sensor_bars[index]["value"] = 0
            style = ttk.Style()
            style.configure(self.pb_styles[index], background=PALETTE["progress_bg"])
        except Exception as e:
            print(f"Error updating sensor UI ({index}): {e}")
            self.sensor_bars[index]["value"] = 0
            style = ttk.Style()
            style.configure(self.pb_styles[index], background=PALETTE["progress_bg"])

    # --- TCP Data Reading Loop ---
    def read_data_loop(self):
        buffer = ""
        while self.is_connected and self.sock:
            try:
                self.send_command_to_esp("GETSENSOR")
                while self.is_connected and self.sock:
                    try:
                        chunk = self.sock.recv(1024).decode('utf-8', errors='ignore')
                        if not chunk:
                            print("Connection closed by server.")
                            self.root.after(0, self.disconnect_from_server)
                            return
                        buffer += chunk
                        if '\n' in buffer:
                            data, buffer = buffer.split('\n', 1)
                            data = data.strip()
                            if data.startswith("SENSORS:"):
                                parts_str = data.replace("SENSORS:", "")
                                if parts_str:
                                    parts = parts_str.split(",")
                                    if len(parts) == 5:
                                        self.root.after(0, lambda p=list(parts): [self.update_sensor_value(i, val) for i, val in enumerate(p)])
                                    else:
                                        print(f"Incomplete sensor data received: {data}")
                                else:
                                    print(f"Empty sensor data received: {data}")
                            elif data:
                                print("ESP32:", data)
                            break
                    except socket.timeout:
                        break
                    except UnicodeDecodeError as ude:
                        print(f"Unicode decode error: {ude}. Buffer: {buffer}")
                        buffer = ""
                        break
                    except Exception as e_recv:
                        if self.is_connected:
                            print(f"Error receiving data: {e_recv}")
                        self.root.after(0, self.disconnect_from_server)
                        return
            except (socket.error, BrokenPipeError, ConnectionResetError) as e_sock:
                if self.is_connected:
                    print(f"Socket error: {e_sock}. Disconnecting.")
                    messagebox.showerror("Connection Error", f"Connection to ESP32 lost: {e_sock}")
                self.root.after(0, self.disconnect_from_server)
                return
            except Exception as e_outer:
                if self.is_connected:
                    print(f"Error in data read loop: {e_outer}")
            if self.is_connected:
                time.sleep(0.2)
            else:
                break
        print("Data read loop stopped.")

    def send_command_to_esp(self, command_str):
        if self.is_connected and self.sock:
            try:
                full_command = command_str + "\n"
                self.sock.sendall(full_command.encode('utf-8'))
                print(f"Sent to ESP32: {command_str}")
            except (socket.error, BrokenPipeError) as e:
                messagebox.showerror("Error", f"Failed to send data to ESP32: {e}")
                print(f"Socket error while sending: {e}")
                self.disconnect_from_server()
            except Exception as e_send:
                messagebox.showerror("Error", f"Error while sending: {e_send}")
                print(f"General error while sending: {e_send}")
        else:
            messagebox.showwarning("Warning", "Not connected to ESP32.")
            print("Failed to send: Not connected.")

    # --- Motor and Servo Control ---
    def stop_motor(self):
        pwm = self.get_pwm_value_from_entry()
        self.send_command_to_esp(f"M:{pwm}:S")
        self.status_var.set("Status: Stopped")
        self.moving_direction = None
        if self.move_job:
            self.root.after_cancel(self.move_job)
            self.move_job = None
        self.circle_x = self.tracking_canvas.winfo_width() / 2 if self.tracking_canvas.winfo_width() > 0 else 110
        self.circle_y = self.tracking_canvas.winfo_height() / 2 if self.tracking_canvas.winfo_height() > 0 else 110
        self.tracking_canvas.coords(
            self.tracking_circle,
            self.circle_x - self.circle_radius, self.circle_y - self.circle_radius,
            self.circle_x + self.circle_radius, self.circle_y + self.circle_radius
        )

    def move_forward(self):
        pwm = self.get_pwm_value_from_entry()
        self.send_command_to_esp(f"M:{pwm}:F")
        self.status_var.set(f"Status: Forward (PWM: {pwm})")
        self.moving_direction = "up"
=======
        except Exception:
            pass
        return 150  # Default PWM

    def update_move_speed(self):
        pwm = self.get_pwm_value()
        # Skala kecepatan: minimal 2, maksimal 10 (lebih realistis di canvas)
        self.move_speed = max(2, min(10, int(pwm / 25)))

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
        self.last_action = None
        if self.move_job:
            self.root.after_cancel(self.move_job)
            self.move_job = None

    def move_forward(self):
        pwm = self.get_pwm_value()
        self.send_motor_command(pwm, "F")
        self.status_var.set("Status: Maju")
        self.moving_direction = "up"
        self.last_action = "F"
>>>>>>> c7cef9e5d201617952badf4591486a0d0f40215a
        if self.move_job:
            self.root.after_cancel(self.move_job)
        self.move_tracking_circle_continuous()

    def move_backward(self):
<<<<<<< HEAD
        pwm = self.get_pwm_value_from_entry()
        self.send_command_to_esp(f"M:{pwm}:B")
        self.status_var.set(f"Status: Backward (PWM: {pwm})")
        self.moving_direction = "down"
=======
        pwm = self.get_pwm_value()
        self.send_motor_command(pwm, "B")
        self.status_var.set("Status: Mundur")
        self.moving_direction = "down"
        self.last_action = "B"
>>>>>>> c7cef9e5d201617952badf4591486a0d0f40215a
        if self.move_job:
            self.root.after_cancel(self.move_job)
        self.move_tracking_circle_continuous()

    def turn_left(self):
<<<<<<< HEAD
        pwm = self.get_pwm_value_from_entry()
        self.send_command_to_esp(f"M:{pwm}:L")
        self.status_var.set(f"Status: Left (PWM: {pwm})")
        self.moving_direction = "left"
=======
        pwm = self.get_pwm_value()
        self.send_motor_command(pwm, "L")
        self.status_var.set("Status: Kiri")
        self.moving_direction = "left"
        self.last_action = "L"
>>>>>>> c7cef9e5d201617952badf4591486a0d0f40215a
        if self.move_job:
            self.root.after_cancel(self.move_job)
        self.move_tracking_circle_continuous()

    def turn_right(self):
<<<<<<< HEAD
        pwm = self.get_pwm_value_from_entry()
        self.send_command_to_esp(f"M:{pwm}:R")
        self.status_var.set(f"Status: Right (PWM: {pwm})")
        self.moving_direction = "right"
=======
        pwm = self.get_pwm_value()
        self.send_motor_command(pwm, "R")
        self.status_var.set("Status: Kanan")
        self.moving_direction = "right"
        self.last_action = "R"
>>>>>>> c7cef9e5d201617952badf4591486a0d0f40215a
        if self.move_job:
            self.root.after_cancel(self.move_job)
        self.move_tracking_circle_continuous()

<<<<<<< HEAD
    def submit_manual_value(self, entry_widget, label_text):
        val_str = entry_widget.get()
        try:
            val_int = int(val_str)
            if label_text == "Motor Speed":
                if 0 <= val_int <= 255:
                    self.send_command_to_esp(f"M:{val_int}:F")
                    messagebox.showinfo("Success", f"Motor speed command {val_int} sent!")
                else:
                    messagebox.showwarning("Input Error", "Motor Speed must be between 0 and 255.")
            elif label_text == "Servo Angle":
                if 0 <= val_int <= 180:
                    self.send_command_to_esp(f"S:{val_int}")
                    messagebox.showinfo("Success", f"Servo angle command {val_int} sent!")
                else:
                    messagebox.showwarning("Input Error", "Servo Angle must be between 0 and 180.")
        except ValueError:
            messagebox.showwarning("Input Error", "Input must be a number.")

=======
    def submit(self, entry, label):
        val = entry.get()
        if label == "Motor Speed":
            # Validasi dan kirim perintah motor speed manual
            if val.isdigit() and 0 <= int(val) <= 255:
                pwm_val = int(val)
                if self.serial_conn and self.serial_conn.is_open:
                    try:
                        # Jika sedang berjalan, kirim ulang perintah dengan aksi terakhir
                        if self.moving_direction and self.last_action:
                            self.send_motor_command(pwm_val, self.last_action)
                        else:
                            self.serial_conn.write(f"M:{val}:F\n".encode())
                        messagebox.showinfo("Sukses", f"Perintah motor speed {val} terkirim!")
                    except serial.SerialException:
                        messagebox.showerror("Error", "Gagal mengirim data ke perangkat Serial.")
                # Jika sedang berjalan, update kecepatan lingkaran
                if self.moving_direction:
                    self.update_move_speed()
                # Jika PWM 0, hentikan gerak lingkaran dan status
                if pwm_val == 0:
                    self.stop_motor()
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
>>>>>>> c7cef9e5d201617952badf4591486a0d0f40215a
if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorApp(root)
    root.mainloop()