import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk
from tabla import generar_tabla_verdad_con_intermedios, traducir_expresion
import re

def generar_tabla():
    expresion = expresion_entry.get().strip()
    variables = variables_entry.get().replace(" ", "").split(',')
    
    # Subexpresiones predeterminadas
    subexpresiones = [
        "(p and q)", 
        "(not r or p)",
        "not s", 
        "not s or q"
    ]
    
    # Lista de operadores lógicos que deben ser ignorados
    operadores_logicos = {"and", "or", "not", "(", ")", "==", "<->", "->"}
    
    # Verificar que todas las variables necesarias están presentes
    for subexp in subexpresiones:
        for var in re.findall(r'\b\w+\b', subexp):
            if var not in variables and var not in operadores_logicos:
                messagebox.showerror("Error", f"Variable '{var}' no definida en las variables ingresadas.")
                return
    
    try:
        # Traducir la expresión antes de evaluarla
        expresion_traducida = traducir_expresion(expresion)
        subexpresiones_traducidas = [traducir_expresion(subexp) for subexp in subexpresiones]
        
        # Generar tabla de verdad
        tabla_verdad = generar_tabla_verdad_con_intermedios(variables, expresion_traducida, subexpresiones_traducidas)
        
        if tabla_verdad:
            # Mostrar la tabla en el cuadro de texto
            resultado_textbox.config(state=tk.NORMAL)
            resultado_textbox.delete(1.0, tk.END)
            resultado_textbox.insert(tk.END, tabla_verdad)
            resultado_textbox.config(state=tk.DISABLED)
            
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def iniciar_gui():
    global expresion_entry, variables_entry, resultado_textbox, root
    
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Truth Table Generator")
    root.geometry("900x600")  # Tamaño inicial adecuado
    root.configure(bg='#F0F0F0')  # Fondo suave
    
    # Estilos ttk
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", font=("Arial", 12), background='#F0F0F0')
    style.configure("TButton", font=("Arial", 12), background="#4CAF50", foreground="white")
    style.configure("TEntry", font=("Arial", 12))

    # Frame para la expresión y las variables
    frame = ttk.Frame(root, padding="10 10 10 10")
    frame.pack(fill=tk.BOTH, expand=True)

    # Etiqueta y cuadro de texto para la expresión
    ttk.Label(frame, text="Logical expression (use not, and, or, <->, ->):").grid(row=0, column=0, sticky=tk.W, pady=5)
    expresion_entry = ttk.Entry(frame, width=50)
    expresion_entry.grid(row=1, column=0, sticky=tk.W, pady=5)

    # Etiqueta y cuadro de texto para las variables
    ttk.Label(frame, text="Variables (separated by commas):").grid(row=2, column=0, sticky=tk.W, pady=5)
    variables_entry = ttk.Entry(frame, width=50)
    variables_entry.grid(row=3, column=0, sticky=tk.W, pady=5)

    # Botón para generar la tabla de verdad
    generar_btn = ttk.Button(frame, text="Generate Truth Table", command=generar_tabla)
    generar_btn.grid(row=4, column=0, pady=20)

    # Cuadro de texto con barras de desplazamiento para mostrar el resultado
    ttk.Label(frame, text="Result:").grid(row=5, column=0, sticky=tk.W, pady=5)

    # Agregar cuadro de texto con scroll horizontal y vertical
    resultado_textbox = scrolledtext.ScrolledText(frame, wrap=tk.NONE, font=("Courier", 10))
    resultado_textbox.grid(row=6, column=0, pady=5, sticky=tk.NSEW)

    # Permitir desplazamiento horizontal y vertical
    frame.grid_rowconfigure(6, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Iniciar el bucle de la interfaz gráfica
    root.mainloop()
