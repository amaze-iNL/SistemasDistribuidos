from cliente.Interface.interface import Interface
from servidor.gestor.maquina import Maquina


def main():
    minha_maquina = Maquina()
    minha_interface = Interface(minha_maquina)

    minha_interface.execute()


if __name__ == '__main__':
    main()


