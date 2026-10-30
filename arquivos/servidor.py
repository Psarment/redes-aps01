import socket
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORTA = 5050

agenda = {}
proximo_id = 1
lock = threading.Lock()

def ler_data(texto):
    try:
        return datetime.strptime(texto, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        return None


def ler_hora(texto):
    try:
        return datetime.strptime(texto, "%H:%M").strftime("%H:%M")
    except ValueError:
        return None


def ler_duracao(texto):
    if texto.isdigit() and int(texto) > 0:
        return int(texto)
    return None

def adicionar(argumentos):
    global proximo_id
    principal, _, descricao = argumentos.partition("|")
    partes = principal.split(maxsplit=3)
    if len(partes) < 4:
        return ["ERRO uso: ADD <data> <hora> <duracao> <titulo> | <descricao>"]
    data = ler_data(partes[0])
    hora = ler_hora(partes[1])
    duracao = ler_duracao(partes[2])
    if data is None:
        return ["ERRO data invalida, use AAAA-MM-DD"]
    if hora is None:
        return ["ERRO hora invalida, use HH:MM"]
    if duracao is None:
        return ["ERRO duracao invalida, use minutos"]
    evento = {
        "titulo": partes[3].strip(),
        "data": data,
        "hora": hora,
        "duracao": duracao,
        "descricao": descricao.strip(),
    }
    with lock:
        id_evento = proximo_id
        agenda[id_evento] = evento
        proximo_id += 1
    return [f"OK evento {id_evento} criado"]


def formatar(id_evento, evento):
    linha = f"{id_evento} {evento['data']} {evento['hora']} {evento['duracao']}min {evento['titulo']}"
    if evento["descricao"]:
        linha += " | " + evento["descricao"]
    return linha

def pegar_hora(par):
    return par[1]["hora"]

def listar(argumentos):
    partes = argumentos.split()
    if len(partes) != 1:
        return ["ERRO uso: LIST <data>"]
    data = ler_data(partes[0])
    if data is None:
        return ["ERRO data invalida, use AAAA-MM-DD"]
    with lock:
        encontrados = []
        for i, e in agenda.items():
            if e["data"] == data:
                encontrados.append((i, e))
        encontrados.sort(key=pegar_hora)
        linhas = []
        for i, e in encontrados:
            linhas.append(formatar(i, e))
    return [f"OK {len(linhas)}"] + linhas

def atualizar(argumentos):
    partes = argumentos.split(maxsplit=2)
    if len(partes) < 3:
        return ["ERRO uso: UPDATE <id> <campo> <novo_valor>"]
    if not partes[0].isdigit():
        return ["ERRO id invalido"]
    id_evento = int(partes[0])
    campo = partes[1].lower()
    valor = partes[2].strip()
    if campo == "data":
        valor = ler_data(valor)
    elif campo == "hora":
        valor = ler_hora(valor)
    elif campo == "duracao":
        valor = ler_duracao(valor)
    elif campo != "titulo" and campo != "descricao":
        return ["ERRO campo invalido, use titulo, data, hora, duracao ou descricao"]
    if valor is None:
        return [f"ERRO valor invalido para {campo}"]
    with lock:
        if id_evento not in agenda:
            return [f"ERRO evento {id_evento} nao encontrado"]
        agenda[id_evento][campo] = valor
    return [f"OK evento {id_evento} atualizado"]


def remover(argumentos):
    partes = argumentos.split()
    if len(partes) != 1 or not partes[0].isdigit():
        return ["ERRO uso: DELETE <id>"]
    id_evento = int(partes[0])
    with lock:
        if id_evento not in agenda:
            return [f"ERRO evento {id_evento} nao encontrado"]
        del agenda[id_evento]
    return [f"OK evento {id_evento} removido"]


def processar(linha):
    comando, _, argumentos = linha.strip().partition(" ")
    comando = comando.upper()
    if comando == "ADD":
        return adicionar(argumentos)
    if comando == "LIST":
        return listar(argumentos)
    if comando == "UPDATE":
        return atualizar(argumentos)
    if comando == "DELETE":
        return remover(argumentos)
    return ["ERRO comando desconhecido"]


def atender(conexao, endereco):
    print(f"conectado: {endereco}")
    try:
        leitor = conexao.makefile("r", encoding="utf-8")
        while True:
            linha = leitor.readline()
            if not linha:
                break
            resposta = processar(linha)
            conexao.sendall(("\n".join(resposta) + "\n").encode("utf-8"))
    except (ConnectionResetError, BrokenPipeError):
        pass
    finally:
        conexao.close()
        print(f"desconectado: {endereco}")


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen()
    print(f"servidor ouvindo na porta {PORTA}")
    while True:
        conexao, endereco = servidor.accept()
        threading.Thread(target=atender, args=(conexao, endereco), daemon=True).start()


if __name__ == "__main__":
    main()