# Mundo Invest — Backend Technical Challenge

## 📌 Sobre o Projeto

Este projeto foi desenvolvido como solução para o teste técnico de Desenvolvedor Backend da Mundo Invest.

A aplicação simula um sistema interno responsável por:

* Gerenciamento de clientes
* Controle de patrimônio investido
* Processamento de webhooks
* Simulação de integração com o Pipefy via GraphQL

O sistema foi desenvolvido utilizando:

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Docker
* Pytest

Além da implementação dos fluxos solicitados, o projeto foi estruturado utilizando uma arquitetura modular orientada a domínio/feature, priorizando:

* Baixo acoplamento
* Separação de responsabilidades
* Escalabilidade
* Facilidade de manutenção
* Facilidade de testes
* Isolamento de integrações externas

---

# 🚀 Como Executar o Projeto

## 📋 Pré-requisitos

Antes de iniciar, é necessário possuir instalado:

* Docker
* Docker Compose
* Python 3.13+

---

# 📦 Clonando o Projeto

```bash
git clone https://github.com/LucasWar/mundo_invest_api.git

cd mundo_invest_api
```

---

# ⚙️ Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto utilizando o `.env.example` como base:

```bash
cp .env.example .env
```

Exemplo do `.env`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/mundoinvest

PIPEFY_PIPE_ID=123456
```

---

# 🐳 Executando Apenas o Banco de Dados

O projeto permite subir apenas o PostgreSQL de forma isolada.

Isso é útil para:

* desenvolvimento local
* execução manual da API
* testes locais sem container da aplicação

## Comando

```bash
docker compose up db -d
```

O banco ficará disponível em:

```text
localhost:5433
```

---

# 🐳 Executando Toda a Aplicação

O projeto também pode ser totalmente containerizado utilizando Docker Compose.

Neste modo:

* PostgreSQL sobe automaticamente
* API FastAPI sobe automaticamente
* as variáveis de ambiente de produção são carregadas
* toda a aplicação roda de forma isolada

## Build da Aplicação

```bash
poetry run build
```

Este comando:

* sobe o PostgreSQL
* sobe a API
* executa toda a aplicação em ambiente containerizado

---

## Executar Apenas Ambiente de Desenvolvimento

```bash
poetry run dev
```

Este comando:

* sobe apenas o PostgreSQL via Docker
* executa a API localmente
* ativa hot reload do Uvicorn
* facilita debug e desenvolvimento

---

## Executar Containers

```bash
docker compose up
```

ou:

```bash
docker compose up -d
```

---

## Build + Inicialização

```bash
docker compose up --build
```

Este comando:

* realiza o build da imagem
* sobe o PostgreSQL
* sobe a API
* aplica o ambiente containerizado completo

---

# 🌐 Acessando a API

Após subir o projeto:

## Swagger/OpenAPI

```text
http://localhost:8000/docs
```

## ReDoc

```text
http://localhost:8000/redoc
```

---

# 🧱 Executando as Migrations

## Criar Migration

```bash
alembic revision --autogenerate -m "migration_name"
```

## Aplicar Migration

```bash
alembic upgrade head
```

---

# ⚙️ Variáveis de Ambiente

O projeto utiliza dois arquivos de ambiente separados.

---

## `.env`

Responsável pelo ambiente de desenvolvimento local.

Utilizado principalmente quando:

* a API roda localmente
* apenas o banco está em Docker
* desenvolvimento sem containerização completa

---

## `.env.prod`

Responsável pelo ambiente containerizado/build.

Utilizado pelo Docker Compose para:

* inicializar PostgreSQL
* inicializar API
* configurar variáveis do ambiente containerizado

---

# 🧪 Executando os Testes

```bash
poetry run test
```

ou:

```bash
pytest
```

---

# 📬 Endpoints Principais

## Criar Cliente

### Endpoint

```http
POST /clientes
```

### Payload

```json
{
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualização cadastral",
  "valor_patrimonio": 250000
}
```

---

## Simular Webhook Pipefy

### Endpoint

```http
POST /webhooks/pipefy/card-updated
```

### Payload

```json
{
  "event_id": "evt_123",
  "card_id": "card_456",
  "cliente_email": "joao.silva@example.com",
  "timestamp": "2026-05-18T12:00:00Z"
}
```

---

# 🧠 Arquitetura do Projeto

O projeto foi estruturado utilizando uma arquitetura modular orientada a domínio/feature.

A principal ideia desta abordagem é manter cada módulo responsável por seu próprio contexto de negócio, reduzindo acoplamento e facilitando escalabilidade futura.

---

# 📁 Estrutura Geral

```text
app/
├── core/
├── domain/
├── integrations/
├── models/
├── modules/
│     ├── customer/
│     └── webhook/
└── main.py
```

---

# 🔧 Core

```text
core/
├── config.py
└── database.py
```

Responsável pelas configurações centrais da aplicação.

## config.py

Centraliza:

* Variáveis de ambiente
* Configurações globais
* URLs de conexão
* Configurações da aplicação

Vantagens:

* Evita hardcode
* Facilita troca de ambientes
* Centraliza configuração da aplicação

---

## database.py

Responsável por:

* Inicialização do SQLAlchemy
* Criação da Session
* Configuração do engine
* Controle de conexão com banco

---

# 🧩 Domain

```text
domain/
├── contracts/
└── dto/
```

Camada responsável pelas abstrações da aplicação.

---

## contracts/

Contém protocolos/interfaces utilizados pelos repositórios.

Exemplo:

```text
CustomerRepositoryProtocol
```

Objetivo:

* Aplicar inversão de dependência
* Reduzir acoplamento
* Facilitar mocking em testes
* Facilitar troca de implementação

Isso permite que os services dependam de contratos e não de implementações concretas.

---

# 🔌 Integrations

```text
integrations/
└── pipefy/
```

Responsável por encapsular integrações externas.

Neste projeto, toda comunicação relacionada ao Pipefy foi isolada nesta camada.

---

## client.py

Responsável por:

* Simular comunicação com Pipefy
* Montar payload GraphQL
* Encapsular lógica da integração

Vantagens:

* Services não conhecem GraphQL diretamente
* Redução de acoplamento
* Facilita manutenção futura
* Facilita troca de integração

---

## mutations.py

Centraliza todas as mutations GraphQL utilizadas pela integração.

Exemplo:

* createCard
* updateCardField

Vantagens:

* Organização
* Reutilização
* Facilita manutenção
* Facilita visualização da integração

---

# 🧱 Modules

A aplicação foi dividida em módulos independentes.

Cada módulo possui:

* DTOs
* Models
* Repositories
* Routes
* Services
* Dependencies

Isso torna cada contexto autocontido.

---

# 👤 Customer Module

```text
modules/customer/
├── dto/
├── models/
├── repositories/
├── routes/
├── services/
└── dependencies.py
```

Responsável pelo domínio de clientes.

---

## dto/

Contém os DTOs utilizados para:

* Requests
* Responses
* Validação de entrada

Objetivo:

* Separar contrato HTTP da entidade do banco
* Melhor organização
* Maior previsibilidade

---

## models/

Contém os models SQLAlchemy relacionados ao domínio de clientes.

Responsável pela representação das tabelas do banco.

---

## repositories/

Responsável pela camada de persistência.

Toda interação com banco foi isolada nesta camada.

Objetivo:

* Separar regra de negócio do acesso ao banco
* Facilitar manutenção
* Facilitar testes
* Permitir troca futura de banco/ORM

---

## services/

Responsável pelas regras de negócio.

Exemplos:

* Validação de email duplicado
* Criação de cliente
* Orquestração da integração com Pipefy

Os services não possuem responsabilidade de:

* acesso HTTP
* acesso direto ao banco
* GraphQL

Isso reduz acoplamento e melhora organização.

---

## routes/

Responsável apenas pela camada HTTP.

Funções:

* Receber requests
* Validar entrada
* Chamar services
* Retornar responses

Toda regra de negócio foi isolada nos services.

---

## dependencies.py

Responsável pela injeção de dependências.

Exemplos:

* Instanciar repositories
* Instanciar services
* Injetar integrações externas

A utilização de Dependency Injection traz:

* Baixo acoplamento
* Facilidade de testes
* Melhor organização
* Facilidade de substituição de implementações

---

# 🔄 Webhook Module

```text
modules/webhook/
├── dto/
├── models/
├── repositories/
├── routes/
├── services/
└── dependencies.py
```

Responsável pelo processamento de webhooks do Pipefy.

---

## Responsabilidades principais

* Processamento de eventos
* Controle de idempotência
* Atualização de status
* Definição de prioridade
* Comunicação com integração Pipefy

---

## Regra de Prioridade

O módulo aplica a seguinte regra:

### Patrimônio >= 200.000

```text
prioridade_alta
```

### Patrimônio < 200.000

```text
prioridade_normal
```

---

## Idempotência

O sistema possui controle de eventos processados.

Objetivo:

* Evitar processamento duplicado
* Garantir consistência
* Evitar efeitos colaterais

Cada `event_id` é salvo após processamento.

Caso um evento já exista:

* o processamento é interrompido
* evitando duplicidade

---

# 🧪 Estratégia de Testes

Os testes foram divididos entre:

## Testes Unitários

Responsáveis por validar:

* regras de negócio
* prioridade
* idempotência
* services

---

## Testes de Integração

Responsáveis por validar:

* rotas HTTP
* requests/responses
* integração entre camadas

---

# ✅ Cenários Testados

## Criação de Cliente

Valida:

* payload válido
* persistência no banco
* status inicial correto

---

## Processamento de Webhook

Valida:

* aplicação correta da prioridade
* atualização do cliente
* alteração de status

---

## Idempotência

Valida:

* bloqueio de eventos duplicados
* não reprocessamento de event_id

---

# 🐳 Docker

O projeto foi preparado para suportar dois fluxos distintos de execução.

---

## 1. Ambiente de Desenvolvimento

Neste modo:

* apenas o PostgreSQL roda em container
* a API roda localmente
* hot reload permanece ativo
* facilita desenvolvimento e debug

Comando:

```bash
poetry run dev
```

Fluxo executado:

```text
Docker Compose → sobe PostgreSQL
↓
Uvicorn local → inicia FastAPI com --reload
```

---

## 2. Ambiente Containerizado/Build

Neste modo:

* PostgreSQL roda em container
* API FastAPI roda em container
* ambiente totalmente isolado
* simula ambiente próximo de produção

Comando:

```bash
poetry run build
```

---

## Scripts Poetry

Os comandos principais do projeto foram centralizados utilizando Poetry.

Scripts disponíveis:

### Desenvolvimento

```bash
poetry run dev
```

### Testes

```bash
poetry run test
```

### Build Containerizado

```bash
poetry run build
```

A utilização do Poetry permitiu:

* padronização dos comandos
* simplificação do setup
* melhor experiência de desenvolvimento
* centralização da execução do projeto

---

## Docker Compose

O `docker-compose.yml` foi responsável por:

* orquestrar os containers
* controlar dependências entre serviços
* configurar healthcheck do banco
* centralizar variáveis de ambiente
* persistir os dados do PostgreSQL via volume

---

## Healthcheck

Foi implementado healthcheck no PostgreSQL para garantir que a API só seja iniciada após o banco estar disponível.

Isso reduz falhas de inicialização e melhora confiabilidade do ambiente.

---

## Variáveis de Ambiente Separadas

A separação entre `.env` e `.env.prod` foi utilizada para isolar:

* ambiente local de desenvolvimento
* ambiente containerizado/build

Essa abordagem facilita:

* manutenção
* configuração futura de ambientes
* deploy
* escalabilidade

---

# 📈 Escalabilidade da Arquitetura

A arquitetura escolhida facilita crescimento futuro da aplicação.

Exemplos:

* Adição de novos módulos
* Novas integrações externas
* Novas regras de negócio
* Novos tipos de webhook
* Escalabilidade horizontal

O desacoplamento entre:

* HTTP
* regras de negócio
* persistência
* integrações externas

permite evolução do projeto sem alto impacto entre módulos.

---

# ☁️ Possível Evolução para AWS

Em ambiente produtivo, esta aplicação poderia evoluir para:

* API Gateway
* AWS Lambda
* RDS PostgreSQL
* SQS para processamento assíncrono de webhooks
* CloudWatch para observabilidade

O processamento de webhooks poderia ser desacoplado utilizando filas, aumentando resiliência e escalabilidade.

---

# 👨‍💻 Considerações Finais

Este projeto foi desenvolvido priorizando:

* organização
* modularidade
* desacoplamento
* boas práticas backend
* facilidade de manutenção
* escalabilidade

Mesmo sendo um projeto relativamente pequeno, a estrutura foi pensada para suportar crescimento futuro de maneira sustentável.
