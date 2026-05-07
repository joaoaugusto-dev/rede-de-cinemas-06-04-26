# 🎬 Sistema de Gestão - Rede de Cinemas

Bem-vindo à documentação do sistema de gestão da **Rede de Cinemas**. Este projeto visa centralizar e organizar as operações de diversas unidades, garantindo confiabilidade e facilidade de evolução.

---

## 📂 Documentação Principal

| Documento | Descrição | Link |
| :--- | :--- | :---: |
| **Requisitos Funcionais** | O que o sistema deve fazer. | [📄 RF.md](./docs/RF.md) |
| **Requisitos Não Funcionais** | Critérios de qualidade e restrições. | [📄 RNF.md](./docs/RNF.md) |
| **Regras de Negócio** | Regras e restrições operacionais. | [📄 RN.md](./docs/RN.md) |
| **Casos de Uso** | Lista detalhada de UCs. | [📑 UC.md](./docs/UC.md) |

---

## 📊 Modelagem do Sistema (Diagramas)

### 🗺️ Diagrama de Casos de Uso
Representação das interações entre os usuários (Administrador e Espectador) e o sistema.

![Casos de Uso](./diagrams/exports/Diagrama%20de%20Casos%20de%20Uso%20-%20Rede%20de%20Cinemas.png)

---

### 🏛️ Diagrama de Classes do Domínio
Principais entidades e relacionamentos do negócio.

![Classes do Domínio](./diagrams/exports/Diagrama%20de%20Classes%20de%20Domínio.png)

---

### 🔄 Diagramas de Atividade
Fluxos de processos principais.

#### Gerenciar Sessões
![Atividade Sessão](./diagrams/exports/Diagrama%20de%20Atividade%20-%20Gerenciar%20Sessões.png)

#### Registrar Público Diário
![Atividade Público](./diagrams/exports/Diagrama%20de%20Atividade%20-%20Registrar%20Público%20Diário.png)

---

### ⛓️ Diagramas de Sequência (Arquitetura em Camadas)
Interação entre View, Controller, Service e Repository.

#### Cadastrar Filme
![Sequência Filme](./diagrams/exports/Diagrama%20de%20Sequência%20-%20Cadastrar%20Filme.png)

#### Gerenciar Sessões
![Sequência Sessão](./diagrams/exports/Diagrama%20de%20Sequência%20-%20Gerenciar%20Sessões.png)

#### Registrar Público
![Sequência Público](./diagrams/exports/Diagrama%20de%20Sequência%20-%20Registrar%20Público.png)

---

## 🚀 Contextualização
A rede de cinemas opera em múltiplas cidades, enfrentando desafios como controle de filmes em cartaz, organização de sessões e registro diário de público. Este sistema resolve essas dores centralizando dados de elenco, diretores, gêneros e totalização de público.

---

## ✅ Implementação (UCs Resolvidos)

A implementação atual cobre os principais requisitos operacionais do sistema:

- [x] **UC 1:** [Manter Filmes](./src/views/cli_view.py#L85)
- [x] **UC 2:** [Manter Unidades](./src/views/cli_view.py#L125)
- [x] **UC 3:** [Gerenciar Sessões](./src/views/cli_view.py#L168)
- [x] **UC 4:** [Registrar Público](./src/views/cli_view.py#L239)
- [x] **UC 5:** [Gerar Relatórios](./src/views/cli_view.py#L283)
- [x] **UC 6:** [Consultar Programação](./src/views/cli_view.py#L310)
- [x] **UC 7:** [Consultar Detalhes](./src/views/cli_view.py#L358)

---

## 🛠️ Tecnologias e Arquitetura
- **Linguagem:** Python
- **Interface:** CLI Premium (Rich library)
- **Banco de Dados:** SQLite
- **Arquitetura:** MVC + Service + Repository
