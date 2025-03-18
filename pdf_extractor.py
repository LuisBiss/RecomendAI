import PyPDF2

def buscar_valor(keyword, text):
    position = text.find(keyword)
    if position != -1:
        result_position = text.find("RESULTADO", position)
        if result_position != -1:
            start = result_position + len("RESULTADO") + 1
            end = start + 5
            result_value = text[start:end].strip()
            return result_value.replace(",", ".")
    return None

def buscar_resultados(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

            text = text.replace("\n", " ")

            resultados = {
                "glicose": buscar_valor("GLICOSE JEJUM", text),
                "t3": buscar_valor("T3 TOTAL", text),
                "t4": buscar_valor("T4 TOTAL", text),
                "tsh": buscar_valor("TSH ULTRA SENSÍVEL", text),
                "colesterol": buscar_valor("COLESTEROL TOTAL", text),
                "triglicerideos": buscar_valor("TRIGLICERIDES", text)
            }

            return resultados

    except Exception as e:
        print(f"Erro ao processar o PDF: {e}")
        return None