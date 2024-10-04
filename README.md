# mensagemPadrao

**mensagemPadrao** é uma ferramenta simples para criar, personalizar e organizar mensagens padrão de forma rápida. Ideal para atendimento ao cliente, comunicação interna ou qualquer outra situação que exija mensagens rápidas e padronizadas.

## Índice
- [Recursos](#recursos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Atualizações](#atualizações)
- [Licença](#licença)

---

## Recursos

- **Templates Personalizáveis**: Crie e gerencie diferentes modelos de mensagens.
- **Campos Personalizáveis e Validação**: Adicione detalhes como nome do cliente, status, responsável... Os campos obrigatórios são validados automaticamente.
- **Atualizações Automáticas**: Verifica se há uma nova versão disponível diretamente no GitHub.
- **Gerenciamento Fácil via CSV**: Importação e exportação de templates e grupos solucionadores através de arquivos CSV.
- **Interface Amigável**: Design simples e fácil de usar, garantindo uma experiência tranquila para todos os usuários.

---

## Instalação

### Pré-requisitos
- **Python 3.x**: Certifique-se de que você tem o Python instalado em sua máquina. Você pode baixar a última versão [aqui](https://www.python.org/downloads/).
- **Bibliotecas necessárias**: As bibliotecas necessárias estão listadas no arquivo `requirements.txt`. Para instalá-las, use:
    ```bash
    pip install -r requirements.txt
    ```

### Clonando o Repositório
1. Clone o repositório do GitHub:
    ```bash
    git clone https://github.com/Nai-nailinha/mensagemPadrao.git
    ```
2. Navegue até a pasta do projeto:
    ```bash
    cd mensagemPadrao
    ```

---

## Uso

### Executando o Aplicativo
1. Certifique-se de que está na pasta do projeto.
2. Execute o aplicativo:
    ```bash
    python MensagemPadrao.py
    ```

### Funcionalidades Principais
1. **Selecione uma Mensagem**: Use o `ComboBox` para escolher um template de mensagem existente.
2. **Preencha os Campos Necessários**: Insira informações específicas (nome do cliente, status, etc.).
3. **Gere a Mensagem**: Clique no botão para gerar a mensagem completa e personalizável.
4. **Copie ou Edite**: A mensagem gerada pode ser copiada para ser usada em outros aplicativos ou editada diretamente no "mensagemPadrao".

### Gerenciamento de Templates e Grupos
- **Gerenciar Templates**: Crie, edite ou exclua templates de mensagens. Todos os templates são armazenados em um arquivo CSV (`message_templates.csv`).
- **Gerenciar Grupos**: Adicione, edite ou remova grupos solucionadores que também são gerenciados via CSV (`solucionadores.csv`).

---

## Atualizações

O "mensagemPadrao" verifica automaticamente atualizações. Caso uma nova versão esteja disponível, o aplicativo notificará o usuário.

Para verificar atualizações manualmente:
```bash
python check_for_update.py
