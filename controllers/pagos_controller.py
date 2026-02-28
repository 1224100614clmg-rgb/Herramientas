from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.paypal_service import PayPalService
from datetime import datetime

pagos_bp = Blueprint('pagos', __name__, url_prefix='/pagos')

# ================== DATOS SIMULADOS ==================
# Estos serían daños registrados por el laboratorista
danos_pendientes_demo = {
    1: {
       'nombre': 'Osciloscopio Digital',
        'solicitud_id': 1,
        'alumno': 'Claudia Lizbeth Méndez Galván',
        'num_control': '1224100614',   
        'monto_deposito': 500.00,
        'moneda': 'MXN',
        'descripcion': 'Pantalla rayada',
        'estado_pago': 'Pendiente'
    },
    2: {
        'nombre': 'Multímetro Profesional',
        'solicitud_id': 8,
        'alumno': 'María García',
        'num_control': '123457',
        'monto_deposito': 200.00,
        'moneda': 'MXN',
        'descripcion': 'Cable roto',
        'estado_pago': 'Pendiente'
    }
}
# =====================================================


@pagos_bp.route('/mis-danos')
def mis_danos():
    """El ALUMNO ve sus daños pendientes de pago"""
    if 'usuario' not in session or session.get('rol') != 'alumno':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('index'))

    # Filtrar solo los daños del alumno logueado
    mis = {k: v for k, v in danos_pendientes_demo.items()
           if v['num_control'] == session['usuario']}

    return render_template('mis_danos.html', danos=mis, usuario=session['nombre'])


@pagos_bp.route('/crear/<int:solicitud_id>', methods=['GET', 'POST'])
def crear_pago(solicitud_id):
    """El ALUMNO inicia el pago de su daño"""
    if 'usuario' not in session or session.get('rol') != 'alumno':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            paypal_service = PayPalService()
            amount = request.form.get('amount')
            currency = request.form.get('currency', 'MXN')
            herramienta_nombre = request.form.get('herramienta_nombre')

            description = f"Pago de daño: {herramienta_nombre} - Solicitud #{solicitud_id}"
            return_url = url_for('pagos.ejecutar_pago', _external=True)
            cancel_url = url_for('pagos.cancelar_pago', _external=True)

            success, result = paypal_service.create_payment(
                amount=amount,
                currency=currency,
                description=description,
                return_url=return_url,
                cancel_url=cancel_url,
                solicitud_id=solicitud_id
            )

            if success:
                for link in result.get('links', []):
                    if link.get('rel') == 'approve':
                        return redirect(link.get('href'))
                flash('No se encontró URL de aprobación', 'error')
            else:
                flash(f'Error PayPal: {result}', 'error')

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

        return redirect(url_for('pagos.mis_danos'))

    # GET — mostrar confirmación antes de pagar
    dano = None
    for d in danos_pendientes_demo.values():
        if d['solicitud_id'] == solicitud_id:
            dano = d
            break

    return render_template(
        'realizar_pago_herramienta.html',
        solicitud={'id': solicitud_id},
        herramienta=dano
    )


@pagos_bp.route('/ejecutar')
def ejecutar_pago():
    """Callback de PayPal — puede ser cualquier rol autenticado"""
    if 'usuario' not in session:
        flash('Sesión expirada', 'error')
        return redirect(url_for('index'))

    try:
        paypal_service = PayPalService()
        order_id = request.args.get('token')

        if not order_id:
            flash('Orden no encontrada', 'error')
            return redirect(url_for('pagos.mis_danos'))

        success, result = paypal_service.capture_payment(order_id)

        if success:
            flash('¡Pago completado exitosamente!', 'success')
            return render_template('pago_exitoso.html', pago=result)
        else:
            flash('Error al capturar el pago', 'error')
            return redirect(url_for('pagos.mis_danos'))

    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('pagos.mis_danos'))


@pagos_bp.route('/cancelar')
def cancelar_pago():
    flash('Pago cancelado', 'warning')
    return render_template('pago_cancelado.html')


# ── Vista solo para el LABORATORISTA: ver qué daños ya fueron pagados ──
@pagos_bp.route('/reporte-danos')
def reporte_danos():
    if 'usuario' not in session or session.get('rol') != 'laboratorista':
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('index'))

    return render_template('reporte_danos.html',
                           danos=danos_pendientes_demo,
                           usuario=session['nombre'])