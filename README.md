# Atividade Redes 01 - Grupo 02 (Agenda)

## Equipe 02
Trabalho da disciplina de Sistemas Distribuídos (Equipe 02).

A ideia é ter um servidor que guarda uma agenda de compromissos na memória e vários clientes conectados ao mesmo tempo, cada um podendo adicionar, listar, atualizar e remover eventos. A comunicação é feita com socket TCP, e a conexão fica aberta até o cliente sair.

**Integrantes:**

- Daniel Acioly
- Pedro Sarmento
- Luís Felipe Londres 
- Lucas Cabral Matheus Santos
- Matheus Santos
- Pablo Henrique

## Requisitos

Só o Python 3\. Não usamos nenhuma biblioteca externa, então não precisa de `pip install`.

Para ver se já está instalado:

```
python --version
```

No Linux e no Mac normalmente o comando é `python3` em vez de `python`.

## Estrutura do repositório

```
aps01/
├── README.md
└── arquivos/
    ├── servidor.py
    ├── cliente.py
    └── teste_concorrencia.py
```

| Arquivo | O que faz |
|---------|-----------|
| `README.md` | explica o projeto, como rodar, os comandos e as decisões que tomamos |
| `arquivos/servidor.py` | servidor TCP que guarda a agenda na memória e atende cada cliente em uma thread |
| `arquivos/cliente.py` | cliente de terminal: conecta no servidor, envia os comandos e mostra as respostas |
| `arquivos/teste_concorrencia.py` | abre vários clientes ao mesmo tempo para conferir se os ids não se repetem |

## Como rodar

Os arquivos ficam dentro da pasta `arquivos`:

```
arquivos/
  servidor.py
  cliente.py
```

**1\. Baixar o projeto**

```
git clone <link do repositório>
cd aps01/arquivos
```

**2\. Subir o servidor**

Em um terminal:

```
python servidor.py
```

Se der certo, aparece `servidor ouvindo na porta 5050`. Deixe esse terminal aberto. Cada cliente que conectar ou sair vai aparecer nele.

**3\. Abrir o cliente**

Em outro terminal, na mesma pasta:

```
python cliente.py
```

Vai aparecer `conectado. digite sair para encerrar`, e aí é só digitar os comandos da próxima seção.

Para testar vários usuários ao mesmo tempo, abra mais terminais e rode `python cliente.py` em cada um. Todos usam a mesma agenda. Então, se um cliente adicionar um evento, o outro já vê o evento quando der `LIST`.

**4\. Encerrar**

- Cliente: digite `sair`.  
- Servidor: `Ctrl + C` no terminal dele. No Windows às vezes o `Ctrl + C` só funciona depois que algum cliente conecta ou sai. Se travar, é só fechar o terminal.

### Rodando em computadores diferentes

Por padrão o cliente conecta em `127.0.0.1`, ou seja, na própria máquina. Para conectar no servidor rodando em outro computador da mesma rede:

1. Descubra o IP da máquina do servidor (`ipconfig` no Windows, `ip a` no Linux ou `ifconfig` no Mac).  
2. No `cliente.py`, troque a linha `HOST = "127.0.0.1"` pelo IP do servidor.  
3. Se mesmo assim não conectar, provavelmente é o firewall bloqueando a porta 5050\.

### Problemas que tivemos

- **`nao foi possivel conectar em 127.0.0.1:5050`**: o servidor não está rodando, ou foi aberto depois do cliente. Suba o servidor primeiro.  
- **`Address already in use`**: já tem um servidor rodando em outro terminal. Feche o outro antes.  
- **Porta 5000 no Mac**: no começo usamos a 5000, mas no Mac ela já é usada pelo AirPlay. Por isso trocamos para a 5050\.

## Comandos

Os comandos podem ser digitados em maiúsculo ou minúsculo. As datas usam o formato `AAAA-MM-DD`, as horas `HH:MM` e a duração é em minutos.

**ADD**: adiciona um compromisso. A descrição é opcional e vem depois do `|`.

```
ADD <data> <hora> <duracao> <titulo> | <descricao>

ADD 2026-11-10 14:00 60 Reuniao do grupo | revisar o codigo
ADD 2026-11-10 09:30 30 Aula de SD
```

Resposta: `OK evento 1 criado`. O número é o id do evento, que é usado no UPDATE e no DELETE.

**LIST**: lista os compromissos de um dia, ordenados pela hora. A data é obrigatória.

```
LIST 2026-11-10
```

Resposta: primeiro vem `OK` com a quantidade de eventos e depois um evento por linha:

```
OK 2
2 2026-11-10 09:30 30min Aula de SD
1 2026-11-10 14:00 60min Reuniao do grupo | revisar o codigo
```

**UPDATE**: altera um campo de um compromisso. Os campos são `titulo`, `data`, `hora`, `duracao` e `descricao`.

```
UPDATE <id> <campo> <novo_valor>

UPDATE 1 hora 15:00
UPDATE 1 titulo Reuniao final do grupo
```

Resposta: `OK evento 1 atualizado`

**DELETE**: remove um compromisso pelo id.

```
DELETE 2
```

Resposta: `OK evento 2 removido`

**sair**: fecha o cliente. Esse comando não vai para o servidor, é tratado no próprio `cliente.py`.

### Quando dá erro

Se algo estiver errado, o servidor responde com uma linha começando com `ERRO`, e a conexão continua aberta normalmente. Alguns exemplos:

```
> LIST
ERRO uso: LIST <data>
> ADD 10/11/2026 14:00 60 Teste
ERRO data invalida, use AAAA-MM-DD
> DELETE 99
ERRO evento 99 nao encontrado
> ABC
ERRO comando desconhecido
```

## Protocolo

## Decisões de projeto

## Concorrência e integridade dos dados

## Exemplo

## Testes
