# Reporte técnico — QA Automation Framework

Este documento describe el estado actual del repositorio y da prioridad al código sobre el README.

## 1. Project Overview

El proyecto es un framework inicial de automatización UI para navegador, implementado en Python. Actualmente automatiza el flujo de inicio de sesión del sitio externo `https://the-internet.herokuapp.com/login`.

Su objetivo es encapsular interacciones de Selenium mediante Page Object Model (POM), reutilizar esperas explícitas y ejecutar pruebas con pytest.

Actualmente están implementados:

- Creación de un navegador Chrome con Selenium y WebDriver Manager.
- Configuración central de URL y timeout.
- `BasePage` con acciones y esperas reutilizables.
- Page Objects para Login y Dashboard.
- Fixtures de pytest para el ciclo de vida del navegador y `LoginPage`.
- Pruebas de login válido e inválido.

## 2. Technology Stack

| Tecnología | Uso en el proyecto | Por qué se utiliza |
|---|---|---|
| Python | Lenguaje del framework y las pruebas. | Implementa páginas, fixtures, configuración y tests. |
| Selenium | Automatización del navegador. | Localiza elementos, escribe, hace clic, navega y espera condiciones UI. |
| Google Chrome | Navegador automatizado. | `create_driver()` crea exclusivamente un `webdriver.Chrome`. |
| WebDriver Manager | Gestión de ChromeDriver. | Descarga/localiza el driver compatible mediante `ChromeDriverManager().install()`. |
| pytest | Ejecución y organización de pruebas. | Descubre tests, resuelve fixtures y parametriza escenarios negativos. |
| Page Object Model | Patrón de organización. | Separa los detalles de UI (`pages/`) de la intención de negocio de los tests. |
| Git | Control de versiones. | El repositorio contiene historial y archivos versionados. |
| `python-dotenv`, `requests` | Dependencias declaradas. | Están en `requirements.txt`, pero el código actual no las importa ni utiliza directamente. |

`requirements.txt` también incluye paquetes auxiliares y transitivos de Selenium/pytest, todos con versiones fijadas. El entorno virtual registrado fue creado con Python 3.14.0.

## 3. Project Structure

```text
qa-automation-framework/
├── .gitignore
├── README.md
├── requirements.txt
├── conftest.py
├── browser/
│   ├── __init__.py
│   └── driver.py
├── config/
│   ├── __init__.py
│   └── config.py
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── dashboard_page.py
│   └── login_page.py
└── tests/
    ├── _init_.py
    └── test_login.py
```

- `.gitignore`: excluye entorno virtual, cachés Python, caché pytest, VS Code y archivos macOS.
- `requirements.txt`: dependencias exactas del entorno.
- `conftest.py`: define fixtures globales de pytest.
- `browser/driver.py`: crea, maximiza y devuelve el navegador Chrome.
- `config/config.py`: define `BASE_URL`, `LOGIN_URL` y timeout por defecto de 10 segundos.
- `pages/base_page.py`: clase base abstracta para Page Objects.
- `pages/login_page.py`: representa el formulario de login y su resultado.
- `pages/dashboard_page.py`: representa la página segura posterior a un login exitoso.
- `tests/test_login.py`: contiene los escenarios automatizados actuales.
- `tests/_init_.py`: archivo vacío. Su nombre tiene un guion bajo a cada lado de `init`, no el nombre convencional `__init__.py`; no afecta la colección actual de pytest, pero no convierte explícitamente `tests` en paquete Python.

## 4. Architecture

El framework usa Page Object Model:

- Los tests expresan el escenario y validan resultados.
- Las páginas encapsulan localizadores y acciones UI.
- `BasePage` concentra primitivas comunes de Selenium.
- Las fixtures construyen y destruyen el navegador.
- Selenium ejecuta las interacciones reales con Chrome.

`BasePage` es abstracta: obliga a cada página concreta a implementar `wait_until_loaded()`. `LoginPage` considera cargada la página al ser visible el campo de usuario; `DashboardPage`, cuando es visible el encabezado “Secure Area”.

