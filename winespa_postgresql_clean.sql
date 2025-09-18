-- PostgreSQL dump - Solo tablas de lógica de negocio
-- Base de datos: winespaapi
-- Sin tablas de Django, solo aplicación

-- Drop tables in reverse dependency order
DROP TABLE IF EXISTS ventaservicios_ventaservicio_citas CASCADE;
DROP TABLE IF EXISTS ventaservicios_detalleventaservicio CASCADE;
DROP TABLE IF EXISTS ventaservicios_ventaservicio CASCADE;
DROP TABLE IF EXISTS usuarios_usuario_user_permissions CASCADE;
DROP TABLE IF EXISTS usuarios_usuario_groups CASCADE;
DROP TABLE IF EXISTS usuarios_usuario CASCADE;
DROP TABLE IF EXISTS servicios_servicio CASCADE;
DROP TABLE IF EXISTS roles_rolhaspermiso CASCADE;
DROP TABLE IF EXISTS roles_rol CASCADE;
DROP TABLE IF EXISTS roles_permiso CASCADE;
DROP TABLE IF EXISTS roles_modulo CASCADE;
DROP TABLE IF EXISTS roles_accion CASCADE;
DROP TABLE IF EXISTS proveedores_proveedor CASCADE;
DROP TABLE IF EXISTS novedades_novedad CASCADE;
DROP TABLE IF EXISTS manicuristas_manicurista CASCADE;
DROP TABLE IF EXISTS liquidaciones CASCADE;
DROP TABLE IF EXISTS insumoshasabastecimientos_insumohasabastecimiento CASCADE;
DROP TABLE IF EXISTS insumos_insumo CASCADE;
DROP TABLE IF EXISTS compras_detallecompra CASCADE;
DROP TABLE IF EXISTS comprahasinsumos_comprahasinsumo CASCADE;
DROP TABLE IF EXISTS compras_compra CASCADE;
DROP TABLE IF EXISTS codigorecuperacion_codigorecuperacion CASCADE;
DROP TABLE IF EXISTS clientes_cliente CASCADE;
DROP TABLE IF EXISTS citas_cita_servicios CASCADE;
DROP TABLE IF EXISTS citas_cita CASCADE;
DROP TABLE IF EXISTS categoriainsumos_categoriainsumo CASCADE;
DROP TABLE IF EXISTS abastecimientos_abastecimiento CASCADE;

-- Create tables

-- Table: abastecimientos_abastecimiento
CREATE TABLE abastecimientos_abastecimiento (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    fecha DATE NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad >= 0),
    manicurista_id BIGINT NOT NULL
);

-- Table: categoriainsumos_categoriainsumo
CREATE TABLE categoriainsumos_categoriainsumo (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    estado VARCHAR(10) NOT NULL
);

-- Table: citas_cita
CREATE TABLE citas_cita (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    fecha_cita DATE NOT NULL,
    hora_cita TIME(6) NOT NULL,
    estado VARCHAR(30) NOT NULL,
    observaciones TEXT,
    motivo_cancelacion TEXT,
    precio_total DECIMAL(10,2) NOT NULL,
    precio_servicio DECIMAL(10,2) NOT NULL,
    duracion_total INTEGER NOT NULL CHECK (duracion_total >= 0),
    duracion_estimada INTEGER NOT NULL CHECK (duracion_estimada >= 0),
    fecha_finalizacion TIMESTAMP(6) DEFAULT NULL,
    cliente_id BIGINT NOT NULL,
    manicurista_id BIGINT NOT NULL,
    novedad_relacionada_id BIGINT DEFAULT NULL,
    servicio_id BIGINT NOT NULL,
    UNIQUE (manicurista_id, fecha_cita, hora_cita)
);

-- Table: citas_cita_servicios
CREATE TABLE citas_cita_servicios (
    id BIGSERIAL PRIMARY KEY,
    cita_id BIGINT NOT NULL,
    servicio_id BIGINT NOT NULL,
    UNIQUE (cita_id, servicio_id)
);

