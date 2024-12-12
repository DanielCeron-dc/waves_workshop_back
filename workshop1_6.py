import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse

# Argument parser para recibir la frecuencia como argumento
parser = argparse.ArgumentParser(description="Generar video de vibración 2D de una membrana.")
parser.add_argument("--frecuencia", type=float, required=True, help="Frecuencia de vibración (Hz).")
parser.add_argument("--output", type=str, required=True, help="Ruta del archivo de salida para el video.")
args = parser.parse_args()

# Parámetros recibidos
f = args.frecuencia  # Frecuencia de la vibración
output_path = args.output

# Constantes y parámetros
A = 1.0         # Amplitud de la vibración
kx = 2 * np.pi  # Número de onda en dirección x
ky = 2 * np.pi  # Número de onda en dirección y
fps = 30        # Cuadros por segundo para la animación
T = 10.0        # Tiempo total de simulación (segundos)
frames = int(T * fps)

# Creación de la malla 2D
x = np.linspace(0, 1, 100)
y = np.linspace(0, 1, 100)
X, Y = np.meshgrid(x, y)

def field_data(frecuencia, t):
    omega = 2 * np.pi * frecuencia
    Z = A * np.sin(kx * X) * np.sin(ky * Y) * np.sin(omega * t)
    return Z

# Configuración inicial de la figura
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_title("Vibración 2D de una membrana")
ax.set_xlabel("X")
ax.set_ylabel("Y")

# Campo inicial en t=0
Z = field_data(f, 0)
im = ax.imshow(Z, cmap='viridis', extent=(0, 1, 0, 1), origin='lower', animated=True)
fig.colorbar(im, ax=ax, label="Desplazamiento")

# Función de actualización para la animación
def update(frame):
    t = frame / fps
    Z = field_data(f, t)
    im.set_data(Z)
    return [im]

# Crear la animación
ani = animation.FuncAnimation(fig, update, frames=frames, interval=1000/fps, blit=True)

# Guardar la animación como un archivo de video
ani.save(output_path, writer="ffmpeg", fps=fps)

print(f"Animación guardada en {output_path}")
