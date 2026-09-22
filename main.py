import time
import random
from datetime import datetime


# ============================================================
# CARRO ELÉTRICO
# ============================================================

class CarroEletrico:

    def __init__(self, modelo, bateria_atual, capacidade_max):
        self.modelo = modelo
        self.bateria_atual = bateria_atual
        self.capacidade_max = capacidade_max
        self.potencia_recarga_atual = 0.0
        self.energia_recebida = 0.0

    @property
    def porcentagem_bateria(self):
        return (self.bateria_atual / self.capacidade_max) * 100

    def carregar(self, potencia):
        self.potencia_recarga_atual = potencia

        if potencia > 0:
            energia_recebida = potencia * 0.1

            espaco_disponivel = (
                self.capacidade_max - self.bateria_atual
            )

            energia_recebida = min(
                energia_recebida,
                espaco_disponivel
            )

            self.bateria_atual += energia_recebida
            self.energia_recebida += energia_recebida

        else:
            self.potencia_recarga_atual = 0.0


# ============================================================
# FONTE DE ENERGIA RENOVÁVEL
# ============================================================

class EnergiaSolar:

    def __init__(self, capacidade_maxima):
        self.capacidade_maxima = capacidade_maxima
        self.energia_gerada = 0.0

    def gerar_energia(self):
        self.energia_gerada = random.uniform(
            10.0,
            self.capacidade_maxima
        )

        return self.energia_gerada


# ============================================================
# CHARGEGRID INTELLIGENCE
# ============================================================

class ChargeGridIntelligence:

    def __init__(self, limite_max_rede):

        self.limite_max_rede = limite_max_rede
        self.carros_conectados = []

        self.historico = []

    # --------------------------------------------------------
    # ADICIONAR CARRO
    # --------------------------------------------------------

    def adicionar_carro(self, carro):

        self.carros_conectados.append(carro)

    # --------------------------------------------------------
    # TARIFA DINÂMICA
    # --------------------------------------------------------

    def calcular_tarifa(self, demanda_total):

        proporcao = demanda_total / self.limite_max_rede

        if proporcao > 0.85:
            return 2.50

        elif proporcao > 0.50:
            return 1.20

        else:
            return 0.65

    # --------------------------------------------------------
    # GERENCIAMENTO DA DEMANDA
    # --------------------------------------------------------

    def gerenciar_demanda(self, energia_solar):

        print("\n")
        print("=" * 70)
        print("       CHARGEGRID INTELLIGENCE - MONITORAMENTO")
        print("=" * 70)

        horario = datetime.now().strftime("%H:%M:%S")

        print(f"Horário da simulação: {horario}")

        # ----------------------------------------------------
        # CONSUMO DO PRÉDIO
        # ----------------------------------------------------

        consumo_predio = random.uniform(30.0, 65.0)

        print(
            f"\nConsumo da instalação: "
            f"{consumo_predio:.2f} kW"
        )

        # ----------------------------------------------------
        # ENERGIA DISPONÍVEL
        # ----------------------------------------------------

        energia_rede = max(
            0,
            self.limite_max_rede - consumo_predio
        )

        energia_total_disponivel = (
            energia_rede + energia_solar
        )

        print(
            f"Energia solar disponível: "
            f"{energia_solar:.2f} kW"
        )

        print(
            f"Energia disponível da rede: "
            f"{energia_rede:.2f} kW"
        )

        print(
            f"Energia total disponível para recarga: "
            f"{energia_total_disponivel:.2f} kW"
        )

        # ----------------------------------------------------
        # DEMANDA TOTAL
        # ----------------------------------------------------

        demanda_total = consumo_predio

        tarifa = self.calcular_tarifa(
            demanda_total
        )

        print(
            f"\nTarifa dinâmica: "
            f"R$ {tarifa:.2f}/kWh"
        )

        # ----------------------------------------------------
        # FILTRAR CARROS
        # ----------------------------------------------------

        carros_ativos = [
            carro
            for carro in self.carros_conectados
            if carro.porcentagem_bateria < 100
        ]

        if not carros_ativos:

            print(
                "\nTodos os veículos estão "
                "100% carregados."
            )

            return

        # ----------------------------------------------------
        # DISTRIBUIÇÃO DE POTÊNCIA
        # ----------------------------------------------------

        potencia_por_carro = (
            energia_total_disponivel /
            len(carros_ativos)
        )

        # Limite máximo de carregamento
        if potencia_por_carro > 11:
            potencia_por_carro = 11

        # ----------------------------------------------------
        # SITUAÇÃO CRÍTICA
        # ----------------------------------------------------

        if energia_total_disponivel < 6:

            potencia_por_carro = 0

            print(
                "\n[ALERTA] DEMANDA CRÍTICA!"
            )

            print(
                "Carregamento suspenso "
                "temporariamente."
            )

        elif energia_total_disponivel < 15:

            potencia_por_carro = 2

            print(
                "\n[ALERTA] BAIXA DISPONIBILIDADE "
                "DE ENERGIA."
            )

            print(
                "Carregamento reduzido."
            )

        else:

            print(
                "\n[STATUS] Condições normais."
            )

        # ----------------------------------------------------
        # MOSTRAR POTÊNCIA
        # ----------------------------------------------------

        print(
            f"\nPotência distribuída por veículo: "
            f"{potencia_por_carro:.2f} kW"
        )

        print("\n" + "-" * 70)
        print("STATUS DOS VEÍCULOS")
        print("-" * 70)

        # ----------------------------------------------------
        # CARREGAMENTO
        # ----------------------------------------------------

        for carro in carros_ativos:

            carro.carregar(
                potencia_por_carro
            )

            if potencia_por_carro > 0:

                status = "CARREGANDO"

            else:

                status = "AGUARDANDO"

            print(
                f"{carro.modelo:<18}"
                f"| Bateria: "
                f"{carro.porcentagem_bateria:6.1f}% "
                f"| Potência: "
                f"{carro.potencia_recarga_atual:5.2f} kW "
                f"| {status}"
            )

        # ----------------------------------------------------
        # REGISTRAR HISTÓRICO
        # ----------------------------------------------------

        registro = {

            "horario": horario,

            "consumo_predio": consumo_predio,

            "energia_solar": energia_solar,

            "energia_rede": energia_rede,

            "energia_total": energia_total_disponivel,

            "tarifa": tarifa,

            "potencia_por_carro": potencia_por_carro

        }

        self.historico.append(registro)


