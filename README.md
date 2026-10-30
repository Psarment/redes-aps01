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
```

| Arquivo | O que faz |
|---------|-----------|
| `README.md` | explica o projeto, como rodar, os comandos e as decisões que tomamos |
| `arquivos/servidor.py` | servidor TCP que guarda a agenda na memória e atende cada cliente em uma thread |
| `arquivos/cliente.py` | cliente de terminal: conecta no servidor, envia os comandos e mostra as respostas |

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

A comunicação é toda em texto em cima de uma conexão TCP. O cliente conecta uma vez e manda quantos comandos quiser pela mesma conexão, que só fecha quando ele digita `sair` ou quando o servidor cai.

- Cada comando é uma linha.
- O servidor responde cada comando na ordem em que chegou, e a primeira linha da resposta sempre começa com `OK` ou `ERRO`.
- ADD, UPDATE e DELETE respondem com uma linha só.
- O LIST é o único que responde com várias linhas: a primeira é `OK <n>` e depois vêm exatamente `n` linhas, uma por evento.

Como o TCP é um fluxo de bytes e não separa as mensagens sozinho, a gente usou o `\n` para saber onde termina cada comando e cada resposta. No caso do LIST, o número que vem depois do `OK` serve para o cliente saber quantas linhas ainda faltam ler antes de mostrar o `>` de novo. Sem isso o cliente não teria como saber se a lista acabou.

Formato de cada evento na resposta do LIST:

```
<id> <data> <hora> <duracao>min <titulo> | <descricao>
```

A parte do `| <descricao>` só aparece se o evento tiver descrição.

## Decisões de projeto

**Formato do ADD.** O enunciado sugere `ADD <data> <hora> <titulo>`, mas o evento também precisa ter duração e uma descrição opcional, então o comando ficou assim:

```
ADD <data> <hora> <duracao> <titulo> | <descricao>
```

- Data, hora e duração vêm primeiro porque não têm espaço no meio, então dá para separar pelos espaços sem confusão.
- O título vem por último antes do `|` para poder ter espaços (`Reuniao do grupo`). O servidor separa só os 3 primeiros campos e o que sobrar é o título.
- A descrição também pode ter espaços, então precisava de um separador diferente do espaço. Escolhemos o `|`. Se não tiver `|`, o evento fica sem descrição.

**Formato do UPDATE.** O enunciado sugere `UPDATE <id> <novo_valor>`, mas só com isso o servidor não sabe qual campo trocar (o `15:00` é uma hora, mas o `60` pode ser a duração ou o título). Por isso adicionamos o nome do campo:

```
UPDATE <id> <campo> <novo_valor>
```

Cada UPDATE muda um campo só. O novo valor passa pela mesma validação do ADD, então não dá para colocar uma data inválida editando o evento. Se o campo não existir, o servidor responde com a lista dos campos válidos.

**Data e hora.** Usamos `AAAA-MM-DD` e `HH:MM` (24h). O servidor converte com o `datetime`, então datas que não existem, como `2026-02-30`, já dão erro. Ele também guarda sempre no mesmo formato (`9:30` vira `09:30`), e por isso dá para ordenar o LIST comparando a hora como texto.

**LIST por dia.** O LIST pede a data porque o enunciado usa `LIST <data>` e porque, com muitos eventos, listar a agenda inteira ia ficar confuso. A resposta vem ordenada pela hora.

**Ids.** Cada evento ganha um id que é só um contador que começa em 1. Quando um evento é apagado, o id dele não é reaproveitado. Assim, se um cliente apagar o evento 2 e outro criar um evento logo depois, o novo vai ser o 4 e não o 2. Isso evita que alguém dê UPDATE ou DELETE no evento errado achando que é o antigo.

**Conflito de horário.** O servidor deixa criar dois eventos no mesmo horário. Como a agenda é compartilhada por várias pessoas, não faz sentido bloquear um compromisso só porque outra pessoa marcou algo na mesma hora.

**Erros não derrubam a conexão.** Qualquer comando errado recebe uma linha `ERRO ...` explicando o problema, e o cliente pode continuar mandando comandos.

**Agenda só na memória.** Como pede o enunciado, os eventos ficam em um dicionário dentro do servidor. Se o servidor for fechado, a agenda é perdida.

## Concorrência e integridade dos dados

O servidor cria uma thread para cada cliente que conecta, então vários clientes podem estar mexendo na agenda ao mesmo tempo. Todas as threads usam o mesmo dicionário `agenda` e o mesmo contador `proximo_id`.

Para não dar problema, usamos um `threading.Lock` único:

- **ADD**: ler o `proximo_id`, salvar o evento e somar 1 no contador acontece dentro do lock. Sem isso, dois clientes que dessem ADD ao mesmo tempo podiam ler o mesmo valor do contador e ganhar o mesmo id, e um evento ia sobrescrever o outro.
- **UPDATE e DELETE**: conferir se o id existe e alterar ou apagar o evento é feito dentro do lock. Assim não acontece de um cliente checar que o evento existe, outro apagar ele, e o primeiro tentar alterar algo que já sumiu.
- **LIST**: a busca e a montagem das linhas também ficam dentro do lock, para não ler um evento no meio de uma alteração.

A validação dos dados (data, hora, duração) é feita antes de pegar o lock, porque não mexe na agenda. Assim o lock fica preso o menor tempo possível e um cliente não segura os outros enquanto o servidor confere o que ele digitou.

## Exemplo

Sessão real com o servidor rodando e um cliente conectado:

```
> ADD 2026-11-10 14:00 60 Reuniao do grupo | revisar o codigo
OK evento 1 criado
> ADD 2026-11-10 09:30 30 Aula de SD
OK evento 2 criado
> ADD 2026-11-11 08:00 120 Prova de redes
OK evento 3 criado
> LIST 2026-11-10
OK 2
2 2026-11-10 09:30 30min Aula de SD
1 2026-11-10 14:00 60min Reuniao do grupo | revisar o codigo
> UPDATE 1 hora 16:00
OK evento 1 atualizado
> UPDATE 2 descricao levar o notebook
OK evento 2 atualizado
> UPDATE 1 duracao abc
ERRO valor invalido para duracao
> LIST 2026-11-10
OK 2
2 2026-11-10 09:30 30min Aula de SD | levar o notebook
1 2026-11-10 16:00 60min Reuniao do grupo | revisar o codigo
> DELETE 2
OK evento 2 removido
> DELETE 2
ERRO evento 2 nao encontrado
> UPDATE 3 local CIn
ERRO campo invalido, use titulo, data, hora, duracao ou descricao
> list 2026-11-11
OK 1
3 2026-11-11 08:00 120min Prova de redes
> sair
```

Depois disso, um segundo cliente que conectar já vê a agenda com as alterações do primeiro:

```
> LIST 2026-11-10
OK 1
1 2026-11-10 16:00 60min Reuniao do grupo | revisar o codigo
```