-- Table: clientes_cliente
CREATE TABLE clientes_cliente (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    tipo_documento VARCHAR(2) NOT NULL,
    documento VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    celular VARCHAR(15) NOT NULL,
    correo_electronico VARCHAR(254) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    genero VARCHAR(2) NOT NULL,
    estado BOOLEAN NOT NULL,
    contraseña_temporal VARCHAR(128) DEFAULT NULL,
    debe_cambiar_contraseña BOOLEAN NOT NULL,
    usuario_id BIGINT DEFAULT NULL UNIQUE
);

-- Table: codigorecuperacion_codigorecuperacion
CREATE TABLE codigorecuperacion_codigorecuperacion (
    id BIGSERIAL PRIMARY KEY,
    correo_electronico VARCHAR(254) DEFAULT NULL,
    codigo VARCHAR(6) NOT NULL,
    creado_en TIMESTAMP(6) NOT NULL,
    expiracion TIMESTAMP(6) NOT NULL,
    usado BOOLEAN NOT NULL
);

-- Table: comprahasinsumos_comprahasinsumo
CREATE TABLE comprahasinsumos_comprahasinsumo (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad >= 0),
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    compra_id BIGINT NOT NULL,
    insumo_id BIGINT NOT NULL
);

-- Table: compras_compra
CREATE TABLE compras_compra (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    fecha TIMESTAMP(6) NOT NULL,
    codigo_factura VARCHAR(100) DEFAULT NULL,
    estado VARCHAR(20) NOT NULL,
    observaciones TEXT,
    subtotal DECIMAL(10,2) NOT NULL,
    iva DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    motivo_anulacion TEXT,
    proveedor_id BIGINT NOT NULL
);

-- Table: compras_detallecompra
CREATE TABLE compras_detallecompra (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad >= 0),
    precio_unitario DECIMAL(10,2) NOT NULL,
    compra_id BIGINT NOT NULL,
    insumo_id BIGINT NOT NULL,
    UNIQUE (compra_id, insumo_id)
);

-- Table: insumos_insumo
CREATE TABLE insumos_insumo (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad >= 0),
    estado VARCHAR(10) NOT NULL,
    categoria_insumo_id BIGINT NOT NULL
);

-- Table: insumoshasabastecimientos_insumohasabastecimiento
CREATE TABLE insumoshasabastecimientos_insumohasabastecimiento (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad >= 0),
    abastecimiento_id BIGINT NOT NULL,
    insumo_id BIGINT NOT NULL
);

-- Table: liquidaciones
CREATE TABLE liquidaciones (
    id BIGSERIAL PRIMARY KEY,
    fecha_inicio DATE NOT NULL,
    fecha_final DATE NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    bonificacion DECIMAL(10,2) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    fecha_creacion TIMESTAMP(6) NOT NULL,
    fecha_actualizacion TIMESTAMP(6) NOT NULL,
    observaciones TEXT,
    manicurista_id BIGINT NOT NULL,
    UNIQUE (manicurista_id, fecha_inicio, fecha_final)
);

-- Table: manicuristas_manicurista
CREATE TABLE manicuristas_manicurista (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    tipo_documento VARCHAR(2) DEFAULT NULL,
    numero_documento VARCHAR(20) DEFAULT NULL UNIQUE,
    especialidad VARCHAR(50) DEFAULT NULL,
    celular VARCHAR(15) DEFAULT NULL,
    correo VARCHAR(254) DEFAULT NULL UNIQUE,
    direccion VARCHAR(200) DEFAULT NULL,
    contraseña_temporal VARCHAR(128) DEFAULT NULL,
    debe_cambiar_contraseña BOOLEAN NOT NULL,
    estado VARCHAR(10) NOT NULL,
    disponible BOOLEAN NOT NULL,
    fecha_ingreso DATE DEFAULT NULL,
    usuario_id BIGINT DEFAULT NULL UNIQUE
);

-- Table: novedades_novedad
CREATE TABLE novedades_novedad (
    id BIGSERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    estado VARCHAR(20) NOT NULL,
    hora_entrada TIME(6) DEFAULT NULL,
    turno VARCHAR(20) DEFAULT NULL,
    archivo_soporte VARCHAR(100) DEFAULT NULL,
    dias INTEGER DEFAULT NULL CHECK (dias >= 0),
    tipo_ausencia VARCHAR(20) DEFAULT NULL,
    hora_inicio_ausencia TIME(6) DEFAULT NULL,
    hora_fin_ausencia TIME(6) DEFAULT NULL,
    observaciones TEXT,
    motivo TEXT,
    motivo_anulacion TEXT,
    fecha_anulacion TIMESTAMP(6) DEFAULT NULL,
    fecha_creacion TIMESTAMP(6) NOT NULL,
    fecha_actualizacion TIMESTAMP(6) NOT NULL,
    manicurista_id BIGINT NOT NULL,
    UNIQUE (manicurista_id, fecha)
);

