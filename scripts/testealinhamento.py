import cv2
import pytesseract
import numpy as np
import pandas as pd
import re
import os
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
tessdata_dir_config = '--tessdata-dir "C://Program Files//Tesseract-OCR//tessdata"'

path = r'C:\Users\rafael.munhon\Documents\Python\builtcode\builtnovo\imagens\img3.jpeg'

caminho = input("Qual a pasta dos cupons?\n")
#caminho = "C:\Users\rafael.munhon\Documents\Python\LeituraOcr\br-tax-coupon-ocr-master\Cupons"
arquivos_caminhos = os.listdir( caminho )

caminhos_imagens = []
#Aqui ele vai armazenar os paths para as imagens
for imagem_path in arquivos_caminhos:
    path = [caminho, '\\', imagem_path]
    caminhos_imagens.append("".join(path))


imagens_array = []

#Esse é o kernel uttilizado para a operação com os filtros, 
# nesse caso é um [5x5] para processar os ruídos na operação de Opening

kernel = np.ones((5,5),np.uint8)

# Percorrer as imagens para conseguir todas as informações

for caminho_imagem in caminhos_imagens:
    
    #Carrega a imagem original
    imagem_original = cv2.imread(caminho_imagem)
    
    #Coloca em preto e branco
    imagem_pb = cv2.cvtColor(imagem_original, cv2.COLOR_BGR2GRAY)
    
    #Usa um threshold para planificar sombras das imagens e tentar separar melhor as letras
    imagem_opening = cv2.adaptiveThreshold(imagem_pb,255,
                                         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                         cv2.THRESH_BINARY,11,5)
    
    #Usa um blur para diminuir o processo destrutivo das letras quando passam pelo o threshold
    imagem_opening = cv2.GaussianBlur(imagem_opening,(11,11), 0)
    
    #Usa um filtro de opening para tentar equilibrar o blur com a definição do threshold para a leitura no OCR
    imagem_opening = cv2.morphologyEx(imagem_opening, cv2.MORPH_OPEN, kernel)
    
    #Armazena todas as imagens com os filtros para processamento
    imagens_array.append(imagem_opening)

    binimagem = Image.fromarray(imagem_opening) 
    binimagem.show()

#Armazena todos os textos das notas
texto_notas = []

i = 1

for imagem_nota in imagens_array:
    #Usa o processo do Google Tesseract para ler a imagem com OCR
    texto_notas.append(pytesseract.image_to_string(imagem_nota,lang= 'por',config= tessdata_dir_config,))
    
    
    #Mostra o progresso do processo
    print("Processou nota " + str(i) + "\n")
    i = i + 1

strings_notas = []

#Percorre os textos de todas as notas e tira algumas leituras erradas
for texto_nota in texto_notas:
    
    #Junta todas as linhas dividas que são maior que três caracteres
    strings_notas.append([linha for linha in texto_nota.splitlines() if linha.strip() and len(linha)>3])


def encontra_nome_empresa (nota_strings):
    #Vai procurar no padrão de ser as duas primeiras linhas da nota fiscal o nome da empresa, caso encontra, devolve a str
    # caso não, devolve não encontrou
    for i in range (2):
        if nota_strings[i].find("LTDA") != -1:
            return nota_strings[i] 
    return ("Não encontrada")


def encontra_cnpj_empresa (nota_strings):
    for i in range (2,10):
        # O CNPJ está entre as primeiras linhas do CNPJ, porém variam muito em relação a posição, portanto, é preciso 
        # Procurar com o inicio em C ou c
        if nota_strings[i].find("C") == 0 or nota_strings[i].find("c") == 0:
            # Essa expressão regular significa pega a primeira parte sendo qualquer caractere, em segudo um dois pontos
            # Após isso pega a expressão do CNPJ, o resto liga com o IE.
            # match_cnpj = re.match(r'^(.+)(:)(.+)( )([A-Z]+)(.+)', nota_strings[i], re.I)
            # O terceiro grupo é o do CNPJ (Porém, falha no da freitas, assim foi deixado de lado)
            #cnpj = match_cnpj.group(3) 
            
            #Foi improvisado uma seleção, porém não é o ideal. 
            return i, nota_strings[i][4:24]
    #Devolve 0 para o indice de procura dos itens não ser prejudicada e pesquisar do inicio do arquivo, caso necessário
    return 0, ("Não encontrada")

def encontra_valor_total(nota_strings, linha_inicial):
    for i in range (len(nota_strings)):
        #Procura o valor total após a string do CNPJ pois esta no final da nota
        if nota_strings[i].find("TOTAL") != -1 and i > linha_inicial:
                #Acha com expressão regular o total do valor
                match_valor = re.match(r'(.+)( )(.+)', nota_strings[i], re.I)
                return i, match_valor.group(3)
    #Devolve o final do arquivo para o indice de procura dos itens não ser prejudicada e 
    # pesquisar do final do arquivo, caso necessário
    return len(nota_strings), ("Não encontrada")


def encontra_itens_nota(nota_strings, linha_inicial, linha_final):
    # Faz uma lista com todos os itens que podem ter numa nota
    lista_itens = []
    for i in range(linha_inicial, linha_final):
        match_item = re.match(r'^([0-9]{2,4})( )([0-9]+)( )(.+)', nota_strings[i], re.I)
        match_other_item = re.match(r'^([0-9]{2,10})( )(.+)', nota_strings[i], re.I)
        if match_item:
            lista_itens.append(match_item.group(5))
            continue

        if match_other_item:
            lista_itens.append(match_other_item.group(3))  
    return lista_itens


dados_notas = []

for nota in strings_notas:
    
    nome_empresa = encontra_nome_empresa(nota)
    indice_inicial_itens, cnpj_empresa = encontra_cnpj_empresa(nota)
    indice_final_itens, valor_nota = encontra_valor_total(nota, indice_inicial_itens)
    itens_nota = encontra_itens_nota(nota, indice_inicial_itens, indice_final_itens)
    dado_nota = [nome_empresa, cnpj_empresa, valor_nota, itens_nota]
    dados_notas.append(dado_nota)
    
print(dados_notas)


#organizar texto
pd.DataFrame(dados_notas)

def encontra_cnpj_empresa_regex (nota_strings):
    for i in range (2,10):
        # O CNPJ está entre as primeiras linhas do CNPJ, porém variam muito em relação a posição, portanto, é preciso 
        # Procurar com o inicio em C ou c
        if nota_strings[i].find("C") == 0 or nota_strings[i].find("c") == 0:
            # Essa expressão regular significa pega a primeira parte sendo qualquer caractere, em segudo um dois pontos
            # Após isso pega a expressão do CNPJ, o resto liga com o IE.
            match_cnpj = re.match(r'^(.+)(:)(.+)( )([A-Z]+)(.+)', nota_strings[i], re.I)
            # O terceiro grupo é o do CNPJ (Porém, falha no da freitas, assim foi deixado de lado)
            cnpj = match_cnpj.group(3) 
            
            #Foi improvisado uma seleção, porém não é o ideal. 
            return i, cnpj
    #Devolve 0 para o indice de procura dos itens não ser prejudicada e pesquisar do inicio do arquivo, caso necessário
    return 0, ("Não encontrada")


for nota in strings_notas:
    indice_inicial_itens, cnpj_empresa = encontra_cnpj_empresa_regex(nota)
    print(cnpj_empresa)