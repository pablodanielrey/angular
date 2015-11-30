
CREATE SCHEMA  expedientes  ;


-- -----------------------------------------------------
-- Table expedientes.lugar
-- -----------------------------------------------------
CREATE TABLE  expedientes.lugar (
  id SERIAL,
  descripcion VARCHAR(255) NOT NULL UNIQUE,
  PRIMARY KEY (id))
;


-- -----------------------------------------------------
-- Table expedientes.persona
-- -----------------------------------------------------
CREATE TABLE  expedientes.persona (
  id SERIAL,
  nombres VARCHAR(255) NOT NULL,
  apellidos VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (id))
;


-- -----------------------------------------------------
-- Table expedientes.tema
-- -----------------------------------------------------
CREATE TABLE  expedientes.tema (
  id SERIAL,
  descripcion VARCHAR(255) NOT NULL UNIQUE,
  PRIMARY KEY (id))
;




-- -----------------------------------------------------
-- Table expedientes.expediente
-- -----------------------------------------------------
CREATE TABLE  expedientes.expediente (
  id SERIAL,
  numero VARCHAR(45) NOT NULL UNIQUE,
  fecha_origen DATE NULL DEFAULT NULL,
  fecha_entrada DATE NULL DEFAULT NULL,
  archivo_numero INTEGER NULL DEFAULT NULL,
  archivo_anio INTEGER NULL DEFAULT NULL,
  antecedente VARCHAR(255) NULL DEFAULT NULL,
  extracto TEXT NULL DEFAULT NULL,
  resolucion_iniciador VARCHAR(255) NULL DEFAULT NULL,
  iniciador INTEGER NULL DEFAULT NULL,
  agregado INTEGER NULL DEFAULT NULL,
  lugar_iniciador INTEGER NULL DEFAULT NULL,
  tema INTEGER NULL DEFAULT NULL,
  ultimo_destino INTEGER NULL DEFAULT NULL UNIQUE,
  PRIMARY KEY (id),
    FOREIGN KEY (agregado)
    REFERENCES expedientes.expediente (id)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
    FOREIGN KEY (lugar_iniciador)
    REFERENCES expedientes.lugar (id)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
    FOREIGN KEY (iniciador)
    REFERENCES expedientes.persona (id)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
    FOREIGN KEY (tema)
    REFERENCES expedientes.tema (id)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT);




-- -----------------------------------------------------
-- Table expedientes.destino
-- -----------------------------------------------------
CREATE TABLE  expedientes.destino (
  id SERIAL,
  fecha_entrada DATE NOT NULL,
  fecha_salida DATE NULL DEFAULT NULL,
  expediente INTEGER NOT NULL,
  lugar INTEGER NOT NULL,
  PRIMARY KEY (id),
    FOREIGN KEY (expediente)
    REFERENCES expedientes.expediente (id)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
    FOREIGN KEY (lugar)
    REFERENCES expedientes.lugar (id)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT);



-- -----------------------------------------------------
-- Table expedientes.nota
-- -----------------------------------------------------
CREATE TABLE  expedientes.nota (
  id SERIAL,
  codigo VARCHAR(8) NOT NULL UNIQUE,
  fecha DATE NULL DEFAULT NULL,
  descripcion TEXT NULL DEFAULT NULL,
  observaciones TEXT NULL DEFAULT NULL,
  persona INTEGER NOT NULL,
  PRIMARY KEY (id),
    FOREIGN KEY (persona)
    REFERENCES expedientes.persona (id)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
;




-- -----------------------------------------------------
-- Table expedientes.participacion
-- -----------------------------------------------------
CREATE TABLE  expedientes.participacion (
  id SERIAL,
  expediente INTEGER NOT NULL,
  persona INTEGER NOT NULL,
  PRIMARY KEY (id),
    FOREIGN KEY (expediente)
    REFERENCES expedientes.expediente (id)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
    FOREIGN KEY (persona)
    REFERENCES expedientes.persona (id)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
;




