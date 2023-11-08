from fpdf import FPDF
import pandas as pd
import os
import datetime

# Configurar el google sheet
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS9cPVtFsCK_Y5yMaTqLbE2ADxgypL2jh_JWjc96wq-IWht3Cx08sPGbwL2cyvfonmXHNENOg77G3W7/pub?output=csv"  # Reemplaza con tu URL de archivo CSV
df = pd.read_csv(url)

today = datetime.date.today()
folder_name = today.strftime('%Y-%m-%d')
os.makedirs(folder_name, exist_ok=True)

# Clase personalizada para el PDF
class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            self.image('logo.jpg', x=10, y=10, w=30)
            self.image('Esquinero.png', x=self.w - 40, y=10, w=30)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Página %s' % self.page_no(), 0, 0, 'C')

     # Función personalizada para multi_cell con control de interlineado
    def set_text_with_line_height(self, text, line_height):
        font_size = self.font_size_pt / 72.0
        line_height_pt = font_size * 72.0 * line_height

        lines = text.split("\n")
        for line in lines:
            words = line.split()
            current_line = ""
            for word in words:
                if self.get_string_width(current_line + " " + word) > self.w - 2 * self.l_margin:
                    self.multi_cell(self.w - 2 * self.l_margin, line_height_pt, current_line, align="L")
                    current_line = word
                else:
                    current_line += " " + word
            self.multi_cell(self.w - 2 * self.l_margin, line_height_pt, current_line, align="L")

        # Restaurar la posición de las coordenadas después de escribir todo el texto
            # self.set_xy(current_x, current_y)


# Leer el contenido de los archivos renta_fija.txt y renta_variable.txt con la codificación UTF-8
with open('renta_fija.txt', 'r', encoding='utf-8') as file_fija:
    renta_fija_content = file_fija.read()

#with open('renta_variable.txt', 'r', encoding='utf-8') as file_variable:
   # renta_variable_content = file_variable.read()

# Leer el contenido del archivo 'renta_variable.txt'
with open('renta_variable.txt', 'r', encoding='utf-8') as file_variable:
    renta_variable_content = file_variable.read()

# Eliminar líneas en blanco del texto
renta_variable_content = "\n".join(line for line in renta_variable_content.splitlines() if line.strip())

# Reescribir el archivo con el texto modificado
with open('renta_variable.txt', 'w', encoding='utf-8') as file_variable:
    file_variable.write(renta_variable_content)


