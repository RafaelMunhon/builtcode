from PIL import Image
import cv2
import pytesseract as pts
import numpy as np

pts.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
tessdata_dir_config = '--tessdata-dir "C://Program Files//Tesseract-OCR//tessdata"'

path = r'C:\Users\rafael.munhon\Documents\Python\builtcode\builtnovo\imagens\img3.jpeg'

# Window name in which image is displayed
window_name = 'Image'

#Tratamento da imagem

# tipando a leitura para os canais de ordem RGB
imagem = Image.open(path).convert('RGB')
#imagem= imagem.rotate(-7)

# convertendo em um array editável de numpy[x, y, CANALS]
npimagem = np.asarray(imagem).astype(np.uint8)  

# diminuição dos ruidos antes da binarização
npimagem[:, :, 0] = 0 # zerando o canal R (RED)
npimagem[:, :, 2] = 0 # zerando o canal B (BLUE)

# atribuição em escala de cinza
#teste
img = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY)
#img = cv2.medianBlur(img,5)

#_,thresh = cv2.threshold(img,127,255,cv2.THRESH_BINARY) 
#_,thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) 
#_,thresh = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV) 

#_,thresh = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
#_,thresh = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
#_,thresh = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)

thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
retval2,thresh = cv2.threshold(thresh,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)


#thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

#binimagem = cv2.Canny(img,50,100)

binimagem = Image.fromarray(thresh) 
binimagem.show()
'''
#Search for contours and select the biggest one
contours, hierarchy =     cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
cnt = max(contours, key=cv2.contourArea)

#Create a new mask for the result image
h, w = npimagem.shape[:2]
mask = np.zeros((h, w), np.uint8)

#Draw the contour on the new mask and perform the bitwise operation
cv2.drawContours(mask, [cnt],-1, 255, -1)
res = cv2.bitwise_and(npimagem, npimagem, mask=mask)

#Display the result
cv2.imwrite(path, res)
#cv2.imshow('img', res)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
##fim teste

#resimg.resizeimg(im)

# aplicação da truncagem binária para a intensidade
# pixels de intensidade de cor abaixo de 127 serão convertidos para 0 (PRETO)
# pixels de intensidade de cor acima de 127 serão convertidos para 255 (BRANCO)
# A atrubição do THRESH_OTSU incrementa uma análise inteligente dos nivels de truncagem
#ret, thresh = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) 

# reconvertendo o retorno do threshold em um objeto do tipo PIL.Image
##binimagem = Image.fromarray(thresh) 
#Abrindo a imagem tratada
#binimagem.show()

# chamada ao tesseract OCR
text = pts.image_to_string(binimagem,lang= 'por',config= tessdata_dir_config,)

print(text)
