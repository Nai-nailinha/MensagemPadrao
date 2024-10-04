[Setup]
AppName=mensagemPadrao
AppVersion=1.0.0
DefaultDirName={pf}\mensagemPadrao
DefaultGroupName=mensagemPadrao
OutputBaseFilename=mensagemPadraoSetup

[Files]
; Executável do aplicativo
Source: "C:\Users\enailel\PycharmProjects\MensagemPadrao\dist\MensagemPadrao.exe"; DestDir: "{app}"; Flags: ignoreversion

; Arquivos CSV (dados) - serão colocados no diretório de dados do usuário
Source: "C:\Users\enailel\PycharmProjects\MensagemPadrao\message_templates.csv"; DestDir: "{userappdata}\mensagemPadrao_data"; Flags: ignoreversion; Check: NotExistingCSV()
Source: "C:\Users\enailel\PycharmProjects\MensagemPadrao\solucionadores.csv"; DestDir: "{userappdata}\mensagemPadrao_data"; Flags: ignoreversion; Check: NotExistingCSVS()

[Icons]
; Atalho no menu Iniciar
Name: "{group}\mensagemPadrao"; Filename: "{app}\MensagemPadrao.exe"

; Atalho na área de trabalho
Name: "{commondesktop}\mensagemPadrao"; Filename: "{app}\MensagemPadrao.exe"; Tasks: desktopicon

; Opção de criar um atalho fixo na barra de tarefas (somente Windows 10+)
; Observe que o Inno Setup não consegue fixar automaticamente na barra de tarefas,
; então apenas criamos o atalho e o usuário pode fixar manualmente.
Name: "{group}\mensagemPadrao (Fixar na Barra de Tarefas)"; Filename: "{app}\MensagemPadrao.exe"; Tasks: taskbaricon

[Tasks]
; Adicionar opção para criar atalho na área de trabalho durante a instalação
Name: "desktopicon"; Description: "Criar um atalho na área de trabalho"; GroupDescription: "Opções do Atalho"

; Adicionar opção para criar atalho fixo na barra de tarefas
Name: "taskbaricon"; Description: "Criar um atalho para fixação manual na barra de tarefas"; GroupDescription: "Opções do Atalho"

[Run]
; Executa o aplicativo após a instalação (opcional)
Filename: "{app}\MensagemPadrao.exe"; Description: "{cm:LaunchProgram,Gerador de Mensagens}"

[Code]
function NotExistingCSV(): Boolean;
begin
    Result := not FileExists(ExpandConstant('{userappdata}\mensagemPadrao_data\message_templates.csv'));
end;

function NotExistingCSVS(): Boolean;
begin
    Result := not FileExists(ExpandConstant('{userappdata}\mensagemPadrao_data\solucionadores.csv'));
end;
