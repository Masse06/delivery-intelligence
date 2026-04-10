# Delivery Intelligence Engine

> **Convirtiendo datos brutos de reparto en inteligencia de negocio accionable.**

Este proyecto nace de un caso de uso real: la optimización de rutas y beneficios durante mi etapa como repartidor. Lo que empezó como un registro manual de pedidos se ha transformado en un sistema de Business Intelligence capaz de identificar qué zonas y en qué franjas horarias se obtiene una mayor rentabilidad (propinas).

---

## Vista del Dashboard

<img width="1828" height="793" alt="image" src="https://github.com/user-attachments/assets/a8f795ef-9bd8-4c05-aaf6-2c3f722d9a9c" />
<img width="1782" height="845" alt="image" src="https://github.com/user-attachments/assets/5eac34d0-94cd-4f9a-9dc4-91dc82dcc6dc" />
<img width="1625" height="864" alt="image" src="https://github.com/user-attachments/assets/a281da93-85cf-4bd0-9abf-ed479d20efc6" />
<img width="1646" height="795" alt="image" src="https://github.com/user-attachments/assets/bf31e725-468f-4453-ba8c-3cd7a572ca72" />

---

## Arquitectura del Sistema

El proyecto sigue un flujo de datos completo **de extremo a extremo (End-to-End)**, estructurado en tres capas principales:

```
┌─────────────────────────────────────────────────────┐
│              CAPA DE VISUALIZACIÓN                  │
│       Dashboard Streamlit  ·  Gráficos Altair       │
└──────────────────────┬──────────────────────────────┘
                       │ API REST
┌──────────────────────▼──────────────────────────────┐
│               CAPA DE BACKEND                       │
│      Java 21  ·  Spring Boot  ·  Arq. Hexagonal     │
│        Spring Data JDBC  ·  PostgreSQL              │
└──────────────────────┬──────────────────────────────┘
                       │ SQL
┌──────────────────────▼──────────────────────────────┐
│              CAPA DE DATOS (ETL)                    │
│       Python  ·  Pandas  ·  SQLAlchemy              │
│   Pipeline de Anonimización  ·  Cumplimiento GDPR   │
└─────────────────────────────────────────────────────┘
```

### Detalle de cada capa

**1. Capa de Datos (ETL)**
Script en Python que procesa el dataset original, realiza la limpieza de tipos y aplica un **algoritmo de anonimización de direcciones** para garantizar la privacidad y el cumplimiento del GDPR.

**2. Capa de Backend**
API REST construida con **Java 17/21 y Spring Boot** siguiendo una **Arquitectura Hexagonal**. Utiliza SQL nativo para consultas analíticas complejas sobre una base de datos PostgreSQL alojada en la nube (Neon.tech).

**3. Capa de Visualización**
Cuadro de mando interactivo desarrollado con **Streamlit** que consume la API REST y genera visualizaciones avanzadas de densidad y rentabilidad.

---

## Tecnologías Utilizadas

| Capa | Tecnologías |
|---|---|
| **Backend** | Java · Spring Boot · Spring Data JDBC · Lombok |
| **Ingeniería de Datos** | Python · Pandas · SQLAlchemy |
| **Base de Datos** | PostgreSQL (Nube — Neon.tech) |
| **Frontend** | Streamlit · Altair |

---

## Estructura de Paquetes (Arquitectura Hexagonal)

```
src/main/java/com/danimt/deliveryintelligence
├── domain                  # Núcleo del negocio (Modelos y Puertos)
│   ├── model               # Entidades de dominio
│   └── port                # Interfaces de entrada y salida
├── application             # Casos de uso (Servicios)
└── infrastructure          # Adaptadores (Controladores REST y Persistencia SQL)
```

---

## ⚙️ Configuración del Proyecto

Las credenciales de la base de datos **no están incluidas** en el repositorio por seguridad.

**1. Clonar el repositorio**
```bash
git clone https://github.com/masse06/delivery-intelligence.git
cd delivery-intelligence
```

**2. Ejecutar el Backend**

Lanza la aplicación Spring Boot desde tu IDE o mediante Maven:
```bash
./mvnw spring-boot:run
```

**3. Lanzar el Dashboard**
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

---

## Notas sobre Seguridad y Privacidad

Este proyecto utiliza **datos reales que han sido anonimizados** mediante un proceso de limpieza en Python antes de ser cargados en el Data Warehouse.

La siguiente información personal ha sido eliminada u ofuscada para proteger la identidad de los clientes:
- Calle del pedido

El proceso de anonimización es completamente reproducible a través del script ETL y cumple con los principios de **minimización de datos y privacidad desde el diseño (GDPR)**.
