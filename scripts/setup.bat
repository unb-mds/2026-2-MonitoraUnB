@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul

:: Garante que o script seja executado a partir da raiz do repositório (sobe 1 nível)
cd /d "%~dp0\.."

call :main
exit /b %ERRORLEVEL%

:: ========================================================
:: FUNÇÕES DO SISTEMA (Correspondentes ao setup.sh)
:: ========================================================

:cabecalho
cls
echo.
echo  __  __             _ _
echo ^|  \/  ^| ___  _ __ (_) ^|_ ___  _ __ __ _
echo ^| ^|\/^| ^|/ _ \^| '_ \^| ^| __/ _ \^| '__/ _` ^|
echo ^| ^|  ^| ^| (_) ^| ^| ^| ^| ^| ^|^| (_) ^| ^| ^| (_^| ^|
echo ^|_^|  ^|_^|\___/^|_^| ^|_^|_^|\__\___/^|_^|  \__,_^|
echo.
echo  _   _       ____
echo ^| ^| ^| ^|_ __ ^| __ )
echo ^| ^| ^| ^| '_ \^|  _ \
echo ^| ^|_^| ^| ^| ^| ^|_) ^|
echo  \___/^|_^| ^|_^|____/
echo.
echo ──────────────────────────────────────────
echo   Sistema de Gerenciamento de Monitorias
echo   Universidade de Brasília
echo   MDS 2026.2 ^| Equipe G11
echo ──────────────────────────────────────────
echo.
echo   CONFIGURAÇÃO INICIAL DO SISTEMA
echo.
goto :eof

:sucesso
echo [OK] %~1
goto :eof

:erro
echo [ERRO] %~1 >&2
pause
exit /b 1

:preparar_env
if not exist .env (
    if exist .env.example (
        copy /y .env.example .env >nul
        call :sucesso "Arquivo .env criado."
    ) else (
        call :erro "Arquivo .env.example nao encontrado."
    )
)
goto :eof

:atualizar_env
set "CHAVE=%~1"
set "VALOR=%~2"
powershell -NoProfile -Command "$k='%CHAVE%'; $v='%VALOR%'; $f='.env'; if (Test-Path $f) { $c = Get-Content $f -Raw; if ($c -match ('(?m)^' + [regex]::Escape($k) + '=')) { $c = [regex]::Replace($c, '(?m)^' + [regex]::Escape($k) + '=.*', ($k + '=' + $v)) } else { $c += [Environment]::NewLine + $k + '=' + $v }; [IO.File]::WriteAllText($f, $c) }"
goto :eof

:instalar_dependencias
echo.
echo Preparando ambiente Python...
echo.

where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    call :erro "Python nao esta instalado no Windows ou nao esta no PATH."
)

if not exist .venv\Scripts\python.exe (
    python -m venv .venv
    if %ERRORLEVEL% neq 0 (
        call :erro "Falha ao criar o ambiente virtual .venv."
    )
    call :sucesso "Ambiente virtual criado."
)

.venv\Scripts\python.exe -c "import bcrypt" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Instalando dependencias do setup...
    .venv\Scripts\python.exe -m pip install --disable-pip-version-check --quiet -r backend/requirements/setup.txt
    if %ERRORLEVEL% neq 0 (
        call :erro "Falha ao instalar dependencias do setup."
    )
    call :sucesso "Dependencias instaladas."
) else (
    call :sucesso "Dependencias ja instaladas."
)
goto :eof

:configurar_professor
set /p "USUARIO=Usuario do professor [professor]: "
if "%USUARIO%"=="" set "USUARIO=professor"

:: Le a senha oculta e confirma usando PowerShell nativo
for /f "delims=" %%p in ('powershell -NoProfile -Command "$s1 = Read-Host 'Senha do professor' -AsSecureString; $b1 = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($s1)); $s2 = Read-Host 'Confirme a senha' -AsSecureString; $b2 = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($s2)); if ($b1 -ne $b2) { Write-Output 'ERRO_SENHAS_DIFERENTES'; exit }; if ([string]::IsNullOrWhiteSpace($b1)) { Write-Output 'ERRO_SENHA_VAZIA'; exit }; Write-Output $b1"') do (
    set "SENHA_PROFESSOR=%%p"
)

if "%SENHA_PROFESSOR%"=="ERRO_SENHAS_DIFERENTES" (
    call :erro "As senhas nao coincidem."
)
if "%SENHA_PROFESSOR%"=="ERRO_SENHA_VAZIA" (
    call :erro "A senha nao pode ser vazia."
)

:: Gera o hash bcrypt usando o Python do .venv
for /f "delims=" %%h in ('.venv\Scripts\python.exe -c "import bcrypt; print(bcrypt.hashpw('%SENHA_PROFESSOR%'.encode(), bcrypt.gensalt()).decode())"') do (
    set "HASH=%%h"
)

if "%HASH%"=="" (
    call :erro "Nao foi possivel gerar o hash da senha."
)

call :atualizar_env "PROFESSOR_USERNAME" "%USUARIO%"
call :atualizar_env "PROFESSOR_PASSWORD_HASH" "'%HASH%'"

echo.
call :sucesso "Usuario configurado."
call :sucesso "Senha protegida com sucesso."
goto :eof

:configurar_sessao
:: Gera token de 32 bytes em hexadecimal (equivalente ao openssl rand -hex 32)
for /f "delims=" %%s in ('powershell -NoProfile -Command "$b = New-Object byte[] 32; (New-Object Security.Cryptography.RNGCryptoServiceProvider).GetBytes($b); -join ($b ^| ForEach-Object { '{0:x2}' -f $_ })"') do (
    set "SESSION_SECRET=%%s"
)

call :atualizar_env "SESSION_SECRET" "%SESSION_SECRET%"
call :sucesso "Chave de sessao configurada."
goto :eof

:configurar_banco
echo.
set /p "SENHA_BANCO=Senha do banco de dados (Enter para padrao): "

if "%SENHA_BANCO%"=="" (
    findstr /r /c:"^DB_PASSWORD=.+" .env >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        findstr /c:"DB_PASSWORD=substitua_por_uma_senha_segura" .env >nul 2>&1
        if %ERRORLEVEL% neq 0 (
            call :sucesso "Senha existente do banco mantida."
            goto :eof
        )
    )
    for /f "delims=" %%b in ('powershell -NoProfile -Command "$b = New-Object byte[] 8; (New-Object Security.Cryptography.RNGCryptoServiceProvider).GetBytes($b); -join ($b ^| ForEach-Object { '{0:x2}' -f $_ })"') do (
        set "SENHA_BANCO=%%b"
    )
    call :sucesso "Senha padrao gerada automaticamente."
) else (
    call :sucesso "Senha personalizada selecionada."
)

call :atualizar_env "DB_PASSWORD" "%SENHA_BANCO%"
call :sucesso "Senha do PostgreSQL configurada."
goto :eof

:finalizar
docker compose config --quiet
if %ERRORLEVEL% neq 0 (
    call :erro "Configuracao do Docker Compose invalida."
)

call :sucesso "Docker Compose validado."

echo.
echo ──────────────────────────────────────────
echo.
echo AMBIENTE CONFIGURADO COM SUCESSO!
echo.
echo Para iniciar o MonitoraUnB, execute:
echo   docker compose up -d
echo.
echo Endereco do sistema:
echo   http://localhost:3000/pages/inicio.html
echo.
pause
goto :eof

:main
call :cabecalho
call :instalar_dependencias
call :preparar_env
call :configurar_professor
call :configurar_sessao
call :configurar_banco
call :finalizar
goto :eof
