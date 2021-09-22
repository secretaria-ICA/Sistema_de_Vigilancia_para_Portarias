import os
import os
import cv2
import numpy as np
import dlib
import matplotlib.pyplot as plt
from scipy.spatial import distance as dist
from time import sleep


# Implementação Yolo
labelsPath = os.path.join("Yolo/classes.names")
LABELS = open(labelsPath).read().strip().split("\n")
net = cv2.dnn.readNetFromDarknet("Yolo/yolov4_custom.cfg","Yolo/yolov4_custom_last.weights")

# Classificador de 68 pontos
classificador_68_path = "shape_predictor_68_face_landmarks.dat"
classificador_dlib = dlib.shape_predictor(classificador_68_path)
detector_face = dlib.get_frontal_face_detector()

# Pontos do rosto
ROSTO = list(range(17, 68))
ROSTO_COMPLETO = list(range(0, 68))
LABIOS = list(range(48, 61))
SOBRANCELHA_DIREITA = list(range(17, 22))
SOBRANCELHA_ESQUERDA = list(range(22, 27))
OLHO_ESQUERDO = list(range(36, 42))
OLHO_DIREITO = list(range(42, 48))
NARIZ = list(range(27, 35))
MANDIBULA = list(range(0, 17))

def detecta_humano(imagem):
    #converte imagem para RGB
    imagem = cv2.cvtColor(imagem, cv2.COLOR_GRAY2RGB)

    # initialize a list of colors to represent each possible class label
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")
    (H, W) = imagem.shape[:2]

    # determine only the "ouput" layers name which we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input imagem and then perform a forward pass of the YOLO object detector,
    # giving us our bounding boxes and associated probabilities
    blob = cv2.dnn.blobFromImage	(imagem, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    boxes = []
    confidences = []
    classIDs = []
    threshold = 0.2

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            # confidence type=float, default=0.5
            if confidence > threshold:
                # scale the bounding box coordinates back relative to the
                # size of the imagem, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping bounding boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, threshold, 0.1)

    ha_humano = False

    imagem = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)

    # ensure at least one detection exists
    if len(idxs) > 0:
        ha_humano = True
	    # loop over the indexes we are keeping
        for i in idxs.flatten():
        # extract the bounding box coordinates
           (x, y) = (boxes[i][0], boxes[i][1])
           (w, h) = (boxes[i][2], boxes[i][3])

        #draw a bounding box rectangle and label on the imagem
           color = (255,0,0)
           cv2.rectangle(imagem, (x, y), (x + w, y + h), color, 2)
           text = "{}".format(LABELS[classIDs[i]], confidences[i])
           cv2.putText(imagem, text, (x +15, y - 10), cv2.FONT_HERSHEY_SIMPLEX,1, color, 2)
    return ha_humano

def pontos_marcos_faciais(imagem):
    retangulos = detector_face(imagem, 1)
    if len(retangulos) == 0:
        return None
    marcos = []
    for ret in retangulos:
        marcos.append(
            np.matrix([[p.x, p.y] for p in classificador_dlib(imagem, ret).parts()])
        )
    return marcos


def aspecto_razao_olhos(pontos_olhos):
    a = dist.euclidean(pontos_olhos[1], pontos_olhos[5])
    b = dist.euclidean(pontos_olhos[2], pontos_olhos[4])
    c = dist.euclidean(pontos_olhos[0], pontos_olhos[3])
    aspecto_razao = (a + b) / (c * 2.0)
    return aspecto_razao


