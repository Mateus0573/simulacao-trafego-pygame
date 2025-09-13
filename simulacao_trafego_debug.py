import pygame

largura, altura = 1280, 720


class Jogador:

    def __init__(self):

        self.x = largura / 2
        self.y = altura / 2
        self.largura = 50
        self.altura = 50
        self.velocidade = 5

    def mover(self):

        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self.y -= self.velocidade

        if key[pygame.K_a]:
            self.x -= self.velocidade

        if key[pygame.K_s]:
            self.y += self.velocidade

        if key[pygame.K_d]:
            self.x += self.velocidade


class Carro:

    def __init__(self):

        self.x = 400
        self.y = 400
        self.altura = 50
        self.largura = 50


if __name__ == "__main__":

    pygame.init()

    pygame.font.init()
    font_debug = pygame.font.Font(None, 24)

    jogador = Jogador()
    carro = Carro()

    tela = pygame.display.set_mode((largura, altura))

    relogio = pygame.time.Clock()

    rodando = True

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

        jogador.mover()

        condicao1 = jogador.x + jogador.largura > carro.x
        condicao2 = jogador.x < carro.x + carro.largura
        condicao3 = jogador.y < carro.y + carro.altura
        condicao4 = jogador.y + jogador.altura > carro.y

        cor_condicao1 = (0, 255, 0) if condicao1 else (255, 0, 0)
        cor_condicao2 = (0, 255, 0) if condicao2 else (255, 0, 0)
        cor_condicao3 = (0, 255, 0) if condicao3 else (255, 0, 0)
        cor_condicao4 = (0, 255, 0) if condicao4 else (255, 0, 0)

        houve_colisao = False
        if condicao1 and condicao2 and condicao3 and condicao4:
            houve_colisao = True

        tela.fill((0, 0, 0))

        if houve_colisao:
            colisao = font_debug.render("COLISÃO", True, (255, 0, 0))
            tela.blit(colisao, (700, 20))

        pygame.draw.rect(
            tela, ((255, 0, 0)), (jogador.x, jogador.y, jogador.altura, jogador.largura)
        )

        pygame.draw.rect(
            tela, ((0, 255, 0)), (carro.x, carro.y, carro.altura, carro.largura)
        )

        pygame.draw.rect(tela, cor_condicao1, (50, altura - 50, 50, 50))
        pygame.draw.rect(tela, cor_condicao2, (125, altura - 50, 50, 50))
        pygame.draw.rect(tela, cor_condicao3, (200, altura - 50, 50, 50))
        pygame.draw.rect(tela, cor_condicao4, (275, altura - 50, 50, 50))

        info_carro = f"X: {carro.x} Y: {carro.y} X + largura: {carro.x + carro.largura} Y + altura: {carro.y + carro.altura}"
        info_jogador = f"X: {jogador.x} Y: {jogador.y} X + largura: {jogador.x + jogador.largura} Y + altura: {jogador.y + jogador.altura}"

        texto_surface = font_debug.render(info_carro, True, (255, 255, 255))
        texto_surface1 = font_debug.render(info_jogador, True, (255, 255, 255))

        posicao_y = 10
        posicao_y2 = 30

        tela.blit(texto_surface, (10, posicao_y))
        tela.blit(texto_surface1, (10, posicao_y2))

        pygame.display.flip()

        relogio.tick(60)

pygame.quit()
