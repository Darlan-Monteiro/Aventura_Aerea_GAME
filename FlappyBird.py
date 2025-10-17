import pygame
import os
import random
import sys 

# função para obter o caminho correto dos recursos
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# parâmetros da janela do jogo
largura_janela = 800
altura_janela = 900

#carregamento das imagens
imagem_asteroide = pygame.transform.scale2x(pygame.image.load(resource_path(os.path.join('imgs', 'pipe.png'))))
imagem_superficie = pygame.transform.scale2x(pygame.image.load(resource_path(os.path.join('imgs', 'base.png'))))
imagem_fundo_original = pygame.image.load(resource_path(os.path.join('imgs', 'bg.png')))
imagem_fundo = pygame.transform.scale(imagem_fundo_original, (largura_janela, altura_janela))
imagens_nave = [
    pygame.transform.scale2x(pygame.image.load(resource_path(os.path.join('imgs', 'bird1.png')))),
    pygame.transform.scale2x(pygame.image.load(resource_path(os.path.join('imgs', 'bird2.png')))),
    pygame.transform.scale2x(pygame.image.load(resource_path(os.path.join('imgs', 'bird3.png')))),
]

# inicialização das fontes
pygame.font.init()
fonte_score = pygame.font.SysFont('bahnschrift', 45)
fonte_game_over = pygame.font.SysFont('bahnschrift', 80)
fonte_instrucao = pygame.font.SysFont('bahnschrift', 30)
fonte_titulo = pygame.font.SysFont('bahnschrift', 70)
fonte_input = pygame.font.SysFont('bahnschrift', 50)
fonte_placar = pygame.font.SysFont('bahnschrift', 28)

# cores
AMARELO = (255, 255, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO_FIM = (255, 40, 40)

# classes do jogo
class NaveJogador:
    imagens = imagens_nave
    inclinacao_maxima = 25
    velocidade_inclinacao = 20
    duracao_animacao = 4

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura_inicial = self.y
        self.tempo_voo = 0
        self.contador_imagem = 0
        self.imagem_atual = self.imagens[0]
    
    def subir(self):
        self.velocidade = -12.5
        self.tempo_voo = 0
        self.altura_inicial = self.y
    
    def mover(self):
        self.tempo_voo += 1
        deslocamento = 1.8 * (self.tempo_voo**2) + self.velocidade * self.tempo_voo
        if deslocamento > 18:
            deslocamento = 18
        elif deslocamento < 0:
            deslocamento -= 2
        self.y += deslocamento
        if deslocamento < 0 or self.y < (self.altura_inicial + 50):
            if self.angulo < self.inclinacao_maxima:
                self.angulo = self.inclinacao_maxima
        else:
            if self.angulo > -90:
                self.angulo -= self.velocidade_inclinacao
    # função para desenhar
    def desenhar(self, tela):
        self.contador_imagem += 1
        if self.contador_imagem < self.duracao_animacao:
            self.imagem_atual = self.imagens[0]
        elif self.contador_imagem < self.duracao_animacao * 2:
            self.imagem_atual = self.imagens[1]
        elif self.contador_imagem < self.duracao_animacao * 3:
            self.imagem_atual = self.imagens[2]
        elif self.contador_imagem < self.duracao_animacao * 4:
            self.imagem_atual = self.imagens[1]
        elif self.contador_imagem >= self.duracao_animacao * 4 + 1:
            self.imagem_atual = self.imagens[0]
            self.contador_imagem = 0
        if self.angulo <= -80:
            self.imagem_atual = self.imagens[1]
            self.contador_imagem = self.duracao_animacao * 2
        imagem_rotacionada = pygame.transform.rotate(self.imagem_atual, self.angulo)
        centro_imagem = self.imagem_atual.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem_atual)
