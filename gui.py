import tkinter as tk
from tkinter import filedialog, ttk

from file_reader import leer_procesos
from scheduler import fcfs, spn, srt, rr
from metrics import calcular_metricas

class SimuladorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Planificación")
        self.root.geometry("800x600")

        self.procesos = []

        self.crear_widgets()
        self.timeline = []
        self.tiempo_actual = 0
        self.bloque_width = 40
        self.colores = {}
        self.tiempo_total = 0
        self.tiempo_cpu = 0

    def crear_widgets(self):
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)

        self.btn_cargar = tk.Button(frame_top, text="Cargar CSV", command=self.cargar_archivo)
        self.btn_cargar.grid(row=0, column=0, padx=10)

        self.algoritmo = tk.StringVar()
        self.combo = ttk.Combobox(frame_top, textvariable=self.algoritmo)
        self.combo['values'] = ("FCFS", "SPN", "SRT", "RR")
        self.combo.current(0)
        self.combo.grid(row=0, column=1, padx=10)

        self.btn_ejecutar = tk.Button(frame_top, text="Ejecutar", command=self.ejecutar)
        self.btn_ejecutar.grid(row=0, column=2, padx=10)

        self.texto = tk.Text(self.root, height=15)
        self.texto.pack(pady=10, fill="both", expand=True)

        self.canvas = tk.Canvas(self.root, height=150, bg="white")
        self.canvas.pack(fill="x", pady=10)
        # Indicadores en tiempo real
        self.label_cpu = tk.Label(self.root, text="Uso CPU: 0%")
        self.label_cpu.pack()

        self.label_procesos = tk.Label(self.root, text="Procesos activos: 0")
        self.label_procesos.pack()

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if ruta:
            self.procesos = leer_procesos(ruta)
            self.texto.insert(tk.END, f"Archivo cargado: {ruta}\n")

    def ejecutar(self):
        self.texto.delete(1.0, tk.END)
        if not self.procesos:
            self.texto.insert(tk.END, "Primero carga un archivo\n")
            return
        for p in self.procesos:
            p.restante = p.duracion

        self.canvas.delete("all")
        self.tiempo_actual = 0

        algoritmo = self.algoritmo.get()

        if algoritmo == "FCFS":
            resultado = fcfs(self.procesos.copy())
            self.timeline = self.generar_timeline(resultado)

        elif algoritmo == "SPN":
            resultado = spn(self.procesos.copy())
            self.timeline = self.generar_timeline(resultado)

        elif algoritmo == "SRT":
            resultado, self.timeline = srt(self.procesos.copy())

        elif algoritmo == "RR":
            resultado, self.timeline = rr(self.procesos.copy(), quantum=2)

        # Obtener métricas
        resultados, prom_esp, prom_ret = calcular_metricas(resultado)

        self.texto.insert(tk.END, f"\n--- {algoritmo} ---\n")

        # Encabezado
        self.texto.insert(tk.END, "Proc | L | D | Ini | Fin | Esp | Ret\n")
        self.texto.insert(tk.END, "-"*40 + "\n")

        # Filas
        for r in resultados:
            linea = f"{r['nombre']} | {r['llegada']} | {r['duracion']} | {r['inicio']} | {r['fin']} | {r['espera']} | {r['retorno']}\n"
        self.texto.insert(tk.END, linea)

        # Promedios
        self.texto.insert(tk.END, "-"*40 + "\n")
        self.texto.insert(tk.END, f"Promedio espera: {prom_esp:.2f}\n")
        self.texto.insert(tk.END, f"Promedio retorno: {prom_ret:.2f}\n\n")

        self.simular()
        self.tiempo_total = len(self.timeline)
        self.tiempo_cpu = 0

    def generar_timeline(self, procesos):
        timeline = []

        for p in procesos:
            for t in range(p.inicio, p.fin):
                timeline.append(p.nombre)

        return timeline

    def simular(self):
        if self.tiempo_actual >= len(self.timeline):
            return

        proceso = self.timeline[self.tiempo_actual]
        # Contar CPU ocupado
        if proceso != "idle":
            self.tiempo_cpu += 1

# Calcular porcentaje CPU
        uso_cpu = (self.tiempo_cpu / (self.tiempo_actual + 1)) * 100
        self.label_cpu.config(text=f"Uso CPU: {uso_cpu:.2f}%")

# Procesos activos
        activos = self.procesos_activos(self.tiempo_actual)
        self.label_procesos.config(text=f"Procesos activos: {activos}")

        x1 = self.tiempo_actual * self.bloque_width
        x2 = x1 + self.bloque_width

        color = self.obtener_color(proceso)
        self.canvas.create_rectangle(x1, 20, x2, 80, fill=color)
        self.canvas.create_text((x1 + x2)//2, 50, text=proceso)

        self.canvas.create_text(x1, 90, text=str(self.tiempo_actual))

        self.tiempo_actual += 1

        self.root.after(500, self.simular)
    def obtener_color(self, proceso):
        if proceso not in self.colores:
            colores_base = ["red", "green", "blue", "orange", "purple", "cyan"]
            self.colores[proceso] = colores_base[len(self.colores) % len(colores_base)]
        return self.colores[proceso]
    def procesos_activos(self, tiempo):
        return len([p for p in self.procesos if p.llegada <= tiempo and p.fin > tiempo])