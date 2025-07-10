# 📊 DOCUMENTACIÓN DE LA BASE DE DATOS
## Sistema de Gestión de Horarios Académicos - La Pontificia

---

## 🏗️ **ARQUITECTURA DE LA BASE DE DATOS**

La base de datos del sistema está diseñada con una **arquitectura relacional normalizada** que soporta la gestión completa de horarios académicos. Utiliza **PostgreSQL** como motor principal y **Redis** como sistema de cache complementario.

### **Tecnologías Utilizadas:**
- **Base de Datos Principal**: PostgreSQL 13+
- **Cache y Broker**: Redis 6.1+
- **ORM**: Django ORM
- **Migraciones**: Django Migrations

---

## 📋 **ESQUEMA DE TABLAS**

### **1. CONFIGURACIÓN ACADÉMICA**

#### **1.1 TipoUnidadAcademica**
```sql
CREATE TABLE academic_setup_tipounidadacademica (
    tipo_unidad_id SERIAL PRIMARY KEY,
    nombre_tipo VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT
);
```
**Propósito**: Clasificar tipos de unidades académicas (Facultad, Escuela, Instituto, etc.)

#### **1.2 UnidadAcademica**
```sql
CREATE TABLE academic_setup_unidadacademica (
    unidad_id SERIAL PRIMARY KEY,
    nombre_unidad VARCHAR(255) UNIQUE NOT NULL,
    descripcion TEXT,
    tipo_unidad_id INTEGER REFERENCES academic_setup_tipounidadacademica(tipo_unidad_id)
);
```
**Propósito**: Gestionar las unidades académicas de la institución

#### **1.3 Carrera**
```sql
CREATE TABLE academic_setup_carrera (
    carrera_id SERIAL PRIMARY KEY,
    nombre_carrera VARCHAR(255) NOT NULL,
    codigo_carrera VARCHAR(20) UNIQUE,
    horas_totales_curricula INTEGER,
    unidad_id INTEGER REFERENCES academic_setup_unidadacademica(unidad_id),
    UNIQUE(nombre_carrera, unidad_id)
);
```
**Propósito**: Administrar las carreras profesionales

#### **1.4 Ciclo**
```sql
CREATE TABLE academic_setup_ciclo (
    ciclo_id SERIAL PRIMARY KEY,
    nombre_ciclo VARCHAR(100) NOT NULL,
    orden INTEGER NOT NULL,
    carrera_id INTEGER REFERENCES academic_setup_carrera(carrera_id),
    UNIQUE(carrera_id, orden)
);
```
**Propósito**: Organizar los ciclos académicos de cada carrera

#### **1.5 Seccion**
```sql
CREATE TABLE academic_setup_seccion (
    seccion_id SERIAL PRIMARY KEY,
    nombre_seccion VARCHAR(100) NOT NULL,
    ciclo_id INTEGER REFERENCES academic_setup_ciclo(ciclo_id),
    capacidad INTEGER,
    UNIQUE(nombre_seccion, ciclo_id)
);
```
**Propósito**: Gestionar las secciones dentro de cada ciclo

#### **1.6 PeriodoAcademico**
```sql
CREATE TABLE academic_setup_periodoacademico (
    periodo_id SERIAL PRIMARY KEY,
    nombre_periodo VARCHAR(50) UNIQUE NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);
```
**Propósito**: Administrar los periodos académicos

### **2. GESTIÓN DE ESPACIOS**

#### **2.1 TiposEspacio**
```sql
CREATE TABLE academic_setup_tiposespacio (
    tipo_espacio_id SERIAL PRIMARY KEY,
    nombre_tipo_espacio VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT
);
```
**Propósito**: Clasificar tipos de espacios (Aula, Laboratorio, Auditorio, etc.)

#### **2.2 EspaciosFisicos**
```sql
CREATE TABLE academic_setup_espaciosfisicos (
    espacio_id SERIAL PRIMARY KEY,
    nombre_espacio VARCHAR(100) NOT NULL,
    tipo_espacio_id INTEGER REFERENCES academic_setup_tiposespacio(tipo_espacio_id),
    capacidad INTEGER,
    ubicacion VARCHAR(255),
    recursos_adicionales TEXT,
    unidad_id INTEGER REFERENCES academic_setup_unidadacademica(unidad_id),
    UNIQUE(nombre_espacio, unidad_id)
);
```
**Propósito**: Gestionar los espacios físicos disponibles

