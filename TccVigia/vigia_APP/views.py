from cv2 import data
from cv2 import data
from django.shortcuts import render
from django.http import HttpResponse
from .vigia_APP import main
from vigia_APP.models import Analise, Alarme
from datetime import datetime

# Create your views here.

def index(request):
    dados = main()

    resultado = Analise(rosto_identificado=dados['face_detectada'], posicao=dados['orientacao_face'],
    olhos=dados['identificacao_olhos'],abertura_olho_esquerdo=dados['dist_olho_esq'],
    abertura_olho_direito=dados['dist_olho_esq'],situacao=dados['situacao'],nomeVigilante=dados['nomeVigilante'])
    resultado.save()

    numero_registros = len(Analise.objects.all())
    
    situacoes = []
    datas = []
    lista_status = []

    if numero_registros > 1:
        for i in range(numero_registros):
            situacoes.append(Analise.objects.get(pk=(i+1)).situacao)
            datas.append(Analise.objects.get(pk=(i+1)).data)
            lista_status.append(Analise.objects.get(pk=(i+1)).status)
    if len(situacoes) > 5:
        alerta = 0
        status = ''
        ultimas_situacoes = situacoes[-5:]
        dados['status'] = lista_status[-1]
        print('ultimas situacoes',ultimas_situacoes)
        for i in range(len(ultimas_situacoes)):
            if i < len(ultimas_situacoes) - 1:
                if ultimas_situacoes[i] == ultimas_situacoes[i + 1]:
                    alerta += 1
                    if alerta == 3 and ultimas_situacoes[i]:
                        status = ultimas_situacoes[i]
                        mensagem = ''
                        tipo_alarme = ''
                        if status == 'Normal':
                            dados['status'] = 'Normal'
                        elif status == "Ausente":
                            alarme = Alarme(tipo_alarme='Ausência',mensagem='Ausência. Funcionário não se encontra no local.',
                            situacao=status)
                            dados['status'] = 'Ausência'                            
                            alarme.save()
                        elif status == "Posição incorreta":
                            alarme = Alarme(tipo_alarme='Não monitoramento',mensagem='Funcionário não está monitorando corretamente.',
                            situacao=status)
                            dados['status'] = 'Não monitorando'
                            alarme.save()
                        elif status == "Dormindo":
                            alarme = Alarme(tipo_alarme='Não monitoramento',mensagem='Funcionário está dormindo em serviço.',
                            situacao=status)
                            dados['status'] = 'Não monitorando'
                            alarme.save()
                        resultado.status = status
                        resultado.save()
                        break

    qtd_alarme = len(Alarme.objects.all())
    dados['qtd_alarmes'] = qtd_alarme
    tipo_alarme = []
    mensagem_alarme = ''
    if qtd_alarme > 1:
        for i in range(qtd_alarme):
            tipo_alarme.append(Alarme.objects.get(pk=(i+1)).tipo_alarme)
            mensagem_alarme = Alarme.objects.get(pk=(i+1)).mensagem
    dados['qtd_nao_monitorando'] = tipo_alarme.count('Não monitoramento')
    dados['qtd_ausencia'] = tipo_alarme.count('Ausência')
    if dados['status'] != 'Normal':
        dados['mensagem_alarme'] = mensagem_alarme
    
    d = datetime.now()
    d.strftime('%Y-%m-%d %H:%M:%S.%f')
    dados['horario'] = d
    print("horário ",d)

    return render(request, "vigia_APP/index.html", dados)