# ============================================================
# RELATÓRIO FINAL
# ============================================================

def gerar_relatorio(sistema):

    print("\n\n")
    print("=" * 70)
    print("              RELATÓRIO FINAL DA SESSÃO")
    print("=" * 70)

    if not sistema.historico:

        print("Nenhum dado registrado.")

        return

    total_solar = sum(
        item["energia_solar"]
        for item in sistema.historico
    )

    media_consumo = (
        sum(
            item["consumo_predio"]
            for item in sistema.historico
        )
        /
        len(sistema.historico)
    )

    media_potencia = (
        sum(
            item["potencia_por_carro"]
            for item in sistema.historico
        )
        /
        len(sistema.historico)
    )

    print(
        f"\nCiclos de monitoramento: "
        f"{len(sistema.historico)}"
    )

    print(
        f"Energia solar total simulada: "
        f"{total_solar:.2f} kW"
    )

    print(
        f"Consumo médio da instalação: "
        f"{media_consumo:.2f} kW"
    )

    print(
        f"Potência média por veículo: "
        f"{media_potencia:.2f} kW"
    )

    print("\nSTATUS FINAL DOS VEÍCULOS")

    print("-" * 70)

    for carro in sistema.carros_conectados:

        print(
            f"{carro.modelo:<18}"
            f"| Bateria: "
            f"{carro.porcentagem_bateria:6.1f}% "
            f"| Energia recebida: "
            f"{carro.energia_recebida:.2f} kWh"
        )

    print("\n" + "=" * 70)

    print(
        "Simulação finalizada com sucesso."
    )

    print("=" * 70)


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    print("=" * 70)

    print(
        "     CHARGEGRID INTELLIGENCE - SPRINT 3"
    )

    print(
        "     PROTOTIPAGEM FUNCIONAL E INTEGRAÇÃO"
    )

    print("=" * 70)

    # --------------------------------------------------------
    # SISTEMA
    # --------------------------------------------------------

    central_chargegrid = ChargeGridIntelligence(
        limite_max_rede=80.0
    )

    # --------------------------------------------------------
    # FONTE RENOVÁVEL
    # --------------------------------------------------------

    painel_solar = EnergiaSolar(
        capacidade_maxima=30.0
    )

    # --------------------------------------------------------
    # VEÍCULOS
    # --------------------------------------------------------

    carro1 = CarroEletrico(
        "BYD Dolphin",
        bateria_atual=15.0,
        capacidade_max=45.0
    )

    carro2 = CarroEletrico(
        "GWM Ora 03",
        bateria_atual=38.0,
        capacidade_max=48.0
    )

    carro3 = CarroEletrico(
        "Volvo EX30",
        bateria_atual=42.0,
        capacidade_max=51.0
    )

    # --------------------------------------------------------
    # CONECTAR VEÍCULOS
    # --------------------------------------------------------

    central_chargegrid.adicionar_carro(carro1)
    central_chargegrid.adicionar_carro(carro2)
    central_chargegrid.adicionar_carro(carro3)

    print(
        "\nSistema inicializado."
    )

    print(
        "Fonte renovável conectada."
    )

    print(
        "Veículos conectados."
    )

    print(
        "Monitoramento iniciado."
    )

    # --------------------------------------------------------
    # SIMULAÇÃO
    # --------------------------------------------------------

    for ciclo in range(5):

        print(
            f"\n\n******** CICLO {ciclo + 1} ********"
        )

        energia_solar = (
            painel_solar.gerar_energia()
        )

        central_chargegrid.gerenciar_demanda(
            energia_solar
        )

        time.sleep(2)

    # --------------------------------------------------------
    # RELATÓRIO
    # --------------------------------------------------------

    gerar_relatorio(
        central_chargegrid
    )
