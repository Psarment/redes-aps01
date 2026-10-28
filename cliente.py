import socket

HOST = "127.0.0.1"
PORTA = 5050


def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((HOST, PORTA))
    except ConnectionRefusedError:
        print(f"nao foi possivel conectar em {HOST}:{PORTA}")
        return
    leitor = cliente.makefile("r", encoding="utf-8")
    print("conectado. digite sair para encerrar")
    while True:
        comando = input("> ").strip()
        if not comando:
            continue
        if comando.lower() == "sair":
            break
        cliente.sendall((comando + "\n").encode("utf-8"))
        resposta = leitor.readline()
        if not resposta:
            print("o servidor encerrou a conexao")
            break
        print(resposta.strip())
        if comando.upper().startswith("LIST") and resposta.startswith("OK"):
            quantidade = int(resposta.split()[1])
            for _ in range(quantidade):
                print(leitor.readline().strip())
    cliente.close()


if __name__ == "__main__":
    main()