-- Table: proveedores_proveedor
CREATE TABLE proveedores_proveedor (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    tipo_persona VARCHAR(10) NOT NULL,
    nombre_empresa VARCHAR(100) NOT NULL,
    nit VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    correo_electronico VARCHAR(254) NOT NULL,
    celular VARCHAR(15) NOT NULL,
    estado VARCHAR(10) NOT NULL
);

-- Table: roles_accion
CREATE TABLE roles_accion (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    estado VARCHAR(10) NOT NULL
);

-- Table: roles_modulo
CREATE TABLE roles_modulo (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    estado VARCHAR(10) NOT NULL
);

-- Table: roles_permiso
CREATE TABLE roles_permiso (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    estado VARCHAR(10) NOT NULL,
    accion_id BIGINT NOT NULL,
    modulo_id BIGINT NOT NULL,
    UNIQUE (modulo_id, accion_id)
);

-- Table: roles_rol
CREATE TABLE roles_rol (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    estado VARCHAR(10) NOT NULL
);

-- Table: roles_rolhaspermiso
CREATE TABLE roles_rolhaspermiso (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    permiso_id BIGINT NOT NULL,
    rol_id BIGINT NOT NULL,
    UNIQUE (rol_id, permiso_id)
);

-- Table: servicios_servicio
CREATE TABLE servicios_servicio (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    descripcion TEXT NOT NULL,
    duracion INTEGER NOT NULL CHECK (duracion >= 0),
    estado VARCHAR(10) NOT NULL,
    imagen VARCHAR(500) DEFAULT NULL
);

-- Table: usuarios_usuario
CREATE TABLE usuarios_usuario (
    id BIGSERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP(6) DEFAULT NULL,
    is_superuser BOOLEAN NOT NULL,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    tipo_documento VARCHAR(2) NOT NULL,
    documento VARCHAR(20) NOT NULL UNIQUE,
    direccion VARCHAR(200) DEFAULT NULL,
    celular VARCHAR(15) NOT NULL,
    correo_electronico VARCHAR(254) NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL,
    is_staff BOOLEAN NOT NULL,
    date_joined TIMESTAMP(6) NOT NULL,
    contraseña_temporal VARCHAR(128) DEFAULT NULL,
    debe_cambiar_contraseña BOOLEAN NOT NULL,
    rol_id BIGINT NOT NULL
);

-- Table: usuarios_usuario_groups
CREATE TABLE usuarios_usuario_groups (
    id BIGSERIAL PRIMARY KEY,
    usuario_id BIGINT NOT NULL,
    group_id INTEGER NOT NULL,
    UNIQUE (usuario_id, group_id)
);

-- Table: usuarios_usuario_user_permissions
CREATE TABLE usuarios_usuario_user_permissions (
    id BIGSERIAL PRIMARY KEY,
    usuario_id BIGINT NOT NULL,
    permission_id INTEGER NOT NULL,
    UNIQUE (usuario_id, permission_id)
);

-- Table: ventaservicios_detalleventaservicio
CREATE TABLE ventaservicios_detalleventaservicio (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad >= 0),
    precio_unitario DECIMAL(10,2) NOT NULL,
    descuento_linea DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    servicio_id BIGINT NOT NULL,
    venta_id BIGINT NOT NULL
);

-- Table: ventaservicios_ventaservicio
CREATE TABLE ventaservicios_ventaservicio (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP(6) NOT NULL,
    updated_at TIMESTAMP(6) NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad >= 0),
    precio_unitario DECIMAL(10,2) NOT NULL,
    descuento DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    metodo_pago VARCHAR(20) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    fecha_venta TIMESTAMP(6) NOT NULL,
    fecha_pago TIMESTAMP(6) DEFAULT NULL,
    observaciones TEXT,
    comision_manicurista DECIMAL(10,2) NOT NULL,
    porcentaje_comision DECIMAL(5,2) NOT NULL,
    cita_id BIGINT DEFAULT NULL,
    cliente_id BIGINT NOT NULL,
    manicurista_id BIGINT NOT NULL,
    servicio_id BIGINT DEFAULT NULL
);

