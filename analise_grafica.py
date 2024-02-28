import pandas as pd
import os
import matplotlib.pyplot as plt


#hipose é que começo com 2000 reais 
#primeira aposta 0,25 
#ordem é 0,25 0,5 1 2 5, 10 ,20 25, 50 ,100 200, 250, 500 1000

#probabilidade de vitoria é % de vermelha u % de preto (p = q, 2:1 o pagamento)

# 18/37 18/37 e 1/37

#caso hipotetico do que teria dado mais lucro jogando na roleta
apostas = [0.25,0.5,1,2,5,10,20,50,100,200,500,1000]

def Martingale(ordem_cor,cor,aposta_inicial,conta):
    global apostas
    balanco = [conta]
    multi = apostas.index(aposta_inicial)
    valores_apostados = [0]
    acertos,erros = 0,0
    for i in ordem_cor:
        valores_apostados.append(apostas[multi])
        if apostas[multi] > balanco[-1]:
            print('quebrei a banca')
        if cor == i:
            acertos += 1 
            balanco.append(conta+apostas[multi])
            multi = apostas.index(aposta_inicial)
        else:
            erros += 1 
            balanco.append(conta-apostas[multi])
            multi += 1 
        conta = balanco[-1]
    print(acertos,erros)
    print(max(valores_apostados))
    balanco = [i - balanco[0] for i in balanco]
    return balanco, valores_apostados

df = pd.read_excel('registro_cores_20-02-2024.xlsx')
ordem_cor = df.cor.to_list()

cor = "vermelho"

prim_aposta = 0.25
balanco, apostas = Martingale(ordem_cor,cor,prim_aposta,1000)
print(balanco)
x = list(range(len(balanco)))


plt.plot(x, balanco, label='Lucro Acumulado', marker='o')
plt.bar(x, apostas, label='Valor da aposta', color='orange', alpha=0.7)

plt.xlabel('Numero de apostas')
plt.ylabel('$')
plt.title(f'Cenário hipotetico apostando nas {cor}, e usando {prim_aposta} como primeira aposta')

# Adding legend
plt.legend()

# Display the chart
plt.show()
