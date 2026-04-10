-- Esquema Analitico para Delivery Intelligence Engine (Modelo de Estrella)

-- Tabla de Dimension: Zonas Analiticas
CREATE TABLE dim_zones (
    zone_id VARCHAR(50) PRIMARY KEY,
    zone_alias VARCHAR(100) NOT NULL
);

-- Tabla de Dimension: Franjas Horarias
CREATE TABLE dim_times (
    time_id VARCHAR(50) PRIMARY KEY,
    time_slot VARCHAR(50) NOT NULL
);

-- Tabla de Hechos: Registros de Pedidos
CREATE TABLE fact_orders (
    order_id SERIAL PRIMARY KEY,
    zone_id VARCHAR(50) NOT NULL,
    time_id VARCHAR(50) NOT NULL,
    tip_percentage DECIMAL(5, 2) NOT NULL,
    
    -- Relaciones de integridad referencial
    CONSTRAINT fk_zone FOREIGN KEY (zone_id) REFERENCES dim_zones (zone_id) ON DELETE CASCADE,
    CONSTRAINT fk_time FOREIGN KEY (time_id) REFERENCES dim_times (time_id) ON DELETE CASCADE
);

-- Indices para optimizacion de consultas de agregacion (AVG, COUNT)
CREATE INDEX idx_fact_zone_id ON fact_orders(zone_id);
CREATE INDEX idx_fact_time_id ON fact_orders(time_id);