```mermaid
flowchart TD
    T[Test pytest] --> LPF[Fixture login_page]
    LPF --> DF[Fixture driver]
    DF --> CD[create_driver]
    CD --> Chrome[Chrome + ChromeDriver]
    LPF --> LP[LoginPage]
    T --> LP
    LP --> BP[BasePage]
    DP[DashboardPage] --> BP
    BP --> SEL[Selenium / WebDriverWait]
    SEL --> Chrome
```

## 5. Execution Flow: `pytest -v`

1. pytest busca archivos con su convención predeterminada; `tests/test_login.py` coincide.
2. Carga `conftest.py`, que expone las fixtures `driver` y `login_page`.
3. Para cada test que solicita `login_page`, pytest primero resuelve `driver`.
4. La fixture `driver` invoca `create_driver()`.
5. `create_driver()` instala/localiza ChromeDriver con WebDriver Manager, crea Chrome y maximiza la ventana.
6. La fixture `login_page` crea `LoginPage(driver)`, llama a `open()` y espera el campo de usuario.
7. El test ejecuta `login_page.login(usuario, contraseña)`.
8. `LoginPage` espera que cada campo y botón sea clickeable antes de interactuar.
9. Después del clic, espera que el mensaje flash contenga uno de los tres mensajes reconocidos.
10. El test compara el texto devuelto con el resultado esperado.
11. Al terminar el test, pytest reanuda la fixture `driver` después de `yield` y ejecuta `driver.quit()`.

Las fixtures no declaran `scope`, por lo que usan el alcance predeterminado de pytest: una instancia por función de test. Cada caso parametrizado recibe un navegador nuevo.

```mermaid
flowchart TD
    A[pytest -v] --> B[Descubre tests/test_login.py]
    B --> C[Resuelve fixture login_page]
    C --> D[Resuelve fixture driver]
    D --> E[create_driver]
    E --> F[Chrome maximizado]
    F --> G[LoginPage.open]
    G --> H[Espera campo username visible]
    H --> I[Ejecuta test]
    I --> J[login: escribir y hacer clic]
    J --> K[Espera mensaje flash reconocido]
    K --> L[Assertion]
    L --> M[Fin del test]
    M --> N[driver.quit]
```

## 6. Login Flow

`LoginPage` contiene estos localizadores:

- `USERNAME`: elemento con id `username`.
- `PASSWORD`: elemento con id `password`.
- `LOGIN_BUTTON`: elemento por clase `radius`.
- `FLASH_MESSAGE`: elemento con id `flash`.

Reconoce tres resultados mediante coincidencia parcial de texto:

| Resultado | Mensaje reconocido |
|---|---|
| Login exitoso | `You logged into a secure area!` |
| Usuario inválido | `Your username is invalid!` |
| Contraseña inválida | `Your password is invalid!` |

`login()` escribe credenciales, hace clic y devuelve el mensaje reconocido. No devuelve un `DashboardPage`; el test exitoso lo crea explícitamente después de validar el mensaje.

```mermaid
flowchart TD
    A[LoginPage.login] --> B[Escribir username]
    B --> C[Escribir password]
    C --> D[Clic en Login]
    D --> E[Leer flash message]
    E --> F{¿Mensaje conocido?}
    F -->|Éxito| G[Devuelve mensaje exitoso]
    F -->|Usuario inválido| H[Devuelve mensaje de usuario inválido]
    F -->|Contraseña inválida| I[Devuelve mensaje de contraseña inválida]
    F -->|Otro o sin mensaje reconocido| J[Sigue esperando]
    J --> K{¿Expira timeout?}
    K -->|Sí| L[TimeoutException de Selenium]
    K -->|No| E
```

## 7. Synchronization Strategy

La sincronización actual se basa exclusivamente en esperas explícitas.

- `WebDriverWait`: creado en `BasePage.wait()`, con timeout por defecto de 10 segundos.
- `expected_conditions`: importado como `EC`.
- `wait()`: recibe una condición de Selenium o una función personalizada y espera hasta que devuelva un valor válido.
- `wait_for_visible()`: espera `EC.visibility_of_element_located(locator)`.
- `click()`: espera `EC.element_to_be_clickable(locator)` antes de hacer clic.
- `type()`: también espera que el elemento sea clickeable antes de enviar texto.
- `wait_until_loaded()`: contrato abstracto que cada Page Object implementa con su propia señal de carga.

