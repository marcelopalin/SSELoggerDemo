import time
import os


def localize_a_lista_e_nao_faca_nada():
    for valor in [1,2,3,4,5,100]:
        yield valor

def consumir_lista():
    # lst = [1,2,3,4,5,100]
    # for it in localize_a_lista_e_nao_faca_nada():
    #     print(it)

    lst = localize_a_lista_e_nao_faca_nada()
    print(next(lst))
    print(next(lst))

if __name__ == '__main__':
    consumir_lista()