def verificar_rosto_virado(pontos):
    esquerdo = dist.euclidean(pontos[0], pontos[27])
    direito = dist.euclidean(pontos[27], pontos[16])
    rosto_distancia = dist.euclidean(pontos[0], pontos[16])
    lado_1 = esquerdo < (0.35 * rosto_distancia) and direito > (0.65 * rosto_distancia)
    lado_2 = esquerdo > (0.65 * rosto_distancia) and direito < (0.35 * rosto_distancia)
    esta_virado = lado_1 or lado_2
    print(
        "Cálculo distância lateral do rosto: \n"
        f"Lado esquerdo: {round(esquerdo,2)} \n"
        f"Lado direito: {round(direito, 2)}\n"
        f"Distância rosto: {round(rosto_distancia, 2)}\n"
        f"Está virado: {esta_virado}\n"
    )
    return {
        "rosto_virado": esta_virado,
        "dist_esq": esquerdo,
        "dist_dir": direito,
        "dist_rosto": rosto_distancia,
    }


def verifica_distancia_olhos(marcos_faciais):
    valor_olho_direito = round(
        aspecto_razao_olhos(marcos_faciais[0][OLHO_DIREITO]) * 100, 2)
    valor_olho_esquerdo = round(
        aspecto_razao_olhos(marcos_faciais[0][OLHO_ESQUERDO]) * 100, 2
    )
    print(
        "Razão dos olhos: \n"
        f"Olho esquerdo {valor_olho_esquerdo} \n"
        f"Olho direito {valor_olho_direito}\n"
    )
    return {"dist_olho_esq": valor_olho_esquerdo, "dist_olho_dir": valor_olho_direito}


def captura_imagem():
    captura_video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
	
    captura_ok, frame = captura_video.read()
    sleep(5)
    cv2.imwrite("vigia_APP/static/vigia_fotos/rosto_atual.jpg", frame)
    captura_video.release()
    imagem = cv2.imread(
        "vigia_APP/static/vigia_fotos/rosto_atual.jpg", cv2.IMREAD_GRAYSCALE
    )
    return imagem


def anotar_marcos_faciais(imagem, marcos):
    for marco in marcos:
        for idx, ponto in enumerate(marco):
            centro = (ponto[0, 0], ponto[0, 1])
            cv2.circle(imagem, centro, 3, (0, 0, 0), -1)
    return imagem


def detecta(imagem, classe):
    classificador = cv2.CascadeClassifier(cv2.data.haarcascades + classe)
    alvo = classificador.detectMultiScale(imagem, 1.3, 3)
    if alvo is ():
        return (0, alvo)
    return (1, alvo)


def verifica_olhos_abertos(imagem):
    olhos = detecta(imagem, "haarcascade_eye.xml")
    return olhos


def verifica_olhos_fechados(imagem):
    olho_esquerdo = detecta(imagem, "haarcascade_lefteye_2splits.xml")
    olho_direito = detecta(imagem, "haarcascade_lefteye_2splits.xml")
    olhos = [olho_esquerdo, olho_direito]
    if olho_direito[0] or olho_esquerdo[0]:
        return (1, olhos)
    return (0, olhos)


def analisa_situacao(situacao):
    # Verifica situações possíveis
    if situacao == 0:
       print("Situação normal.")
    if situacao == 1:
       print("Suspeita de estar dormindo...")
    if situacao == 2:
       print("Suspeita de posição incorreta...")
    if situacao == 3:
       print("Suspeita de ausência...")
    return situacao


def checa_alerta(lista_alerta):
    alerta = 0
    problema = 0
    for i in range(len(lista_alerta)):
        if i < len(lista_alerta) - 1:
            if lista_alerta[i] == lista_alerta[i + 1]:
                alerta += 1
                if alerta == 2:
                    problema = lista_alerta[i]
                    break
            else:
                alerta = 0
                problema = 0


    if problema == 1:
        gera_alerta("DORMINHOCO!")
    if problema == 2:
        gera_alerta("POSIÇÃO DE TRABALHO INCORRETA, OLHE PARA O MONITOR!")
    if problema == 3:
        gera_alerta("CADÊ VOCÊ, VIGILANTE?")
    return alerta


def gera_alerta(frase):
    print(frase)
    sleep(2)
    print(frase)
    sleep(2)
    print(frase)
    sleep(2)
    print(frase)
    sleep(2)
    print(frase)


