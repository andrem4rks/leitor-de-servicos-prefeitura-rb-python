# abrir arquivo
import PyPDF2

import functions

arquivo_pdf = open('SEFIN-Relação-de-Serviços-e-Aliquotas.pdf', 'rb')

pdf = PyPDF2.PdfReader(arquivo_pdf)

# concatenar todas as paginas
text = ""
for i in range(len(pdf.pages)):
    text = text + pdf.pages[i].extract_text()

aux = 0;
bloco = ""
lista_blocos = []
titulo_bloco = ""
lines = text.splitlines()
i = 0
while i < len(lines):
    try:
        if functions.identifica_topico(lines[i]):
            bloco = lines[i] + "\n"
            aux = i + 1
            while bool(1) and aux < len(lines) - 1:
                bloco = bloco + lines[aux] + "\n"
                aux = aux + 1
                if functions.identifica_topico(lines[aux]):
                    i = aux - 1
                    break
    except IndexError:
        print("Lista fora do range!")
        pass
    if bloco != "":
        lista_blocos.append(bloco)
    bloco = ""
    i = i + 1

functions.processa_blocos(lista_blocos)
