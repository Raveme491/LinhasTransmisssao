import numpy as np

# Número para formatação em notação científica com expoente múltiplo de 3
numero = 12345.6789

# Calcule o expoente que é múltiplo de 3
expoente = 9  # Arredonda para baixo

# Formate o número em notação científica com expoente múltiplo de 3
numero_formatado = '{:.2e}'.format(
    numero / 10**expoente
)  # 3 casas decimais no coeficiente

# Imprima o número formatado
print(numero_formatado)
