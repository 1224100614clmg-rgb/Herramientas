# Sistema de Gestión de Herramientas

---

## 📌 Descripción del Proyecto

El **Sistema de Gestión de Herramientas** es una aplicación web desarrollada en **Python** utilizando el framework **Flask**, diseñada para optimizar la administración y control de herramientas dentro de un laboratorio académico.

El sistema permite registrar herramientas, gestionar préstamos, controlar la disponibilidad en tiempo real y almacenar la información en una base de datos **MySQL**.  

Además, integra diversas APIs externas que amplían su funcionalidad y demuestran la aplicación práctica de servicios web en un entorno real.

El proyecto está estructurado bajo una arquitectura modular basada en el patrón **Modelo–Vista–Controlador (MVC)**, organizada en carpetas como `controllers`, `models`, `services` y `views`, facilitando el mantenimiento y la escalabilidad.

---

## 🎯 Propósito del Proyecto

Automatizar el proceso de control y préstamo de herramientas, reduciendo errores manuales, mejorando la organización administrativa y permitiendo la consulta de información en tiempo real.

Asimismo, aplicar conocimientos de desarrollo web, integración de APIs, conexión a bases de datos y buenas prácticas en la estructuración de proyectos.

---

## 🚀 Funcionalidades Principales

- Registro de herramientas  
- Edición y eliminación de herramientas  
- Gestión y control de préstamos  
- Control automático de disponibilidad  
- Persistencia de datos mediante MySQL  
- Arquitectura modular organizada por capas  
- Integración con APIs externas  

---

## 🌐 APIs Implementadas

El sistema integra los siguientes servicios externos:

- **API de Geolocalización:** Permite obtener información de ubicación para contextualizar operaciones dentro del sistema.
- **API de PayPal:** Implementada para simular o gestionar procesos de pago relacionados con el sistema.
- **API de YouTube:** Integrada para mostrar contenido multimedia informativo dentro de la aplicación.
- **MySQL:** Base de datos relacional utilizada para la gestión y almacenamiento de la información.

---

## 🛠 Tecnologías Utilizadas

- Python  
- Flask  
- MySQL  
- HTML5  
- CSS3  
- Bootstrap  
- mysql-connector-python  
- APIs externas (Geolocalización, PayPal, YouTube)  

---

## 🗂 Estructura del Proyecto
Proyecto_Herramientas/
│
├── controllers/
├── models/
├── services/
├── views/
├── static/
├── app.py
├── config.py
├── requirements.txt
└── README.md

## ⚙️ Instalación y Configuración

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/TUUSUARIO/Proyecto_Herramientas.git
2️⃣ Ingresar a la carpeta del proyecto
cd Proyecto_Herramientas
3️⃣ Crear entorno virtual (opcional pero recomendado)
python -m venv env

Activar entorno virtual en Windows:

env\Scripts\activate
4️⃣ Instalar dependencias
pip install -r requirements.txt
🗄 Configuración de Base de Datos (MySQL)

Crear una base de datos en MySQL.

Importar el script SQL correspondiente (si aplica).

Configurar el archivo config.py con los datos de conexión:

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "tu_contraseña"
DB_NAME = "nombre_base_datos"

Verificar que el servidor MySQL esté en ejecución antes de iniciar la aplicación.

▶️ Ejecución del Proyecto

Ejecutar la aplicación con:

python app.py

Abrir en el navegador:

http://127.0.0.1:5000/
📷 Evidencia de Funcionamiento


![Uploading Captura de pantalla 2026-02-28 003242.png…]()


Enlace al video explicativo del proyecto:

https://youtu.be/FA8swC66Srg?si=TG1oAMnUEpfNrTrb

👩‍💻 Autoras

Claudia Lizbeth Mendez Galván
Elsy Joselyn Godinez Juarez
Crystal Hernandez Aguilar

Carrera: Ingeniería en Desarrollo y Gestión de Software
Institución: Universidad Tecnológica del Norte de Guanajuato
Fecha de entrega: 27 de febrero de 2026
