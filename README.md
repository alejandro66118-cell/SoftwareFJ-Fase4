# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

**Curso:** Programación (213023) – UNAD, ECBTI · **Fase 4:** Componente práctico – Prácticas simuladas
**Autor:** Alejandro Rincón García · **Entrega:** individual

Aplicación orientada a objetos en Python, **sin base de datos**, que gestiona clientes, servicios
(reserva de salas, alquiler de equipos y asesorías especializadas) y reservas de la empresa
Software FJ, con manejo robusto de excepciones y registro de eventos en un archivo de logs.

## Cómo ejecutar

Requiere Python 3.10 o superior (no usa librerías externas).

```bash
python main.py
```

También se puede abrir `SoftwareFJ_Fase4.ipynb` en Jupyter o Google Colab y ejecutar todas las celdas.
Al terminar se genera/actualiza el archivo `software_fj.log`.

## Estructura

```
SoftwareFJ-Fase4/
├── main.py                    # Programa principal: 12 simulaciones (válidas e inválidas)
├── SoftwareFJ_Fase4.ipynb     # Misma solución en formato notebook
├── software_fj/
│   ├── excepciones.py         # Jerarquía de excepciones personalizadas
│   ├── registro_logs.py       # Configuración del archivo de logs
│   ├── entidades.py           # Clase abstracta EntidadBase y clase Cliente
│   ├── servicios.py           # Clase abstracta Servicio + 3 servicios especializados
│   ├── reserva.py             # Clase Reserva (confirmar, cancelar, procesar)
│   └── sistema.py             # Gestor con listas internas (clientes, servicios, reservas)
└── software_fj.log            # Log de ejemplo generado por una ejecución
```

## Cumplimiento de requisitos (Anexo 3)

| Requisito | Dónde se implementa |
|---|---|
| Clase abstracta de entidades generales | `EntidadBase` (ABC) en `entidades.py` |
| Cliente con validaciones y encapsulación | `Cliente`: atributos privados + `@property`/setters con validación |
| Clase abstracta `Servicio` + 3 servicios | `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| Polimorfismo / métodos sobrescritos | `costo_base`, `validar_parametros`, `describir` en cada servicio |
| Métodos sobrecargados | `calcular_costo(horas, impuesto=None, descuento=None)` con variantes |
| Clase `Reserva` (confirmar, cancelar, procesar) | `reserva.py` |
| Excepciones personalizadas | `SoftwareFJError` y 6 subclases en `excepciones.py` |
| `try/except` | `SistemaFJ._ejecutar` |
| `try/except/else` | `Reserva.confirmar` |
| `try/except/finally` | `Reserva.cancelar` |
| `try/except/else/finally` | `Reserva.procesar` |
| Encadenamiento (`raise ... from`) | `Reserva.validar`, `confirmar`, `procesar` |
| Archivo de logs | `software_fj.log` mediante `logging` |
| ≥ 10 simulaciones válidas e inválidas | 12 simulaciones en `main.py` (31 operaciones) |
| Sin base de datos | Solo objetos y listas internas en `SistemaFJ` |

## Simulaciones incluidas

1. Registro de clientes válidos · 2. Clientes inválidos (correo, documento, nombre faltante) ·
3. Servicios correctos · 4. Servicios incorrectos (tarifa negativa, nivel inexistente, capacidad 0) ·
5. Reserva exitosa (confirmar y procesar) · 6. Costo con descuento y sin impuesto (sobrecarga) ·
7. Duración inválida (encadenamiento) · 8. Cliente inválido · 9. Servicio no disponible ·
10. Cálculo inconsistente · 11. Operaciones no permitidas (doble cancelación) ·
12. Procesar sin confirmar y reserva inexistente.

## Códigos de error

| Código | Excepción | Situación |
|---|---|---|
| FJ-100 | `DatosInvalidosError` | Dato con formato o rango inválido |
| FJ-110 | `ParametroFaltanteError` | Falta un dato obligatorio |
| FJ-200 | `ServicioNoDisponibleError` | Servicio deshabilitado |
| FJ-300 | `ReservaInvalidaError` | Reserva no se puede crear/confirmar/procesar |
| FJ-310 | `OperacionNoPermitidaError` | Operación no válida para el estado actual |
| FJ-400 | `CalculoInconsistenteError` | Impuesto, descuento o total fuera de rango |

## Nota sobre el trabajo colaborativo

Esta fase se desarrolló de manera **individual** porque el estudiante no quedó integrado en un grupo
de trabajo. Aun así se siguió el flujo profesional de GitHub: una rama por módulo (`feature/...`),
commits descriptivos, fusiones a `main` e *issues* para el seguimiento de tareas.

## Referencias

- Van Rossum, G., & Drake Jr., F. L. (2024). *El tutorial de Python* (Cap. 8: Errores y excepciones). Python Software Foundation. https://docs.python.org/es/3.12/tutorial/errors.html
- Cuevas Álvarez, A. (2016). *Python 3: curso práctico*. RA-MA Editorial.
- Mishra, P. (2024). *Ultimate Git and GitHub for Modern Software Development*. Orange Education Pvt Ltd.