# classe dos asteroides
class Asteroide:
    distancia_vertical = 250
    velocidade_cenario = 7

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.asteroide_topo = pygame.transform.flip(imagem_asteroide, False, True)
        self.asteroide_base = imagem_asteroide
        self.passou = False
        self.definir_altura()
    
    def definir_altura(self):
        self.altura = random.randrange(100, 600)
        self.pos_topo = self.altura - self.asteroide_topo.get_height()
        self.pos_base = self.altura + self.distancia_vertical
    
    def mover(self):
        self.x -= self.velocidade_cenario
    
    def desenhar(self, tela):
        tela.blit(self.asteroide_topo, (self.x, self.pos_topo))
        tela.blit(self.asteroide_base, (self.x, self.pos_base))
    
    def colidir(self, nave):
        nave_mask = nave.get_mask()
        topo_mask = pygame.mask.from_surface(self.asteroide_topo)
        base_mask = pygame.mask.from_surface(self.asteroide_base)
        offset_topo = (self.x - nave.x, self.pos_topo - round(nave.y))
        offset_base = (self.x - nave.x, self.pos_base - round(nave.y))
        colisao_topo = nave_mask.overlap(topo_mask, offset_topo)
        colisao_base = nave_mask.overlap(base_mask, offset_base)
        return bool(colisao_topo or colisao_base)
# classe do chão/superfície
class Superficie:
    velocidade_cenario = 7
    largura = imagem_superficie.get_width()
    imagem = imagem_superficie
    
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.largura
    
    def mover(self):
        self.x1 -= self.velocidade_cenario
        self.x2 -= self.velocidade_cenario
        if self.x1 + self.largura < 0:
            self.x1 = self.x2 + self.largura
        if self.x2 + self.largura < 0:
            self.x2 = self.x1 + self.largura
    
    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.imagem, (self.x2, self.y))
# funções de desenho
def desenhar_texto_com_sombra(tela, texto, fonte, cor_principal, pos_centro, cor_sombra=PRETO):
    texto_sombra = fonte.render(texto, True, cor_sombra)
    pos_sombra = texto_sombra.get_rect(center=(pos_centro[0] + 2, pos_centro[1] + 2))
    tela.blit(texto_sombra, pos_sombra)
    texto_principal = fonte.render(texto, True, cor_principal)
    pos_principal = texto_principal.get_rect(center=pos_centro)
    tela.blit(texto_principal, pos_principal)
# função para desenhar a janela do jogo
def desenhar_janela(tela, naves, asteroides, chao, score):
    tela.blit(imagem_fundo, (0, 0))
    for nave in naves:
        nave.desenhar(tela)
    for asteroide in asteroides:
        asteroide.desenhar(tela)

    pos_score = (largura_janela - 120, 40)
    desenhar_texto_com_sombra(tela, f"SCORE: {score}", fonte_score, AMARELO, pos_score)
    chao.desenhar(tela)
# função para desenhar a tela de game over
def desenhar_tela_game_over(tela, score):
    s = pygame.Surface((largura_janela, altura_janela), pygame.SRCALPHA)
    s.fill((0,0,0, 180))
    tela.blit(s, (0,0))
    desenhar_texto_com_sombra(tela, "FIM DE JOGO", fonte_game_over, VERMELHO_FIM, (largura_janela/2, altura_janela/2 - 100))
    desenhar_texto_com_sombra(tela, f"Score final: {score}", fonte_score, AMARELO, (largura_janela/2, altura_janela/2))
    desenhar_texto_com_sombra(tela, "Pressione R para continuar ou Q para sair", fonte_instrucao, BRANCO, (largura_janela/2, altura_janela/2 + 100))