-- Table: ventaservicios_ventaservicio_citas
CREATE TABLE ventaservicios_ventaservicio_citas (
    id BIGSERIAL PRIMARY KEY,
    ventaservicio_id BIGINT NOT NULL,
    cita_id BIGINT NOT NULL,
    UNIQUE (ventaservicio_id, cita_id)
);

-- Create indexes
CREATE INDEX abastecimientos_abas_manicurista_id_27e0eefa_fk_manicuris ON abastecimientos_abastecimiento (manicurista_id);
CREATE INDEX citas_cita_cliente_id_c277d0e3_fk_clientes_cliente_id ON citas_cita (cliente_id);
CREATE INDEX citas_cita_novedad_relacionada__910a49f9_fk_novedades ON citas_cita (novedad_relacionada_id);
CREATE INDEX citas_cita_servicio_id_e2034bca_fk_servicios_servicio_id ON citas_cita (servicio_id);
CREATE INDEX citas_cita_servicios_servicio_id_9cccf56d_fk_servicios ON citas_cita_servicios (servicio_id);
CREATE INDEX comprahasinsumos_com_compra_id_d0ab3545_fk_compras_c ON comprahasinsumos_comprahasinsumo (compra_id);
CREATE INDEX comprahasinsumos_com_insumo_id_b20e8d63_fk_insumos_i ON comprahasinsumos_comprahasinsumo (insumo_id);
CREATE INDEX compras_compra_proveedor_id_d647dfa3_fk_proveedores_proveedor_id ON compras_compra (proveedor_id);
CREATE INDEX compras_detallecompra_insumo_id_f9161ac5_fk_insumos_insumo_id ON compras_detallecompra (insumo_id);
CREATE INDEX insumos_insumo_categoria_insumo_id_45556920_fk_categoria ON insumos_insumo (categoria_insumo_id);
CREATE INDEX insumoshasabastecimi_abastecimiento_id_81f00977_fk_abastecim ON insumoshasabastecimientos_insumohasabastecimiento (abastecimiento_id);
CREATE INDEX insumoshasabastecimi_insumo_id_3e347afc_fk_insumos_i ON insumoshasabastecimientos_insumohasabastecimiento (insumo_id);
CREATE INDEX roles_permiso_accion_id_150a1764_fk_roles_accion_id ON roles_permiso (accion_id);
CREATE INDEX roles_rolhaspermiso_permiso_id_f386bc0e_fk_roles_permiso_id ON roles_rolhaspermiso (permiso_id);
CREATE INDEX usuarios_usuario_rol_id_b0d64932_fk_roles_rol_id ON usuarios_usuario (rol_id);
CREATE INDEX ventaservicios_detal_servicio_id_4035dd54_fk_servicios ON ventaservicios_detalleventaservicio (servicio_id);
CREATE INDEX ventaservicios_detal_venta_id_2daa938b_fk_ventaserv ON ventaservicios_detalleventaservicio (venta_id);
CREATE INDEX ventaservicios_ventaservicio_cita_id_a667bd5a_fk_citas_cita_id ON ventaservicios_ventaservicio (cita_id);
CREATE INDEX ventaservicios_venta_cliente_id_931451b7_fk_clientes_ ON ventaservicios_ventaservicio (cliente_id);
CREATE INDEX ventaservicios_venta_manicurista_id_ca3e4e55_fk_manicuris ON ventaservicios_ventaservicio (manicurista_id);
CREATE INDEX ventaservicios_venta_servicio_id_1ea209b9_fk_servicios ON ventaservicios_ventaservicio (servicio_id);
CREATE INDEX ventaservicios_venta_cita_id_dfd9d601_fk_citas_cit ON ventaservicios_ventaservicio_citas (cita_id);

