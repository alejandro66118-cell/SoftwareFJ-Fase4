"""
main.py
Programa principal de Software FJ - Fase 4 (Programacion 213023, UNAD).

Simula mas de 10 operaciones completas (validas e invalidas) para demostrar que
el sistema continua funcionando aunque ocurran errores. Todos los eventos y
errores quedan registrados en 'software_fj.log'.

Ejecucion:  python main.py
"""

# Importa el gestor del sistema
from software_fj.sistema import SistemaFJ
# Importa los tres servicios especializados
from software_fj.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
# Importa la ruta del log para mostrarla al final
from software_fj.registro_logs import obtener_logger, RUTA_LOG

# Logger principal
log = obtener_logger()


# Funcion auxiliar para imprimir el titulo de cada simulacion
def titulo(numero, texto):
    # Imprime el encabezado de la simulacion
    print(f"\n--- Simulacion {numero}: {texto} ---")
    # Registra el inicio de la simulacion en el log
    log.info(f"=== Simulacion {numero}: {texto} ===")


# Funcion principal que ejecuta todas las simulaciones
def main():
    # Registra el inicio de la ejecucion
    log.info("========== INICIO DE EJECUCION SOFTWARE FJ ==========")
    # Crea el sistema con sus listas internas vacias
    sistema = SistemaFJ()

    # 1. Registro de clientes validos
    titulo(1, "Registro de clientes validos")
    ana = sistema.registrar_cliente(documento="1023456789", nombre="ana torres",
                                    correo="ana.torres@correo.com", telefono="3104567890")
    luis = sistema.registrar_cliente(documento="80123456", nombre="Luis Pardo",
                                     correo="lpardo@empresa.co")

    # 2. Registro de clientes invalidos (correo mal escrito, documento con letras, nombre faltante)
    titulo(2, "Registro de clientes invalidos")
    sistema.registrar_cliente(documento="12345678", nombre="Carlos Ruiz", correo="carlos-arroba-mail")
    sistema.registrar_cliente(documento="ABC123", nombre="Maria Gil", correo="maria@mail.com")
    sistema.registrar_cliente(documento="99887766", nombre=None, correo="sin@nombre.com")

    # 3. Creacion correcta de los tres tipos de servicio
    titulo(3, "Creacion correcta de servicios")
    sala = sistema.crear_servicio(ReservaSala, "Sala Bogota", 80000, capacidad=12)
    portatil = sistema.crear_servicio(AlquilerEquipo, "Portatil Dell", 15000, tipo_equipo="Portatil")
    asesoria = sistema.crear_servicio(AsesoriaEspecializada, "Asesoria BI", 120000, area="Power BI", nivel="senior")

    # 4. Creacion incorrecta de servicios (tarifa negativa, nivel inexistente, capacidad invalida)
    titulo(4, "Creacion incorrecta de servicios")
    sistema.crear_servicio(ReservaSala, "Sala Fantasma", -5000, capacidad=10)
    sistema.crear_servicio(AsesoriaEspecializada, "Asesoria X", 100000, area="Redes", nivel="maestro")
    sistema.crear_servicio(ReservaSala, "Sala Mini", 50000, capacidad=0)

    # 5. Reserva exitosa con costo por defecto (IVA 19 %) y procesamiento
    titulo(5, "Reserva exitosa: confirmar y procesar")
    r1 = sistema.crear_reserva(ana, sala, 4)
    sistema.confirmar_reserva(r1)
    sistema.procesar_reserva(r1)

    # 6. Reserva con metodo sobrecargado: descuento del 10 % y sin impuesto
    titulo(6, "Costo con descuento y sin impuesto (sobrecarga)")
    r2 = sistema.crear_reserva(luis, asesoria, 2)
    sistema.confirmar_reserva(r2, impuesto=0.0, descuento=0.10)

    # 7. Reserva con duracion invalida (encadenamiento: DatosInvalidos -> ReservaInvalida)
    titulo(7, "Reserva con duracion invalida")
    sistema.crear_reserva(ana, asesoria, 10)

    # 8. Reserva con cliente inexistente (fallo en el registro previo)
    titulo(8, "Reserva con cliente invalido")
    sistema.crear_reserva(None, portatil, 5)

    # 9. Servicio no disponible: se deshabilita y luego se intenta confirmar
    titulo(9, "Servicio no disponible")
    r3 = sistema.crear_reserva(luis, portatil, 24)
    portatil.deshabilitar()
    sistema.confirmar_reserva(r3)
    portatil.habilitar()
    sistema.confirmar_reserva(r3)

    # 10. Calculo inconsistente: descuento del 80 % (fuera de rango)
    titulo(10, "Calculo inconsistente (descuento excesivo)")
    r4 = sistema.crear_reserva(ana, portatil, 8)
    sistema.confirmar_reserva(r4, descuento=0.80)

    # 11. Operaciones no permitidas: cancelar dos veces y procesar una cancelada
    titulo(11, "Operaciones no permitidas sobre una reserva")
    sistema.cancelar_reserva(r4, motivo="cliente desiste")
    sistema.cancelar_reserva(r4)
    sistema.procesar_reserva(r4)

    # 12. Procesar una reserva que no ha sido confirmada y confirmar una inexistente
    titulo(12, "Procesar sin confirmar / confirmar reserva inexistente")
    r5 = sistema.crear_reserva(luis, sala, 9)
    sistema.procesar_reserva(r5)
    sistema.confirmar_reserva(None)
    sistema.confirmar_reserva(r5)
    sistema.procesar_reserva(r5)

    # Muestra el resumen final: la aplicacion llego hasta aqui sin detenerse
    sistema.resumen()
    print(f"\nEl sistema termino sin interrupciones. Revise el log en: {RUTA_LOG}")
    # Registra el fin de la ejecucion
    log.info("========== FIN DE EJECUCION SOFTWARE FJ ==========")


# Punto de entrada: solo se ejecuta si el archivo se corre directamente
if __name__ == "__main__":
    main()