# função para desenhar a tela do menu
def desenhar_tela_menu(tela, nick_atual, scores_da_sessao):
    tela.blit(imagem_fundo, (0, 0))
    desenhar_texto_com_sombra(tela, "Aventura Aérea", fonte_titulo, AMARELO, (largura_janela/2, 150))
    desenhar_texto_com_sombra(tela, "Placar da Sessão", fonte_score, AMARELO, (largura_janela/2, 250))
    scores_ordenados = sorted(scores_da_sessao, key=lambda item: item[1], reverse=True)
    top_scores = scores_ordenados[:3]

    y_pos_score = 310
    if not top_scores:
        desenhar_texto_com_sombra(tela, "Nenhuma pontuação ainda!", fonte_placar, BRANCO, (largura_janela/2, y_pos_score))
    else:
        for i, (nick, score) in enumerate(top_scores):
            desenhar_texto_com_sombra(tela, f"{i+1}. {nick} - {score} pontos", fonte_placar, BRANCO, (largura_janela/2, y_pos_score))
            y_pos_score += 40

    desenhar_texto_com_sombra(tela, "Digite seu Nick:", fonte_score, BRANCO, (largura_janela/2, altura_janela/2 + 100))
    desenhar_texto_com_sombra(tela, nick_atual + "_", fonte_input, BRANCO, (largura_janela/2, altura_janela/2 + 160))
    desenhar_texto_com_sombra(tela, "Pressione ENTER para começar ou Q para sair", fonte_instrucao, BRANCO, (largura_janela/2, altura_janela/2 + 250))
    desenhar_texto_com_sombra(tela, "Pressione ESPAÇO para fazer o pássaro pular", fonte_instrucao, BRANCO, (largura_janela/2, altura_janela/2 + 350))
# função principal do jogo   
def main():
    tela = pygame.display.set_mode((largura_janela, altura_janela))
    pygame.display.set_caption("Aventura Aérea")
    clock = pygame.time.Clock()
    estado_jogo = 'MENU'
    rodando_programa = True
    nick_atual = ""
    scores_da_sessao = []
    naves, superficie, asteroides, score = [], None, [], 0
    
    while rodando_programa:
        clock.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando_programa = False
            
            if evento.type == pygame.KEYDOWN:
                if estado_jogo == 'MENU':
                    if evento.key == pygame.K_RETURN and len(nick_atual) > 0:
                        naves = [NaveJogador(350, 450)]
                        superficie = Superficie(900)
                        asteroides = [Asteroide(850)]
                        score = 0
                        estado_jogo = 'JOGANDO'
                    elif evento.key == pygame.K_BACKSPACE:
                        nick_atual = nick_atual[:-1]
                    elif evento.key == pygame.K_q:
                        rodando_programa = False
                    elif len(nick_atual) < 10:
                        if evento.unicode.isalnum():
                            nick_atual += evento.unicode
                
                elif estado_jogo == 'JOGANDO':
                    if evento.key == pygame.K_SPACE or evento.key == pygame.K_UP:
                        for nave in naves:
                            nave.subir()
                
                elif estado_jogo == 'GAME_OVER':
                    if evento.key == pygame.K_r:
                        estado_jogo = 'MENU'
                        nick_atual = ""
                    if evento.key == pygame.K_q:
                        rodando_programa = False
        
        if estado_jogo == 'JOGANDO':
            for nave in naves: nave.mover()
            superficie.mover()

            criar_novo_asteroide = False
            asteroides_a_remover = []
            for asteroide in asteroides:
                for i, nave in enumerate(naves):
                    if asteroide.colidir(nave): naves.pop(i)
                    if not asteroide.passou and nave.x > asteroide.x:
                        asteroide.passou = True
                        criar_novo_asteroide = True
                
                asteroide.mover()
                if asteroide.x + asteroide.asteroide_topo.get_width() < 0:
                    asteroides_a_remover.append(asteroide)

            if criar_novo_asteroide:
                score += 1
                asteroides.append(Asteroide(850))
            for asteroide in asteroides_a_remover:
                asteroides.remove(asteroide)

            for i, nave in enumerate(naves):
                if (nave.y + nave.imagem_atual.get_height()) > superficie.y or nave.y < 0:
                    naves.pop(i)
            
            if len(naves) == 0:
                scores_da_sessao.append((nick_atual, score))
                estado_jogo = 'GAME_OVER'
        
        if estado_jogo == 'MENU':
            desenhar_tela_menu(tela, nick_atual, scores_da_sessao)
        elif estado_jogo == 'JOGANDO':
            desenhar_janela(tela, naves, asteroides, superficie, score)
        elif estado_jogo == 'GAME_OVER':
            desenhar_janela(tela, naves, asteroides, superficie, score)
            desenhar_tela_game_over(tela, score)
        
        pygame.display.update()

    pygame.quit()
    sys.exit()
    
if __name__ == '__main__':
    main()