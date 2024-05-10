import tkinter as tk
from tkinter import messagebox, colorchooser, simpledialog

class Tarea:
    def __init__(self, descripcion, completada=False):
        self.descripcion = descripcion
        self.completada = completada

class HistorialTareasApp:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.master.title("Historial de Tareas Borradas")

        self.historial_frame = tk.Frame(self.master)
        self.historial_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        tk.Label(self.historial_frame, text="Tareas Borradas", font=("Georgia Pro", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=5)

        self.actualizar_historial()

    def restaurar_tarea(self, index):
        tarea_restaurada = self.app.historial_tareas_borradas.pop(index)
        tarea = Tarea(tarea_restaurada.descripcion, tarea_restaurada.completada)  # Crear nueva tarea con los mismos atributos
        self.app.lista_tareas.append(tarea)
        self.app.actualizar_texto_tareas()
        self.actualizar_historial()

    def eliminar_tarea_borrada(self, index):
        del self.app.historial_tareas_borradas[index]
        self.app.actualizar_texto_tareas()
        self.actualizar_historial()

    def actualizar_historial(self):
        for widget in self.historial_frame.winfo_children():
            widget.destroy()

        tk.Label(self.historial_frame, text="Tareas Borradas", font=("Georgia Pro", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=5)

        for i, tarea in enumerate(self.app.historial_tareas_borradas, start=1):
            descripcion_label = tk.Label(self.historial_frame, text=tarea.descripcion)
            descripcion_label.grid(row=i, column=0, sticky="w")

            restaurar_button = tk.Button(self.historial_frame, text="Restaurar", command=lambda index=i-1: (self.restaurar_tarea(index)))
            restaurar_button.grid(row=i, column=1, padx=5)

            eliminar_definitivo_button = tk.Button(self.historial_frame, text="Eliminar Definitivamente", command=lambda index=i-1: (self.eliminar_tarea_borrada(index)))
            eliminar_definitivo_button.grid(row=i, column=2, padx=5)

class ListaTareasApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Lista de Tareas")
        self.color_fondo = "blue"  # Cambiar el color predeterminado a azul

        self.lista_tareas = []
        self.historial_tareas_borradas = []

        self.frame = tk.Frame(self.master, bg=self.color_fondo)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.frame, text="PENDIENTES", font=("Georgia Pro Black", 14, "bold"), bg=self.color_fondo, fg="white")
        self.label.pack(fill=tk.X)

        self.text = tk.Text(self.frame, height=25, width=60, bg="white")
        self.text.pack(fill=tk.BOTH, expand=True)

        # Agregar barra de desplazamiento vertical
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=self.scrollbar.set)

        self.input_frame = tk.Frame(self.frame, bg=self.color_fondo)
        self.input_frame.pack(fill=tk.X)

        self.descripcion_entry = tk.Entry(self.input_frame, width=33)
        self.descripcion_entry.pack(side=tk.LEFT, padx=2)
        self.descripcion_entry.bind("<Return>", lambda event: self.agregar_tarea())  # Asociar la función agregar_tarea al evento de presionar Enter

        self.agregar_button = tk.Button(self.input_frame, text="Agregar Tarea", command=self.agregar_tarea)
        self.agregar_button.pack(side=tk.LEFT, padx=1)

        self.eliminar_entry = tk.Entry(self.input_frame, width=5)
        self.eliminar_entry.pack(side=tk.LEFT, padx=2)

        self.eliminar_button = tk.Button(self.input_frame, text="Eliminar", command=self.eliminar_tarea_por_posicion)
        self.eliminar_button.pack(side=tk.LEFT, padx=1)

        # Botón para abrir la paleta de colores
        self.color_button = tk.Button(self.frame, text="Cambiar Color", command=self.cambiar_color)
        self.color_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.historial_button = tk.Button(self.frame, text="Historial", command=self.mostrar_historial)
        self.historial_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Botón "OK" para borrar tareas finalizadas
        self.ok_button = tk.Button(self.frame, text="OK", command=self.borrar_finalizados)
        self.ok_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Botón para mostrar los créditos
        self.creditos_button = tk.Button(self.frame, text="Créditos", command=self.mostrar_creditos)
        self.creditos_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Botón para mostrar el manual
        self.manual_button = tk.Button(self.frame, text="Manual", command=self.mostrar_manual)
        self.manual_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.actualizar_texto_tareas()

    def agregar_tarea(self):
        descripcion = self.descripcion_entry.get()
        tarea = Tarea(descripcion)
        self.lista_tareas.append(tarea)
        self.actualizar_texto_tareas()
        self.descripcion_entry.delete(0, tk.END)

    def toggle_completada(self, event):
        index = self.text.index(tk.CURRENT)
        index_tarea = int(index.split('.')[0]) - 1
        tarea = self.lista_tareas[index_tarea]
        tarea.completada = not tarea.completada
        self.actualizar_texto_tareas()

    def eliminar_tarea(self, index):
        tarea_eliminada = self.lista_tareas.pop(index)
        self.historial_tareas_borradas.append(tarea_eliminada)
        self.actualizar_texto_tareas()

    def editar_descripcion(self, index):
        tarea = self.lista_tareas[index]
        nueva_descripcion = simpledialog.askstring("Editar Descripción", "Ingrese la nueva descripción:", initialvalue=tarea.descripcion)
        if nueva_descripcion is not None:
            tarea.descripcion = nueva_descripcion
            self.actualizar_texto_tareas()

    def restaurar_tarea(self, index):
        tarea_restaurada = self.historial_tareas_borradas.pop(index)
        tarea = Tarea(tarea_restaurada.descripcion, tarea_restaurada.completada)  # Crear nueva tarea con los mismos atributos
        self.lista_tareas.append(tarea)
        self.actualizar_texto_tareas()

    def eliminar_tarea_borrada(self, index):
        del self.historial_tareas_borradas[index]
        self.actualizar_texto_tareas()

    def eliminar_tarea_por_posicion(self):
        posicion = self.eliminar_entry.get()
        try:
            posicion = int(posicion)
            if 1 <= posicion <= len(self.lista_tareas):
                self.eliminar_tarea(posicion - 1)
                self.eliminar_entry.delete(0, tk.END)
            else:
                raise ValueError("La posición ingresada está fuera de rango.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def cambiar_color(self):
        color_nuevo = colorchooser.askcolor(title="Seleccionar color")[1]
        if color_nuevo:
            self.color_fondo = color_nuevo
            self.frame.configure(bg=self.color_fondo)
            self.label.configure(bg=self.color_fondo)
            self.input_frame.configure(bg=self.color_fondo)

    def mostrar_historial(self):
        historial_window = tk.Toplevel(self.master)
        historial_app = HistorialTareasApp(historial_window, self)

    def mostrar_creditos(self):
        creditos_window = tk.Toplevel(self.master)
        creditos_window.title("Créditos")

        creditos_frame = tk.Frame(creditos_window)
        creditos_frame.pack(padx=10, pady=10)

        tk.Label(creditos_frame, text="Creador: Jesús A. Valera Raga", font=("Georgia Pro", 12)).pack()
        tk.Label(creditos_frame, text="Empresa: IBM Becario-Python", font=("Georgia Pro", 12)).pack()
        tk.Label(creditos_frame, text="Soporte Técnico: valera25@gmail.com", font=("Georgia Pro", 12)).pack()
        tk.Label(creditos_frame, text="Trabajo fin de curso. versión 1.3.9 05/05/2024", font=("Georgia Pro", 12)).pack()

    def mostrar_manual(self):
        manual_window = tk.Toplevel(self.master)
        manual_window.title("Manual de Usuario")

        manual_frame = tk.Frame(manual_window)
        manual_frame.pack(padx=10, pady=10)

        manual_text = """
        Manual de Usuario

        Lista de Tareas

        Agregar Tarea: Escribe la descripción de la tarea en el cuadro de entrada de texto y haz clic en el botón "Agregar Tarea". La nueva tarea se agregará a la lista de tareas pendientes.

        Marcar como Completada: Haz clic en el recuadro cuadrado a la izquierda de una tarea para marcarla como completada. Esto tachará la descripción de la tarea y la resaltará en verde.

        Editar Descripción: Haz clic en el icono de lápiz junto a una tarea para editar su descripción. Se abrirá una ventana emergente donde podrás ingresar la nueva descripción.

        Eliminar Tarea 1: Puedes eliminar una tarea de la lista directamente haciendo clic en el botón de papelera junto a la tarea.

        Eliminar Tarea 2: Desde su posición en la lista ingresando el número de la tarea en el cuadro de entrada de texto "Eliminar" y haciendo clic en el botón "Eliminar".

        Restaurar Tarea: En el historial de tareas borradas, haz clic en el botón "Restaurar" para devolver una tarea eliminada a la lista de tareas pendientes.

        Eliminar Definitivamente: En el historial de tareas borradas, haz clic en el botón "Eliminar Definitivamente" para eliminar permanentemente una tarea de la aplicación.

        Cambiar Color: Haz clic en el botón "Cambiar Color" para seleccionar un color de fondo personalizado para la aplicación.

        Ver Historial: Haz clic en el botón "Historial" para abrir una ventana con el historial de tareas borradas.

        Borrar Tareas Finalizadas: Haz clic en el botón "OK" para enviar a la papelera todas las tareas marcadas como completadas.

        Ver Créditos: Haz clic en el botón "Créditos" para ver información sobre el creador y la versión de la aplicación.

        Creador: Jesús A. Valera Raga
        Empresa: IBM Becario-Python
        Soporte Técnico: valera25@gmail.com
        """

        manual_label = tk.Label(manual_frame, text=manual_text, justify=tk.LEFT, font=("Georgia Pro", 12))
        manual_label.pack()

    def actualizar_texto_tareas(self):
        self.text.delete(1.0, tk.END)
        for i, tarea in enumerate(self.lista_tareas, start=1):
            marca = "[x]" if tarea.completada else "[ ]"
            self.text.insert(tk.END, f"{i}. ")
            self.text.insert(tk.END, marca + " ", f"marca_{i}")
            self.text.insert(tk.END, tarea.descripcion + " ", f"descripcion_{i}")
            eliminar_icono = "🗑️"
            eliminar_button = tk.Button(self.text, text=eliminar_icono, bd=0, fg="gray", command=lambda index=i-1: self.eliminar_tarea(index))
            self.text.window_create(tk.END, window=eliminar_button)
            self.text.insert(tk.END, " ")
            self.text.insert(tk.END, "✏️", f"lapiz_{i}")
            self.text.insert(tk.END, " ")
            completado_text = "Completado" if tarea.completada else "Pendiente"
            self.text.insert(tk.END, completado_text, f"completado_{i}")
            self.text.insert(tk.END, "\n")
            self.text.tag_config(f"marca_{i}", foreground="green" if tarea.completada else "red")
            self.text.tag_config(f"descripcion_{i}", foreground="red", overstrike=tarea.completada)
            self.text.tag_config(f"completado_{i}", foreground="green" if tarea.completada else "blue")
            self.text.tag_config(f"lapiz_{i}", foreground="blue", underline=1)
            self.text.tag_bind(f"marca_{i}", "<Button-1>", self.toggle_completada)
            self.text.tag_bind(f"lapiz_{i}", "<Button-1>", lambda event, index=i-1: self.editar_descripcion(index))

    def borrar_finalizados(self):
        tareas_finalizadas = [tarea for tarea in self.lista_tareas if tarea.completada]
        for tarea in tareas_finalizadas:
            self.historial_tareas_borradas.append(tarea)
            self.lista_tareas.remove(tarea)
        self.actualizar_texto_tareas()

def main():
    root = tk.Tk()
    app = ListaTareasApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
