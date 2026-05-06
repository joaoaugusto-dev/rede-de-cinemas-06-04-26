# ⚖️ Regras de Negócio (RN)

As regras de negócio definem as diretrizes e restrições que regem os processos operacionais da rede de cinemas.

---

### 🕒 Gestão de Sessões
- **RN01 (Sobreposição):** Não é permitido o cadastro de duas sessões no mesmo horário para a mesma sala de um cinema.
- **RN02 (Intervalo):** Deve haver um intervalo mínimo de **20 minutos** entre o término de uma sessão e o início da próxima na mesma sala (destinado à limpeza e organização).
- **RN03 (Duração):** O horário de término de uma sessão deve ser calculado automaticamente com base na duração do filme + tempo de trailers (estimado em 10 minutos).

### 👥 Registro de Público
- **RN04 (Limite de Capacidade):** O público registrado em uma sessão não pode exceder a capacidade máxima da sala onde ela ocorre.
- **RN05 (Prazo de Registro):** O registro de público de uma sessão deve ser realizado obrigatoriamente no mesmo dia da exibição.

### 🎥 Filmes e Unidades
- **RN06** (Filmes em Cartaz): Somente filmes marcados como "Em Cartaz" podem ser vinculados a novas sessões.

### 🔐 Segurança e Acesso
- **RN07** (Acesso Restrito): Funcionalidades de gestão (filmes, cinemas, sessões e relatórios) são exclusivas para usuários com perfil de Administrador/Funcionário.
- **RN08** (Senha Forte): As senhas dos usuários devem conter no mínimo 8 caracteres, incluindo letras e números.

---