# Projeto FCCPD — Containers, Redes, Persistência, Microsserviços e API Gateway

Trabalho da segunda unidade da disciplina **Fundamentos de Computação Concorrente, Paralela e Distribuída (FCCPD)**.

Este repositório apresenta **cinco desafios progressivos**, cada um explorando conceitos essenciais para a construção de sistemas distribuídos modernos utilizando Docker e Docker Compose.
Cada desafio aprofunda um aspecto da comunicação, persistência e organização de serviços executados em ambientes isolados.


# Desafio 1 — Containers em Rede

## Objetivo

Demonstrar a comunicação direta entre dois containers utilizando uma **rede Docker customizada**.
O propósito é entender como o Docker cria redes virtuais isoladas e como os containers podem se comunicar sem expor portas ao host.

---

## Instruções de Execução

1. Acesse o diretório do desafio:

   ```bash
   cd desafio1
   ```
2. Execute o ambiente:

   ```bash
   docker compose up
   ```
3. Observar no terminal:

   * O container **cliente** faz requisições HTTP contínuas ao servidor a cada 5 segundos.
   * O container **servidor** responde através do Nginx configurado na porta 8080 interna.

Para encerrar: `Ctrl + C`.

---

## Arquitetura

Este desafio é composto por dois containers em uma rede exclusiva:

* **Servidor (Nginx):**
  Configurado via um arquivo `nginx.conf` personalizado para responder na porta 8080.
  É responsável por retornar uma resposta simples de texto confirmando o recebimento da requisição HTTP.

* **Cliente (alpine/curl):**
  Executa um loop infinito com comando shell usando `curl` para enviar requisições contínuas ao servidor.
  Usa o nome do serviço como hostname, aproveitando o sistema interno de DNS do Docker.

* **Rede Bridge Customizada:**
  Criada automaticamente pelo Docker Compose, garante isolamento e visibilidade apenas entre os containers envolvidos.

---

## Decisões Técnicas

1. **Uso de Docker Compose:**
   Permite definir infraestrutura como código, garantindo reprodutibilidade e facilidade de execução.

2. **Uso de nomes de serviços como DNS:**
   Dentro da rede Docker, cada serviço é acessível pelo nome definido no `docker-compose.yml`.
   Isso elimina a necessidade de descobrir IPs dinâmicos.

3. **Imagens Alpine:**
   Escolhidas pela leveza, baixo custo de download e inicialização rápida.

4. **Modo interativo:**
   É possível visualizar facilmente o fluxo de requisições em tempo real.

---

# Desafio 2 — Volumes e Persistência de Dados

## Objetivo

Demonstrar como persistir dados em um ambiente Docker, mesmo após a remoção de containers.
A ideia é provar que os dados pertencem ao **volume** e não ao container.

---

## Instruções de Execução

1. Acesse o diretório:

   ```bash
   cd desafio2
   ```

2. Execute:

   ```bash
   docker compose up -d
   ```

3. Acesse o container do banco:

   ```bash
   docker exec -it desafio2-db sh
   /# psql -U admin -d desafio2
   ```

   Insira a tabela e dados desejados.

4. Teste a persistência:

   ```bash
   docker compose down
   docker compose up -d
   docker exec -it desafio2-db psql -U admin -d desafio2 -c "SELECT * FROM usuarios;"
   ```

5. Container leitor (opcional):

   ```bash
   docker exec -it desafio2-leitor sh -c "PGPASSWORD=admin psql -h desafio2-db -U admin -d desafio2 -c 'SELECT * FROM usuarios;'"
   ```

---

## Arquitetura

* **PostgreSQL:** container principal com persistência configurada.
* **Volume Nomeado:** armazena os dados do banco mesmo após remoção do container.
* **Container Leitor:** demonstra comunicação via rede Docker acessando o banco pela hostname interna.
* **Rede Bridge:** isola a comunicação entre DB e leitor.

---

## Decisões Técnicas

1. **Volumes Nomeados:**
   São a abordagem recomendada pelo Docker para persistência real.
   Podem sobreviver a `docker rm` e `docker compose down`.

2. **Comprovação prática:**
   A remoção do container e depois sua recriação demonstra que os dados persistem.

3. **Isolamento:**
   A rede customizada garante que o acesso ao DB ocorre apenas por containers autorizados.

4. **Cliente PSQL com segundo container:**
   Demonstra um cenário real de uma aplicação se conectando ao banco.

---

# Desafio 3 — Orquestração com Docker Compose

## Objetivo