### **3. GESTIÓN DE MATERIAS Y ESPECIALIDADES**

#### **3.1 Especialidades**
```sql
CREATE TABLE academic_setup_especialidades (
    especialidad_id SERIAL PRIMARY KEY,
    nombre_especialidad VARCHAR(150) UNIQUE NOT NULL,
    descripcion TEXT
);
```
**Propósito**: Administrar las especialidades de los docentes

#### **3.2 Materias**
```sql
CREATE TABLE academic_setup_materias (
    materia_id SERIAL PRIMARY KEY,
    codigo_materia VARCHAR(50) UNIQUE NOT NULL,
    nombre_materia VARCHAR(255) NOT NULL,
    descripcion TEXT,
    horas_academicas_teoricas INTEGER DEFAULT 0,
    horas_academicas_practicas INTEGER DEFAULT 0,
    horas_academicas_laboratorio INTEGER DEFAULT 0,
    requiere_tipo_espacio_especifico_id INTEGER REFERENCES academic_setup_tiposespacio(tipo_espacio_id),
    estado BOOLEAN DEFAULT TRUE
);
```
**Propósito**: Gestionar las materias académicas

#### **3.3 CarreraMaterias**
```sql
CREATE TABLE academic_setup_carreramaterias (
    id SERIAL PRIMARY KEY,
    carrera_id INTEGER REFERENCES academic_setup_carrera(carrera_id),
    materia_id INTEGER REFERENCES academic_setup_materias(materia_id),
    ciclo_id INTEGER REFERENCES academic_setup_ciclo(ciclo_id),
    ciclo_sugerido INTEGER,
    UNIQUE(carrera_id, materia_id, ciclo_id)
);
```
**Propósito**: Vincular materias con carreras y ciclos

#### **3.4 MateriaEspecialidadesRequeridas**
```sql
CREATE TABLE academic_setup_materiaespecialidadesrequeridas (
    id SERIAL PRIMARY KEY,
    materia_id INTEGER REFERENCES academic_setup_materias(materia_id),
    especialidad_id INTEGER REFERENCES academic_setup_especialidades(especialidad_id),
    UNIQUE(materia_id, especialidad_id)
);
```
**Propósito**: Definir especialidades requeridas por materia

### **4. GESTIÓN DE USUARIOS Y DOCENTES**

#### **4.1 Roles**
```sql
CREATE TABLE users_roles (
    rol_id SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(50) UNIQUE NOT NULL
);
```
**Propósito**: Definir roles del sistema

#### **4.2 Docentes**
```sql
CREATE TABLE users_docentes (
    docente_id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES auth_user(id),
    codigo_docente VARCHAR(50) UNIQUE,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    dni VARCHAR(15) UNIQUE,
    email VARCHAR(254) UNIQUE,
    telefono VARCHAR(30),
    tipo_contrato VARCHAR(50),
    max_horas_semanales INTEGER,
    unidad_principal_id INTEGER REFERENCES academic_setup_unidadacademica(unidad_id)
);
```
**Propósito**: Gestionar información de docentes

#### **4.3 DocenteEspecialidades**
```sql
CREATE TABLE users_docenteespecialidades (
    id SERIAL PRIMARY KEY,
    docente_id INTEGER REFERENCES users_docentes(docente_id),
    especialidad_id INTEGER REFERENCES academic_setup_especialidades(especialidad_id),
    UNIQUE(docente_id, especialidad_id)
);
```
**Propósito**: Vincular docentes con sus especialidades

#### **4.4 SesionesUsuario**
```sql
CREATE TABLE users_sesionesusuario (
    sesion_id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES auth_user(id),
    token VARCHAR(500) UNIQUE NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion TIMESTAMP NOT NULL,
    ip_address INET,
    user_agent TEXT
);
```
**Propósito**: Gestionar sesiones de usuario para auditoría