def desenhar_imagem(lista, marcos):
    imagem = lista[0]
    imagem = anotar_marcos_faciais(imagem, marcos) if marcos is not None else lista[0]

    # Desenhar olhos abertos
    if lista[1][0]:
        imagem = desenhar(imagem, lista[1][1])
    # Desenhar olhos fechados
    if lista[2][0]:
        imagem = desenhar(imagem, lista[2][1][0][1])
        imagem = desenhar(imagem, lista[2][1][1][1])
    return imagem


def desenhar(imagem, pontos):
    for (x, y, w, h) in pontos:
        cv2.rectangle(imagem, (x, y), (x + w, y + h), (255, 255, 0), 2)
    return imagem


def analisa_foto(imagem):
    # Inicia detecção
    dados = {}
    marcos_faciais = pontos_marcos_faciais(imagem)
    ha_humano = detecta_humano(imagem)
    olhos_abertos = verifica_olhos_abertos(imagem)
    olhos_fechados = verifica_olhos_fechados(imagem)
    distancia_olhos = verifica_distancia_olhos(marcos_faciais) if marcos_faciais is not None else {'dist_olho_esq':False, 'dist_olho_dir':False}
    
    dados.update(distancia_olhos)
    
    # # Desenha imagem
    lista_desenho = [imagem, olhos_abertos, olhos_fechados]
    imagem = desenhar_imagem(lista_desenho, marcos_faciais)

    # # Salva imagem desenhada
    cv2.imwrite("imagem_desenhada.jpg", imagem)

    # Realiza testes
    face_virada = (
        verificar_rosto_virado(marcos_faciais[0][ROSTO_COMPLETO])
        if marcos_faciais is not None
        else {
            "rosto_virado": False,
            "dist_esq": False,
            "dist_dir": False,
            "dist_rosto": False,
        }
    )
    dados.update(face_virada)

    face_detectada = True if marcos_faciais is not None else False
    dados["face_detectada"] = face_detectada
    dados["nomeVigilante"] = LABELS[0]


    ha_olhos = olhos_abertos[0] or olhos_fechados[1][0][0] or olhos_fechados[1][1][0]

    if face_detectada:
        acordado = (
            ha_olhos
            and distancia_olhos.get("dist_olho_esq") > 20
            and distancia_olhos.get("dist_olho_dir") > 20
        )
        dormindo = ha_olhos and (
            distancia_olhos.get("dist_olho_esq") <= 20
            or distancia_olhos.get("dist_olho_esq") <= 20
        )

    if face_detectada and not face_virada.get('rosto_virado') and ha_humano:  # Reconhece face frontal
        print("Face frontal detectada.")
        dados["identificacao_olhos"] = ""
        dados["orientacao_face"] = "Face frontal detectada"

        # Verifica se olhos estão abertos e abertura dos olhos é maior que 20
        if acordado:
            print("Olhos abertos detectados.")
            dados["identificacao_olhos"] = "Olhos abertos detectados"
            dados["situacao"] = "Normal"

            return dados
        # Verifica se olhos estão fechados e abertura dos olhos é menor ou igual 20
        if dormindo:
            print("Olhos fechados detectados.")
            dados["identificacao_olhos"] = "Olhos fechados detectados"
        if not ha_olhos:
            print("Face identificada, olhos não foram identificados.")
            dados[
                "identificacao_olhos"
            ] = "Face identificada, olhos não foram identificados."
            # Verifica se foi identificado rosto mas não tenha sido identificado olhos
        dados["situacao"] = "Dormindo"
        return dados
    elif face_detectada and face_virada.get('rosto_virado') and ha_humano:  
        # Reconhece face virada
        print("Face lateral detectada.")
        dados["orientacao_face"] = "Face lateral detectada"
        # Verifica se olhos estão abertos
        if acordado:
            print("Olhos abertos detectados.")
            dados["identificacao_olhos"] = "Olhos abertos detectados"
            dados["situacao"] = "Posição incorreta"
            return dados
        # Verifica se olhos estão fechados
        if dormindo:
            print("Olhos fechados detectados.")
            dados["identificacao_olhos"] = "Olhos fechados detectados"
        # Verifica ausência de olhos
        if not ha_olhos:
            print("Face lateral identificada, olhos não foram identificados.")
            dados[
                "identificacao_olhos"
            ] = "Face identificada, olhos não foram identificados."
        dados["situacao"] = "Dormindo"
        return dados
    elif ha_humano:
        dados['orientacao_face'] = "Rosto não detectado, porém há alguém presente."
        dados['identificacao_olhos'] = "Nenhum olho detectado."
        dados['situacao'] = "Posição incorreta"
        return dados
    else:
        # Retorna 7 caso nenhuma face tenha sido reconhecida
        print("Nenhum rosto ou olho foi detectado nessa imagem.")
        dados["orientacao_face"] = "Nenhum rosto detectado."
        dados["identificacao_olhos"] = "Nenhum olho detectado."
        dados["situacao"] = "Ausente"
        return dados


