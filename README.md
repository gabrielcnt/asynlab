# AsynLab

AsynLab é um projeto de CRM e organização de leads para captar e acompanhar interessados em páginas profissionais para psicólogos. O sistema foi pensado para centralizar contatos recebidos pela landing page e por outras fontes, permitindo registrar o interesse, manter histórico de envio e organizar o acompanhamento de potenciais clientes.

## 1. Apresentação

O projeto busca resolver a necessidade de um negócio que oferece landing pages e soluções digitais para psicólogos de organizar contatos de potenciais pacientes e clientes em um único ponto de controle. Em vez de depender apenas de mensagens ou de fontes dispersas, o sistema centraliza os dados de interessados e define uma estrutura mínima para acompanhar o status do relacionamento.

A ideia central do CRM é manter um fluxo simples de entrada de leads, validando dados essenciais (nome, e-mail, WhatsApp e origem), evitando duplicatas por e-mail e permitindo que o status do contato seja atualizado ao longo do processo de prospecção.

## 2. Funcionalidades

### Funcionalidades concluídas

- Landing page estática para apresentação da AsynLab e seus serviços.
- Formulário de contato com validação de campos no frontend.
- Backend em Django com API REST para receber leads.
- Registro de leads com os campos: nome, e-mail, WhatsApp, origem, status e datas de criação/última submissão.
- Validação de dados do formulário da API.
- Normalização do e-mail para minúsculas e remoção de espaços.
- Prevenção de duplicidade por e-mail, comparando de forma case-insensitive.
- Atualização da data de última submissão quando o mesmo lead envia novos dados.
- Padronização do WhatsApp com DDD e formato brasileiro.
- Limitação de requisições anônimas configurada com throttle do Django REST Framework.
- Administração Django padrão para gerenciamento do app.

### Funcionalidades parcialmente implementadas

- Integração entre frontend e backend ainda não está ativa: o arquivo JavaScript possui um endpoint configurável, mas o valor está vazio (`API_ENDPOINT = ""`). Portanto, o envio real do formulário não está habilitado no momento.
- A estrutura de CRM ainda é inicial: o sistema registra e organiza leads, mas não possui painel administrativo completo, autenticação de usuários para operação do CRM, filtros avançados, dashboards ou fluxo de acompanhamento completo.
- O projeto tem uma base de dados preparada para PostgreSQL, mas a automação completa de ambiente de desenvolvimento e deploy não está documentada como parte de um ambiente de produção.

### Funcionalidades planejadas

- Integração completa do formulário da landing page com a API.
- Painel interno para visualizar, filtrar, acompanhar e atualizar leads.
- Fluxos de atendimento, notas e comentários por lead.
- Evolução para um sistema mais completo de CRM e gestão de prospecção.

Essas ideias aparecem no contexto do projeto e na proposta da landing page, mas não estão implementadas como funcionalidades concluídas no código atual.

## 3. Tecnologias utilizadas

### Frontend

- HTML5
- CSS3
- JavaScript puro (vanilla JS)
- Sem framework frontend identificado no código
- Sem gerenciador de dependências (`package.json`, `vite`, `webpack`, `npm`, `pnpm`, `yarn` não foram encontrados)

### Backend

- Python
- Django 6.1.2
- Django REST Framework 3.18.3
- psycopg (driver PostgreSQL)
- python-dotenv

### Banco de dados

- PostgreSQL

### Ferramentas de desenvolvimento/testes

- Django test runner
- SQLite foi encontrado no repositório como arquivo local (`backend/db.sqlite3`), mas a configuração ativa do projeto aponta para PostgreSQL via variáveis de ambiente

## 4. Arquitetura e estrutura do projeto

A organização do repositório contém duas partes separadas:

- `frontend/`: interface pública/landing page
- `backend/`: aplicação Django responsável pela API e regras de negócio

Estrutura real do projeto:

