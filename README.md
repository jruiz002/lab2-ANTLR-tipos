# 🧪 Laboratorio 2: Sistema de Tipos con ANTLR

> 🎥 **Video de demostración (Entregable Principal):** [Ver en YouTube](https://youtu.be/dxTE32nsZ1U)

## 📋 Descripción General

En este laboratorio trabajarás con **ANTLR**, un generador de analizadores sintácticos. Hemos proporcionado un `Dockerfile` para ayudarte a configurar el entorno rápidamente. Utilizaremos Python para hacer pruebas, ya que es más sencillo que Java para pruebas pequeñas.

Experimentarás con un sistema de tipos básico, extenderás una gramática y completarás el sistema de tipos. Con ello, aprenderás sobre la marcha lo básico al utilizar sistemas de tipos en el análisis semántico.

* **Modalidad: Individual**

## 🚀 Solución y Cumplimiento de Entregables

A continuación se detalla cómo se ha dado cumplimiento a cada uno de los requisitos solicitados en este laboratorio:

### 1. Uso de Visitor y Listener
Se ha implementado el análisis semántico utilizando **ambas metodologías**:
- `TypeCheckVisitor`: Falla rápido (se detiene en el primer error que encuentra).
- `TypeCheckListener`: Recorre el árbol completo y recolecta **múltiples errores** de una sola pasada.
*(Nota: Para que ambos funcionen en el mismo entorno, el parser se generó con `antlr -Dlanguage=Python3 -visitor -listener SimpleLang.g4` para evitar sobrescrituras de ANTLR).*

### 2. Análisis de Archivos Provistos
- **`program_test_pass.txt`**: Pasa correctamente porque solo contiene sumas y multiplicaciones entre tipos aritméticos válidos (`int` y `float`). El sistema de tipos sabe que estas operaciones son semánticamente correctas.
- **`program_test_no_pass.txt`**: Falla debido a errores intencionales de tipado (por ejemplo, intentar dividir un `int` entre un `string`, o restar un `bool` de un `float`). El analizador detecta estas incompatibilidades gracias a las validaciones de instancia que pusimos en los métodos de ANTLR.

### 3. Extensión de la Gramática (2 Nuevas Operaciones)
Se extendió el archivo `SimpleLang.g4` para incluir dos nuevas reglas de operaciones (Líneas 9 y 10):
1. **Igualdad (`Equality`)**: Se soporta `==` y `!=`.
2. **Lógicas (`Logical`)**: Se soporta `&&` y `||`.

### 4. Nuevos Conflictos de Tipos (3 Nuevos Conflictos)
Se extendió el sistema de tipos para detectar al menos 3 nuevos errores lógicos, los cuales pueden probarse en el archivo **`program_test_custom.txt`**:
- **Conflicto 1**: Intento de sumar un tipo numérico con un String (Ej: `"hola" + 3`). *Nota: Se habilitó como válida la concatenación normal de String + String*.
- **Conflicto 2**: Evaluar igualdad entre tipos que no coinciden (Ej: `5 == "5"`).
- **Conflicto 3**: Aplicar operaciones lógicas `&&` o `||` a tipos que no son booleanos (Ej: `5 && true`).

---

## 🧰 Instrucciones de Configuración y Ejecución

1. **Construir y Ejecutar el Contenedor Docker**
   Desde el directorio raíz de este laboratorio, ejecuta:
   ```bash
   docker build --rm . -t lab2-image && docker run --rm -ti -v "$(pwd)/program":/program lab2-image
   ```

2. **Generar Archivos de Lexer y Parser (IMPORTANTE)**
   Dentro del contenedor, compila la gramática ANTLR para usar Visitor y Listener simultáneamente:
   ```bash
   antlr -Dlanguage=Python3 -visitor -listener SimpleLang.g4
   ```

3. **Ejecutar el Analizador (Visitor vs Listener)**
   Puedes probar el Visitor (detención rápida) y el Listener (análisis completo) con los archivos de prueba:

   **Archivos Base:**
   ```bash
   python3 Driver.py program_test_pass.txt
   python3 DriverListener.py program_test_pass.txt

   python3 Driver.py program_test_no_pass.txt
   python3 DriverListener.py program_test_no_pass.txt
   ```

   **Archivo con los 3 Conflictos Propios:**
   ```bash
   python3 Driver.py program_test_custom.txt
   python3 DriverListener.py program_test_custom.txt
   ```