Estas esperas reducen fallos por intentar interactuar con una UI todavía no visible o no interactuable. No hay espera implícita, `sleep`, reintentos configurables ni estrategia adicional de sincronización.

## 8. Error Handling

### Estado real de `UnexpectedLoginResult`

`UnexpectedLoginResult` no existe en el repositorio actual.

- No está definida en ningún archivo.
- Ninguna clase la lanza.
- No hay test que la valide.
- Tampoco existen usos de `Mock` ni `pytest.raises`.

El comportamiento actual ante un resultado de login no reconocido es distinto: la función interna `login_result()` devuelve `False`; `WebDriverWait` sigue consultando hasta expirar los 10 segundos y Selenium lanza un `TimeoutException`.

| Situación | Comportamiento actual |
|---|---|
| Resultado esperado de aplicación | El flash contiene uno de los tres mensajes definidos y `wait_for_login_result()` devuelve ese mensaje. |
| Resultado inesperado de aplicación | No coincide con ningún mensaje conocido; el predicado devuelve `False` y continúa esperando. |
| Timeout de Selenium | Tras el timeout, Selenium lanza `TimeoutException`. Puede deberse a un resultado inesperado, ausencia del flash o un problema de carga; el framework no distingue estas causas. |

Por tanto, una excepción de dominio como `UnexpectedLoginResult` sería una posible mejora futura, pero no forma parte de la implementación actual.

## 9. Testing Strategy

Los tests son UI end-to-end contra un sitio externo real. Cubren un caso positivo y dos negativos.

| Test | Scenario | Expected Result |
|---|---|---|
| `test_valid_login` | Usuario `tomsmith` y contraseña `SuperSecretPassword!` | Mensaje de login exitoso y encabezado “Secure Area” visible. |
| `test_invalid_login[invalid_password]` | Usuario válido y contraseña inválida | Mensaje `Your password is invalid!`. |
| `test_invalid_login[invalid_username]` | Usuario inválido y contraseña válida | Mensaje `Your username is invalid!`. |

Detalles:

- `test_valid_login` usa la fixture `login_page`.
- Valida el texto de resultado y, después, crea `DashboardPage` para verificar que su encabezado sea visible.
- `test_invalid_login` usa `@pytest.mark.parametrize` para compartir la misma lógica con dos combinaciones de credenciales.
- Los casos tienen IDs legibles: `invalid_password` e `invalid_username`.
- Las assertions comparan igualdad exacta entre el resultado retornado y las constantes de `LoginPage`.
- No se usa `Mock`.
- No se usa `pytest.raises`.
- No hay prueba automatizada del resultado inesperado ni del timeout.

## 10. Important Design Decisions

| Decisión existente | Implementación | Beneficio |
|---|---|---|
| Separar páginas de tests | `LoginPage` y `DashboardPage` encapsulan UI; `test_login.py` describe escenarios. | Reduce duplicación de localizadores e interacciones en pruebas. |
| Centralizar acciones comunes | `BasePage` implementa `click`, `type`, `wait`, `open` y `wait_for_visible`. | Mantiene comportamiento consistente entre páginas. |
| Exigir una señal de carga | `BasePage` es abstracta y requiere `wait_until_loaded()`. | Cada página define una condición explícita para considerarse lista. |
| Usar esperas explícitas | `WebDriverWait` y `expected_conditions`. | Evita depender de tiempos fijos. |
| Gestionar driver con fixtures | `driver` usa `yield` y luego `quit()`. | Aísla tests y libera el navegador al terminar. |
| Preparar LoginPage en fixture | `login_page` abre y espera la página antes de devolverla. | Los tests empiezan con una página de login lista. |
| Parametrizar negativos | Un único test recibe credenciales y resultados esperados. | Evita duplicar el mismo flujo de prueba. |
| Separar espera y evaluación del login | `wait_for_login_result()` contiene un predicado que identifica textos permitidos. | El test recibe un resultado de negocio simple: el mensaje reconocido. |

