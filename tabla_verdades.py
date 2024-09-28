
from itertools import product
import re
from tabulate import tabulate

def traducir_expresion(expression):
    """
    Función que traduce conectores lógicos en español a operadores en Python.
    Asegura que las flechas se reemplacen correctamente por operadores lógicos de Python.
    """
    # Reemplazo de operadores lógicos en texto a Python
    expression = re.sub(r'\bno\b', 'not', expression)
    expression = re.sub(r'\by\b', 'and', expression)
    expression = re.sub(r'\bo\b', 'or', expression)
    
    # Reemplazar "<->" por el operador de bicondicional "=="
    expression = re.sub(r'<->', '==', expression)  # Bicondicional (equivalencia)
    
    # Reemplazar "->" por la forma condicional (not A or B)
    expression = re.sub(r'(\w+)\s*->\s*(\w+)', r'(not \1 or \2)', expression)  # Condicional (implicación)
    
    return expression

def generar_tabla_verdad_con_intermedios(variables, expresion, subexpresiones):
    """
    Genera y muestra una tabla de verdad basada en las variables, la expresión lógica dada
    y las subexpresiones, mostrando los resultados intermedios.
    """
    # Combinaciones posibles de True y False para las variables
    num_variables = len(variables)
    combinaciones = list(product([False, True], repeat=num_variables))

    # Encabezado de la tabla
    headers = variables + subexpresiones + ['Resultado']
    tabla = []

    # Evaluar la expresión lógica para cada combinación
    for combinacion in combinaciones:
        asignaciones = dict(zip(variables, combinacion))
        fila = list(combinacion)

        try:
            # Evaluar subexpresiones intermedias
            resultados_intermedios = []
            for subexp in subexpresiones:
                resultado_intermedio = eval(subexp, {}, asignaciones)
                resultados_intermedios.append(resultado_intermedio)
            # Evaluar la expresión completa
            resultado_final = eval(expresion, {}, asignaciones)
            fila.extend(resultados_intermedios)
            fila.append(resultado_final)
            tabla.append(fila)
        except Exception as e:
            print(f"Error al evaluar la expresión: {e}")
            return

    # Imprimir la tabla de verdad de manera estética con resultados intermedios
    print(tabulate(tabla, headers, tablefmt="fancy_grid"))

def main():
    # Entrada del usuario
    expresion = input("Ingrese la expresión lógica completa (use not, and, or, <->, ->): ").strip()
    variables = input("Ingrese las variables (separadas por comas, sin límite): ").replace(" ", "").split(',')
    
    # Definir subexpresiones intermedias
    subexpresiones = [
        "(p and q)", 
        "(r -> p)",
        "not s", 
        "not s or q"
    ]
    
    # Traducir la expresión y las subexpresiones antes de generar la tabla de verdad
    expresion_traducida = traducir_expresion(expresion)
    subexpresiones_traducidas = [traducir_expresion(subexp) for subexp in subexpresiones]

    # Generar la tabla de verdad con resultados intermedios
    generar_tabla_verdad_con_intermedios(variables, expresion_traducida, subexpresiones_traducidas)

if __name__ == "__main__":
    main()
