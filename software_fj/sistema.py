"""
sistema.py
Clase SistemaFJ: administra clientes, servicios y reservas en listas internas
(sin base de datos). Cada operacion captura sus excepciones, las registra en el
log y devuelve None para que la aplicacion siga funcionando.
"""

# Importa las clases del dominio
from .entidades import Cliente
from .reserva import Reserva
# Importa la excepcion raiz para capturar cualquier error del negocio
from .excepciones import SoftwareFJError
# Importa el logger
from .registro_logs import obtener_logger

# Logger del modulo
log = obtener_logger()


# Clase que coordina toda la operacion de Software FJ
class SistemaFJ:
    """Gestor central de clientes, servicios y reservas."""

    # Constructor: crea las listas internas vacias
    def __init__(self):
        # Lista interna de clientes
        self.clientes = []
        # Lista interna de servicios
        self.servicios = []
        # Lista interna de reservas
        self.reservas = []
        # Contadores de operaciones exitosas y fallidas
        self.exitos = 0
        self.fallos = 0

    # Metodo privado que ejecuta cualquier operacion de forma segura
    def _ejecutar(self, descripcion, funcion, *args, **kwargs):
        """Ejecuta 'funcion' capturando errores para que el sistema nunca se detenga."""
        try:
            # Intenta ejecutar la operacion solicitada
            resultado = funcion(*args, **kwargs)
        except SoftwareFJError as error:
            # Error controlado del negocio: se registra con su causa (si fue encadenado)
            causa = f" | causa: {error.__cause__}" if error.__cause__ else ""
            log.error(f"{descripcion} FALLIDA -> {error}{causa}")
            # Se informa en consola y se cuenta el fallo
            print(f"   [X] {descripcion}: {error}{causa}")
            self.fallos += 1
            # Devuelve None para indicar fallo sin detener la app
            return None
        except Exception as error:
            # Error inesperado: tambien se registra con traza completa
            log.exception(f"{descripcion} ERROR INESPERADO -> {error!r}")
            print(f"   [!] {descripcion}: error inesperado {error!r}")
            self.fallos += 1
            return None
        else:
            # Solo si no hubo error se cuenta el exito
            self.exitos += 1
            print(f"   [OK] {descripcion}")
            # Devuelve el resultado de la operacion
            return resultado

    # Registra un cliente y lo agrega a la lista interna
    def registrar_cliente(self, **datos):
        # Ejecuta la creacion del cliente de forma segura
        cliente = self._ejecutar(f"Registrar cliente {datos.get('nombre')}", Cliente, **datos)
        # Si se creo correctamente se agrega a la lista
        if cliente:
            self.clientes.append(cliente)
        # Devuelve el cliente o None
        return cliente

    # Crea un servicio de la clase indicada y lo agrega a la lista
    def crear_servicio(self, clase, *args, **kwargs):
        # Ejecuta la creacion del servicio de forma segura
        servicio = self._ejecutar(f"Crear servicio {clase.__name__} '{args[0] if args else '?'}'",
                                  clase, *args, **kwargs)
        # Si se creo correctamente se agrega a la lista
        if servicio:
            self.servicios.append(servicio)
        # Devuelve el servicio o None
        return servicio

    # Crea una reserva y la agrega a la lista
    def crear_reserva(self, cliente, servicio, horas):
        # Nombre legible para el log aunque cliente o servicio sean None
        nombre_c = getattr(cliente, "nombre", cliente)
        nombre_s = getattr(servicio, "nombre", servicio)
        # Ejecuta la creacion de la reserva de forma segura
        reserva = self._ejecutar(f"Crear reserva {nombre_c} -> {nombre_s} ({horas} h)",
                                 Reserva, cliente, servicio, horas)
        # Si se creo correctamente se agrega a la lista
        if reserva:
            self.reservas.append(reserva)
        # Devuelve la reserva o None
        return reserva

    # Confirma una reserva existente (admite impuesto y descuento opcionales)
    def confirmar_reserva(self, reserva, **kwargs):
        # Si la reserva no existe se registra el fallo sin detener la app
        if reserva is None:
            log.warning("Se intento confirmar una reserva inexistente")
            print("   [X] Confirmar reserva: la reserva no existe")
            self.fallos += 1
            return None
        # Ejecuta la confirmacion de forma segura
        return self._ejecutar(f"Confirmar reserva #{reserva.id}", reserva.confirmar, **kwargs)

    # Cancela una reserva existente
    def cancelar_reserva(self, reserva, motivo="solicitud del cliente"):
        # Ejecuta la cancelacion de forma segura
        return self._ejecutar(f"Cancelar reserva #{reserva.id}", reserva.cancelar, motivo)

    # Procesa una reserva existente
    def procesar_reserva(self, reserva):
        # Ejecuta el procesamiento de forma segura
        return self._ejecutar(f"Procesar reserva #{reserva.id}", reserva.procesar)

    # Muestra un resumen del estado del sistema
    def resumen(self):
        # Imprime totales y el detalle de cada reserva
        print("\n================ RESUMEN DEL SISTEMA ================")
        print(f"Clientes registrados: {len(self.clientes)}")
        print(f"Servicios creados:    {len(self.servicios)}")
        print(f"Reservas creadas:     {len(self.reservas)}")
        print(f"Operaciones exitosas: {self.exitos} | fallidas (controladas): {self.fallos}")
        # Recorre la lista de reservas y muestra cada una (polimorfismo de describir)
        for reserva in self.reservas:
            print("  -", reserva)
        # Registra el resumen en el log
        log.info(f"Resumen: {self.exitos} exitos, {self.fallos} fallos controlados")