## 11. End-to-End Example: Valid Login

```mermaid
sequenceDiagram
    participant P as pytest
    participant F as login_page fixture
    participant D as driver fixture
    participant L as LoginPage
    participant B as Browser
    participant DB as DashboardPage

    P->>D: solicita driver
    D->>B: create_driver() / Chrome
    P->>F: solicita login_page
    F->>L: instancia LoginPage(driver)
    L->>B: open(LOGIN_URL)
    L->>B: espera username visible
    P->>L: login(tomsmith, SuperSecretPassword!)
    L->>B: enter_username()
    L->>B: enter_password()
    L->>B: click_login()
    L->>B: wait_for_login_result()
    B-->>L: mensaje exitoso
    L-->>P: texto de éxito
    P->>P: assertion
    P->>DB: DashboardPage(driver)
    DB->>B: espera encabezado Secure Area
    D->>B: quit()
```

La secuencia exacta es:

`pytest → fixture → WebDriver → LoginPage → open() → enter_username() → enter_password() → click_login() → wait_for_login_result() → resultado → assertion → DashboardPage`.

## 12. Current Limitations

Estas son limitaciones actuales, no necesariamente errores:

- Solo se automatiza el flujo de login.
- Solo se crea Chrome; no hay selección de navegador.
- La URL está fija en código y no hay gestión de ambientes.
- Los tests dependen de un sitio externo, su disponibilidad, red y contenido.
- No hay reporting avanzado ni integración Allure implementada.
- No hay configuración CI/CD ni workflows de GitHub Actions en el repositorio.
- No hay capturas automáticas de pantalla.
- No hay logging propio del framework.
- No hay automatización API, validación de base de datos ni gestión de datos de prueba externa.
- No hay manejo de una excepción específica para resultados inesperados de login.
- No hay configuración pytest dedicada (`pytest.ini`, `pyproject.toml` o `tox.ini`).
- El entorno virtual actual no puede ejecutarse en este equipo porque su intérprete base configurado no está disponible.

## 13. Future Roadmap

| Estado | Alcance | Beneficio |
|---|---|---|
| CURRENT | Framework UI de login con Selenium, POM, fixtures y tres escenarios. | Base clara y pequeña para extender. |
| IMPLEMENTED | Esperas explícitas, ciclo de vida de Chrome, LoginPage, DashboardPage y parametrización negativa. | Pruebas más legibles y menos dependientes de tiempos fijos. |
| NEXT | Recuperar/recrear el entorno Python y verificar la ejecución reproducible. Añadir configuración de pytest y documentar el comando de instalación. | Facilita onboarding y ejecución consistente. |
| NEXT | Añadir pruebas para resultados inesperados y decidir si debe existir una excepción de dominio. | Distinguiría mejor fallos funcionales de timeouts técnicos. |
| FUTURE | Configuración por ambiente y selección de navegador. | Permitirá ejecutar contra distintos entornos y navegadores. |
| FUTURE | Evidencias de ejecución: reportes, screenshots y logging. | Mejora diagnóstico de fallos. |
| FUTURE | CI/CD. | Ejecuta validaciones de forma automática en cambios. |
| FUTURE | Nuevos Page Objects y cobertura de otros flujos. | Amplía la cobertura funcional manteniendo el mismo patrón. |

## 14. How to Start Working on This Project

1. Lee primero `config/config.py`, `pages/base_page.py`, `pages/login_page.py`, `conftest.py` y `tests/test_login.py`.
2. Antes de modificar código, entiende que los tests dependen de fixtures por función y de un sitio externo.
3. Normalmente, ejecuta:

   ```powershell
   python -m pytest -v
   ```

   En este repositorio, el `.venv` actual apunta a Python 3.14.0 en una ruta no disponible; primero debe restaurarse un intérprete/entorno válido.

