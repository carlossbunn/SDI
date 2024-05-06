# Sistema de Envio de Tarefas

Este projeto consiste em um sistema de escalonamento de tarefas implementado em Python, utilizando o RabbitMQ como broker de mensagens. Com atualização contínua dos gráficos de consumo do servidor.

## Pré-requisitos

- Python 3.x
- RabbitMQ

## Uso

1. Certifique-se de que o RabbitMQ está instalado e em execução localmente.

2. Execute o script principal `main.py`:

```bash
python main.py
```

3. Acompanhe a geração de tarefas pelos clientes, o processamento pelos servidores e a atualização dos gráficos de consumo do servidor.

4. Ajuste as variáveis `NUMBER_OF_SERVERS`, `NUMBER_OF_TASKS` e `NUMBER_OF_CLIENTS` no script para controlar o número de servidores, tarefas e clientes utilizados nos testes.

## Estrutura do Projeto

- `Main.py`: Script principal para iniciar e testar o sistema.
- `Server.py`: Implementação da classe Server para processar tarefas.
- `Client.py`: Implementação da classe Client para enviar tarefas.
- `Graph.py`: Implementação da classe Graph para visualizar dados.
