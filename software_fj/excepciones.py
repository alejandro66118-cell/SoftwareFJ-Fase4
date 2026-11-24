"""
excepciones.py
Excepciones personalizadas del sistema Software FJ.

Se define una jerarquia propia de excepciones para que cada tipo de error
del negocio pueda capturarse de forma especifica, registrarse en el log
y permitir que la aplicacion siga funcionando.
"""


# Clase base de todas las excepciones del sistema; hereda de Exception
class SoftwareFJError(Exception):
    """Excepcion raiz del sistema Software FJ."""

    # Constructor: recibe el mensaje y un codigo opcional de error
    def __init__(self, mensaje, codigo="FJ-000"):
        # Llama al constructor de Exception para guardar el mensaje
        super().__init__(mensaje)
        # Guarda el codigo de error para identificarlo en los logs
        self.codigo = codigo

    # Representacion en texto: incluye el codigo y el mensaje
    def __str__(self):
        # Devuelve el texto con formato [codigo] mensaje
        return f"[{self.codigo}] {super().__str__()}"


# Error de validacion de datos (cliente, servicio o reserva con datos invalidos)
class DatosInvalidosError(SoftwareFJError):
    """Se lanza cuando un dato no cumple las reglas de validacion."""

    # Constructor: recibe el campo que fallo y el motivo
    def __init__(self, campo, motivo):
        # Guarda el nombre del campo invalido
        self.campo = campo
        # Construye el mensaje y asigna el codigo FJ-100
        super().__init__(f"Dato invalido en '{campo}': {motivo}", "FJ-100")


# Error cuando falta un parametro obligatorio
class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando no se envia un parametro requerido."""

    # Constructor: recibe el nombre del parametro faltante
    def __init__(self, parametro):
        # Construye el mensaje y asigna el codigo FJ-110
        super().__init__(f"Falta el parametro obligatorio '{parametro}'", "FJ-110")


# Error cuando un servicio no esta disponible para reservar
class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar un servicio inactivo u ocupado."""

    # Constructor: recibe el nombre del servicio
    def __init__(self, nombre_servicio):
        # Construye el mensaje y asigna el codigo FJ-200
        super().__init__(f"El servicio '{nombre_servicio}' no esta disponible", "FJ-200")


# Error de reserva (estado incorrecto, duracion invalida, etc.)
class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva no puede crearse o procesarse."""

    # Constructor: recibe el motivo del fallo
    def __init__(self, motivo):
        # Construye el mensaje y asigna el codigo FJ-300
        super().__init__(f"Reserva invalida: {motivo}", "FJ-300")


# Error de operacion no permitida (p. ej. cancelar una reserva ya cancelada)
class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se intenta una operacion que el estado actual no permite."""

    # Constructor: recibe la operacion y el estado actual
    def __init__(self, operacion, estado):
        # Construye el mensaje y asigna el codigo FJ-310
        super().__init__(
            f"No se permite '{operacion}' cuando la reserva esta en estado '{estado}'",
            "FJ-310",
        )


# Error de calculo (costos negativos, impuestos fuera de rango, etc.)
class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un calculo de costos produce un resultado inconsistente."""

    # Constructor: recibe el detalle del problema de calculo
    def __init__(self, detalle):
        # Construye el mensaje y asigna el codigo FJ-400
        super().__init__(f"Calculo inconsistente: {detalle}", "FJ-400")
