import pandas as pd
import numpy as np
from datetime import datetime

def process_olist_data():
    """
    Script para consolidar fuentes de datos de e-commerce y generar campos calculados
    para el análisis de logística y retrasos.
    """
    
    # Nota: En un entorno real, se cargarían los archivos CSV individuales.
    # Aquí simulamos la estructura de datos basada en los campos provistos.
    
    try:
        # 1. Carga de datos (Simulada para estructura de ejemplo)
        # Se asume que existen archivos como orders.csv, customers.csv, etc.
        # df_orders = pd.read_csv('orders.csv')
        # df_customers = pd.read_csv('customers.csv')
        
        # Para propósitos de este script, creamos un DataFrame con la estructura requerida
        # que representa la unión de las fuentes mencionadas.
        data = {
            'order_id': ['ord_001', 'ord_002', 'ord_003'],
            'customer_id': ['cust_001', 'cust_002', 'cust_003'],
            'order_status': ['delivered', 'delivered', 'delivered'],
            'order_purchase_timestamp': ['2023-05-10 10:00:00', '2023-05-12 15:30:00', '2023-06-01 09:00:00'],
            'order_approved_at': ['2023-05-10 10:15:00', '2023-05-12 16:00:00', '2023-06-01 09:45:00'],
            'order_delivered_carrier_date': ['2023-05-11', '2023-05-13', '2023-06-02'],
            'order_delivered_customer_date': ['2023-05-15 14:00:00', '2023-05-22 18:00:00', '2023-06-05 12:00:00'],
            'order_estimated_delivery_date': ['2023-05-16 00:00:00', '2023-05-18 00:00:00', '2023-06-07 00:00:00'],
            'distance_distribution_center': [15.5, 120.3, 45.0],
            'customer_unique_id': ['u_001', 'u_002', 'u_003'],
            'customer_zip_code_prefix': ['01001', '20001', '30001'],
            'customer_city': ['sao paulo', 'rio de janeiro', 'belo horizonte'],
            'customer_state': ['SP', 'RJ', 'MG'],
            'geolocation_zip_code_prefix': ['01001', '20001', '30001'],
            'geolocation_lat': [-23.55, -22.90, -19.91],
            'geolocation_lng': [-46.63, -43.17, -43.93],
            'geolocation_city': ['sao paulo', 'rio de janeiro', 'belo horizonte'],
            'geolocation_state': ['SP', 'RJ', 'MG'],
            'abbreviation': ['SP', 'RJ', 'MG'],
            'state_name': ['São Paulo', 'Rio de Janeiro', 'Minas Gerais'],
            # Datos para cálculos de ventas (normalmente vendrían de order_items)
            'item_price': [100.0, 50.0, 200.0],
            'item_count': [1, 2, 1]
        }
        
        df = pd.DataFrame(data)

        # 2. Conversión de campos de fecha a datetime
        date_columns = [
            'order_purchase_timestamp', 
            'order_approved_at', 
            'order_delivered_customer_date', 
            'order_estimated_delivery_date'
        ]
        for col in date_columns:
            df[col] = pd.to_datetime(df[col])

        # 3. Cálculo de campos solicitados
        
        # total_products y total_sales
        # Nota: En una consolidación real, esto sería un groupby por order_id
        df['total_products'] = df['item_count']
        df['total_sales'] = df['item_price'] * df['item_count']

        # Campos temporales basados en order_purchase_timestamp
        df['year'] = df['order_purchase_timestamp'].dt.year
        df['month'] = df['order_purchase_timestamp'].dt.month
        df['quarter'] = df['order_purchase_timestamp'].dt.quarter
        df['year_month'] = df['order_purchase_timestamp'].dt.strftime('%Y-%m')

        # delta_days: días entre entrega estimada y entrega efectiva
        # (Positivo significa retraso, negativo significa entrega adelantada)
        df['delta_days'] = (df['order_delivered_customer_date'] - df['order_estimated_delivery_date']).dt.days

        # delay_status: clasificación del retraso
        def classify_delay(days):
            if days <= 0:
                return "sin retraso"
            elif days <= 3:
                return "retraso corto"
            else:
                return "retraso largo"

        df['delay_status'] = df['delta_days'].apply(classify_delay)

        # 4. Limpieza final de columnas (quitar columnas auxiliares si existen)
        columns_to_keep = [
            'order_id', 'customer_id', 'order_status', 'order_purchase_timestamp',
            'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date',
            'order_estimated_delivery_date', 'distance_distribution_center', 'customer_unique_id',
            'customer_zip_code_prefix', 'customer_city', 'customer_state', 'geolocation_zip_code_prefix',
            'geolocation_lat', 'geolocation_lng', 'geolocation_city', 'geolocation_state',
            'abbreviation', 'state_name', 'total_products', 'total_sales', 'year', 'month',
            'quarter', 'year_month', 'delta_days', 'delay_status'
        ]
        
        df_consolidated = df[columns_to_keep]

        # 5. Exportación a CSV
        output_filename = "oilst_processed.csv"
        df_consolidated.to_csv(output_filename, index=False, encoding='utf-8')
        
        print(f"Procesamiento completado exitosamente. Archivo guardado como: {output_filename}")
        print(df_consolidated[['order_id', 'delta_days', 'delay_status']].head())
        
        return df_consolidated

    except Exception as e:
        print(f"Error durante el procesamiento: {e}")

if __name__ == "__main__":
    process_olist_data()