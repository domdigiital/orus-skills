#!/usr/bin/env bash
# Proposito: instalar somente a skill escolhida e preservar backups anteriores.
set -euo pipefail

falhar() { printf 'Falha: %s\n' "$*" >&2; exit 1; }
destino='' ambiente='' skill=''
while (($#)); do
    (($# >= 2)) || falhar 'Argumento sem valor.'
    case "$1" in
        --destino) destino=$2 ;;
        --ambiente) ambiente=$2 ;;
        --skill) skill=$2 ;;
        *) falhar "Argumento invalido: $1" ;;
    esac
    shift 2
done
[[ -n "$destino" && -n "$ambiente" && -n "$skill" ]] || falhar 'Informe destino, ambiente e skill.'
[[ "$skill" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || falhar 'Nome de skill invalido.'
case "$ambiente" in
    codex) pasta='.agents' ;;
    claude) pasta='.claude' ;;
    *) falhar 'Ambiente invalido: use codex ou claude.' ;;
esac

# Normaliza sem criar diretorios e sem seguir links da entrada.
absoluto() {
    local entrada=$1 parte resultado='' segmentos
    if command -v cygpath >/dev/null 2>&1; then entrada=$(cygpath -u "$entrada"); fi
    [[ "$entrada" == /* ]] || entrada="$PWD/$entrada"
    IFS='/' read -r -a segmentos <<< "$entrada"
    for parte in "${segmentos[@]}"; do
        case "$parte" in
            ''|.) ;;
            ..) resultado=${resultado%/*} ;;
            *) resultado="$resultado/$parte" ;;
        esac
    done
    printf '%s\n' "${resultado:-/}"
}

confirmar_caminho() {
    local atual=$1
    while [[ -n "$atual" && "$atual" != / ]]; do
        [[ ! -L "$atual" ]] || falhar "Link nao permitido: $atual"
        atual=${atual%/*}
    done
}

confirmar_arvore() {
    confirmar_caminho "$1"
    if [[ -d "$1" ]]; then
        local links
        links=$(find "$1" -type l -print) || falhar 'Nao foi possivel conferir a arvore.'
        [[ -z "$links" ]] || falhar "Link nao permitido: $links"
    fi
}

mostrar_caminho() {
    if command -v cygpath >/dev/null 2>&1; then cygpath -m "$1"; else printf '%s\n' "$1"; fi
}

repositorio=$(absoluto "$(dirname "${BASH_SOURCE[0]}")")
fonte="$repositorio/skills/$skill"
confirmar_arvore "$fonte"
[[ -f "$fonte/SKILL.md" ]] || falhar "Skill inexistente ou incompleta: $skill"
projeto=$(absoluto "$destino")
projeto_comparado=$projeto fonte_comparada=$fonte
case "${OSTYPE-}" in
    msys*|cygwin*)
        projeto_comparado=$(printf '%s' "$projeto" | tr '[:upper:]' '[:lower:]')
        fonte_comparada=$(printf '%s' "$fonte" | tr '[:upper:]' '[:lower:]') ;;
esac
case "$projeto_comparado/" in "$fonte_comparada/"*) falhar 'Destino nao pode ficar dentro da origem da skill.' ;; esac
raiz="$projeto/$pasta/skills"
alvo="$raiz/$skill"
arquivo_historico="$projeto/.skill-backups"
ambiente_historico="$arquivo_historico/$ambiente"
historico="$ambiente_historico/$skill"
confirmar_arvore "$alvo"
for caminho in "$projeto" "$projeto/$pasta" "$raiz" "$alvo" \
    "$arquivo_historico" "$ambiente_historico" "$historico"; do
    confirmar_caminho "$caminho"
    [[ ! -e "$caminho" || -d "$caminho" ]] || falhar "Destino conflitante: $caminho"
done

mkdir -p "$raiz" "$historico"
preparo=$(mktemp -d "$historico/preparo-XXXXXXXX")
backup="$historico/backup-${preparo##*/preparo-}"
[[ ! -e "$backup" && ! -L "$backup" ]] || falhar "Backup ja existe: $backup"
cp -R "$fonte/." "$preparo/"
if [[ -e "$alvo" ]]; then
    mv "$alvo" "$backup"
    printf 'Backup: %s\n' "$(mostrar_caminho "$backup")"
fi
if ! mv "$preparo" "$alvo"; then
    if [[ -d "$backup" && ! -e "$alvo" ]]; then mv "$backup" "$alvo"; fi
    falhar "Copia nao ativada. Preparo preservado: $preparo"
fi
printf 'Origem: %s\n' "$(mostrar_caminho "$fonte")"
printf 'Instalada: %s\n' "$(mostrar_caminho "$alvo")"