4. Interpreta cada caso de pytest como un escenario individual; los dos negativos aparecen con sus IDs parametrizados.
5. Conoce primero estos archivos: `browser/driver.py`, `config/config.py`, `pages/base_page.py`, `pages/login_page.py`, `conftest.py` y `tests/test_login.py`.
6. Para agregar un test, reutiliza la fixture `login_page`, invoca métodos del Page Object y valida el resultado desde el test.
7. Para agregar un Page Object, crea una clase que herede de `BasePage`, define sus localizadores y acciones, e implementa `wait_until_loaded()` usando una señal real de disponibilidad.
8. Mantén localizadores y acciones UI dentro de los Page Objects; evita poner Selenium directo en los tests.
9. No agregues esperas fijas con `sleep`; usa las primitivas de espera explícita existentes.
10. No asumas que hay reporting, CI, múltiples ambientes, mocks o excepciones de negocio: actualmente no existen.

## 15. Glossary

- **Page Object Model:** patrón que representa cada página mediante una clase. En este proyecto, `LoginPage` y `DashboardPage` encapsulan elementos y acciones de UI.
- **Fixture:** función que prepara recursos para los tests. Aquí `driver` crea y cierra Chrome, y `login_page` abre el formulario de login.
- **Explicit Wait:** espera controlada hasta que se cumpla una condición UI. `BasePage.wait()` usa `WebDriverWait`.
- **WebDriver:** interfaz de Selenium que controla el navegador. El proyecto crea un WebDriver de Chrome.
- **Expected Condition:** condición reutilizable de Selenium, como “elemento visible” o “clickeable”. Se usa mediante `EC`.
- **Parametrization:** ejecución de un test con múltiples datos. `test_invalid_login` se ejecuta para contraseña inválida y usuario inválido.
- **Mock:** objeto simulado para aislar dependencias. No se usa actualmente en el repositorio.
- **Exception:** señal de un error o condición excepcional. No hay excepciones personalizadas; un login sin resultado reconocido termina actualmente en `TimeoutException` de Selenium.
- **Assertion:** validación de una expectativa de prueba. Los tests comparan el mensaje retornado con una constante esperada.

## 16. Technical Summary

La arquitectura actual es un framework UI pequeño basado en Selenium, pytest y Page Object Model. El flujo principal crea un Chrome por test, abre la página de login, ejecuta acciones sincronizadas con esperas explícitas, identifica el mensaje flash y valida el resultado.

Sus componentes principales son `BasePage`, `LoginPage`, `DashboardPage`, las fixtures de pytest y el creador de WebDriver. La estrategia de testing cubre un login válido y dos fallos de autenticación parametrizados.

Las fortalezas actuales son la separación básica por responsabilidades, las esperas explícitas, la limpieza del navegador y la legibilidad de los escenarios. Los siguientes pasos recomendados son restaurar un entorno ejecutable, actualizar la documentación y extender la cobertura sin perder esta separación.

## Repository Analysis Notes

### Archivos analizados

- `.gitignore`
- `README.md`
- `requirements.txt`
- `conftest.py`
- `browser/__init__.py`
- `browser/driver.py`
- `config/__init__.py`
- `config/config.py`
- `pages/__init__.py`
- `pages/base_page.py`
- `pages/dashboard_page.py`
- `pages/login_page.py`
- `tests/_init_.py`
- `tests/test_login.py`

También se revisó la configuración del entorno virtual (`.venv/pyvenv.cfg`) y la caché de pytest como evidencia auxiliar.

### Posibles inconsistencias

- El README indica que pytest y Page Object Model están “Coming Soon”, pero ambos ya están implementados.
- El README menciona GitHub Actions y Allure Reports como futuros; no hay archivos que los implementen.
- El requerimiento de documentar `UnexpectedLoginResult`, `Mock` y `pytest.raises` no coincide con el código actual: ninguno existe o se utiliza.
- `tests/_init_.py` no usa el nombre convencional `__init__.py`.

### Aspectos no determinables con certeza

- No fue posible ejecutar o colectar tests desde el entorno actual: `.venv` fue creado contra `C:\Users\itzel\AppData\Local\Programs\Python\Python314\python.exe`, instalación que no está disponible/accesible.
- Por ello, no se puede confirmar desde esta máquina el resultado actual de la suite ni la compatibilidad efectiva de Chrome/ChromeDriver.
