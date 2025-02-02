import turtle
import math

# Configurações da tela
LARGURA, ALTURA = 1200, 800
GRAVIDADE = -0.1
CORES = {'PRETO': (0, 0, 0),
         'BRANCO': (255, 255, 255),
         'VERDE': (0, 255, 0),
         'VERMELHO': (255, 0, 0),
         'AZUL': (0, 0, 255),
         'ROXO': (128, 0, 128),
         'LARANJA': (255, 140, 0)}

# Cria a tela
janela = turtle.Screen()
janela.colormode(255)
janela.title("Lee Sin Jump Challenge!")
janela.setup(LARGURA, ALTURA)
janela.bgcolor(CORES['PRETO'])
janela.tracer(0)

# Adiciona Shapes
janela.register_shape("lee-sin.gif")
janela.register_shape("lee-sin-inverso.gif")

# Caneta Turtle
caneta = turtle.Turtle()
caneta.speed(0)
caneta.color(CORES['BRANCO'])
caneta.penup()
caneta.hideturtle()
caneta.goto(0, 0)

# Variáveis de controle de teclas pressionadas
tecla_esquerda_pressionada = False
tecla_direita_pressionada = False


# Funções para lidar com a pressão e liberação das teclas
def ao_pressionar_tecla_esquerda():
    global tecla_esquerda_pressionada
    tecla_esquerda_pressionada = True
    jogador.esquerda()


def ao_liberar_tecla_esquerda():
    global tecla_esquerda_pressionada
    tecla_esquerda_pressionada = False
    if not tecla_direita_pressionada:
        jogador.dx = 0


def ao_pressionar_tecla_direita():
    global tecla_direita_pressionada
    tecla_direita_pressionada = True
    jogador.direita()


def ao_liberar_tecla_direita():
    global tecla_direita_pressionada
    tecla_direita_pressionada = False
    if not tecla_esquerda_pressionada:
        jogador.dx = 0


# Função para Pular
pulos_disponiveis = 2


def jogador_pular():
    global pulos_disponiveis

    if pulos_disponiveis > 0:
        jogador.pular()
        pulos_disponiveis -= 1


# Função para reiniciar o contador de pulos
def reiniciar_pulos():
    global pulos_disponiveis
    pulos_disponiveis = 2


# Função que centraliza câmera no usuário
def centrar_camera():
    offset_x = jogador.x
    offset_y = jogador.y

    janela.setworldcoordinates(offset_x - LARGURA / 2, offset_y - ALTURA / 2,
                               offset_x + LARGURA / 2, offset_y + ALTURA / 2)


# Criação das classes
class Sprite:
    def __init__(self, x, y, largura, altura):
        self.x, self.y, self.dx, self.dy = x, y, 0, 0
        self.largura, self.altura = largura, altura
        self.cor = CORES['VERDE']
        self.atrito = 1

    def ir_para(self, x, y):
        self.x, self.y = x, y

    def renderizar(self):
        caneta.pencolor(self.cor)
        caneta.fillcolor(self.cor)
        caneta.penup()
        caneta.goto(self.x - self.largura / 2, self.y + self.altura / 2)
        caneta.pendown()
        caneta.begin_fill()
        caneta.goto(self.x + self.largura / 2, self.y + self.altura / 2)
        caneta.goto(self.x + self.largura / 2, self.y - self.altura / 2)
        caneta.goto(self.x - self.largura / 2, self.y - self.altura / 2)
        caneta.goto(self.x - self.largura / 2, self.y + self.altura / 2)
        caneta.end_fill()
        caneta.penup()
        caneta.ht()

    def colisao_aabb(self, outro):
        colisao_x = (math.fabs(self.x - outro.x) * 2) < (self.largura + outro.largura)
        colisao_y = (math.fabs(self.y - outro.y) * 2) < (self.altura + outro.altura)
        return colisao_x and colisao_y