# Crear un PDF para cada ID de cuenta
for index, row in df.iterrows():
    idCuenta = str(row[0])
    denominacion = str(row[1])
    desde = str(row[2])
    hasta = str(row[3])
    dias = str(row[4])
    vInicial = str(row[5])
    fondeo = str(row[6])
    retiro = str(row[13])
    vFinal = str(row[7])
    bruto = str(row[8])
    periodo = str(row[9])
    anualizada = str(row[10])
    tna = str(row[11])
    cartera = str(row[12])

    # Crear el objeto PDF usando la clase personalizada PDF
    pdf = PDF()
    pdf.add_page()

    # Agregar el contenido al PDF
    pdf.set_y(25)
    pdf.set_font('Arial', 'B', 22)
    pdf.cell(0, 10, 'Informe de cartera', ln=True, align='L')

    pdf.set_y(35)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Segundo trimestre 2023', ln=True, align='L')

    pdf.set_y(50)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Cuenta N° ' + idCuenta, ln=True, align='L')

    pdf.set_y(55)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, denominacion, ln=True, align='L')

    # Agregar contenido adicional a la primera página
    if pdf.page_no() == 1:
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, 'Al cierre del período, la cartera teórica mantenía la siguiente distribución global y composición de activos individuales:', align='L')

        image_width = 160  # Ancho de la imagen
        page_width = pdf.w  # Ancho de la página
        x = (page_width - image_width) / 2  # Cálculo de la posición x para centrar la imagen

        pdf.image('grafico.jpg', x=x, y=100, w=image_width)

    # Agregar el contenido de los archivos de texto en el PDF
        pdf.set_y(160)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 10, 'Renta Fija:', ln=True, align='L')
        pdf.set_font('Arial', '', 11)
        pdf.set_text_with_line_height(renta_fija_content, line_height=0.5)  # Puedes ajustar el valor de line_height según tus necesidades.

        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 10, 'Renta Variable:', ln=True, align='L')
        pdf.set_font('Arial', '', 11)
        pdf.set_text_with_line_height(renta_variable_content, line_height=0.5)  # Puedes ajustar el valor de line_height según tus necesidades.

    # se arma la tabla del periodo  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------  

    # Agregar encabezados de columna
  
    pdf.set_y(260)
    pdf.set_fill_color(255,255,255)  # blanco (RGB)
    pdf.cell(190, 6, "", ln=True, align='C', fill=True)
    pdf.set_fill_color(255,255,255)  # blanco (RGB)
    pdf.cell(190, 6, "", ln=True, align='C', fill=True)


    pdf.set_fill_color(255,255,255)  # blanco (RGB)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(190, 6, "Período", ln=True, align='C', fill=True)

    pdf.set_fill_color(253,190,40)  # Amarillo (RGB)
    pdf.cell(185, 6, desde +"  -  " + hasta, ln=True, align='C', fill=True)

    pdf.set_fill_color(255,255,255)  # blanco (RGB)
    pdf.cell(185, 6, "", ln=True, align='C', fill=True)

    pdf.set_fill_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(95, 6, 'Valuación', fill=True, align='C')
    pdf.cell(95, 6, 'Flujo de Fondos', fill=True, align='C', ln=True)

    pdf.set_fill_color(253,190,40)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(40, 6, 'Inicial', fill=True, align='C')
    pdf.cell(2, 6, '|', fill=True, align='C')
    pdf.cell(40, 6, 'Final', fill=True, align='C')

    pdf.set_fill_color(253,190,40)
    pdf.cell(20, 6, ' ', fill=True)

    pdf.set_fill_color(253,190,40)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(40, 6, 'Aporte', fill=True, align='C')
    pdf.cell(2, 6, '|', fill=True, align='C')
    pdf.cell(40, 6, 'Retiro', fill=True, align='C', ln=True)


    pdf.set_fill_color(255,255,255)
    pdf.cell(40, 6,"$" + vInicial , fill=True, align='C')
    pdf.cell(2, 6, '|', fill=True, align='C')
    pdf.cell(40, 6,"$" + vFinal, fill=True, align='C')

    pdf.set_fill_color(255,255,255)
    pdf.cell(20, 6, ' ', fill=True)
    pdf.set_fill_color(255,255,255)

    pdf.cell(40, 6,"$" + fondeo, fill=True, align='C')
    pdf.cell(2, 6, '|', fill=True, align='C')
    pdf.cell(40, 6,"$" + retiro, fill=True, align='C')

    pdf.set_fill_color(255,255,255)  # blanco (RGB)
    pdf.cell(190, 6, "", ln=True, align='C', fill=True)
    pdf.set_fill_color(255,255,255)  # blanco (RGB)
    pdf.cell(190, 6, "", ln=True, align='C', fill=True)
    pdf.set_fill_color(255,255,255)  # blanco (RGB)
    pdf.cell(190, 6, "", ln=True, align='C', fill=True)




    pdf.set_fill_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(95, 6, 'Resultado del Período', fill=True, align='C')
    pdf.cell(95, 6, 'Resultado Anualizado', fill=True, align='C', ln=True)

    pdf.set_fill_color(253,190,40)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(40, 6, 'En pesos', fill=True, align='C')
    pdf.cell(2, 6, '|', fill=True, align='C')
    pdf.cell(40, 6, 'Porcentaje', fill=True, align='C')

    pdf.set_fill_color(253,190,40)
    pdf.cell(20, 6, ' ', fill=True)

    pdf.set_fill_color(253,190,40)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(40, 6, 'TNA', fill=True, align='C')
    pdf.cell(2, 6, '|', fill=True, align='C')
    pdf.cell(40, 6, 'TEA', fill=True, align='C', ln=True)


    pdf.set_fill_color(255,255,255)
    pdf.cell(40, 6,"$" + bruto , fill=True, align='C')
    pdf.cell(2, 6, '|', fill=True, align='C')
    pdf.cell(40, 6, periodo, fill=True, align='C')

    pdf.set_fill_color(255,255,255)
    pdf.cell(20, 6, ' ', fill=True)
    pdf.set_fill_color(255,255,255)

    pdf.cell(40, 6, tna, fill=True, align='C')
    pdf.cell(2, 6, '|', fill=True, align='C')
    pdf.cell(40, 6, anualizada, fill=True, align='C')

    # espacio en blanco 
    #pdf.set_fill_color(255,255,255)  # blanco (RGB)
    #pdf.cell(190, 50, "", ln=True, align='C', fill=True)
   
    # Tabla final
    pdf.set_y(100)
    pdf.cell(50, 6, "",  align='C', fill=True)
    pdf.set_fill_color(253,190,40)  # Amarillo (RGB)
    pdf.cell(80, 6, "Referencias de Mercado TNA", ln=True, align='C', fill=True)

    
    pdf.set_fill_color(255,255,255)  # blanco (RGB)
    pdf.cell(50, 6, "",  align='C', fill=True)
    pdf.cell(80, 6, "BADLAR (1)",  align='L', fill=True)
    pdf.cell(1, 6, "80,63%", ln=True, align='R', fill=True)

    pdf.cell(50, 6, "",  align='C', fill=True)
    pdf.set_fill_color(254,228,151)  # Amarillo (RGB)
    pdf.cell(80, 6, "IAMCP (2)",  align='L', fill=True)
    pdf.cell(1, 6, "148,14%", ln=True, align='R', fill=True)

    
    pdf.set_fill_color(255,255,255)  # blanco (RGB)
    pdf.cell(50, 6, "",  align='C', fill=True)
    pdf.cell(80, 6, "S&P MERVAL (3)",  align='L', fill=True)
    pdf.cell(1, 6, "193,96%", ln=True, align='R', fill=True)

    pdf.cell(50, 6, "",  align='C', fill=True)
    pdf.set_fill_color(254,228,151)  # Amarillo (RGB)
    pdf.cell(80, 6, "S&P 500 (4)",  align='L', fill=True)
    pdf.cell(1, 6, "131,09%", ln=True, align='R', fill=True)

    
    pdf.set_y(150)
    pdf.set_fill_color(255,255,255)  # Blanco (RGB)
    pdf.set_font('Arial', size=8)
    pdf.cell(190, 6, "(1) Tasa de referencia para depósitos de 30 a 35 días" , ln=True, align='L', fill=True )

    
    pdf.set_fill_color(255,255,255)  # Blanco (RGB)
    pdf.set_font('Arial', size=8)
    pdf.cell(190, 6, "(2) Índice de Bonos general elaborado por el Instituo Argentino de Mercado de Capitales (IAMC)" , ln=True, align='L', fill=True )

    
    pdf.set_fill_color(255,255,255)  # Blanco (RGB)
    pdf.set_font('Arial', size=8)
    pdf.cell(190, 6, "(3) Índice de acciones Argentinas" , ln=True, align='L', fill=True )

    
    pdf.set_fill_color(255,255,255)  # Blanco (RGB)
    pdf.set_font('Arial', size=8)
    pdf.cell(190, 6, "(4) Índice de acciones Norteamericanas" , ln=True, align='L', fill=True )

    # Guardar el PDF
    pdf.output(os.path.join(folder_name, f'informe_cartera_{idCuenta}.pdf'))