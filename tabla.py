from itertools import product
from tabulate import tabulate
import re

def traducir_expresion(expression):
    """
    Función que traduce conectores lógicos a operadores en Python.
    """
    # Reemplazar "<->" por su equivalente en Python: equivalencia lógica
    expression = re.sub(r'(\w+)\s*<->\s*(\w+)', r'(\1 and \2) or (not \1 and not \2)', expression)
    
    # Reemplazar "->" por la forma condicional (not A or B)
    expression = re.sub(r'(\w+)\s*->\s*(\w+)', r'(not \1 or \2)', expression)
    
    return expression

def generar_tabla_verdad_con_intermedios(variables, expresion, subexpresiones):
    """
    Genera y retorna una tabla de verdad basada en las variables y la expresión lógica dada.
    """
    combinaciones = list(product([False, True], repeat=len(variables)))

    # Encabezado de la tabla
    headers = variables + subexpresiones + ['Resultado']
    tabla = []

    # Evaluar la expresión lógica para cada combinación
    for combinacion in combinaciones:
        asignaciones = dict(zip(variables, combinacion))
        fila = list(combinacion)

        try:
            # Evaluar subexpresiones intermedias
            resultados_intermedios = [eval(subexp, {}, asignaciones) for subexp in subexpresiones]
            # Evaluar la expresión completa
            resultado_final = eval(expresion, {}, asignaciones)

            fila.extend(resultados_intermedios)
            fila.append(resultado_final)
            tabla.append(fila)
        except Exception as e:
            raise ValueError(f"Error al evaluar la expresión: {e}")

    return tabulate(tabla, headers, tablefmt="fancy_grid")