class Jogador(Sprite):
    def __init__(self, x, y, largura, altura):
        super().__init__(x, y, largura, altura)
        self.cor = CORES['VERDE']
        self.ultima_direcao = "direita"  # Variável para rastrear a última direção

    def mover(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += GRAVIDADE

    def pular(self):
        self.dy = 7

    def esquerda(self):
        self.dx -= 0.1  # Velocidade
        if self.dx < -2.5:
            self.dx = -2.5
        self.ultima_direcao = "esquerda"  # Atualiza a última direção

    def direita(self):
        self.dx += 0.1  # Velocidade
        if self.dx > 2.5:
            self.dx = 2.5
        self.ultima_direcao = "direita"  # Atualiza a última direção

    # Função para verificar se o jogador está tocando um obstaculo para "deslizar" sobre ele
    def deslizante(self):
        for obstaculo in obstaculos:
            if self.colisao_aabb(obstaculo) and self.y > obstaculo.y:
                return True
        return False


class Tiro(Sprite):
    def __init__(self, jogador, direcao):
        super().__init__(jogador.x, jogador.y, 20, 20)
        self.cor = CORES['AZUL']
        self.velocidade = 10

        # Utiliza a direção do jogador para determinar a direção do tiro
        if direcao == "esquerda":
            self.dx = -self.velocidade
        else:
            self.dx = self.velocidade

    def mover(self):
        self.x += self.dx
        self.y += self.dy

    def renderizar(self):
        caneta.pencolor(self.cor)
        caneta.fillcolor(self.cor)
        caneta.penup()
        caneta.goto(self.x, self.y - self.altura / 2)
        caneta.pendown()
        caneta.begin_fill()
        caneta.circle(self.largura / 2)
        caneta.end_fill()
        caneta.penup()


# Inimigo Horizontal
class Inimigo(Sprite):
    def __init__(self, x, y, largura, altura, velocidade, limite_esquerda, limite_direita):
        super().__init__(x, y, largura, altura)
        self.cor = CORES['VERMELHO']
        self.atrito = 1
        self.velocidade = velocidade
        self.limite_esquerda = limite_esquerda
        self.limite_direita = limite_direita
        self.dx = self.velocidade  # Inicializa a velocidade horizontal

    def mover(self):
        self.x += self.dx
        self.y += self.dy

        # Verifica se atingiu o limite esquerdo
        if self.x < self.limite_esquerda:
            self.x = self.limite_esquerda
            self.dx = abs(self.dx)  # Inverte a direção (torna positiva)

        # Verifica se atingiu o limite direito
        elif self.x > self.limite_direita:
            self.x = self.limite_direita
            self.dx = -abs(self.dx)  # Inverte a direção (torna negativa)


# Inimigo Vertical
class InimigoVertical(Sprite):
    def __init__(self, x, y, largura, altura, velocidade_vertical, limite_superior, limite_inferior):
        super().__init__(x, y, largura, altura)
        self.cor = CORES['VERMELHO']
        self.atrito = 1
        self.velocidade_vertical = velocidade_vertical
        self.limite_superior = limite_superior
        self.limite_inferior = limite_inferior
        self.dy = self.velocidade_vertical  # Inicializa a velocidade vertical

    def mover(self):
        self.y += self.dy

        # Verifica se atingiu o limite superior
        if self.y > self.limite_superior:
            self.y = self.limite_superior
            self.dy = -abs(self.dy)  # Inverte a direção vertical (torna negativa)

        # Verifica se atingiu o limite inferior
        elif self.y < self.limite_inferior:
            self.y = self.limite_inferior
            self.dy = abs(self.dy)  # Inverte a direção vertical (torna positiva)


# Classe para gerar um portal que faz o player teleportar
class Teleport(Sprite):
    def __init__(self, x, y, largura, altura, destino_x, destino_y):
        super().__init__(x, y, largura, altura)
        self.destino_x = destino_x
        self.destino_y = destino_y
        self.cor = CORES['ROXO']

    def colisao_teleport(self, jogador):
        if self.colisao_aabb(jogador):
            jogador.ir_para(self.destino_x, self.destino_y)

    def renderizar(self):
        caneta.pencolor(self.cor)
        caneta.fillcolor(self.cor)
        caneta.penup()
        caneta.goto(self.x - self.largura / 2, self.y + self.altura / 2)
        caneta.pendown()
        caneta.begin_fill()
        caneta.goto(self.x + self.largura / 2, self.y + self.altura / 2)
        caneta.goto(self.x + self.largura / 2, self.y - self.altura / 2)
        caneta.goto(self.x - self.largura / 2, self.y - self.altura / 2)
        caneta.goto(self.x - self.largura / 2, self.y + self.altura / 2)
        caneta.end_fill()
        caneta.penup()


# Classe para criar textos na tela
class ObjetoTexto:
    def __init__(self, x, y, texto, cor='branco', tamanho_fonte=12):
        self.x = x
        self.y = y
        self.texto = texto
        self.cor = cor
        self.tamanho_fonte = tamanho_fonte

        # Inicializa a tartaruga para renderizar texto
        self.tartaruga = turtle.Turtle()
        self.tartaruga.speed(0)
        self.tartaruga.color(self.cor)  # Corrige a cor aqui
        self.tartaruga.penup()
        self.tartaruga.hideturtle()
        self.tartaruga.goto(self.x, self.y)

    def renderizar(self):
        self.tartaruga.clear()  # Limpa o texto anterior
        self.tartaruga.goto(self.x, self.y)
        self.tartaruga.color(self.cor)  # Corrige a cor aqui
        self.tartaruga.write(self.texto, align='center', font=('Arial', self.tamanho_fonte, 'normal'))
        self.tartaruga.ht()


# Variável para controlar vidas do jogador
vidas = 3


# Função para exibir o número de vidas na tela
def exibir_vidas():
    # Calcula as coordenadas relativas ao jogador
    rel_x = jogador.x - LARGURA / 2 + 20
    rel_y = jogador.y + ALTURA / 2 - 40

    # Atualiza as coordenadas da tela
    caneta.goto(rel_x, rel_y)
    caneta.color(CORES['BRANCO'])
    caneta.write(f"Vidas: {vidas}", align="left", font=("Arial", 16, "normal"))


# Função para verificar colisão do jogador com inimigos
def verificar_colisao_inimigos():
    global vidas
    for inimigo in inimigos:
        if jogador.colisao_aabb(inimigo):
            vidas -= 1
            if vidas == 0:
                vidas = 3
                jogador.ir_para(0, 100)  # Reposiciona o jogador para o menu
            else:
                print(f"Você perdeu uma vida! Vidas restantes: {vidas}")
                jogador.ir_para(3000, 100)  # Reposiciona o jogador no início

    for inimigo_vertical in inimigos_verticais:
        if jogador.colisao_aabb(inimigo_vertical):
            vidas -= 1
            if vidas == 0:
                vidas = 3
                jogador.ir_para(0, 100)  # Reposiciona o jogador no início
            else:
                print(f"Você perdeu uma vida! Vidas restantes: {vidas}")
                jogador.ir_para(3000, 100)  # Reposiciona o jogador para o menu


# Função para verificar se o jogador caiu do mapa
def verificar_limites_mapa():
    global vidas
    if jogador.y < -ALTURA / 0.5:
        vidas -= 1
        if vidas == 0:
            print("Game Over! Você perdeu todas as vidas.")
            vidas = 3
            jogador.ir_para(0, 100)  # Reposiciona o jogador para o menu
        else:
            print(f"Você perdeu uma vida! Vidas restantes: {vidas}")
            jogador.ir_para(3000, 100)  # Reposiciona o jogador no início


# Lista Teleport
teleportadores = [Teleport(600, 12, 50, 100, 3000, 100),  # Menu - > Jogo
                  Teleport(-600, 12, 50, 100, 0, 1500),  # Menu - > Tutorial
                  Teleport(200, 1202, 50, 100, 0, 100),
                  Teleport(5900, 1862, 50, 100, 0, 100)]  # Tutorial -> Menu

# Lista Jogador
jogador = Jogador(0, 0, 50, 100)

# Lista Sprite
obstaculos = [Sprite(0, 100, 600, 20),  # Plataforma Inicial
              Sprite(0, -150, 800, 20),  # Plataforma Abaixo da Inicial
              Sprite(0, -800, 1800, 1000),  # Chão do Menu
              Sprite(600, -50, 150, 20),  # Plataforma da direita
              Sprite(-600, -50, 150, 20),  # Plataforma da Esquerda
              Sprite(1500, 0, 1200, 2000),  # Parede direita Menu
              Sprite(-1500, 0, 1200, 2000),  # Parede esquerda Menu
              Sprite(0, 900, 1800, 500),  # Teto Menu
              Sprite(900, 1202, 20, 1100),  # Parede tutorial direita
              Sprite(3000, 0, 400, 20),  # Chão Jogo
              Sprite(3600, 100, 100, 20),  # Jogo  --
              Sprite(3900, 0, 50, 1500),
              Sprite(4400, -200, 300, 20),
              Sprite(5050, -100, 500, 20),
              Sprite(5000, 1200, 50, 2000),
              Sprite(5350, 1000, 50, 2000),
              Sprite(5900, 1800, 600, 20),]  # Jogo  --


# Lista Inimigo e InimigoVertical
inimigos = [Inimigo(3500, 50, 50, 50, 3, 3200, 3400),
            Inimigo(3900, 850, 50, 50, 3, 3800, 4000),
            Inimigo(3900, -850, 50, 50, 3, 3800, 4000),
            Inimigo(5200, 50, 50, 50, 3, 5100, 5300)]
inimigos_verticais = [InimigoVertical(-600, 1300, 50, 50, 2, 1300, 1200),
                      InimigoVertical(3600, 50, 50, 50, 2, 200, 0),
                      InimigoVertical(3800, 300, 50, 50, 2, 600, 400),
                      InimigoVertical(4800, 0, 50, 50, 1, 300, 0),
                      InimigoVertical(4900, 0, 50, 50, 2, 300, 0),
                      InimigoVertical(5000, 0, 50, 50, 3, 100, 0)]

# Lista ObjetoTexto
textos = [ObjetoTexto(0, 200, "Lee Sin Jump Challenge!", 'white', 26),  # Texto Menu
          ObjetoTexto(0, 150, "Você está preparado para começar essa aventura?!", 'white', 14),  # Texto Menu
          ObjetoTexto(-600, 110, "Tutorial", 'white', 14),  # Tutorial Menu
          ObjetoTexto(-600, 75, "  |\n v", 'white', 8),  # Tutorial Menu
          ObjetoTexto(600, 110, "Jogar", 'white', 14),  # Jogar Menu
          ObjetoTexto(600, 75, "  |\n v", 'white', 8),  # Jogar Menu
          ObjetoTexto(0, 1400, "Tutorial", 'white', 26),  # Texto Tutorial
          ObjetoTexto(200, 1292, "Menu", 'white', 14),  # Tutorial - > Portal Menu
          ObjetoTexto(200, 1262, "  |\n v", 'white', 8),  # Tutorial - > Portal Menu
          ObjetoTexto(-200, 1300, "Movimentação", 'white', 18),  # Tutorial Movimentação
          ObjetoTexto(-200, 1220, 'Para andar utilize as teclas "a" e "d" \n para ir para os lados. Para pular \n '
                                  'utilize a tecla "w" ou para dar \n "Double Jump" precione noavamente.', 'white', 12),  # Tutorial Movimentação
          ObjetoTexto(-600, 1300, "Disparo", 'white', 18),  # Tutorial Disparo
          ObjetoTexto(-600, 1250, 'Para disparar utilize a tecla \n "Espaço" do seu teclado.', 'white', 12),  # Tutorial Disparo
          ObjetoTexto(500, 1300, "Mecânica de Jogo", 'white', 18),  # Tutorial Mecânica
          ObjetoTexto(500, 1175, 'Para deslizar nas paredes basta \n andar para o lado dela, assim, seu personagem \n vai '
                                 'começar a deslizar pela parede. \n Você pode estar pulando para o lado \n oposto da parede e voltar para mesma, \n'
                                 'assim conseguindo escalar a parede.', 'white', 12),  # Tutorial Mecânica
          ObjetoTexto(5900, 2000, "Parabéns, \n Você chegou no final do desafio!", 'white', 26)]  # Texto Final

# Associação de teclas
janela.listen()
janela.onkeypress(ao_pressionar_tecla_esquerda, "a")
janela.onkeyrelease(ao_liberar_tecla_esquerda, "a")
janela.onkeypress(ao_pressionar_tecla_direita, "d")
janela.onkeyrelease(ao_liberar_tecla_direita, "d")
janela.onkeypress(jogador_pular, "w")


# Função para sair do jogo
def sair_do_jogo():
    janela.bye()  # Fecha a janela do turtle


# Associação de tecla para sair do jogo
janela.onkey(sair_do_jogo, "Escape")


# Função para exibir o "Quit" do game
def exibir_quit():
    # Calcula as coordenadas relativas ao jogador
    rel_x = jogador.x - LARGURA / 2 + 1000
    rel_y = jogador.y + ALTURA / 2 - 40

    # Atualiza as coordenadas da tela
    caneta.goto(rel_x, rel_y)
    caneta.color(CORES['BRANCO'])
    caneta.write(f'Pressione "Esc" para sair do jogo', align="center", font=("Arial", 16, "normal"))


# Função para criar e adicionar um tiro à lista de tiros
def atirar():
    global pode_atirar
    if pode_atirar:
        tiro = Tiro(jogador, jogador.ultima_direcao)  # Passa a última direção para o construtor do Tiro
        tiros.append(tiro)
        pode_atirar = False  # Impede novos tiros temporariamente
        janela.ontimer(resetar_pode_atirar, 500)  # Define um timer para permitir tiros novamente após 1 segundo


# Função para resetar a permissão de atirar
def resetar_pode_atirar():
    global pode_atirar
    pode_atirar = True


# Distância máxima que um tiro pode percorrer antes de ser removido
DISTANCIA_MAXIMA_TIRO = 1000

# Lista para armazenar os tiros
tiros = []

# Variável para controlar se o jogador pode atirar novamente
pode_atirar = True

# Associação de tecla para atirar
janela.onkeypress(atirar, "space")

# Renderiza o jogador
turtle.shape("lee-sin.gif")

# Loop principal do jogo
while True:
    # Renderiza o jogador
    turtle.goto(jogador.x, jogador.y)
    turtle.penup()

    # Move/Atualiza objetos
    if tecla_esquerda_pressionada:
        jogador.esquerda()
        turtle.shape("lee-sin-inverso.gif")  # Muda a imagem para a esquerda
    elif tecla_direita_pressionada:
        jogador.direita()
        turtle.shape("lee-sin.gif")  # Muda a imagem para a direita
    jogador.mover()

    # Verifica colisões com o chão
    if jogador.deslizante():
        jogador.dy = 0  # Reseta a velocidade vertical quando está no chão

    jogador.mover()

    # Verifica colisões
    for obstaculo in obstaculos:
        if jogador.colisao_aabb(obstaculo):
            if jogador.x < obstaculo.x - obstaculo.largura / 2.0 and jogador.dx > 0:
                jogador.dx, jogador.x = 0, obstaculo.x - obstaculo.largura / 2.0 - jogador.largura / 2.0
                reiniciar_pulos()
            elif jogador.x > obstaculo.x + obstaculo.largura / 2.0 and jogador.dx < 0:
                jogador.dx, jogador.x = 0, obstaculo.x + obstaculo.largura / 2.0 + jogador.largura / 2.0
                reiniciar_pulos()
            elif jogador.y > obstaculo.y:
                jogador.dy, jogador.y, jogador.dx = 0, obstaculo.y + obstaculo.altura / 2.0 + jogador.altura / 2.0 - 1, jogador.dx * obstaculo.atrito
                reiniciar_pulos()
                jogador.dy = 0
            elif jogador.y < obstaculo.y:
                jogador.dy, jogador.y = 0, obstaculo.y - obstaculo.altura / 2.0 - jogador.altura / 2.0
                reiniciar_pulos()
                jogador.dy = 0

    # Verifica colisões com inimigos
    verificar_colisao_inimigos()

    # Verifica se o jogador caiu do mapa
    verificar_limites_mapa()

    # Exibe o número de vidas na tela
    exibir_vidas()

    # Exibe o quit do jogo
    exibir_quit()

    # Move/Atualiza tiros
    for tiro in tiros:
        tiro.mover()

        # Verifica colisão entre tiro e inimigos
        for inimigo in inimigos:
            if tiro.colisao_aabb(inimigo):
                inimigos.remove(inimigo)  # Remove o inimigo atingido
                tiros.remove(tiro)  # Remove o tiro
        # Verifica colisão entre tiro e inimigos
        for inimigo_vertical in inimigos_verticais:
            if tiro.colisao_aabb(inimigo_vertical):
                inimigos_verticais.remove(inimigo_vertical)  # Remove o inimigo atingido
                tiros.remove(tiro)  # Remove o tiro

    # Remove tiros que atingiram a distância máxima
    tiros = [tiro for tiro in tiros if
             math.sqrt((tiro.x - jogador.x) ** 2 + (tiro.y - jogador.y) ** 2) < DISTANCIA_MAXIMA_TIRO]

    # Renderiza outros objetos
    for obstaculo in obstaculos:
        obstaculo.renderizar()

    # Renderizar inimigos
    for inimigo in inimigos:
        inimigo.renderizar()

    # Move/Atualiza inimigos
    for inimigo in inimigos:
        inimigo.mover()

    # Move/Atualiza inimigos verticais
    for inimigo_vertical in inimigos_verticais:
        inimigo_vertical.mover()

    # Renderizar inimigos verticais
    for inimigo_vertical in inimigos_verticais:
        inimigo_vertical.renderizar()

    # Renderiza tiros
    for tiro in tiros:
        tiro.renderizar()

    # Renderiza Teleport e carrega
    for teleportador in teleportadores:
        teleportador.colisao_teleport(jogador)
        teleportador.renderizar()

    # Renderiza o texto
    for texto in textos:
        texto.renderizar()

    # Centra a câmera no jogador
    centrar_camera()

    # Atualiza a tela
    janela.update()

    # Limpa a tela
    caneta.clear()