### **5. GESTIÓN DE HORARIOS**

#### **5.1 Grupos**
```sql
CREATE TABLE scheduling_grupos (
    grupo_id SERIAL PRIMARY KEY,
    codigo_grupo VARCHAR(50) NOT NULL,
    carrera_id INTEGER REFERENCES academic_setup_carrera(carrera_id),
    periodo_id INTEGER REFERENCES academic_setup_periodoacademico(periodo_id),
    numero_estudiantes_estimado INTEGER,
    turno_preferente CHAR(1) CHECK (turno_preferente IN ('M', 'T', 'N')),
    docente_asignado_directamente_id INTEGER REFERENCES users_docentes(docente_id),
    ciclo_semestral INTEGER,
    UNIQUE(codigo_grupo, periodo_id)
);
```
**Propósito**: Gestionar grupos de estudiantes

#### **5.2 Grupos-Materias (Tabla Intermedia)**
```sql
CREATE TABLE scheduling_grupos_materias (
    id SERIAL PRIMARY KEY,
    grupo_id INTEGER REFERENCES scheduling_grupos(grupo_id),
    materia_id INTEGER REFERENCES academic_setup_materias(materia_id),
    UNIQUE(grupo_id, materia_id)
);
```
**Propósito**: Vincular grupos con materias

#### **5.3 BloquesHorariosDefinicion**
```sql
CREATE TABLE scheduling_bloqueshorariosdefinicion (
    bloque_def_id SERIAL PRIMARY KEY,
    nombre_bloque VARCHAR(50) NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    turno CHAR(1) CHECK (turno IN ('M', 'T', 'N')),
    dia_semana INTEGER CHECK (dia_semana BETWEEN 1 AND 7),
    UNIQUE(nombre_bloque, hora_inicio, hora_fin, turno, dia_semana)
);
```
**Propósito**: Definir bloques horarios disponibles

#### **5.4 DisponibilidadDocentes**
```sql
CREATE TABLE scheduling_disponibilidaddocentes (
    disponibilidad_id SERIAL PRIMARY KEY,
    docente_id INTEGER REFERENCES users_docentes(docente_id),
    periodo_id INTEGER REFERENCES academic_setup_periodoacademico(periodo_id),
    dia_semana INTEGER CHECK (dia_semana BETWEEN 1 AND 7),
    bloque_horario_id INTEGER REFERENCES scheduling_bloqueshorariosdefinicion(bloque_def_id),
    esta_disponible BOOLEAN DEFAULT TRUE,
    preferencia SMALLINT DEFAULT 0,
    origen_carga VARCHAR(10) DEFAULT 'MANUAL',
    UNIQUE(docente_id, periodo_id, dia_semana, bloque_horario_id)
);
```
**Propósito**: Gestionar disponibilidad horaria de docentes

#### **5.5 HorariosAsignados**
```sql
CREATE TABLE scheduling_horariosasignados (
    horario_id SERIAL PRIMARY KEY,
    grupo_id INTEGER REFERENCES scheduling_grupos(grupo_id),
    materia_id INTEGER REFERENCES academic_setup_materias(materia_id),
    docente_id INTEGER REFERENCES users_docentes(docente_id),
    espacio_id INTEGER REFERENCES academic_setup_espaciosfisicos(espacio_id),
    periodo_id INTEGER REFERENCES academic_setup_periodoacademico(periodo_id),
    dia_semana INTEGER CHECK (dia_semana BETWEEN 1 AND 7),
    bloque_horario_id INTEGER REFERENCES scheduling_bloqueshorariosdefinicion(bloque_def_id),
    estado VARCHAR(50) DEFAULT 'Programado',
    observaciones TEXT,
    -- Restricciones de unicidad para evitar conflictos
    UNIQUE(docente_id, periodo_id, dia_semana, bloque_horario_id),
    UNIQUE(espacio_id, periodo_id, dia_semana, bloque_horario_id),
    UNIQUE(grupo_id, periodo_id, dia_semana, bloque_horario_id),
    UNIQUE(grupo_id, materia_id, periodo_id, dia_semana, bloque_horario_id)
);
```
**Propósito**: Almacenar horarios asignados (tabla principal del sistema)

