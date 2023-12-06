from CasamentoGeral import CasamentoCapacitorIndutor
from CasamentoQO import CasadorQuartoOnda
from LinhasTerminadas import LTTerminadas
from ParaDist import CabosCoaxias, CaboCondGemeos
from TocoParalelo import TocoSimples
from TocoSerie import TocoSerie
from transitorios import TransitoriosDegrau

inicio = input('Qual unidade deseja solucionar o problema?\n Digite:\n "1" para unidade 1\n "2" para unidade 2\n "3" para unidade 3: ')

match inicio:
    case '1':
        assunto = input('Transitório: 1\n Parâmetros distribuidos: 2\n Linhas Terminadas: 3\n')
        match assunto:
            case '1':
                z0 = float(input("Z0: "))
                zl = float(input("Zl: "))
                zs = float(input("Zs: "))
                vs = float(input("vs: "))
                up = float(input("up (em porcentagem da luz): "))
                comp = float(input("comprimento(escrever na forma cientifica 'x'e-'n')"))
                ciclos = int(input('digite o número de ciclos desejados: '))
                transi = TransitoriosDegrau(z0=z0, zl=zl, zs=zs, vs=vs, up=up, comprimento=comp)
                referencia = input("1:fonte \n 2:meio da linha \n 3:na carga \n")
                match referencia:
                    case 1:
                        transi.plot_transiente_fonte(ciclos=ciclos)
                    case 2:
                        transi.plot_transiente_meio_linha(ciclos=ciclos)
                    case 3:
                        transi.plot_transiente_carga(ciclos=ciclos)
            case '2':
                cabo = input('coaxial: 1 \npar gemeos:2 \n')
                a = float(input('a: '))
                b = float(input('b: '))
                freq = float(input('frequencia: '))
                mu_r = float(input('permeabilidade relativa: '))
                e_r = float(input('permissividade relativa: '))
                sigma_c = float(input('sigma_c: '))
                sigma_d = float(input('sigma_d: '))
                if cabo == '1':
                    coaxial = CabosCoaxias(a=a, b=b, frequencia=freq, mu_r=mu_r, e_r=e_r, sigma_c=sigma_c, sigma_d=sigma_d)
                    coaxial.param_dist()
                elif cabo == '2':
                    gemeos = CaboCondGemeos(a=a, b=b, frequencia=freq, mu_r=mu_r, e_r=e_r, sigma_c=sigma_c, sigma_d=sigma_d)
                    gemeos.param_dist()
            case '3':
                z0 = complex(input('Z0: '))
                zl = complex(input('Zl: '))
                z_s = complex(input('Zs: '))
                gamma = complex(input('Gamma: '))
                comp = float(input('comprimento da linha (quantidade de comprimentos de onda): '))
                vss = complex(input('vss (para formas complexas, escreva na forma algebrica): '))
                z = float(input('posição na linha (em lambdas): '))

                lt = LTTerminadas(z0=z0, zl=zl, z_s=z_s, gama=gamma, comprimento=comp, vss = vss)
                lt.linha_t(z)


    case '2':
        assunto = input('Quarto de onda: 1\n Casamento com indutor/capacitor: 2\n Toco paralelo: 3\n Toco serie: 4\n')
    case '3':
        ...
    case _:
        print("Por favor, digite um valor válido")
