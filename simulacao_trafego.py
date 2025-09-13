import pygame
import random

largura, altura = 1280, 720


class Ambiente:

    def __init__(self):

        self.semaforo = Semaforo()

        self.largura_rua = 150
        self.altura_rua = 150
        self.distancia_parada = 5

        self.altura_cruzamento = 25
        self.largura_cruzamento = 25

        self.lista_carro = []

        self.spawn_cooldown = 500
        self.ultimo_spawn = 0

        self.lista_spawns = ["baixo", "direita", "esquerda", "cima"]

        faixa_vertical_cima_x = (largura / 2) - (self.largura_rua / 4)
        faixa_vertical_cima_y = 0

        faixa_vertical_baixo_x = (largura / 2) + (self.largura_rua / 4)
        faixa_vertical_baixo_y = altura

        faixa_horizontal_direita_x = largura
        faixa_horizontal_direita_y = (altura / 2) - (self.altura_rua / 4)

        faixa_horizontal_esquerda_x = 0
        faixa_horizontal_esquerda_y = (altura / 2) + (self.altura_rua / 4)

        self.dicionario_faixas = {
            "cima": (faixa_vertical_cima_x, faixa_vertical_cima_y),
            "baixo": (faixa_vertical_baixo_x, faixa_vertical_baixo_y),
            "direita": (faixa_horizontal_direita_x, faixa_horizontal_direita_y),
            "esquerda": (faixa_horizontal_esquerda_x, faixa_horizontal_esquerda_y),
        }

        borda_superior_cruzamento = (
            (altura / 2)
            - (self.largura_rua / 2)
            - (self.altura_cruzamento)
            - self.distancia_parada
        )
        borda_inferior_cruzamento = (
            (altura / 2)
            + (self.largura_rua / 2)
            + (self.altura_cruzamento)
            + self.distancia_parada
        )
        borda_esquerda_cruzamento = (
            (largura / 2)
            - (self.largura_rua / 2)
            - (self.largura_cruzamento)
            - self.distancia_parada
        )
        borda_direita_cruzamento = (
            (largura / 2)
            + (self.largura_rua / 2)
            + (self.largura_cruzamento)
            + self.distancia_parada
        )

        self.dicionario_cruzamentos = {
            "cima": borda_superior_cruzamento,
            "baixo": borda_inferior_cruzamento,
            "direita": borda_direita_cruzamento,
            "esquerda": borda_esquerda_cruzamento,
        }

    def update(self):

        self.semaforo.trocar_estado()

        self.agora = pygame.time.get_ticks()

        if (
            self.agora - self.ultimo_spawn > self.spawn_cooldown
            and len(self.lista_carro) <= 20
        ):

            lista_spaw = random.choice(self.lista_spawns)
            carro = Carro(50, 50, lista_spaw, self.dicionario_faixas)
            self.lista_carro.append(carro)

            self.ultimo_spawn = self.agora

        for carro in self.lista_carro:
            carro.mover(self.semaforo.estado, self.dicionario_cruzamentos)
            carro.limites()

        faixas_verticais = ["cima", "baixo"]
        faixas_horizontais = ["esquerda", "direita"]

        for i in range(len(self.lista_carro)):
            for j in range(i + 1, len(self.lista_carro)):
                carro_A = self.lista_carro[i]
                carro_B = self.lista_carro[j]

                if (
                    carro_A.ponto_spawn in faixas_horizontais
                    and carro_B.ponto_spawn in faixas_verticais
                ) or (
                    carro_A.ponto_spawn in faixas_verticais
                    and carro_B.ponto_spawn in faixas_horizontais
                ):
                    if (
                        carro_A.x + carro_A.largura > carro_B.x
                        and carro_A.x < carro_B.x + carro_B.largura
                        and carro_A.y < carro_B.y + carro_B.altura
                        and carro_A.y + carro_A.altura > carro_B.y
                    ):
                        carro_A.ativo = False
                        carro_B.ativo = False

                        print("colisão")

        self.lista_carro = [carro for carro in self.lista_carro if carro.ativo]

    def draw(self, tela):

        tela.fill((0, 0, 0))

        # faixa vertical cima-baixo
        pygame.draw.rect(
            tela, (0, 255, 0), ((largura / 2) - self.largura_rua / 2, 0, 150, altura)
        )

        # faixa horizontal esquerda-direita
        pygame.draw.rect(
            tela, (0, 255, 0), (0, (altura / 2) - self.altura_rua / 2, largura, 150)
        )

        # faixa cruzamento cima
        pygame.draw.rect(
            tela,
            (255, 255, 255),
            (
                (largura // 2) - (self.largura_rua // 2),
                (altura // 2) - (self.altura_rua // 2) - self.altura_cruzamento,
                self.largura_rua,
                self.altura_cruzamento,
            ),
        )

        # faixa cruzamento direita
        pygame.draw.rect(
            tela,
            (255, 255, 255),
            (
                (largura // 2) + (self.largura_rua // 2),
                (altura // 2) - (self.altura_rua // 2),
                self.largura_cruzamento,
                self.altura_rua,
            ),
        ),

        # faixa cruzamento baixo
        pygame.draw.rect(
            tela,
            (255, 255, 255),
            (
                (largura // 2) - (self.largura_rua // 2),
                (altura // 2) + (self.altura_rua // 2),
                self.largura_rua,
                self.altura_cruzamento,
            ),
        ),

        pygame.draw.rect(
            tela,
            (255, 255, 255),
            (
                (largura // 2) - (self.largura_rua // 2) - self.largura_cruzamento,
                (altura // 2) - (self.altura_rua // 2),
                self.largura_cruzamento,
                self.altura_rua,
            ),
        )

        for carro in self.lista_carro:
            pygame.draw.rect(
                tela, (0, 0, 255), (carro.x, carro.y, carro.largura, carro.altura)
            )

        if self.semaforo.estado == "verde_vertical":
            pygame.draw.circle(tela, (0, 255, 0), (largura - 30, 30), 15)
        else:
            pygame.draw.circle(tela, (255, 0, 0), (largura - 30, 30), 15)

        semaforo_estado = font.render(self.semaforo.estado, True, (255, 255, 255))
        tela.blit(semaforo_estado, (largura - 140, 60))


class Carro:

    def __init__(self, player_altura, player_largura, ponto_spawn, dicionario_faixas):

        self.altura = player_altura
        self.largura = player_largura
        self.velocidade = 5
        self.ativo = True
        self.ponto_spawn = ponto_spawn

        self.velocidade_x = 0
        self.velocidade_y = 0

        nascimento = dicionario_faixas[self.ponto_spawn]

        self.x = nascimento[0]
        self.y = nascimento[1]

        if self.ponto_spawn == "cima":
            self.x = self.x - self.largura / 2
            self.velocidade_y = self.velocidade

        elif self.ponto_spawn == "baixo":
            self.x = self.x - self.largura / 2
            self.velocidade_y = -(self.velocidade)

        elif self.ponto_spawn == "direita":
            self.y = self.y - self.altura / 2
            self.velocidade_x = -(self.velocidade)

        elif self.ponto_spawn == "esquerda":
            self.y = self.y - self.altura / 2
            self.velocidade_x = self.velocidade

    def mover(self, estado_semaforo, dicionario_cruzamentos):

        self.borda = dicionario_cruzamentos[self.ponto_spawn]

        pode_mover = True

        if (
            self.ponto_spawn == "cima"
            and estado_semaforo != "verde_vertical"
            and self.y + self.altura >= self.borda
        ):
            pode_mover = False

            if (
                estado_semaforo in ["verde_horizontal", "amarelo"]
                and self.y > self.borda
            ):
                pode_mover = True

        elif (
            self.ponto_spawn == "baixo"
            and estado_semaforo != "verde_vertical"
            and self.y <= self.borda
        ):
            pode_mover = False

            if (
                estado_semaforo in ["verde_horizontal", "amarelo"]
                and self.y < self.borda
            ):
                pode_mover = True

        elif (
            self.ponto_spawn == "esquerda"
            and estado_semaforo != "verde_horizontal"
            and self.x + self.largura >= self.borda
        ):
            pode_mover = False

            if estado_semaforo in ["verde_vertical", "amarelo"] and self.x > self.borda:
                pode_mover = True

        elif (
            self.ponto_spawn == "direita"
            and estado_semaforo != "verde_horizontal"
            and self.x <= self.borda
        ):
            pode_mover = False

            if (
                estado_semaforo in ["verde_vertical", "amarelo"]
                and self.x + self.largura < self.borda
            ):
                pode_mover = True

        if pode_mover:
            self.y += self.velocidade_y
            self.x += self.velocidade_x

    def limites(self):

        # esquerda
        if self.x + self.largura < 0:
            self.ativo = False
            # print("sai, esquerda")

        # cima
        if self.y + self.altura < 0:
            self.ativo = False
            # print("sai, cima")

        # direita
        if self.x > largura:
            self.ativo = False
            # print("sai, direita")

        # abaixo
        if self.y > altura:
            self.ativo = False
            # print("sai, baixo")


class Semaforo:

    def __init__(self):

        self.estado = random.choice(["verde_vertical", "verde_horizontal"])

        self.ultimo_estado_semaforo = 0
        self.semaforo_cooldown = 5000

        self.estado_anterior = self.estado

        self.cooldown_amarelo = 4000

    def trocar_estado(self):

        semaforo_tempo = pygame.time.get_ticks()

        if (
            self.estado in ["verde_vertical", "verde_horizontal"]
            and semaforo_tempo - self.ultimo_estado_semaforo > self.semaforo_cooldown
        ):

            self.estado_anterior = self.estado

            self.estado = "amarelo"

            self.ultimo_estado_semaforo = semaforo_tempo

        elif (
            self.estado == "amarelo"
            and semaforo_tempo - self.ultimo_estado_semaforo > self.cooldown_amarelo
        ):

            if self.estado_anterior == "verde_vertical":
                self.estado = "verde_horizontal"

            elif self.estado_anterior == "verde_horizontal":
                self.estado = "verde_vertical"

            self.ultimo_estado_semaforo = semaforo_tempo


if __name__ == "__main__":

    pygame.init()

    tela = pygame.display.set_mode((largura, altura))

    relogio = pygame.time.Clock()

    pygame.font.init()

    font = pygame.font.Font(None, 24)

    ambiente = Ambiente()

    rodando = True

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

        ambiente.update()

        ambiente.draw(tela)

        pygame.display.flip()

        relogio.tick(60)

pygame.quit()
