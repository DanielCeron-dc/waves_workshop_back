import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse

# Parámetros de la onda
def onda_acustica_video(y_amplitud, tiempo_total, rango_x, output_path):
    # Constantes
    omega = 1980  # Frecuencia angular (rad/s)
    k = 6         # Número de onda (rad/m)
    A = y_amplitud  # Amplitud de la onda en cm
    rho = 1.21     # Densidad del aire (kg/m³)
    c = omega / k  # Velocidad de propagación de la onda (m/s)

    # Calcular propiedades
    frecuencia = omega / (2 * np.pi)  # Frecuencia (Hz)
    longitud_onda = 2 * np.pi / k     # Longitud de onda (m)
    u_amplitud = omega * A / 100      # Amplitud de velocidad (convertir A a metros)
    p_amplitud = rho * c * u_amplitud # Amplitud de presión (Pa)

    # Configuración para la animación (ralentizada x10)
    fps = 30  # Cuadros por segundo
    video_duracion = tiempo_total  # Duración del video (en segundos reales)
    frames = int(video_duracion * fps)  # Número de cuadros reales
    tiempo_animado = tiempo_total * 10  # Tiempo "simulado" (ralentizado x10)
    interval = 1000 / fps  # Intervalo en ms entre cuadros

    # Creación de la malla 2D
    x_vals = np.linspace(0, rango_x, 500)
    t_vals = np.linspace(0, tiempo_animado, frames)  # Más tiempo comprimido en menos cuadros

    # Configuración inicial de la figura
    fig, (ax, ax_text) = plt.subplots(
        2, 1, figsize=(8, 6), gridspec_kw={'height_ratios': [4, 1]}
    )
    ax.set_xlim(0, rango_x)  # Ajustar el rango del eje x dinámicamente
    ax.set_ylim(-1.5 * A, 1.5 * A)  # Amplitud en el eje y
    ax.set_xlabel("Posición x (m)")
    ax.set_ylabel("Desplazamiento y (cm)")
    ax.set_title("Propagación de la Onda Acústica (ralentizada x10)")

    # Línea inicial para la animación
    line, = ax.plot([], [], lw=2, color="blue")

    # Configuración para mostrar datos
    ax_text.axis("off")  # Ocultar el eje del texto
    text_props = ax_text.text(
        0.5, 0.5, "", fontsize=10, ha="center", va="center", wrap=True
    )

    # Función para inicializar la animación
    def init():
        line.set_data([], [])
        text_props.set_text("")  # Vaciar el texto al inicio
        return line, text_props

    # Función para actualizar la animación
    def update(frame):
        t = t_vals[frame]
        Y = A * np.sin(omega * t - k * x_vals)  # Ecuación de la onda
        line.set_data(x_vals, Y)

        # Actualizar datos calculados
        velocidad_particula = u_amplitud * np.cos(omega * t - k * x_vals)
        text_props.set_text(
            f"Frecuencia: {frecuencia:.2f} Hz\n"
            f"Velocidad de propagación: {c:.2f} m/s\n"
            f"Longitud de onda: {longitud_onda:.2f} m\n"
            f"Amplitud de oscilación (u): {u_amplitud:.2f} m/s\n"
            f"Amplitud de presión (p): {p_amplitud:.2f} Pa"
        )
        return line, text_props

    # Crear la animación
    ani = animation.FuncAnimation(
        fig, update, frames=frames, init_func=init, blit=True, interval=interval
    )

    # Guardar la animación como archivo de video
    ani.save(output_path, writer="ffmpeg", fps=fps)
    print(f"Animación guardada en {output_path}")

# Argumentos del script
parser = argparse.ArgumentParser(description="Generar video de la onda acústica (ralentizada x10).")
parser.add_argument("--amplitud", type=float, default=0.05, help="Amplitud de la onda (cm).")
parser.add_argument("--tiempo", type=float, required=True, help="Tiempo total de video (s).")
parser.add_argument("--rango_x", type=float, required=True, help="Rango máximo del eje x (m).")
parser.add_argument("--output", type=str, required=True, help="Ruta del archivo de salida para el video.")
args = parser.parse_args()

# Ejecutar la función
onda_acustica_video(args.amplitud, args.tiempo, args.rango_x, args.output)
