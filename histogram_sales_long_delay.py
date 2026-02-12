import pandas as pd
import numpy as np
import os

# Intentar importar matplotlib para la generación de la figura gráfica
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Error: La librería 'matplotlib' no está instalada.")
    plt = None

def generate_sales_histogram():
    """
    Construye un histograma de total_sales para órdenes completadas y calcula
    los intervalos de la regla empírica débil (Chebyshev) para el 88.88% de los datos.
    """
    if plt is None:
        print("No se puede generar el histograma sin la librería matplotlib.")
        return

    input_file = 'oilst_processed.csv'
    output_image = "histogram_sales_long_delay.png"

    try:
        # 1. Verificar si el archivo fuente existe
        if not os.path.exists(input_file):
            print(f"Error: No se encontró el archivo '{input_file}'.")
            return

        # 2. Cargar los datos procesados
        df = pd.read_csv(input_file)

        # 3. Filtrar por órdenes con status completo ('delivered')
        # Es fundamental asegurar que solo analizamos ventas de pedidos finalizados
        df_delivered = df[df['order_status'] == 'delivered'].copy()

        if df_delivered.empty:
            print("Error: No se encontraron órdenes con status 'delivered' para analizar.")
            return

        # Limpieza de datos: extraer ventas y eliminar nulos
        sales_data = df_delivered['total_sales'].dropna()

        # 4. Cálculo de la Regla Empírica Débil (Teorema de Chebyshev)
        # Para cubrir al menos el 88.88% de los datos, k debe ser igual a 3
        # Fórmula: 1 - (1/k^2) = 0.8888 => k = 3
        mean_sales = sales_data.mean()
        std_sales = sales_data.std()
        k = 3
        
        lower_bound = mean_sales - (k * std_sales)
        upper_bound = mean_sales + (k * std_sales)
        
        # Ajuste lógico: El límite inferior de ventas monetarias no puede ser menor a 0
        lower_bound = max(0, lower_bound)

        # 5. Generación de la Figura Gráfica
        plt.figure(figsize=(12, 7))
        
        # Histograma de frecuencias
        plt.hist(sales_data, bins=50, color='#3498db', alpha=0.7, 
                 edgecolor='white', label='Frecuencia de Ventas')
        
        # Línea indicadora de la Media
        plt.axvline(mean_sales, color='red', linestyle='dashed', linewidth=2, 
                    label=f'Promedio: {mean_sales:.2f}')
        
        # Líneas de los intervalos de Chebyshev (88.88%)
        plt.axvline(lower_bound, color='green', linestyle='dotted', linewidth=2, 
                    label=f'Límite Inferior (k=3): {lower_bound:.2f}')
        plt.axvline(upper_bound, color='green', linestyle='dotted', linewidth=2, 
                    label=f'Límite Superior (k=3): {upper_bound:.2f}')
        
        # Sombrear el área de la regla empírica débil
        plt.axvspan(lower_bound, upper_bound, color='green', alpha=0.1, 
                    label='Zona 88.88% (Chebyshev)')

        # Personalización y Títulos
        plt.title('Distribución de Ventas Totales y Regla Empírica Débil', fontsize=14)
        plt.xlabel('Ventas Totales (USD)', fontsize=12)
        plt.ylabel('Número de Órdenes (Frecuencia)', fontsize=12)
        plt.legend()
        plt.grid(axis='y', alpha=0.3)

        # 6. Guardar la figura resultante
        plt.savefig(output_image, dpi=300)
        plt.close()

        print(f"Procesamiento finalizado. La figura '{output_image}' ha sido generada.")
        print(f"--- Estadísticas Descriptivas ---")
        print(f"Promedio de Ventas: {mean_sales:.2f}")
        print(f"Desviación Estándar: {std_sales:.2f}")
        print(f"Intervalo del 88.88%: [{lower_bound:.2f}, {upper_bound:.2f}]")

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    generate_sales_histogram()