Criar três serviços (Web, DB e Cache) que se comunicam entre si.
Este desafio reforça a importância da orquestração, dependências entre serviços e verificação de comunicação interna.

---

## Instruções de Execução

```bash
cd desafio3
docker compose up -d
```

Para testar conectividade:

```bash
docker exec -it desafio3-web-app sh
ping cache -c 3
nc -vz db 5432
```

O `ping` confirma comunicação com o Redis,
e o `nc` (netcat) confirma que a porta do PostgreSQL está aberta.

---

## Arquitetura

* **DB:** PostgreSQL com persistência.
* **Cache:** Redis, acessado pela porta padrão 6379.
* **Aplicação Web:** BusyBox utilizada para teste da rede (executando comandos como ping e nc).
* **Rede única:** Garante comunicação interna entre os três containers.

---

## Decisões Técnicas

1. **depends_on:**
   Usado para controlar ordem de inicialização, garantindo que DB e Cache iniciem antes da aplicação.

2. **Testes práticos:**
   Comandos como `ping` e `nc` asseguram que os serviços estão acessíveis via rede Docker.

3. **Infraestrutura como código:**
   Docker Compose automatiza a criação da rede, volumes e serviços.

4. **Uso do BusyBox:**
   Simples, leve e perfeito para simulação de testes em ambientes distribuídos.

---

# Desafio 4 — Microsserviços Independentes

## Objetivo

Criar dois microsserviços independentes, onde um consome o outro via HTTP interno.
Este desafio simula uma arquitetura real baseada em microserviços.

---

## Instruções de Execução

```bash
cd desafio4
docker compose up --build -d
```

### Serviço A:

Lista de usuários mockados:

```
http://localhost:5000/api/usuarios
```

### Serviço B:

Consome A via HTTP interno:

```
http://localhost:5001/api/info-usuarios
```

---

## Arquitetura

* **Microsserviço A:** fornece usuários.
* **Microsserviço B:** consome e formata dados de A.
* **Rede:** isolada para comunicação interna.
* **Dockerfiles independentes:** garantindo isolamento real.
* **Variáveis de ambiente:** SERVICE_A_URL usada para apontar para o serviço A.

---

## Decisões Técnicas

1. **Isolamento completo:**
   Cada microsserviço tem seu próprio Dockerfile, dependências e ambiente.

2. **Comunicação HTTP:**
   O serviço B se comunica com A por meio do hostname interno definido no Compose.

3. **Flexibilidade:**
   Ao usar variável de ambiente, é possível alterar o endereço do serviço sem alterar o código.

4. **Padronização JSON:**
   Ambos os serviços retornam respostas bem estruturadas e documentadas.

---

# Desafio 5 — Microsserviços com API Gateway

## Objetivo

Criar dois microsserviços (usuários e pedidos) e um **API Gateway** centralizando o acesso externo.
O Gateway deve fornecer rotas unificadas para usuários e pedidos, servindo de fachada para o sistema.

---

## Instruções de Execução

```bash
cd desafio5
docker compose up --build -d
```

### Acesso pelo Gateway (porta 80):

* Lista de usuários:

  ```
  http://localhost/users
  ```
* Lista de pedidos:

  ```
  http://localhost/orders
  ```

Todos os acessos externos são feitos através do gateway.

---

## Arquitetura

* **Gateway (NGINX):**
  Recebe todas as requisições e encaminha via `proxy_pass` para os serviços internos.

* **Microsserviço 1 (users):**
  Expõe `/api/users` internamente na porta 5000.

* **Microsserviço 2 (orders):**
  Expõe `/api/orders` internamente na porta 5001.

* **Rede interna:**
  Os microsserviços não expõem portas externamente, apenas para o gateway.

---

## Decisões Técnicas

1. **API Gateway com NGINX:**
   Solução eficiente e amplamente adotada em sistemas distribuídos.

2. **Roteamento centralizado:**
   Simplifica o consumo dos microsserviços por clientes externos.

3. **Isolamento de microsserviços:**
   Apenas o gateway expõe portas para fora do ambiente Docker.

4. **Configuração clara:**
   O `nginx.conf` define as rotas externas e seus respectivos serviços internos, reproduzindo uma arquitetura moderna de gateway.

---

# Conclusão Geral

Os cinco desafios progridem naturalmente desde conceitos fundamentais de containers e redes até arquiteturas modernas baseadas em microsserviços e API Gateway.

Este repositório demonstra:

* Criação e comunicação entre containers
* Persistência de dados via volumes
* Orquestração com Docker Compose
* Comunicação HTTP entre microsserviços
* Centralização de acesso por gateway reverso
