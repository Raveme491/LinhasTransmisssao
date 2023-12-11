import matplotlib.pyplot as plt
import numpy as np


class TransitoriosDegrau:
    def __init__(self, z0, zs, up, vs, comprimento, zl=0) -> None:
        self.z0 = z0
        self.zl = zl
        self.zs = zs
        self.up = up * 3e8
        self.vs = vs
        self.comprimento = comprimento

    def calculo_tensao_inicial(self):
        return (self.z0 * self.vs) / (self.zs + self.z0)

    def calculo_tau_l(self):
        tau_l = (self.zl - self.z0) / (self.zl + self.z0)
        return tau_l

    def calculo_tau_s(self):
        tau_s = (self.zs - self.z0) / (self.zs + self.z0)
        return tau_s

    def calculo_tempo_transito(self):
        return self.comprimento / self.up

    def calculo_tensao_final(self):
        v_final = self.vs * self.zl / (self.zl + self.zs)
        return v_final

    def calculo_tensao_linha(self):
        v_linha = self.vs * self.z0 / (self.zs + self.z0)
        return v_linha

    def tensoes_transiente(self, ciclos=4):
        tensao0 = self.calculo_tensao_linha()
        vetor_taus = [1]

        for i in range(ciclos):
            if not i % 2:
                vetor_taus.append(vetor_taus[-1] * self.calculo_tau_l())
            else:
                vetor_taus.append(vetor_taus[-1] * self.calculo_tau_s())
        tensoes_parciais = [tensao0 * i for i in vetor_taus]
        tensoes_parciais.insert(0, 0)
        tensoes_corrigidas = [self.calculo_tensao_inicial()]
        for index, value in enumerate(tensoes_parciais[2:]):
            if not index:
                result = value + tensoes_parciais[index + 1]
                tensoes_corrigidas.append(round(result, 2))
            else:
                result = value + tensoes_corrigidas[-1]
                tensoes_corrigidas.append(round(result, 2))
        return tensoes_corrigidas

    def plot_transiente_fonte(self, ciclos=4):
        tensoes = self.tensoes_transiente()
        intervalos = [
            int(str(self.calculo_tempo_transito())[0]) * i
            for i in range(1, ciclos + 1)
        ]
        intervalos.insert(0, 0)
        tempo = np.linspace(0, intervalos[-1], 1000)
        vetor_tensao = np.full_like(tempo, tensoes[0])
        for intervalo, tensao in zip(intervalos, tensoes):
            vetor_tensao[tempo > intervalo * 2] = tensao

        plt.figure(figsize=(8, 4))
        plt.plot(tempo, vetor_tensao, label='Tensão')
        plt.title('Gráfico de Transiente de tensão na extremidade da linha')
        plt.xlabel('Tempo (ns)')
        plt.ylabel('Tensão (V)')
        plt.grid(True)
        plt.yticks(np.unique(vetor_tensao))
        plt.legend()
        plt.show()

    def plot_transiente_meio_linha(self, ciclos=5):
        tensoes = self.tensoes_transiente()
        tensoes.insert(0, 0)
        intervalos = [
            int(str(self.calculo_tempo_transito())[0]) * i
            - int(str(self.calculo_tempo_transito())[0]) / 2
            for i in range(1, ciclos + 1)
        ]
        intervalos.insert(0, 0)
        tempo = np.linspace(0, intervalos[-1], 1000)
        vetor_tensao = np.full_like(tempo, tensoes[0])
        for intervalo, tensao in zip(intervalos, tensoes):
            if intervalo == intervalos[0]:
                vetor_tensao[tempo < intervalo / 2] = tensoes[0]
            else:
                vetor_tensao[tempo > intervalo] = tensao

        plt.figure(figsize=(8, 4))
        plt.plot(tempo, vetor_tensao, label='Tensão')
        plt.title('Gráfico de Transiente de tensão na extremidade da linha')
        plt.xlabel('Tempo (ns)')
        plt.ylabel('Tensão (V)')
        plt.grid(True)
        plt.yticks(np.unique(vetor_tensao))
        plt.legend()
        plt.show()

    def plot_transiente_carga(self, ciclos=4):
        tempo_unitario = self.calculo_tempo_transito() / 10**-9
        tensoes = self.tensoes_transiente()
        tensoes = tensoes[1::2]

        tensoes.insert(0, 0)
        intervalos = [tempo_unitario * i for i in range(1, ciclos + 1, 2)]
        intervalos.insert(0, 0)
        intervalos.insert(4, ciclos * tempo_unitario)
        tempo = np.linspace(0, intervalos[-1], 1000)
        vetor_tensao = np.full_like(tempo, tensoes[0])
        for intervalo, tensao in zip(intervalos, tensoes):
            vetor_tensao[tempo > intervalo] = tensao

        plt.figure(figsize=(8, 4))
        plt.plot(tempo, vetor_tensao, label='Tensão')
        plt.title('Gráfico de Transiente de tensão na extremidade da linha')
        plt.xlabel('Tempo (ns)')
        plt.ylabel('Tensão (V)')
        plt.grid(True)
        plt.yticks(np.unique(vetor_tensao))
        plt.legend()
        plt.show()


if __name__ == '__main__':
    td = TransitoriosDegrau(
        z0=75, zl=100, zs=45, vs=10, up=0.8, comprimento=10e-2
    )
    td.plot_transiente_meio_linha(ciclos=3)
