"""
reserva.py
Clase Reserva: integra cliente, servicio, duracion y estado.
Implementa confirmacion, cancelacion y procesamiento con manejo de excepciones
(try/except, try/except/else, try/except/finally y encadenamiento con 'raise ... from').
"""

# Importa la entidad base abstracta
from .entidades import EntidadBase, Cliente
# Importa la clase abstracta Servicio para validar el tipo
from .servicios import Servicio
# Importa las excepciones personalizadas
from .excepciones import (
    SoftwareFJError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    CalculoInconsistenteError,
    DatosInvalidosError,
)
# Importa el logger
from .registro_logs import obtener_logger

# Logger del modulo
log = obtener_logger()


# Clase Reserva: hereda de EntidadBase
class Reserva(EntidadBase):
    """Reserva de un servicio por parte de un cliente."""

    # Estados posibles de una reserva
    PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA = "PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"

    # Constructor: recibe cliente, servicio y duracion en horas
    def __init__(self, cliente, servicio, horas):
        # Inicializa el id
        super().__init__()
        # El cliente debe ser una instancia de Cliente
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("el cliente no es valido")
        # El servicio debe ser una instancia de Servicio
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("el servicio no es valido")
        # Guarda los atributos privados
        self.__cliente = cliente
        self.__servicio = servicio
        self.__horas = horas
        # Estado inicial
        self.__estado = Reserva.PENDIENTE
        # Costo aun no calculado
        self.__costo = None
        # Valida la reserva completa
        self.validar()
        # Registra el evento de creacion
        log.info(f"Reserva #{self.id} creada: {cliente.nombre} -> {servicio.nombre} ({horas} h)")

    # Propiedad de solo lectura del estado
    @property
    def estado(self):
        # Devuelve el estado actual
        return self.__estado

    # Propiedad de solo lectura del costo
    @property
    def costo(self):
        # Devuelve el costo calculado (o None)
        return self.__costo

    # Validacion de la reserva (metodo abstracto de EntidadBase)
    def validar(self):
        # Se intenta validar las horas con las reglas del servicio (polimorfismo)
        try:
            # Cada servicio valida sus propios parametros
            self.__servicio.validar_parametros(self.__horas)
        # Si las horas no son validas se captura el error del servicio...
        except DatosInvalidosError as error:
            # ...y se encadena en un error de reserva (encadenamiento de excepciones)
            raise ReservaInvalidaError(f"duracion no permitida para {self.__servicio.nombre}") from error
        # Si no hubo error, la reserva es valida
        return True

    # Confirma la reserva: usa try/except/else
    def confirmar(self, impuesto=None, descuento=None):
        """Confirma la reserva calculando su costo."""
        # Solo se puede confirmar una reserva pendiente
        if self.__estado != Reserva.PENDIENTE:
            raise OperacionNoPermitidaError("confirmar", self.__estado)
        try:
            # Verifica que el servicio este disponible
            self.__servicio.verificar_disponibilidad()
            # Calcula el costo (metodo sobrecargado del servicio)
            costo = self.__servicio.calcular_costo(self.__horas, impuesto=impuesto, descuento=descuento)
        except CalculoInconsistenteError as error:
            # Error de calculo: se registra y se encadena como reserva invalida
            log.error(f"Reserva #{self.id}: error de calculo -> {error}")
            raise ReservaInvalidaError("no fue posible calcular el costo") from error
        else:
            # Solo si no hubo errores: se guarda el costo y se cambia el estado
            self.__costo = costo
            self.__estado = Reserva.CONFIRMADA
            # Registra la confirmacion
            log.info(f"Reserva #{self.id} CONFIRMADA. Costo: ${costo:,.2f}")
            # Devuelve el costo calculado
            return costo

    # Cancela la reserva: usa try/except/finally
    def cancelar(self, motivo="sin motivo"):
        """Cancela la reserva si su estado lo permite."""
        try:
            # No se puede cancelar una reserva ya cancelada o procesada
            if self.__estado in (Reserva.CANCELADA, Reserva.PROCESADA):
                raise OperacionNoPermitidaError("cancelar", self.__estado)
            # Cambia el estado a cancelada
            self.__estado = Reserva.CANCELADA
            # Registra la cancelacion
            log.info(f"Reserva #{self.id} CANCELADA. Motivo: {motivo}")
        except OperacionNoPermitidaError:
            # Registra el intento invalido y relanza la excepcion
            log.error(f"Reserva #{self.id}: intento de cancelacion no permitido (estado {self.__estado})")
            raise
        finally:
            # Siempre se deja traza de la operacion, haya o no error
            log.info(f"Reserva #{self.id}: fin del intento de cancelacion")

    # Procesa la reserva (pago/ejecucion): usa try/except/else/finally
    def procesar(self):
        """Procesa una reserva confirmada."""
        try:
            # Solo se procesan reservas confirmadas
            if self.__estado != Reserva.CONFIRMADA:
                raise OperacionNoPermitidaError("procesar", self.__estado)
            # Se verifica de nuevo la disponibilidad del servicio al momento de procesar
            self.__servicio.verificar_disponibilidad()
        except SoftwareFJError as error:
            # Cualquier error del negocio se registra y se encadena
            log.error(f"Reserva #{self.id}: no se pudo procesar -> {error}")
            raise ReservaInvalidaError(f"la reserva #{self.id} no pudo procesarse") from error
        else:
            # Si todo salio bien, se marca como procesada
            self.__estado = Reserva.PROCESADA
            # Registra el exito
            log.info(f"Reserva #{self.id} PROCESADA correctamente")
        finally:
            # Siempre se registra el cierre del intento
            log.info(f"Reserva #{self.id}: fin del procesamiento (estado {self.__estado})")

    # Descripcion de la reserva
    def describir(self):
        # Texto con el cliente, servicio, horas, estado y costo
        costo = f"${self.__costo:,.2f}" if self.__costo is not None else "sin calcular"
        return (f"Reserva #{self.id}: {self.__cliente.nombre} | {self.__servicio.nombre} | "
                f"{self.__horas} h | {self.__estado} | {costo}")

    # Representacion en texto
    def __str__(self):
        # Reutiliza describir
        return self.describir()
