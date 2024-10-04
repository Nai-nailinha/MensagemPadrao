[Setup]
AppName=mensagemPadrao
AppVersion=1.0.0
DefaultDirName={pf}\mensagemPadrao
DefaultGroupName=mensagemPadrao
OutputBaseFilename=mensagemPadraoSetup

[Files]
; Execut�vel do aplicativo
Source: "dist\MensagemPadrao.exe"; DestDir: "{app}"; Flags: ignoreversion

; Arquivos CSV (dados) - ser�o colocados no diret�rio de dados do usu�rio
Source: "message_templates.csv"; DestDir: "{userappdata}\mensagemPadrao_data"; Flags: ignoreversion; Check: NotExistingCSV()
Source: "solucionadores.csv"; DestDir: "{userappdata}\mensagemPadrao_data"; Flags: ignoreversion; Check: NotExistingCSV()

[Run]
; Executa o aplicativo ap�s a instala��o (opcional)
Filename: "{app}\MensagemPadrao.exe"; Description: "{cm:LaunchProgram,Gerador de Mensagens}"

[Code]
function NotExistingCSV(): Boolean;
begin
    Result := not FileExists(ExpandConstant('{userappdata}\mensagemPadrao_data\message_templates.csv'));
end;
