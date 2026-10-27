# Proposito: instalar somente a skill escolhida, preservando cada versao anterior.
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$Destino,
    [Parameter(Mandatory)][string]$Ambiente,
    [Parameter(Mandatory)][string]$Skill
)
$ErrorActionPreference = 'Stop'

function Confirmar-Caminho([string]$Caminho) {
    $atual = [IO.Path]::GetFullPath($Caminho)
    while ($atual) {
        $item = Get-Item -LiteralPath $atual -Force -ErrorAction SilentlyContinue
        if ($item -and ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw "Link/reparse nao permitido: $atual"
        }
        $pai = [IO.Path]::GetDirectoryName($atual)
        if ($pai -eq $atual) { break }
        $atual = $pai
    }
}

function Confirmar-Arvore([string]$Caminho) {
    Confirmar-Caminho $Caminho
    if (Test-Path -LiteralPath $Caminho -PathType Container) {
        foreach ($item in Get-ChildItem -LiteralPath $Caminho -Force -Recurse) {
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                throw "Link/reparse nao permitido: $($item.FullName)"
            }
        }
    }
}

try {
    if ($Skill -cnotmatch '^[a-z0-9]+(?:-[a-z0-9]+)*$') { throw 'Nome de skill invalido.' }
    $pasta = switch -CaseSensitive ($Ambiente) {
        'codex' { '.agents' }
        'claude' { '.claude' }
        default { throw 'Ambiente invalido: use codex ou claude.' }
    }
    $fonte = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot "skills/$Skill"))
    Confirmar-Arvore $fonte
    if (-not (Test-Path -LiteralPath (Join-Path $fonte 'SKILL.md') -PathType Leaf)) {
        throw "Skill inexistente ou incompleta: $Skill"
    }
    $projeto = [IO.Path]::GetFullPath($Destino)
    $comparacao = if ($IsWindows) { [StringComparison]::OrdinalIgnoreCase } else { [StringComparison]::Ordinal }
    $separador = [IO.Path]::DirectorySeparatorChar
    if ($projeto.Equals($fonte, $comparacao) -or
        $projeto.StartsWith($fonte + $separador, $comparacao)) {
        throw 'Destino nao pode ficar dentro da origem da skill.'
    }
    $raiz = Join-Path $projeto "$pasta/skills"
    $alvo = Join-Path $raiz $Skill
    $arquivoHistorico = Join-Path $projeto '.skill-backups'
    $ambienteHistorico = Join-Path $arquivoHistorico $Ambiente
    $historico = Join-Path $ambienteHistorico $Skill
    Confirmar-Arvore $alvo
    foreach ($caminho in @($projeto, (Join-Path $projeto $pasta), $raiz, $alvo,
                          $arquivoHistorico, $ambienteHistorico, $historico)) {
        Confirmar-Caminho $caminho
        if ((Test-Path -LiteralPath $caminho) -and
            -not (Test-Path -LiteralPath $caminho -PathType Container)) {
            throw "Destino conflitante: $caminho"
        }
    }
    # A copia completa vem antes de mover a versao ativa.
    [IO.Directory]::CreateDirectory($raiz) | Out-Null
    [IO.Directory]::CreateDirectory($historico) | Out-Null
    $identificador = [guid]::NewGuid().ToString('N')
    $preparo = Join-Path $historico "preparo-$identificador"
    $backup = Join-Path $historico "backup-$identificador"
    Copy-Item -LiteralPath $fonte -Destination $preparo -Recurse -Force
    if (Test-Path -LiteralPath $alvo) {
        Move-Item -LiteralPath $alvo -Destination $backup
        Write-Output "Backup: $backup"
    }
    try {
        Move-Item -LiteralPath $preparo -Destination $alvo
    } catch {
        if ((Test-Path -LiteralPath $backup) -and -not (Test-Path -LiteralPath $alvo)) {
            Move-Item -LiteralPath $backup -Destination $alvo
        }
        throw
    }
    Write-Output "Origem: $fonte"
    Write-Output "Instalada: $alvo"
} catch {
    [Console]::Error.WriteLine("Falha: $($_.Exception.Message)")
    exit 1
}
