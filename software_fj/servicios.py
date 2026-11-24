"""
servicios.py
Clase abstracta Servicio y tres servicios especializados:
ReservaSala, AlquilerEquipo y AsesoriaEspecializada.

Cada servicio sobrescribe (polimorfismo) los metodos para calcular costos,
describirse y validar parametros. El metodo calcular_costo esta "sobrecargado":
Python no permite varias firmas con el mismo nombre, asi que la sobrecarga se
implementa con parametros opcionales (impuesto, descuento) y argumentos por nombre.
"""

# Importa ABC y abstractmethod para la clase abstracta Servicio
from abc import abstractmethod

# Importa la entidad base abstracta
from .entidades import EntidadBase
# Importa las excepciones personalizadas que se usan en los servicios
from .excepciones import (
    DatosInvalidosError,
    ParametroFaltanteError,
    CalculoInconsistenteError,
    ServicioNoDisponibleError,
)
# Importa el logger del sistema
from .registro_logs import obtener_logger

# Logger del modulo
log = obtener_logger()


# Clase abstracta Servicio: hereda de EntidadBase
class Servicio(EntidadBase):
    """Servicio generico ofrecido por Software FJ."""

    # Impuesto por defecto (IVA 19 %)
    IVA = 0.19

    # Constructor comun de todos los servicios
    def __init__(self, nombre, tarifa_hora):
        # Inicializa el id de la entidad
        super().__init__()
        # Valida que el nombre exista
        if not nombre:
            raise ParametroFaltanteError("nombre del servicio")
        # Valida que la tarifa sea un numero positivo
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise DatosInvalidosError("tarifa_hora", "debe ser un numero mayor que cero")
        # Atributos protegidos del servicio
        self._nombre = nombre
        self._tarifa_hora = float(tarifa_hora)
        # Todo servicio inicia disponible
        self._disponible = True

    # Propiedad de solo lectura para el nombre
    @property
    def nombre(self):
        # Devuelve el nombre del servicio
        return self._nombre

    # Propiedad para saber si el servicio esta disponible
    @property
    def disponible(self):
        # Devuelve el estado de disponibilidad
        return self._disponible

    # Marca el servicio como no disponible (p. ej. mantenimiento)
    def deshabilitar(self):
        # Cambia la disponibilidad a False
        self._disponible = False
        # Registra el evento
        log.warning(f"Servicio deshabilitado: {self._nombre}")

    # Marca el servicio como disponible
    def habilitar(self):
        # Cambia la disponibilidad a True
        self._disponible = True
        # Registra el evento
        log.info(f"Servicio habilitado: {self._nombre}")

    # Verifica disponibilidad y lanza excepcion si no lo esta
    def verificar_disponibilidad(self):
        # Si no esta disponible se lanza ServicioNoDisponibleError
        if not self._disponible:
            raise ServicioNoDisponibleError(self._nombre)
        # Si esta disponible devuelve True
        return True

    # Metodo abstracto: costo base segun la duracion (cada servicio lo calcula distinto)
    @abstractmethod
    def costo_base(self, horas):
        """Calcula el costo base del servicio para la cantidad de horas indicada."""

    # Metodo abstracto: validacion de parametros propios de cada servicio
    @abstractmethod
    def validar_parametros(self, horas):
        """Valida los parametros de uso del servicio (horas, capacidad, etc.)."""

    # Implementacion general de validar (de EntidadBase)
    def validar(self):
        # Un servicio es valido si tiene nombre y tarifa positiva
        return bool(self._nombre) and self._tarifa_hora > 0

    # Metodo "sobrecargado": admite 3 variantes de llamada
    #   calcular_costo(horas)                       -> costo con IVA
    #   calcular_costo(horas, impuesto=0.0)         -> costo con impuesto personalizado
    #   calcular_costo(horas, descuento=0.10)       -> costo con descuento
    #   calcular_costo(horas, impuesto=x, descuento=y) -> ambas
    def calcular_costo(self, horas, impuesto=None, descuento=None):
        """Calcula el costo total aplicando impuesto y/o descuento opcionales."""
        # Valida los parametros propios del servicio (polimorfismo)
        self.validar_parametros(horas)
        # Si no se envia impuesto se usa el IVA por defecto
        impuesto = Servicio.IVA if impuesto is None else impuesto
        # Si no se envia descuento se usa 0
        descuento = 0.0 if descuento is None else descuento
        # El impuesto debe estar entre 0 y 1
        if not 0 <= impuesto <= 1:
            raise CalculoInconsistenteError(f"impuesto fuera de rango ({impuesto})")
        # El descuento debe estar entre 0 y 0.5 (maximo 50 %)
        if not 0 <= descuento <= 0.5:
            raise CalculoInconsistenteError(f"descuento fuera de rango ({descuento})")
        # Calcula el costo base usando la implementacion de la subclase
        base = self.costo_base(horas)
        # Aplica el descuento y luego el impuesto
        total = base * (1 - descuento) * (1 + impuesto)
        # Un total negativo o cero indica un calculo inconsistente
        if total <= 0:
            raise CalculoInconsistenteError(f"total no positivo ({total})")
        # Devuelve el total redondeado a 2 decimales
        return round(total, 2)

    # Representacion en texto del servicio
    def __str__(self):
        # Reutiliza describir (polimorfico)
        return self.describir()


