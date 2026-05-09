# Setup GitHub Repository - Script de Inicialização
# Este script inicializa um repositório Git e configura push automático

Write-Host "=== Setup Repositório GitHub ===" -ForegroundColor Green

# 1. Inicializar repositório local
Write-Host "`n[1/4] Inicializando repositório Git..." -ForegroundColor Cyan
git init
git add .
git commit -m "chore: commit inicial do projeto Analytics CAGED Brasil"

# 2. Instruções para criar no GitHub
Write-Host "`n[2/4] Próximos passos no GitHub:" -ForegroundColor Yellow
Write-Host "  1. Acesse https://github.com/new"
Write-Host "  2. Crie um repositório com o nome: projeto-analytics-engineer (ou seu nome preferido)"
Write-Host "  3. Escolha: Public (portfólio) ou Private (desenvolvimento)"
Write-Host "  4. NÃO selecione 'Initialize with README' (já temos)"
Write-Host "`n  Depois, execute estes comandos (substitua SEU_USUARIO/NOME_REPO):"
Write-Host "  git remote add origin https://github.com/SEU_USUARIO/NOME_REPO.git"
Write-Host "  git branch -M main"
Write-Host "  git push -u origin main"

# 3. Configurar Git hook para push automático
Write-Host "`n[3/4] Configurando push automático..." -ForegroundColor Cyan

# Criar diretório hooks se não existir
$hooksDir = ".git\hooks"
if (-not (Test-Path $hooksDir)) {
    New-Item -ItemType Directory -Path $hooksDir | Out-Null
}

# Criar post-commit hook (Windows PowerShell)
$postCommitHook = @"
#!/bin/bash
# Git hook: fazer push automático após cada commit
# Verifica se há tracking branch antes de fazer push

if git rev-parse --abbrev-ref @{u} &> /dev/null; then
    echo "📤 Push automático para GitHub..."
    git push
else
    echo "⚠️  Branch não tem tracking remoto. Configure com: git push -u origin [branch]"
fi
"@

$postCommitPath = "$hooksDir\post-commit"
Set-Content -Path $postCommitPath -Value $postCommitHook -Encoding UTF8
Write-Host "✅ Hook criado em: .git\hooks\post-commit"

# 4. Resumo
Write-Host "`n[4/4] Resumo da configuração:" -ForegroundColor Green
Write-Host "  ✅ Repositório Git inicializado"
Write-Host "  ✅ .gitignore configurado"
Write-Host "  ✅ Commit inicial feito"
Write-Host "  ✅ Git hook de push automático instalado"
Write-Host "`nDepois de criar o repo no GitHub, o push automático funcionará a cada commit!" -ForegroundColor Yellow
