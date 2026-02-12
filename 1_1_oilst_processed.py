import pandas as pd
import numpy as np

def process_olist_data():
    """
    Consolida las fuentes orders, customers y geolocation.
    Calcula KPIs logísticos y temporales.
    """
    try:
        # 1. Carga de archivos fuente
        df_orders = pd.read_csv('orders.csv')
        df_customers = pd.read_csv('customers.csv')
        df_geo = pd.read_csv('geolocation.csv')

        # 2. Merge de datos
        # Unimos órdenes con clientes
        df_merged = pd.merge(df_orders, df_customers, on='customer_id', how='left')
        
        # Unimos con geolocalización basada en el código postal
        df_final = pd.merge(
            df_merged, 
            df_geo, 
            left_on='customer_zip_code_prefix', 
            right_on='geolocation_zip_code_prefix', 
            how='left'
        )

        # 3. Conversión de fechas
        date_cols = [
            'order_purchase_timestamp', 'order_approved_at', 
            'order_delivered_customer_date', 'order_estimated_delivery_date'
        ]
        for col in date_cols:
            df_final[col] = pd.to_datetime(df_final[col])

        # 4. Cálculo de Campos Solicitados
        
        # total_products y total_sales
        df_final['total_products'] = df_final['item_count']
        df_final['total_sales'] = df_final['item_price'] * df_final['item_count']

        # Campos temporales (basados en la fecha de compra)
        df_final['year'] = df_final['order_purchase_timestamp'].dt.year
        df_final['month'] = df_final['order_purchase_timestamp'].dt.month
        df_final['quarter'] = df_final['order_purchase_timestamp'].dt.quarter
        df_final['year_month'] = df_final['order_purchase_timestamp'].dt.strftime('%Y-%m')

        # delta_days: días entre estimado y real
        # Nota: (Entrega Real - Entrega Estimada). Si es > 0, es retraso.
        df_final['delta_days'] = (df_final['order_delivered_customer_date'] - df_final['order_estimated_delivery_date']).dt.days

        # delay_status: clasificación del retraso
        def classify_delay(days):
            if pd.isna(days) or days <= 0:
                return "sin retraso"
            elif days <= 3:
                return "retraso corto"
            else:
                return "retraso largo"

        df_final['delay_status'] = df_final['delta_days'].apply(classify_delay)

        # 5. Selección y Ordenamiento de columnas según requerimiento
        ordered_columns = [
            'order_id', 'customer_id', 'order_status', 'order_purchase_timestamp',
            'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date',
            'order_estimated_delivery_date', 'distance_distribution_center', 'customer_unique_id',
            'customer_zip_code_prefix', 'customer_city', 'customer_state', 'geolocation_zip_code_prefix',
            'geolocation_lat', 'geolocation_lng', 'geolocation_city', 'geolocation_state',
            'abbreviation', 'state_name', 'total_products', 'total_sales', 'year', 'month',
            'quarter', 'year_month', 'delta_days', 'delay_status'
        ]
        
        df_consolidated = df_final[ordered_columns]

        # 6. Exportación final
        output_file = "oilst_processed.csv"
        df_consolidated.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"Procesamiento exitoso. El archivo '{output_file}' ha sido generado.")
        print(f"Total de registros procesados: {len(df_consolidated)}")
        print("\nPrimeros registros de campos calculados:")
        print(df_consolidated[['order_id', 'delta_days', 'delay_status']].head())

    except Exception as e:
        print(f"Error durante la consolidación: {e}")

if __name__ == "__main__":
    process_olist_data()