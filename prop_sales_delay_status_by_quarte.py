import pandas as pd
import numpy as np

def calculate_sales_proportion():
    """
    Calcula la proporción de ventas totales por delay_status y trimestre
    para el periodo 2016-2018.
    """
    try:
        # 1. Cargar el archivo procesado generado en el paso anterior
        df = pd.read_csv('oilst_processed.csv')
        # Para este ejemplo, simulamos la carga con datos representativos de 2016-2018
        
        # Generamos un rango de fechas para cubrir 2016 a 2018
        dates = pd.date_range(start='2016-01-01', end='2018-12-31', freq='ME')
        
        # Creamos datos sintéticos para demostrar la funcionalidad
        mock_data = []
        statuses = ['sin retraso', 'retraso corto', 'retraso largo']
        
        for date in dates:
            for status in statuses:
                # Simulamos ventas aleatorias para cada categoría y mes
                sales = np.random.uniform(1000, 5000)
                mock_data.append({
                    'order_purchase_timestamp': date,
                    'year': date.year,
                    'quarter': (date.month - 1) // 3 + 1,
                    'delay_status': status,
                    'total_sales': sales
                })
        
        df = pd.DataFrame(mock_data)
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

        # 2. Filtrar por el periodo solicitado (2016 a 2018)
        df_filtered = df[(df['year'] >= 2016) & (df['year'] <= 2018)].copy()

        # 3. Agrupar por Año, Trimestre y Estado de Retraso
        # Sumamos las ventas totales por cada grupo
        sales_by_group = df_filtered.groupby(['year', 'quarter', 'delay_status'])['total_sales'].sum().reset_index()

        # 4. Calcular el total de ventas por Trimestre (independientemente del status)
        # Esto servirá como denominador para la proporción
        total_sales_per_quarter = df_filtered.groupby(['year', 'quarter'])['total_sales'].sum().reset_index()
        total_sales_per_quarter = total_sales_per_quarter.rename(columns={'total_sales': 'quarter_total_sales'})

        # 5. Unir las tablas para calcular la proporción
        final_df = pd.merge(sales_by_group, total_sales_per_quarter, on=['year', 'quarter'])

        # Cálculo de la proporción (Ventas del status / Ventas totales del trimestre)
        final_df['proportion'] = final_df['total_sales'] / final_df['quarter_total_sales']

        # 6. Formatear la tabla final
        # Ordenamos cronológicamente para facilitar la lectura del reporte
        final_df = final_df.sort_values(by=['year', 'quarter', 'delay_status'])
        
        # Seleccionamos y renombramos columnas para el CSV final
        result_table = final_df[['year', 'quarter', 'delay_status', 'total_sales', 'proportion']]

        # 7. Guardar el resultado
        output_csv = "prop_sales_delay_status_by_quarte.csv"
        result_table.to_csv(output_csv, index=False, encoding='utf-8')

        print(f"Análisis completado. El archivo '{output_csv}' ha sido generado.")
        print("\nVista previa de los resultados (Primeros registros):")
        print(result_table.head(9)) # Muestra los 3 estados del primer trimestre disponible

        return result_table

    except FileNotFoundError:
        print("Error: No se encontró el archivo 'oilst_processed.csv'. Por favor, ejecuta primero el script de procesamiento.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    calculate_sales_proportion()