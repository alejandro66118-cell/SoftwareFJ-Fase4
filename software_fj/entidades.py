"""
entidades.py
Clase abstracta EntidadBase y clase Cliente del sistema Software FJ.
"""

# Importa ABC y abstractmethod para definir clases abstractas
from abc import ABC, abstractmethod
# Importa re para validar correos y telefonos con expresiones regulares
import re
# Importa itertools.count para generar identificadores consecutivos
from itertools import count

# Importa las excepciones personalizadas que usa este modulo
from .excepciones import DatosInvalidosError, ParametroFaltanteError
# Importa la funcion que entrega el logger configurado
from .registro_logs import obtener_logger

# Logger del modulo para registrar eventos y errores
log = obtener_logger()


# Clase abstracta que representa cualquier entidad general del sistema
class EntidadBase(ABC):
    """Entidad general: todo objeto del sistema tiene un id y sabe describirse y validarse."""

    # Contador compartido para asignar ids unicos a cada entidad
    _contador_ids = count(1)

    # Constructor comun de todas las entidades
    def __init__(self):
        # Asigna un identificador unico y privado a la entidad
        self.__id = next(EntidadBase._contador_ids)

    # Propiedad de solo lectura para consultar el id (encapsulacion)
    @property
    def id(self):
        # Devuelve el id privado
        return self.__id

    # Metodo abstracto: cada entidad debe definir como se describe
    @abstractmethod
    def describir(self):
        """Devuelve una descripcion en texto de la entidad."""

    # Metodo abstracto: cada entidad debe definir sus validaciones
    @abstractmethod
    def validar(self):
        """Valida el estado interno de la entidad y lanza excepcion si es invalido."""


# Clase Cliente: hereda de EntidadBase y encapsula los datos personales
class Cliente(EntidadBase):
    """Cliente de Software FJ con validaciones robustas de sus datos."""

    # Patron para validar correos electronicos basicos
    _PATRON_CORREO = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$")
    # Patron para validar telefonos de 7 a 10 digitos
    _PATRON_TELEFONO = re.compile(r"^\d{7,10}$")

    # Constructor: recibe documento, nombre, correo y telefono
    def __init__(self, documento=None, nombre=None, correo=None, telefono=None):
        # Inicializa la parte comun (id) de la entidad
        super().__init__()
        # Asigna cada dato a traves de su setter para que se valide
        self.documento = documento
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        # Valida el objeto completo una vez asignados los datos
        self.validar()
        # Registra en el log que el cliente se creo correctamente
        log.info(f"Cliente registrado: {self.nombre} (doc {self.documento})")

    # ----- Propiedades con validacion (encapsulacion de datos personales) -----

    # Getter del documento
    @property
    def documento(self):
        # Devuelve el documento almacenado en el atributo privado
        return self.__documento

    # Setter del documento: obligatorio y solo digitos (6 a 10)
    @documento.setter
    def documento(self, valor):
        # Si no se envio el documento se lanza ParametroFaltanteError
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("documento")
        # Convierte a texto y quita espacios
        valor = str(valor).strip()
        # Verifica que solo tenga digitos y longitud valida
        if not valor.isdigit() or not 6 <= len(valor) <= 10:
            raise DatosInvalidosError("documento", "debe tener entre 6 y 10 digitos")
        # Guarda el valor en el atributo privado
        self.__documento = valor

    # Getter del nombre
    @property
    def nombre(self):
        # Devuelve el nombre privado
        return self.__nombre

    # Setter del nombre: obligatorio, minimo 3 letras, sin numeros
    @nombre.setter
    def nombre(self, valor):
        # Verifica que el nombre exista
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("nombre")
        # Quita espacios al inicio y al final
        valor = str(valor).strip()
        # Verifica longitud minima y que no contenga numeros
        if len(valor) < 3 or any(c.isdigit() for c in valor):
            raise DatosInvalidosError("nombre", "minimo 3 caracteres y sin numeros")
        # Guarda el nombre en formato titulo
        self.__nombre = valor.title()

    # Getter del correo
    @property
    def correo(self):
        # Devuelve el correo privado
        return self.__correo

    # Setter del correo: obligatorio y con formato valido
    @correo.setter
    def correo(self, valor):
        # Verifica que el correo exista
        if not valor:
            raise ParametroFaltanteError("correo")
        # Verifica el formato con la expresion regular
        if not Cliente._PATRON_CORREO.match(str(valor)):
            raise DatosInvalidosError("correo", f"formato no valido ({valor})")
        # Guarda el correo en minusculas
        self.__correo = str(valor).lower()

    # Getter del telefono
    @property
    def telefono(self):
        # Devuelve el telefono privado
        return self.__telefono

    # Setter del telefono: opcional, pero si se envia debe ser valido
    @telefono.setter
    def telefono(self, valor):
        # Si no se envia telefono se guarda None (es opcional)
        if valor in (None, ""):
            self.__telefono = None
            return
        # Verifica que tenga entre 7 y 10 digitos
        if not Cliente._PATRON_TELEFONO.match(str(valor)):
            raise DatosInvalidosError("telefono", "debe tener entre 7 y 10 digitos")
        # Guarda el telefono como texto
        self.__telefono = str(valor)

    # Implementacion del metodo abstracto validar
    def validar(self):
        # Los setters ya validan cada campo; aqui se verifica que los obligatorios existan
        for campo in ("documento", "nombre", "correo"):
            # Si algun campo obligatorio quedo vacio se lanza la excepcion
            if not getattr(self, campo, None):
                raise ParametroFaltanteError(campo)
        # Si todo esta bien devuelve True
        return True

    # Implementacion del metodo abstracto describir
    def describir(self):
        # Devuelve una descripcion corta del cliente (sin exponer el telefono)
        return f"Cliente #{self.id}: {self.nombre} - {self.correo}"

    # Representacion del objeto en texto
    def __str__(self):
        # Reutiliza el metodo describir
        return self.describir()
