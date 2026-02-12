import pandas as pd
import os

def calculate_order_counts_by_basket_size():
    """
    Construye una tabla que muestra el número de órdenes por cantidad de productos 
    (total_products) y la categoría de retraso (delay_status).
    """
    input_file = 'oilst_processed.csv'
    output_file = 'count_orders_basket_size_by_delay_status.csv'

    try:
        # 1. Verificar si el archivo fuente existe
        if not os.path.exists(input_file):
            print(f"Error: No se encontró el archivo '{input_file}'.")
            return

        # 2. Cargar los datos procesados
        df = pd.read_csv(input_file)

        # 3. Validar que las columnas necesarias estén presentes
        required_columns = ['order_id', 'total_products', 'delay_status']
        if not all(col in df.columns for col in required_columns):
            print(f"Error: El archivo no contiene las columnas necesarias: {required_columns}")
            return

        # 4. Agrupar por tamaño de cesta (total_products) y estado de retraso
        # Contamos los order_id únicos para obtener el volumen de órdenes
        counts_df = df.groupby(['total_products', 'delay_status'])['order_id'].nunique().reset_index()

        # 5. Renombrar columnas para cumplir con el estándar de reporte
        counts_df.columns = ['basket_size', 'delay_status', 'order_count']

        # 6. Ordenar los resultados para facilitar el análisis
        # Ordenamos por tamaño de cesta de menor a mayor
        counts_df = counts_df.sort_values(by=['basket_size', 'delay_status'])

        # 7. Guardar el resultado en formato CSV
        counts_df.to_csv(output_file, index=False, encoding='utf-8')

        print(f"Procesamiento finalizado con éxito.")
        print(f"El archivo '{output_file}' ha sido generado.")
        
        # Mostrar una vista previa de los resultados en la consola
        print("\nVista previa del conteo por tamaño de cesta:")
        print(counts_df.head(15))

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    calculate_order_counts_by_basket_size()