def teste_situacoes(pasta):
    lista_alerta = []
    for i in range(1, 7):
        imagem = cv2.imread(f"teste/{pasta}/ex{i}.jpg", cv2.IMREAD_GRAYSCALE)
        print("\n")
        situacao = analisa_foto(imagem)
        estado = analisa_situacao(situacao)
        sleep(2)
        lista_alerta.append(estado)
        if len(lista_alerta) > 3:
            if checa_alerta(lista_alerta) == 2:
                lista_alerta.clear()
        if len(lista_alerta) == 6:
            lista_alerta.clear()


def renomeia_imagens():
    arquivo = {}
    if os.path.exists("vigia_APP/static/vigia_fotos/ex5.jpg"):
        os.remove("vigia_APP/static/vigia_fotos/ex5.jpg")
    if os.path.exists("vigia_APP/static/vigia_fotos/ex4.jpg"):
        os.rename(
            r"vigia_APP/static/vigia_fotos/ex4.jpg",
            r"vigia_APP/static/vigia_fotos/ex5.jpg",
        )
        arquivo["quinta_foto"] = True
    if os.path.exists("vigia_APP/static/vigia_fotos/ex3.jpg"):
        os.rename(
            r"vigia_APP/static/vigia_fotos/ex3.jpg",
            r"vigia_APP/static/vigia_fotos/ex4.jpg",
        )
        arquivo["quarta_foto"] = True
    if os.path.exists("vigia_APP/static/vigia_fotos/ex2.jpg"):
        os.rename(
            r"vigia_APP/static/vigia_fotos/ex2.jpg",
            r"vigia_APP/static/vigia_fotos/ex3.jpg",
        )
        arquivo["terceira_foto"] = True
    if os.path.exists("vigia_APP/static/vigia_fotos/ex1.jpg"):
        os.rename(
            r"vigia_APP/static/vigia_fotos/ex1.jpg",
            r"vigia_APP/static/vigia_fotos/ex2.jpg",
        )
        arquivo["segunda_foto"] = True
    if os.path.exists("vigia_APP/static/vigia_fotos/rosto_atual.jpg"):
        os.rename(
            r"vigia_APP/static/vigia_fotos/rosto_atual.jpg",
            r"vigia_APP/static/vigia_fotos/ex1.jpg",
        )
        arquivo["primeira_foto"] = True
    return arquivo


def main():
    arquivo = renomeia_imagens()
    imagem = captura_imagem()
    analise = analisa_foto(imagem)
    analise["imagem"] = imagem
    analise.update(arquivo)
    return analise


"""    estado = analisa_situacao(analise.get('situacao'))
    sleep(5)
    lista_alerta.append(estado)
    if len(lista_alerta) > 3:
        if checa_alerta(lista_alerta) == 2:
            lista_alerta.clear()
    if len(lista_alerta) == 6:
        lista_alerta.clear()"""
