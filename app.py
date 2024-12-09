from flask import Flask, render_template, request, url_for

app = Flask(__name__)

# Constantes COCOMO
COCOMO_CONSTANTS = {
    'organico': {'a': 2.4, 'b': 1.05, 'c': 2.5, 'd': 0.38},
    'semi_aplicado': {'a': 3.0, 'b': 1.12, 'c': 2.5, 'd': 0.35},
    'acoplado': {'a': 3.6, 'b': 1.20, 'c': 2.5, 'd': 0.32}
}


@app.route('/', methods=['GET'])
def index():
    """
    Ruta para mostrar el formulario al usuario.
    """
    return render_template('index.html')


@app.route('/results', methods=['POST'])
def results():
    """
    Ruta para procesar los datos enviados y mostrar los resultados.
    """
    try:
        # Recopilación de datos del formulario
        entrada = float(request.form.get('entrada'))
        salida = float(request.form.get('salida'))
        total = entrada + salida

        # Validaciones de factores
        factor_organico = float(request.form.get('factor_organico'))
        factor_semi_aplicado = float(request.form.get('factor_semi_aplicado'))
        factor_acoplado = float(request.form.get('factor_acoplado'))

        # Validación de rangos
        if not (50 <= factor_organico <= 80):
            return render_template('index.html', error="El factor Orgánico debe estar entre 50 y 80.")
        if not (81 <= factor_semi_aplicado <= 100):
            return render_template('index.html', error="El factor Semi Aplicado debe estar entre 81 y 100.")
        if not (101 <= factor_acoplado <= 150):
            return render_template('index.html', error="El factor Acoplado debe estar entre 101 y 150.")

        # Determinar el tipo de cálculo de acuerdo con el tipo de proyecto
        tipo_proyecto = request.form.get('tipo_proyecto')
        if tipo_proyecto == 'organico':
            ldc = factor_organico * total
        elif tipo_proyecto == 'semi_aplicado':
            ldc = factor_semi_aplicado * total
        elif tipo_proyecto == 'acoplado':
            ldc = factor_acoplado * total

        mldc = ldc / 1000  # Conversión a MLOC

        # Constantes COCOMO
        a = COCOMO_CONSTANTS[tipo_proyecto]['a']
        b = COCOMO_CONSTANTS[tipo_proyecto]['b']
        c = COCOMO_CONSTANTS[tipo_proyecto]['c']
        d = COCOMO_CONSTANTS[tipo_proyecto]['d']

        # Cálculo de esfuerzo
        esfuerzo = a * (mldc ** b)
        esfuerzo_redondeado = round(esfuerzo)
        esfuerzo_str = f"{esfuerzo_redondeado} PERSONAS POR MES"

        # Tiempo en meses
        td = c * (esfuerzo ** d)
        td_redondeado = round(td)
        td_str = f"{td_redondeado} MESES DE TRABAJO"

        # Cálculo de la cantidad de personas asignadas
        cp = round(esfuerzo / td)
        cp_str = f"{cp} PERSONAS"

        # LDC por mes
        p = round(ldc / esfuerzo)
        p_str = f"{p} LDC CADA MES A REALIZAR"

        # Salarios y costo total
        salario = float(request.form.get('salario'))
        costo = round(esfuerzo * salario, 2)

        costo_ldc = round(costo / ldc, 2)

        # Renderizar resultados en la plantilla
        return render_template(
            'results.html',
            total=total,
            ldc=ldc,
            mldc=mldc,
            esfuerzo=esfuerzo_str,
            td=td_str,
            cp=cp_str,
            p=p_str,
            costo=costo,
            costo_ldc=costo_ldc
        )
    except Exception as e:
        # Manejo de errores
        return render_template('index.html', error=f"Ocurrió un error: {str(e)}")


if __name__ == '__main__':
    app.run(debug=True)