-- Add foreign key constraints
ALTER TABLE abastecimientos_abastecimiento ADD CONSTRAINT abastecimientos_abas_manicurista_id_27e0eefa_fk_manicuris FOREIGN KEY (manicurista_id) REFERENCES manicuristas_manicurista (id);
ALTER TABLE citas_cita ADD CONSTRAINT citas_cita_cliente_id_c277d0e3_fk_clientes_cliente_id FOREIGN KEY (cliente_id) REFERENCES clientes_cliente (id);
ALTER TABLE citas_cita ADD CONSTRAINT citas_cita_manicurista_id_f3261d8e_fk_manicuris FOREIGN KEY (manicurista_id) REFERENCES manicuristas_manicurista (id);
ALTER TABLE citas_cita ADD CONSTRAINT citas_cita_novedad_relacionada__910a49f9_fk_novedades FOREIGN KEY (novedad_relacionada_id) REFERENCES novedades_novedad (id);
ALTER TABLE citas_cita ADD CONSTRAINT citas_cita_servicio_id_e2034bca_fk_servicios_servicio_id FOREIGN KEY (servicio_id) REFERENCES servicios_servicio (id);
ALTER TABLE citas_cita_servicios ADD CONSTRAINT citas_cita_servicios_cita_id_f9396f28_fk_citas_cita_id FOREIGN KEY (cita_id) REFERENCES citas_cita (id);
ALTER TABLE citas_cita_servicios ADD CONSTRAINT citas_cita_servicios_servicio_id_9cccf56d_fk_servicios FOREIGN KEY (servicio_id) REFERENCES servicios_servicio (id);
ALTER TABLE clientes_cliente ADD CONSTRAINT clientes_cliente_usuario_id_0e496d29_fk_usuarios_usuario_id FOREIGN KEY (usuario_id) REFERENCES usuarios_usuario (id);
ALTER TABLE comprahasinsumos_comprahasinsumo ADD CONSTRAINT comprahasinsumos_com_compra_id_d0ab3545_fk_compras_c FOREIGN KEY (compra_id) REFERENCES compras_compra (id);
ALTER TABLE comprahasinsumos_comprahasinsumo ADD CONSTRAINT comprahasinsumos_com_insumo_id_b20e8d63_fk_insumos_i FOREIGN KEY (insumo_id) REFERENCES insumos_insumo (id);
ALTER TABLE compras_compra ADD CONSTRAINT compras_compra_proveedor_id_d647dfa3_fk_proveedores_proveedor_id FOREIGN KEY (proveedor_id) REFERENCES proveedores_proveedor (id);
ALTER TABLE compras_detallecompra ADD CONSTRAINT compras_detallecompra_compra_id_9d6236ea_fk_compras_compra_id FOREIGN KEY (compra_id) REFERENCES compras_compra (id);
ALTER TABLE compras_detallecompra ADD CONSTRAINT compras_detallecompra_insumo_id_f9161ac5_fk_insumos_insumo_id FOREIGN KEY (insumo_id) REFERENCES insumos_insumo (id);
ALTER TABLE insumos_insumo ADD CONSTRAINT insumos_insumo_categoria_insumo_id_45556920_fk_categoria FOREIGN KEY (categoria_insumo_id) REFERENCES categoriainsumos_categoriainsumo (id);
ALTER TABLE insumoshasabastecimientos_insumohasabastecimiento ADD CONSTRAINT insumoshasabastecimi_abastecimiento_id_81f00977_fk_abastecim FOREIGN KEY (abastecimiento_id) REFERENCES abastecimientos_abastecimiento (id);
ALTER TABLE insumoshasabastecimientos_insumohasabastecimiento ADD CONSTRAINT insumoshasabastecimi_insumo_id_3e347afc_fk_insumos_i FOREIGN KEY (insumo_id) REFERENCES insumos_insumo (id);
ALTER TABLE liquidaciones ADD CONSTRAINT liquidaciones_manicurista_id_135cb2c7_fk_manicuris FOREIGN KEY (manicurista_id) REFERENCES manicuristas_manicurista (id);
ALTER TABLE manicuristas_manicurista ADD CONSTRAINT manicuristas_manicur_usuario_id_e6c44fb9_fk_usuarios_ FOREIGN KEY (usuario_id) REFERENCES usuarios_usuario (id);
ALTER TABLE novedades_novedad ADD CONSTRAINT novedades_novedad_manicurista_id_e9b07828_fk_manicuris FOREIGN KEY (manicurista_id) REFERENCES manicuristas_manicurista (id);
ALTER TABLE roles_permiso ADD CONSTRAINT roles_permiso_accion_id_150a1764_fk_roles_accion_id FOREIGN KEY (accion_id) REFERENCES roles_accion (id);
ALTER TABLE roles_permiso ADD CONSTRAINT roles_permiso_modulo_id_233f39cd_fk_roles_modulo_id FOREIGN KEY (modulo_id) REFERENCES roles_modulo (id);
ALTER TABLE roles_rolhaspermiso ADD CONSTRAINT roles_rolhaspermiso_permiso_id_f386bc0e_fk_roles_permiso_id FOREIGN KEY (permiso_id) REFERENCES roles_permiso (id);
ALTER TABLE roles_rolhaspermiso ADD CONSTRAINT roles_rolhaspermiso_rol_id_2553b94a_fk_roles_rol_id FOREIGN KEY (rol_id) REFERENCES roles_rol (id);
ALTER TABLE usuarios_usuario ADD CONSTRAINT usuarios_usuario_rol_id_b0d64932_fk_roles_rol_id FOREIGN KEY (rol_id) REFERENCES roles_rol (id);
ALTER TABLE ventaservicios_detalleventaservicio ADD CONSTRAINT ventaservicios_detal_servicio_id_4035dd54_fk_servicios FOREIGN KEY (servicio_id) REFERENCES servicios_servicio (id);
ALTER TABLE ventaservicios_detalleventaservicio ADD CONSTRAINT ventaservicios_detal_venta_id_2daa938b_fk_ventaserv FOREIGN KEY (venta_id) REFERENCES ventaservicios_ventaservicio (id);
ALTER TABLE ventaservicios_ventaservicio ADD CONSTRAINT ventaservicios_venta_cliente_id_931451b7_fk_clientes_ FOREIGN KEY (cliente_id) REFERENCES clientes_cliente (id);
ALTER TABLE ventaservicios_ventaservicio ADD CONSTRAINT ventaservicios_venta_manicurista_id_ca3e4e55_fk_manicuris FOREIGN KEY (manicurista_id) REFERENCES manicuristas_manicurista (id);
ALTER TABLE ventaservicios_ventaservicio ADD CONSTRAINT ventaservicios_venta_servicio_id_1ea209b9_fk_servicios FOREIGN KEY (servicio_id) REFERENCES servicios_servicio (id);
ALTER TABLE ventaservicios_ventaservicio ADD CONSTRAINT ventaservicios_ventaservicio_cita_id_a667bd5a_fk_citas_cita_id FOREIGN KEY (cita_id) REFERENCES citas_cita (id);
ALTER TABLE ventaservicios_ventaservicio_citas ADD CONSTRAINT ventaservicios_venta_cita_id_dfd9d601_fk_citas_cit FOREIGN KEY (cita_id) REFERENCES citas_cita (id);
ALTER TABLE ventaservicios_ventaservicio_citas ADD CONSTRAINT ventaservicios_venta_ventaservicio_id_01ce127a_fk_ventaserv FOREIGN KEY (ventaservicio_id) REFERENCES ventaservicios_ventaservicio (id);

-- Set sequences to start from the correct values
SELECT setval('abastecimientos_abastecimiento_id_seq', 2, false);
SELECT setval('categoriainsumos_categoriainsumo_id_seq', 3, false);
SELECT setval('compras_compra_id_seq', 3, false);
SELECT setval('compras_detallecompra_id_seq', 3, false);
SELECT setval('insumos_insumo_id_seq', 3, false);
SELECT setval('insumoshasabastecimientos_insumohasabastecimiento_id_seq', 2, false);
SELECT setval('manicuristas_manicurista_id_seq', 3, false);
SELECT setval('proveedores_proveedor_id_seq', 3, false);
SELECT setval('roles_accion_id_seq', 11, false);
SELECT setval('roles_modulo_id_seq', 16, false);
SELECT setval('roles_permiso_id_seq', 147, false);
SELECT setval('roles_rol_id_seq', 5, false);
SELECT setval('roles_rolhaspermiso_id_seq', 538, false);
SELECT setval('servicios_servicio_id_seq', 2, false);
SELECT setval('usuarios_usuario_id_seq', 6, false);

-- End of clean PostgreSQL dump
