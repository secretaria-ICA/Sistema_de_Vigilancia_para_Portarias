<!-- antes de enviar a versão final, solicitamos que todos os comentários, colocados para orientação ao aluno, sejam removidos do arquivo -->
# Sistema de Vigilância para Portarias.

#### Aluno: [Paulo Jorge Ramalho de Almeida](https://github.com/paulojrapuc)
#### Orientadora: [Manoela Kohler](https://github.com/manoelakohler)

---

Trabalho apresentado ao curso [BI MASTER](https://ica.puc-rio.ai/bi-master) como pré-requisito para conclusão de curso e obtenção de crédito na disciplina "Projetos de Sistemas Inteligentes de Apoio à Decisão".

<!-- para os links a seguir, caso os arquivos estejam no mesmo repositório que este README, não há necessidade de incluir o link completo: basta incluir o nome do arquivo, com extensão, que o GitHub completa o link corretamente -->
- [Link para o código]((https://github.com/paulojrapuc/TCC). <!-- caso não aplicável, remover esta linha -->

---

### Resumo

<!-- trocar o texto abaixo pelo resumo do trabalho, em português -->

Desenvolvimento de projeto utilizando visão computacional para análise de vídeo/foto para detecção de comportamento do vigilante durante o horário de trabalho.

### Abstract <!-- Opcional! Caso não aplicável, remover esta seção -->

<!-- trocar o texto abaixo pelo resumo do trabalho, em inglês -->

Project development using computer vision for video/photo analysis to detect guard behavior during working hours.

### 1. Introdução

Em decorrencia da necessidade de aumentar a segurança dos usuários, surge a necessidade de desenvolver uma solução que oriente e analise o comportamento de vigilantes durante o horário de trabalho, detectando em tempo real através de algoritmos de machine learning cenários como: 

• Identificação do comportamento em tempo real do vigilante;

• Analise da posição do vigilante;

• Analise de presença  ou ausência durante o período de trabalho;

• Detecção se o vigilante está dormindo ou de posição inadequada;

• Apuração do tempo de ausência por parte do vigilante;

• Analisar e informar o que foi detectado;

### 2. Modelagem

Para o desenvolvimento do projeto foi utilizado uma rede convolucional (CNN) para detecção de pessoas e uma rede de detecção de faces, com objetivo de vericar se o vigilante está em posição correta ou dormindo.

1 - Utilização de rede convolucional (CNN) para analise das imagens, foi utilizado rede neural convolucional YoloV4. Foi feito treinamento do modelo com 2000 imagens diversas e todas mapeadas com pessoas, para distinção de pessoas de animais e outros objetos. 

2 - Analise detalhada do individuo para verificação do comportamento. foi utilizado algoritmo haarcascade para análise facial de 68 pontos, para verificação da posição dos olhos e face, detectando cenários se os olhos estão abertos ou fechados;

3 - Foram utilizados base de imagens na Web e/ou google fotos pessoais para treinamento e testes;

4 - Montagem de Dashboard (painel de informações), para visualização das informações.

5 - Utilização de classes e métodos existentes na internet que sejam open-source para desenvolvimento; (será feito na linguagem phyton);

6 - Utilizarei o google colab para desenvolvimento e testes;

7 - Foi utilizado ambiente Django/WEB para execução da aplicação;

8 - Todos as informações e registros do comportamento estão sendo armazenados em base de dados (SQLite)

Para entendimento do projeto e implementação da solução, foram criados várias rotinas necessárias para o desenvolvimento do sistema de vigilancia.
Todos foram desenvolvidos em ambiente google colab.

•  TCC_treino_deteccao_rosto.ipynb - Rotina em python que utiliza rede CNN Convolucional YoloV4 para detecção de imagens, com a geração de uma rede treinada, foram utilizadas 2000 fotos para treinar o modelo com o objetivo de detectar e identificar pessoas;

•  TestaImagensYolo.ipynb - Rotina em python que executa a deteção de fotos, utilizando a rede yolo pré-treinada pelo programa TCC_treino_deteccao_rosto.ipynb;  

•  Mapeamento_rosto_68pontos.ipynb - Rotina em python que faz uso da detecção de marcos facias, visando obter a posição da face e a situação dos olhos se estão abertos ou fechados;

•  Detectar_olho.ipynb - Rotina em python que utiliza metódos do OpenCV, como haar cascade para detectar a presenta de faces e posição dos olhos se estão abertos ou fechados;

O resultados da execuções dos programas acima estão representados em documentos pdf de mesmo nome, que estão localizados no diretório TCC.

![image](https://user-images.githubusercontent.com/73618787/134441314-b87e9d58-41b2-4c5a-98a5-abc9fc970a0d.png)

Através da utilização dos programas acima, possibilitou o entendimento para o desenvolvimento de aplicação Django/WEB, que encontra-se no diretório TccVigia.

![image](https://user-images.githubusercontent.com/73618787/134441473-eb7b58ad-6518-428b-bbb4-87c31a7410df.png)

### 3. Resultados

O sistema de vigilância para portarias, visa auxiliar o porteiro aumentando a segurança do prédio, através de vários benefícios relatados abaixo:

•	Geração de alarmes informativos nos casos de posição inadequada;

•	Registro de histórico com todas as situações analisadas com data e hora;

•	Identificação do vigilante através da imagem;

•	Ambiente de monitoração em tempo real através de dashboard) com  todas as informações do vigilante e imagens históricas.

As caracteristicas acima mencionadas estão representadas no documento em pdf: Aplicação - TccVigia - aplicação web.pdf

![image](https://user-images.githubusercontent.com/73618787/134441337-2f181221-ab19-46d1-a4eb-9f0eeb9e0ac2.png)

### 4. Conclusões

Com a utilização deste projeto, estaremos contribuindo para ter uma maior controle e diagnóstico na atuação dos vigilante durante o horário de trabalho, possibilitando assim aumento da segurança do ambiente de trabalho para todos os usuários.

---

Matrícula: 191.671.031

Pontifícia Universidade Católica do Rio de Janeiro

Curso de Pós Graduação *Business Intelligence Master*
