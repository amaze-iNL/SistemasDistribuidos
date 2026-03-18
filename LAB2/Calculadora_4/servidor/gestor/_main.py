from servidor.gestor.maquina import Maquina

def main():
    print("A iniciar o servidor...")
    minha_maquina = Maquina()
    minha_maquina.ligar_server()

if __name__ == '__main__':
    main()