# Servicio especializado 1: reserva de salas
class ReservaSala(Servicio):
    """Reserva de salas de reuniones con capacidad maxima."""

    # Constructor: agrega la capacidad de la sala
    def __init__(self, nombre, tarifa_hora, capacidad):
        # Inicializa la parte comun del servicio
        super().__init__(nombre, tarifa_hora)
        # Valida la capacidad (entero positivo)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError("capacidad", "debe ser un entero positivo")
        # Guarda la capacidad
        self._capacidad = capacidad
        # Registra el evento
        log.info(f"Servicio creado: {self.describir()}")

    # Sobrescribe costo_base: tarifa por hora, con recargo si supera 8 horas
    def costo_base(self, horas):
        # Costo normal por horas
        costo = self._tarifa_hora * horas
        # Recargo del 10 % para reservas de mas de 8 horas
        return costo * 1.10 if horas > 8 else costo

    # Sobrescribe validar_parametros: entre 1 y 12 horas
    def validar_parametros(self, horas):
        # Verifica tipo y rango de las horas
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 12:
            raise DatosInvalidosError("horas", "una sala se reserva entre 1 y 12 horas")
        # Devuelve True si es valido
        return True

    # Sobrescribe describir
    def describir(self):
        # Descripcion particular de la sala
        return f"Sala '{self._nombre}' (cap. {self._capacidad}) - ${self._tarifa_hora:,.0f}/h"


# Servicio especializado 2: alquiler de equipos
class AlquilerEquipo(Servicio):
    """Alquiler de equipos (portatiles, proyectores) con deposito fijo."""

    # Constructor: agrega el tipo de equipo y el deposito
    def __init__(self, nombre, tarifa_hora, tipo_equipo, deposito=50000):
        # Inicializa la parte comun
        super().__init__(nombre, tarifa_hora)
        # Valida que se indique el tipo de equipo
        if not tipo_equipo:
            raise ParametroFaltanteError("tipo_equipo")
        # Valida que el deposito no sea negativo
        if deposito < 0:
            raise DatosInvalidosError("deposito", "no puede ser negativo")
        # Guarda los atributos propios
        self._tipo_equipo = tipo_equipo
        self._deposito = deposito
        # Registra el evento
        log.info(f"Servicio creado: {self.describir()}")

    # Sobrescribe costo_base: tarifa por hora mas deposito fijo
    def costo_base(self, horas):
        # Suma el deposito al costo por horas
        return self._tarifa_hora * horas + self._deposito

    # Sobrescribe validar_parametros: entre 1 y 72 horas
    def validar_parametros(self, horas):
        # Verifica tipo y rango
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 72:
            raise DatosInvalidosError("horas", "un equipo se alquila entre 1 y 72 horas")
        # Devuelve True si es valido
        return True

    # Sobrescribe describir
    def describir(self):
        # Descripcion particular del equipo
        return f"Equipo '{self._nombre}' ({self._tipo_equipo}) - ${self._tarifa_hora:,.0f}/h + deposito"


# Servicio especializado 3: asesorias especializadas
class AsesoriaEspecializada(Servicio):
    """Asesoria con un especialista; el nivel define un multiplicador de tarifa."""

    # Multiplicadores de tarifa segun el nivel del asesor
    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    # Constructor: agrega el area y el nivel del asesor
    def __init__(self, nombre, tarifa_hora, area, nivel="junior"):
        # Inicializa la parte comun
        super().__init__(nombre, tarifa_hora)
        # Valida que el area exista
        if not area:
            raise ParametroFaltanteError("area")
        # Valida que el nivel sea uno de los permitidos
        if nivel not in AsesoriaEspecializada.NIVELES:
            raise DatosInvalidosError("nivel", f"debe ser uno de {list(self.NIVELES)}")
        # Guarda los atributos propios
        self._area = area
        self._nivel = nivel
        # Registra el evento
        log.info(f"Servicio creado: {self.describir()}")

    # Sobrescribe costo_base: tarifa x horas x multiplicador del nivel
    def costo_base(self, horas):
        # Aplica el multiplicador del nivel
        return self._tarifa_hora * horas * AsesoriaEspecializada.NIVELES[self._nivel]

    # Sobrescribe validar_parametros: entre 1 y 6 horas por sesion
    def validar_parametros(self, horas):
        # Verifica tipo y rango
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 6:
            raise DatosInvalidosError("horas", "una asesoria dura entre 1 y 6 horas")
        # Devuelve True si es valido
        return True

    # Sobrescribe describir
    def describir(self):
        # Descripcion particular de la asesoria
        return f"Asesoria '{self._nombre}' en {self._area} (nivel {self._nivel}) - ${self._tarifa_hora:,.0f}/h"