```text
.
├── .gitignore
├── backend/
│   ├── .env
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── leads/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── migrations/
│       │   ├── 0001_initial.py
│       │   └── 0002_alter_lead_status.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── lead.py
│       ├── repositories/
│       │   ├── __init__.py
│       │   └── repository.py
│       ├── serializers/
│       │   ├── __init__.py
│       │   └── serializer.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── service.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── frontend/
│   ├── assets/
│   │   ├── icons/
│   │   └── images/
│   ├── css/
│   │   └── style.css
│   ├── index.html
│   └── js/
│       └── main.js
└── README.md
```

### Arquitetura do backend

O backend segue uma organização em camadas simples e direta, visível nos módulos do app `leads`:

- `models/lead.py`: definição do modelo `Lead` e os `TextChoices` para origem e status.
- `serializers/serializer.py`: responsável por validar e normalizar os dados da API.
- `services/service.py`: contém a regra de negócio para criar ou atualizar leads com lógica de deduplicação.
- `repositories/repository.py`: camada de acesso ao banco para consulta e criação de registros.
- `views.py`: ponto de entrada da API que valida os dados e chama o serviço.
- `urls.py`: definição da rota pública da aplicação.
- `migrations/`: histórico de alterações do banco.
- `tests.py`: testes de integração da API.

Essa estrutura é coerente com a implementação existente, mas ainda é uma versão enxuta e focada em validação de leads.

## 5. Requisitos

### Requisitos gerais

- Python 3.14 (presente no ambiente virtual do projeto, mas o repositório não contém uma versão fixada em arquivo de configuração como `.python-version` ou `pyproject.toml`)
- PostgreSQL instalado e acessível localmente
- Acesso a um banco PostgreSQL com usuário e senha configurados
- Git

### Frontend

- Navegador moderno para abrir a landing page
- Nenhuma dependência adicional de Node foi detectada

### Backend

- Ambiente virtual Python
- Dependências listadas em `backend/requirements.txt`
- Configuração de variáveis de ambiente com dados do banco PostgreSQL

## 6. Configuração e instalação

### Backend

1. Acesse a pasta do backend:

```bash
cd backend
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente em um arquivo `.env` na pasta `backend/`.

5. Prepare o PostgreSQL localmente, criando um banco e um usuário de acordo com as variáveis configuradas.

6. Execute as migrações:

```bash
python manage.py migrate
```

7. Inicie o servidor:

```bash
python manage.py runserver 0.0.0.0:8000
```

O backend ficará acessível em:

```text
http://localhost:8000/
```

### Frontend

O frontend é estático, então não há build system ou servidor específico de framework. A maneira mais simples de executá-lo é abrir o arquivo `frontend/index.html` diretamente em um navegador ou serví-lo em um servidor HTTP simples, por exemplo:

```bash
cd frontend
python -m http.server 8001
```

A página ficará disponível em:

```text
http://localhost:8001/
```

## 7. Variáveis de ambiente

O backend utiliza as seguintes variáveis de ambiente em `backend/config/settings.py`:

- `DB_NAME`: nome do banco PostgreSQL
- `DB_USER`: usuário do banco PostgreSQL
- `DB_PASSWORD`: senha do usuário do banco
- `DB_HOST`: host do banco (padrão: `localhost`)
- `DB_PORT`: porta do PostgreSQL (padrão: `5432`)

Exemplo de configuração no arquivo `.env`:

```env
DB_NAME=asynlab_db
DB_USER=asynlab_user
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

Importante: valores reais de senha, credenciais ou segredos não devem ser expostos no repositório. O projeto atual inclui um arquivo `.env` no backend, mas ele não foi usado como base para documentação pública neste README.

## 8. Banco de dados

