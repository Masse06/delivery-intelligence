from sqlalchemy import create_engine
import pandas as pd

def load_and_clean_data(file_path):
    # Carga de datos crudos
    df = pd.read_csv(file_path)
    
    # Estandarizacion de texto pasando a minusculas y eliminando espacios
    df['Ubicacion'] = df['Ubicacion'].astype(str).str.strip().str.lower()
    
    # Manejo de valores nulos asignando un string generico
    df['Ubicacion'] = df['Ubicacion'].replace(['nan', ''], 'desconocida')
    
    return df

def anonymize_locations(df):
    # Generacion de identificadores unicos para proteger direcciones reales
    unique_locations = df['Ubicacion'].unique()
    zone_mapping = {real_loc: f"zone_{i}" for i, real_loc in enumerate(unique_locations)}
    
    # Mapeo de zonas y eliminacion de la columna original
    df['zone_id'] = df['Ubicacion'].map(zone_mapping)
    df = df.drop(columns=['Ubicacion'])
    
    # Exportacion del diccionario de zonas para control interno local
    mapping_df = pd.DataFrame(list(zone_mapping.items()), columns=['real_location', 'zone_id'])
    mapping_df.to_csv('internal_zone_mapping.csv', index=False)
    
    return df

def enrich_data(df):
    # Transformacion de cadenas de texto a tipos temporales
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
    df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S').dt.time
    
    # Extraccion de dimensiones temporales
    df['day_of_week'] = df['Fecha'].dt.day_name()
    df['is_weekend'] = df['Fecha'].dt.dayofweek.isin([5, 6])
    
    # Agrupacion en bloques horarios de negocio
    def classify_time_slot(time_val):
        h = time_val.hour
        if 13 <= h <= 16: return 'lunch'
        elif 17 <= h <= 19: return 'afternoon'
        elif 20 <= h <= 23: return 'dinner'
        else: return 'late_night'
        
    df['time_slot'] = df['Hora'].apply(classify_time_slot)
    
    # Creacion de KPI de rentabilidad
    df['tip_percentage'] = (df['Propina'] / df['Monto_Pedido']) * 100
    df['tip_percentage'] = df['tip_percentage'].round(2)
    
    return df

def execute_etl_pipeline():
    # Definicion de rutas de entrada y salida
    input_file = 'tiptracker.csv'
    output_file = 'processed_orders.csv'
    
    # Ejecucion del flujo de transformacion
    df = load_and_clean_data(input_file)
    df = anonymize_locations(df)
    df = enrich_data(df)
    
    # Persistencia de los datos procesados
    df.to_csv(output_file, index=False)

def load_to_postgres(df, zone_mapping_df):
    # ATENCION: Reemplaza esta URL por tu Connection String real de Neon
    db_url = "postgresql://neondb_owner:npg_WyufOFEw98iT@ep-raspy-sky-alb4ogot.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require"
    engine = create_engine(db_url)
    
    print("Conectando a la base de datos en la nube...")
    
    try:
        # 1. Cargar las dimensiones primero (para no romper las Foreign Keys)
        
        # Dimension Zonas (Subimos el ID de zona. NOTA: No subimos las direcciones reales)
        dim_zones = zone_mapping_df[['zone_id']].copy()
        dim_zones['zone_alias'] = "Zona Analitica" # Podriamos darle nombres mas descriptivos despues
        dim_zones.to_sql('dim_zones', engine, if_exists='append', index=False)
        print("- Dimension Zonas cargada.")
        
        # Dimension Fechas (Valores unicos)
        dim_dates = df[['Fecha', 'day_of_week', 'is_weekend']].drop_duplicates()
        dim_dates = dim_dates.rename(columns={'Fecha': 'date_id'})
        dim_dates.to_sql('dim_dates', engine, if_exists='append', index=False)
        print("- Dimension Fechas cargada.")
        
        # Dimension Tiempos (Valores unicos)
        dim_times = df[['Hora', 'time_slot']].drop_duplicates()
        dim_times = dim_times.rename(columns={'Hora': 'time_id'})
        dim_times.to_sql('dim_times', engine, if_exists='append', index=False)
        print("- Dimension Tiempos cargada.")
        
        # 2. Cargar la Tabla de Hechos
        fact_orders = df[['Fecha', 'Hora', 'zone_id', 'Monto_Pedido', 'Propina', 'tip_percentage', 'Metodo_Pago']].copy()
        fact_orders = fact_orders.rename(columns={
            'Fecha': 'date_id',
            'Hora': 'time_id',
            'Monto_Pedido': 'order_amount',
            'Propina': 'tip_amount',
            'Metodo_Pago': 'payment_method'
        })
        fact_orders.to_sql('fact_orders', engine, if_exists='append', index=False)
        print("- Tabla de Hechos cargada exitosamente.")
        
        print("Proceso ETL finalizado con exito. Datos en Produccion.")
        
    except Exception as e:
        print(f"Error durante la carga a la base de datos: {e}")

def execute_etl_pipeline():
    input_file = 'tiptracker.csv'
    
    # E + T
    df = load_and_clean_data(input_file)
    df = anonymize_locations(df)
    
    # Recuperamos el mapeo de zonas para subir los IDs a la base de datos
    zone_mapping_df = pd.read_csv('internal_zone_mapping.csv')
    
    df = enrich_data(df)
    
    # L
    load_to_postgres(df, zone_mapping_df)

if __name__ == "__main__":
    execute_etl_pipeline()