import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def calculate_sales_proportion_with_chart():
    """
    Calcula la proporción de ventas totales por delay_status y trimestre (2016-2018)
    y genera una figura gráfica representativa.
    """
    try:
        # 1. Carga o Simulación de datos
        # Intentamos leer el archivo procesado si existe, de lo contrario simulamos
        file_path = 'oilst_processed.csv'
        
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
        else:
            print(f"Aviso: '{file_path}' no encontrado. Generando datos simulados (2016-2018)...")
            dates = pd.date_range(start='2016-01-01', end='2018-12-31', freq='ME')
            mock_data = []
            statuses = ['sin retraso', 'retraso corto', 'retraso largo']
            for date in dates:
                for status in statuses:
                    # Simulamos ventas con variaciones para que el gráfico sea interesante
                    base_sales = 5000 if status == 'sin retraso' else 1500
                    sales = base_sales + np.random.uniform(-1000, 2000)
                    mock_data.append({
                        'order_purchase_timestamp': date,
                        'year': date.year,
                        'quarter': (date.month - 1) // 3 + 1,
                        'delay_status': status,
                        'total_sales': sales
                    })
            df = pd.DataFrame(mock_data)

        # 2. Procesamiento de Proporciones
        df_filtered = df[(df['year'] >= 2016) & (df['year'] <= 2018)].copy()
        
        # Agrupamos para obtener ventas por status y total trimestral
        grouped = df_filtered.groupby(['year', 'quarter', 'delay_status'])['total_sales'].sum().reset_index()
        totals = df_filtered.groupby(['year', 'quarter'])['total_sales'].sum().reset_index()
        totals = totals.rename(columns={'total_sales': 'quarter_total_sales'})
        
        final_df = pd.merge(grouped, totals, on=['year', 'quarter'])
        final_df['proportion'] = final_df['total_sales'] / final_df['quarter_total_sales']
        
        # Creamos una etiqueta de eje X amigable (ej: 2017-Q1)
        final_df['periodo'] = final_df['year'].astype(str) + '-Q' + final_df['quarter'].astype(str)
        final_df = final_df.sort_values(['year', 'quarter'])

        # 3. Generación de la Figura Gráfica
        plt.figure(figsize=(12, 7))
        sns.set_theme(style="whitegrid")
        
        # Gráfico de barras apiladas o líneas. Usaremos líneas para ver la tendencia.
        chart = sns.lineplot(
            data=final_df, 
            x='periodo', 
            y='proportion', 
            hue='delay_status', 
            marker='o',
            palette={'sin retraso': '#2ecc71', 'retraso corto': '#f1c40f', 'retraso largo': '#e74c3c'},
            linewidth=2.5
        )

        plt.title('Evolución de la Proporción de Ventas por Estado de Retraso (2016-2018)', fontsize=14, pad=15)
        plt.xlabel('Trimestre', fontsize=12)
        plt.ylabel('Proporción del Total de Ventas (%)', fontsize=12)
        plt.ylim(0, 1.1)
        plt.legend(title='Estatus de Entrega', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # 4. Guardar resultados
        output_image = "prop_sales_delay_status_by_quarter_chart.png"
        output_csv = "prop_sales_delay_status_by_quarte.csv"
        
        plt.savefig(output_image, dpi=300)
        final_df[['year', 'quarter', 'delay_status', 'total_sales', 'proportion']].to_csv(output_csv, index=False)
        
        plt.close()

        print(f"Análisis finalizado.")
        print(f"1. Datos guardados en: {output_csv}")
        print(f"2. Gráfica guardada en: {output_image}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    calculate_sales_proportion_with_chart()