# 🔗 Encurtador de Links - API REST

API REST robusta para encurtamento, redirecionamento e rastreamento de métricas de links, construída com **Django** e **Django Ninja**.

---

## 🚀 Funcionalidades

- **Encurtamento Inteligente:** Geração automática de tokens curtos (URL-safe) de 8 caracteres ou definição de tokens personalizados.
- **Redirecionamento Automático:** Redirecionamento instantâneo via HTTP 302 registrando o IP do acesso.
- **Controle de Expiração:** Suporte a links com tempo de expiração finito (`expiration_time`).
- **Limite de Cliques Únicos:** Restrição opcional de quantidade máxima de acessos por IPs distintos (`max_uniques_cliques`).
- **Desativação de Links:** Ativação/desativação de links através do campo `active`.
- **Estatísticas de Acesso:** Métricas detalhadas de cliques totais e cliques únicos por IP.
- **Atualização Parcial Flexível:** Atualizações parciais via HTTP `PATCH` preservando tokens e dados existentes.
- **Documentação Automática:** Interface Swagger/OpenAPI interativa pronta para uso.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.11+
- **Framework Web:** Django 5+
- **API Framework:** Django Ninja (Pydantic v2)
- **Banco de Dados:** SQLite (padrão de desenvolvimento)

---

## ⚙️ Como Executar o Projeto

### 1. Clonar o Repositório e Acessar a Pasta
```bash
git clone <url-do-repositorio>
cd Encurtador_de_link
```

### 2. Criar e Ativar o Ambiente Virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as Dependências
```bash
pip install django django-ninja
```

### 4. Executar as Migrações do Banco de Dados
```bash
python manage.py migrate
```

### 5. Iniciar o Servidor de Desenvolvimento
```bash
python manage.py runserver
```

A API estará disponível em `http://127.0.0.1:8000/api/v1/` e a documentação interativa em `http://127.0.0.1:8000/api/docs`.

---

## 📌 Documentação dos Endpoints

Todos os endpoints da API estão agrupados sob o prefixo `/api/v1/`.

### 1. Criar Link Encurtado
- **Rota:** `POST /api/v1/create/`
- **Descrição:** Cria um novo link encurtado. Se o `token` não for informado, a API gera um token aleatório único de 8 caracteres.

**Corpo da Requisição (`JSON`):**
```json
{
  "redirect_link": "https://www.youtube.com/watch?v=JJPO-DjhW4s",
  "token": "meu-link-custom",
  "expiration_time": "P1D",
  "max_uniques_cliques": 100
}
```

> 💡 *Nota:* `expiration_time` aceita formato de duração ISO 8601 (ex: `"PT2H"` para 2 horas ou `"P1D"` para 1 dia).

**Respostas:**
- `200 OK`: Link criado com sucesso.
- `409 Conflict`: O token informado já está em uso por outro link.

---

### 2. Acessar / Redirecionar Link
- **Rota:** `GET /api/v1/{token}`
- **Descrição:** Valida o token, verifica se o link está ativo/não expirado/dentro do limite de cliques, registra o IP do visitante e redireciona para a URL original (`redirect_link`).

**Respostas:**
- `302 Found`: Redirecionamento HTTP para a URL destino.
- `403 Forbidden`: Limite de cliques únicos atingido.
- `410 Gone`: Link expirado ou desativado (`active=False`).
- `404 Not Found`: Token não encontrado.

---

### 3. Atualizar Link
- **Rota:** `PATCH /api/v1/{link_id}/`
- **Descrição:** Atualiza parcialmente os campos de um link existente. Apenas os campos informados no corpo da requisição são alterados; os demais permanecem inalterados.

**Corpo da Requisição (`JSON`):** *(Exemplo alterando apenas o destino e desativando o link)*
```json
{
  "redirect_link": "https://nova-url.com",
  "active": false
}
```

**Respostas:**
- `200 OK`: Link atualizado com sucesso.
- `409 Conflict`: O novo token informado já está em uso por outro link.
- `404 Not Found`: ID do link não encontrado.

---

### 4. Obter Estatísticas de Acesso
- **Rota:** `GET /api/v1/statistics/{link_id}/`
- **Descrição:** Retorna o total de cliques registrados e o número de acessos únicos por IP.

**Resposta Exemplo (`200 OK`):**
```json
{
  "link": "https://www.youtube.com/watch?v=JJPO-DjhW4s",
  "total_clicks": 15,
  "uniques_clicks": 8
}
```

---

## 🧪 Executando os Testes Automatizados

O projeto conta com suíte de testes unitários para validar a criação, expiração, atualização e lógica de serviços.

Para rodar a suíte de testes:
```bash
python manage.py test
```

---

## 📂 Estrutura do Projeto

```text
.
├── core/                   # Configurações globais do Django e roteador principal da API
│   ├── api.py              # Instância do NinjaAPI e inclusão do router
│   ├── settings.py
│   └── urls.py
├── shorter/                # Aplicação do encurtador de links
│   ├── api.py              # Definição dos endpoints REST
│   ├── models.py           # Modelos de dados (Links e Clicks)
│   ├── schemas/            # Schemas Pydantic / ModelSchema para validação
│   │   └── schemas.py
│   ├── services/           # Lógica de negócio isolada (RedirectService)
│   │   └── services.py
│   └── tests.py            # Testes unitários da aplicação
├── db.sqlite3              # Banco de dados SQLite local
├── manage.py
└── README.md
```

---

## 👨‍💻 Autor

**Benilson Benito**  
*Engenheiro de Software & Dados*

- **GitHub:** [@benilsonbenito7](https://github.com/benilsonbenito7)

