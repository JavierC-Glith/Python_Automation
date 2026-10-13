import streamlit as st
from fpdf import FPDF
import os

# 1. Clase personalizada para extender la funcionalidad de FPDF
class PDF(FPDF):
    def header(self):
        # Muestra el título del documento centrado en el encabezado
        if hasattr(self, 'document_title'):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, self.document_title, border=0, ln=1, align="C")

    def footer(self):
        # Posiciona el pie de página a 15 mm del final y añade número de página
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", border=0, ln=0, align="C")

    def chapter_title(self, title, font="Arial", size=12):
        # Configuración para el título de cada capítulo
        self.set_font(font, "B", size)
        self.cell(0, 10, title, border=0, ln=1, align="L")
        self.ln(10)

    def chapter_body(self, body, font="Arial", size=12):
        # Permite escribir texto en múltiples líneas dentro del capítulo
        self.set_font(font, "", size)
        self.multi_cell(0, 10, body)
        self.ln()

# 2. Función encargada de compilar y guardar el PDF
def create_pdf(file_name, document_title, author, chapters, image_path=None):
    pdf = PDF()
    pdf.document_title = document_title
    pdf.add_page()
    if author:
        pdf.set_author(author)
    
    # Si se cargó una imagen, se posiciona en el documento
    if image_path:
        pdf.image(image_path, x=10, y=30, w=180)
        pdf.ln(120)

    # Renderiza cada capítulo registrado por el usuario
    for chapter in chapters:
        pdf.chapter_title(chapter['title'], chapter['font'], chapter['size'])
        pdf.chapter_body(chapter['body'], chapter['font'], chapter['size'])

    pdf.output(file_name)

# 3. Interfaz gráfica principal con Streamlit
def main():
    st.title("Generador de PDF con Python")
    st.header("Configuración del documento")

    # Inputs principales del documento
    document_title = st.text_input("Título del documento", "El secreto del bosque encantado")
    author = st.text_input("Autor", "")
    
    uploaded_image = st.file_uploader(
        "Sube una imagen para el documento (opcional)", 
        type=["jpg", "jpeg", "png"]
    )

    st.header("Capítulos del documento")
    num_chapters = st.number_input("Número de capítulos", min_value=1, max_value=10, value=1)
    
    chapters = []
    # Captura los datos de cada capítulo dinámicamente
    for i in range(int(num_chapters)):
        st.subheader(f"Capítulo {i + 1}")
        title = st.text_input(f"Título del capítulo {i + 1}", key=f"title_{i}")
        body = st.text_area(f"Cuerpo del capítulo {i + 1}", key=f"body_{i}")
        font = st.selectbox(
            f"Fuente del capítulo {i + 1}", 
            ["Arial", "Courier", "Times"], 
            key=f"font_{i}"
        )
        size = st.slider(
            f"Tamaño de fuente del capítulo {i + 1}", 
            min_value=8, 
            max_value=24, 
            value=12, 
            key=f"size_{i}"
        )
        chapters.append({
            "title": title, 
            "body": body, 
            "font": font, 
            "size": size
        })

    # Botón para generar el PDF
    if st.button("Generar PDF"):
        image_path = None
        if uploaded_image is not None:
            # Extrae la extensión real del archivo subido para evitar conflictos con FPDF
            _, file_extension = os.path.splitext(uploaded_image.name)
            image_path = f"temp_image{file_extension}"
            
            with open(image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())

        output_filename = "documento_generado.pdf"
        create_pdf(output_filename, document_title, author, chapters, image_path)
        
        st.success("PDF generado exitosamente")

        # Botón para descargar el PDF resultante
        with open(output_filename, "rb") as pdf_file:
            st.download_button(
                label="Descargar PDF",
                data=pdf_file,
                file_name=output_filename,
                mime="application/pdf"
            )

        # Limpieza de archivo temporal de imagen si existe
        if image_path and os.path.exists(image_path):
            os.remove(image_path)

if __name__ == "__main__":
    main()