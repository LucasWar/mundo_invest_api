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
git clone <URL_DO_REPOSITORIO>

cd nome-do-projeto
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

Caso deseje executar apenas o PostgreSQL via Docker:

```bash
docker compose up postgres -d
```

O banco ficará disponível em:

```text
localhost:5432
```

---

# 🐳 Executando Toda a Aplicação

## Build + Inicialização

```bash
make dev
```

Este comando:

* Faz o build da aplicação
* Inicializa o PostgreSQL
* Inicializa a API FastAPI
* Ativa hot reload

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
make migration
```

## Aplicar Migration

```bash
make migrate
```

---

# 🧪 Executando os Testes

```bash
make test
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

O projeto foi totalmente containerizado utilizando Docker.

Benefícios:

* Ambiente reproduzível
* Facilidade de setup
* Isolamento da aplicação
* Padronização do ambiente

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
