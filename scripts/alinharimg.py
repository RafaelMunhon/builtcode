from PIL import Image
import matplotlib.pyplot as plt
import cv2
from scipy import misc
import numpy as np
from skimage import transform as tf

#path = r'C:\\Users\\rafael.munhon\Documents\\Python\builtcode\\imgorigem\\img1.jpg'
path = r'C:\\Users\\rafael.munhon\\Documents\\Python\\builtcode\\builtnovo\\imagens\\img3.jpeg'
pathDestino = r'C:\\Users\\rafael.munhon\Documents\\Python\builtcode\\imgdestino\\img1.jpg'

imagem = Image.open(path).convert('RGB')
npimagem = np.asarray(imagem).astype(np.uint8)  

# diminuição dos ruidos antes da binarização
npimagem[:, :, 0] = 0 # zerando o canal R (RED)
npimagem[:, :, 2] = 0 # zerando o canal B (BLUE)

# atribuição em escala de cinza
im = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY) 

# aplicação da truncagem binária para a intensidade
# pixels de intensidade de cor abaixo de 127 serão convertidos para 0 (PRETO)
# pixels de intensidade de cor acima de 127 serão convertidos para 255 (BRANCO)
# A atrubição do THRESH_OTSU incrementa uma análise inteligente dos nivels de truncagem
ret, thresh = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) 

# reconvertendo o retorno do threshold em um objeto do tipo PIL.Image
binimagem = Image.fromarray(thresh) 
#Abrindo a imagem tratada
binimagem.show()

src = np.array((
    (155, 110),
    (774, 110),
    (155, 548),
    (774, 548)
))
dst = np.array((
    (94, 248),
    (664, 7),
    (266, 651),
    (835, 410)
))

tform3 = tf.ProjectiveTransform()
tform3.estimate(src, dst)

img = cv2.imread(path)
img_ajustada = tf.warp(img, tform3, output_shape=(930, 1000))

_,ax = plt.subplots (1,2)
ax[0].imshow (img)
ax[0].plot(dst[:, 0], dst[:, 1], '.r')
ax[1].imshow (img_ajustada)
ax[1].plot(src[:, 0], src[:, 1], '.r')
plt.show()