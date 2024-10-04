[Setup]
AppName=mensagemPadrao
AppVersion=1.0.0
DefaultDirName={pf}\mensagemPadrao
DefaultGroupName=mensagemPadrao
OutputBaseFilename=mensagemPadraoSetup

[Files]
; Execut�vel do aplicativo
Source: "C:\Users\enailel\PycharmProjects\MensagemPadrao\dist\MensagemPadrao.exe"; DestDir: "{app}"; Flags: ignoreversion

; Arquivos CSV (dados) - ser�o colocados no diret�rio de dados do usu�rio
Source: "C:\Users\enailel\PycharmProjects\MensagemPadrao\message_templates.csv"; DestDir: "{userappdata}\mensagemPadrao_data"; Flags: ignoreversion; Check: NotExistingCSV()
Source: "C:\Users\enailel\PycharmProjects\MensagemPadrao\solucionadores.csv"; DestDir: "{userappdata}\mensagemPadrao_data"; Flags: ignoreversion; Check: NotExistingCSVS()

[Icons]
; Atalho no menu Iniciar
Name: "{group}\mensagemPadrao"; Filename: "{app}\MensagemPadrao.exe"

; Atalho na �rea de trabalho
Name: "{commondesktop}\mensagemPadrao"; Filename: "{app}\MensagemPadrao.exe"; Tasks: desktopicon

; Op��o de criar um atalho fixo na barra de tarefas (somente Windows 10+)
; Observe que o Inno Setup n�o consegue fixar automaticamente na barra de tarefas,
; ent�o apenas criamos o atalho e o usu�rio pode fixar manualmente.
Name: "{group}\mensagemPadrao (Fixar na Barra de Tarefas)"; Filename: "{app}\MensagemPadrao.exe"; Tasks: taskbaricon

[Tasks]
; Adicionar op��o para criar atalho na �rea de trabalho durante a instala��o
Name: "desktopicon"; Description: "Criar um atalho na �rea de trabalho"; GroupDescription: "Op��es do Atalho"

; Adicionar op��o para criar atalho fixo na barra de tarefas
Name: "taskbaricon"; Description: "Criar um atalho para fixa��o manual na barra de tarefas"; GroupDescription: "Op��es do Atalho"

[Run]
; Executa o aplicativo ap�s a instala��o (opcional)
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
