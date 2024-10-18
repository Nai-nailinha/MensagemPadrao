# MensagemPadrao

MensagemPadrao é um aplicativo que permite gerar e personalizar mensagens a partir de templates. O usuário pode editar, criar ou excluir templates e grupos de solucionadores conforme necessário.

## Sumário
- [Descrição](#descrição)
- [Instalação](#instalação)
- [Uso](#uso)
- [Funcionalidades](#funcionalidades)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

## Descrição
O MensagemPadrao foi desenvolvido para facilitar a criação de mensagens padronizadas que podem ser personalizadas com dados variáveis, como nome do cliente, status do chamado, grupo de solucionadores e outras informações relevantes. O aplicativo permite a gestão completa de templates e grupos, tornando a comunicação rápida e eficiente.

## Instalação

1. **Baixe ou clone o repositório.**
    ```bash
    git clone https://github.com/Nai-nailinha/MensagemPadrao.git
    ```

2. **Instale as dependências.**
    - Certifique-se de que você tem o Python 3.x instalado e crie um ambiente virtual.
    ```bash
    python -m venv venv
    ```

    - Ative o ambiente virtual:
        - No Windows:
          ```bash
          venv\Scripts\activate
          ```
        - No Linux/macOS:
          ```bash
          source venv/bin/activate
          ```

    - Instale as dependências necessárias:
      ```bash
      pip install -r requirements.txt
      ```

3. **Configure os arquivos CSV.**
    - O aplicativo cria automaticamente dois arquivos CSV para armazenar templates de mensagens e grupos de solucionadores. Eles são armazenados no diretório do usuário:
        - `message_templates.csv`: Templates de mensagens.
        - `solucionadores.csv`: Lista de grupos de solucionadores.

## Uso
1. **Execute o aplicativo.**
    - Acesse o diretório do projeto e execute o script principal:
      ```bash
      python MensagemPadrao.py
      ```

2. **Gerencie templates e grupos.**
    - Use as opções de menu para adicionar, editar ou excluir templates de mensagens e grupos de solucionadores.

3. **Personalize e gere mensagens.**
    - Escolha um template, preencha as informações variáveis (nome do cliente, status, etc.), e gere a mensagem para copiá-la ou utilizá-la conforme necessário.

## Funcionalidades
- **Gerenciamento de Templates**: Criação, edição e exclusão de templates de mensagens, com placeholders para personalização dinâmica.
- **Gerenciamento de Grupos**: Adição, edição e remoção de grupos de solucionadores.
- **Atualizações Automáticas**: Verificação automática de novas versões do aplicativo com opção de atualização.

## Estrutura do Projeto
O projeto segue uma organização modular para facilitar a manutenção e evolução do código:
- `file_handler.py`: Gerencia a leitura, gravação e cópia de arquivos CSV de templates e grupos.
- `MensagemPadrao.py`: Script principal para execução do aplicativo.
- `template_manager.py`: Gerencia a interface de criação, edição e exclusão de templates e grupos.

## Releases
- As versões do aplicativo são publicadas na seção de *Releases* no GitHub. Para baixar a última versão, acesse a página de [Releases](https://github.com/Nai-nailinha/MensagemPadrao/releases).
- Ao iniciar o aplicativo, ele verifica automaticamente se há uma nova versão disponível. Caso uma nova versão seja encontrada, o usuário pode escolher entre atualizar ou continuar usando a versão atual.

## Contribuindo
Atualmente, contribuições externas não são aceitas. Este projeto é mantido por um único desenvolvedor.

## Licença
Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para mais informações.
 