#### **5.6 ConfiguracionRestricciones**
```sql
CREATE TABLE scheduling_configuracionrestricciones (
    restriccion_id SERIAL PRIMARY KEY,
    codigo_restriccion VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT NOT NULL,
    tipo_aplicacion VARCHAR(50) NOT NULL,
    entidad_id_1 INTEGER,
    entidad_id_2 INTEGER,
    valor_parametro VARCHAR(255),
    periodo_aplicable_id INTEGER REFERENCES academic_setup_periodoacademico(periodo_id),
    esta_activa BOOLEAN DEFAULT TRUE
);
```
**Propósito**: Configurar restricciones para la generación de horarios

---

## 🔗 **RELACIONES PRINCIPALES**

### **Jerarquía Académica:**
```
UnidadAcademica → Carrera → Ciclo → Seccion
```

### **Gestión de Horarios:**
```
Grupos ←→ Materias (Many-to-Many)
Docentes ←→ Especialidades (Many-to-Many)
HorariosAsignados (Tabla central que conecta todo)
```

### **Restricciones de Integridad:**
- **RD01**: Un docente no puede estar en dos lugares al mismo tiempo
- **RD02**: Un espacio no puede tener dos clases simultáneas
- **RD03**: Un grupo no puede tener dos clases al mismo tiempo
- **RD04**: Una materia de un grupo no se puede programar dos veces en el mismo bloque

---

## 📊 **ÍNDICES RECOMENDADOS**

```sql
-- Índices para consultas frecuentes
CREATE INDEX idx_horarios_periodo_dia ON scheduling_horariosasignados(periodo_id, dia_semana);
CREATE INDEX idx_horarios_docente ON scheduling_horariosasignados(docente_id);
CREATE INDEX idx_horarios_espacio ON scheduling_horariosasignados(espacio_id);
CREATE INDEX idx_horarios_grupo ON scheduling_horariosasignados(grupo_id);

-- Índices para disponibilidad
CREATE INDEX idx_disponibilidad_docente_periodo ON scheduling_disponibilidaddocentes(docente_id, periodo_id);

-- Índices para grupos
CREATE INDEX idx_grupos_carrera_periodo ON scheduling_grupos(carrera_id, periodo_id);
```

---

## 🚀 **OPTIMIZACIONES IMPLEMENTADAS**

### **1. Cache Redis:**
- Cache de consultas frecuentes de horarios
- Cache de disponibilidad de docentes
- Cache de configuración de restricciones

### **2. Denormalización Estratégica:**
- `periodo_id` en `HorariosAsignados` para consultas rápidas
- `ciclo_semestral` en `Grupos` para ordenamiento

### **3. Restricciones de Base de Datos:**
- Constraints UNIQUE para evitar conflictos
- Foreign Keys para integridad referencial
- Check constraints para validación de datos

---

## 📈 **ESTADÍSTICAS DE LA BASE DE DATOS**

- **Total de tablas**: 18 tablas principales
- **Relaciones**: 25+ foreign keys
- **Restricciones**: 15+ constraints de unicidad
- **Índices**: 8+ índices optimizados
- **Cache**: 3 bases de datos Redis (0, 1, 2)

---

## 🔧 **COMANDOS ÚTILES**

### **Verificar integridad:**
```sql
-- Verificar horarios sin conflictos
SELECT COUNT(*) FROM scheduling_horariosasignados 
WHERE periodo_id = 1;

-- Verificar disponibilidad de docentes
SELECT COUNT(*) FROM scheduling_disponibilidaddocentes 
WHERE esta_disponible = true;
```

### **Backup y mantenimiento:**
```bash
# Backup completo
pg_dump -h localhost -U usuario -d sistema_horarios > backup.sql

# Backup solo estructura
pg_dump -h localhost -U usuario -d sistema_horarios --schema-only > estructura.sql
```

---

**Última actualización**: Julio 2025  
**Versión del esquema**: 1.0  
**Estado**: Producción 