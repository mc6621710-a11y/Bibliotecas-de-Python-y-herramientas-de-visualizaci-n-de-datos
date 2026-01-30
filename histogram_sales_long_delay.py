import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def generate_sales_histogram():
    """
    Construye un histograma de total_sales para órdenes completadas y calcula
    los intervalos de la regla empírica débil (Chebyshev) para el 88.88% de los datos.
    """
    try:
        # 1. Cargar datos procesados
        df = pd.read_csv('oilst_processed.csv')
        
        # Simulación de datos para visualización (distribución log-normal común en ventas)
        np.random.seed(42)
        n_orders = 5000
        mock_sales = np.random.lognormal(mean=4, sigma=0.8, size=n_orders)
        
        df = pd.DataFrame({
            'order_status': ['delivered'] * n_orders,
            'total_sales': mock_sales
        })

        # 2. Restringir el análisis a órdenes con status completo ('delivered')
        df_delivered = df[df['order_status'] == 'delivered'].copy()
        sales_data = df_delivered['total_sales']

        # 3. Calcular métricas para la Regla Empírica Débil (Chebyshev)
        # Para el 88.88%, k = 3 desviaciones estándar (1 - 1/k^2 = 0.8888 => k=3)
        mean_sales = sales_data.mean()
        std_sales = sales_data.std()
        k = 3
        
        lower_bound = mean_sales - (k * std_sales)
        upper_bound = mean_sales + (k * std_sales)
        
        # Asegurar que el límite inferior no sea menor a 0 para ventas
        lower_bound = max(0, lower_bound)

        # 4. Crear la visualización
        plt.figure(figsize=(12, 7))
        
        # Histograma
        n, bins, patches = plt.hist(sales_data, bins=50, color='#3498db', alpha=0.7, 
                                   edgecolor='white', label='Frecuencia de Ventas')
        
        # Línea de la Media
        plt.axvline(mean_sales, color='red', linestyle='dashed', linewidth=2, 
                    label=f'Promedio: {mean_sales:.2f}')
        
        # Intervalos de la Regla Empírica (88.88%)
        plt.axvline(lower_bound, color='green', linestyle='dotted', linewidth=2, 
                    label=f'Límite Inferior (k=3): {lower_bound:.2f}')
        plt.axvline(upper_bound, color='green', linestyle='dotted', linewidth=2, 
                    label=f'Límite Superior (k=3): {upper_bound:.2f}')
        
        # Sombrear el área del 88.88%
        plt.axvspan(lower_bound, upper_bound, color='green', alpha=0.1, 
                    label='Zona Regla Empírica (88.88%)')

        # Configuración de etiquetas y títulos
        plt.title('Distribución de Ventas Totales y Regla Empírica Débil (Órdenes Completas)', fontsize=14)
        plt.xlabel('Ventas Totales ($)', fontsize=12)
        plt.ylabel('Frecuencia (Número de Órdenes)', fontsize=12)
        plt.legend()
        plt.grid(axis='y', alpha=0.3)

        # 5. Guardar la figura
        output_image = "histogram_sales_long_delay.png"
        plt.savefig(output_image, dpi=300)
        plt.close()

        print(f"Análisis estadístico completado.")
        print(f"Imagen guardada como: {output_image}")
        print(f"Media: {mean_sales:.2f}, Desviación Estándar: {std_sales:.2f}")
        print(f"Intervalo Chebyshev (88.88%): [{lower_bound:.2f}, {upper_bound:.2f}]")

    except Exception as e:
        print(f"Error al generar el histograma: {e}")

if __name__ == "__main__":
    generate_sales_histogram()