O projeto está configurado para usar PostgreSQL no backend via Django:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST", "localhost"),
        'PORT': os.getenv("DB_PORT", "5432")
    }
}
```

### Modelo principal: `Lead`

O modelo principal do CRM é o `Lead`, com os seguintes campos:

- `name`: nome do interessado
- `email`: e-mail do interessado
- `whatsapp`: número de WhatsApp em formato padronizado
- `source`: origem do lead (`instagram`, `google`, `direct`, `other`)
- `status`: status do lead (`new`, `contacted`, `converted`, `discarded`)
- `notes`: observações opcionais
- `created_at`: data de criação
- `last_submission_at`: data da última submissão

Além disso, a aplicação define uma restrição de unicidade no campo de e-mail de forma case-insensitive:

```python
models.UniqueConstraint(Lower("email"), name="unique_lower_email")
```

Isso impede que dois e-mails equivalentes em maiúsculas/minúsculas sejam registrados como registros diferentes.

## 9. Endpoints da API

A aplicação expõe uma rota principal, configurada em `backend/leads/urls.py`:

```python
urlpatterns = [
    path("leads/", submit_lead, name="submit-lead")
]
```

### POST `/api/leads/`

- Método: `POST`
- Finalidade: registrar um novo lead ou atualizar a última submissão caso o e-mail já exista
- Autenticação: não há autenticação configurada para esta rota; a API é pública por padrão
- Payload esperado:

```json
{
  "name": "Gabriel Vieira",
  "email": "gabriel@email.com",
  "whatsapp": "21965876798",
  "source": "instagram"
}
```

Validações implementadas:

- `name` obrigatório
- `email` válido
- `whatsapp` deve ter formato brasileiro válido
- `source` deve estar entre as opções permitidas

Resposta esperada em caso de sucesso:

```json
{
  "message": "Recebemos seus dados com sucesso."
}
```

Caso os dados estejam inválidos, a API retorna erro de validação com status `400`.

### Operações adicionais

- `GET /api/leads/` retorna `405 Method Not Allowed`, porque a view foi implementada apenas com `@api_view(["POST"])`.
- `GET /api/leads/1` não é uma rota pública implementada e, em testes do app, retorna `404`.

## 10. Execução local

Para executar o sistema completo localmente:

1. Rode o backend em um terminal:

```bash
cd backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

2. Rode o frontend em outro terminal:

```bash
cd frontend
python -m http.server 8001
```

3. Acesse a landing page em:

```text
http://localhost:8001/
```

4. A API estará disponível em:

```text
http://localhost:8000/api/leads/
```

A comunicação entre as partes ainda está incompleta, porque a página usa `API_ENDPOINT = ""` e não envia os dados para a API de forma ativa.

## 11. Testes

Os testes do backend podem ser executados com:

```bash
cd backend
source venv/bin/activate
python manage.py test leads.tests
```

A aplicação possui testes de integração focados em criação de leads, validações, proteção contra duplicidade, atualização de `last_submission_at`, permissões de admin e throttle de requisições anônimas.

### Observação sobre a última execução dos testes

Na última execução da suíte leads.tests, foram identificados 12 testes, dos quais 4 falharam devido a respostas HTTP 429 (Too Many Requests) relacionadas ao mecanismo de throttling do Django REST Framework.

O comportamento indica que o limite de requisições está interferindo em alguns cenários de teste. A configuração do throttling e sua interação com os testes permanecem pendentes de revisão.

## 12. Considerações finais

O AsynLab está em fase inicial de desenvolvimento, mas já demonstra uma base útil para o contexto de CRM de leads para landing pages de psicólogos. O repositório reúne uma landing page estática com foco em apresentação de serviços e um backend Django com API REST para receber contatos, validar dados e evitar duplicidades.

O projeto está bem posicionado como um exercício de portfólio de backend em Python e Django, especialmente pela organização em camadas, uso de validações, controle de duplicidade e testes de API. O que ainda falta para evoluir de forma mais completa é a integração real entre frontend e backend, o desenvolvimento de um painel administrativo funcional e a expansão do CRM para manter um fluxo mais robusto de prospecção e acompanhamento.
