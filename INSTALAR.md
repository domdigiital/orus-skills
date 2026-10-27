# Instalar clone-expert no projeto

Execute no terminal a partir da raiz desta biblioteca. Os comandos abaixo copiam somente a skill selecionada para o projeto informado. Escolha um destino proprio, fora da pasta da biblioteca.

## 1. Conferir requisitos

- Projeto local que voce pode editar.
- Codex ou Claude Code instalado e configurado.
- PowerShell 7 para `install.ps1`, ou Bash para `install.sh`.
- Permissao para copiar a skill. O instalador nao precisa de rede nem recebe credenciais.

## 2. Instalar no ambiente escolhido

No Windows com PowerShell:

```powershell
pwsh -NoProfile -File ./install.ps1 -Destino "../meu-projeto" -Ambiente codex -Skill clone-expert
```

Para Claude Code, substitua `-Ambiente codex` por `-Ambiente claude`.

Com Bash:

```bash
bash ./install.sh --destino "../meu-projeto" --ambiente codex --skill clone-expert
```

Para Claude Code, substitua `--ambiente codex` por `--ambiente claude`.

Use aspas em caminhos com espacos. Se o instalador recusar um caminho, corrija a causa informada antes de tentar novamente. Nao instale sobre a propria arvore de origem nem use links que desviem a escrita para outro destino.

## 3. Conferir a copia

Codex: `<projeto>/.agents/skills/clone-expert/SKILL.md`.
Claude Code: `<projeto>/.claude/skills/clone-expert/SKILL.md`.

Na pasta instalada, confira tambem `memory/` e `templates/`, com sete referencias e dois modelos. Abra SKILL.md e confirme `name: clone-expert`. A mensagem do instalador informa o destino real.

Abra uma nova sessao do agente no projeto de destino. No Codex, solicite `$clone-expert`. No Claude Code, solicite `/clone-expert`. Peca que ele leia a skill e a referencia de mapeamento e explique quais fontes suas precisa receber. Essa chamada confere recuperacao; nao e ainda a validacao de um clone produzido.

## 4. Reinstalar e recuperar

Repita o comando de instalacao com os mesmos argumentos. Se ja existir uma pasta da skill, o instalador preserva uma copia com identificador unico em `<projeto>/.skill-backups/<ambiente>/<skill>/` antes de colocar a versao nova. Confira o caminho do backup informado na saida e abra um arquivo para verificar seu conteudo. Backups e preparos ficam fora das pastas que os agentes descobrem como skills; backups anteriores permanecem preservados.

A copia instalada inclui LICENSE com o aviso de autoria e licenca da biblioteca.

Para recuperar uma alteracao local, compare o backup com a versao ativa e traga de volta somente o trecho desejado, depois da revisao. O instalador nao combina automaticamente orientacoes contraditorias.

## 5. Criar seu clone

Forneca suas fontes autorizadas e acompanhe o processo. A criadora apresentara texto, referencias e modelos preenchidos para sua avaliacao. O clone recebe outro nome e seus proprios arquivos, em um projeto que voce escolher. Nao grave seu conhecimento privado no checkout publico desta biblioteca.

Antes de chamar o clone de pronto, confira instalacao, recuperacao do conhecimento, explicacao do metodo, conteudo e resposta sobre oferta. Avalie a comunicacao e registre as correcoes. Se incluiu avatar no escopo, confira tambem a geracao e o aceite visual; briefing sem imagem nao comprova geracao.

## Limites por ambiente

As convencoes de destino seguem [OpenAI](https://learn.chatgpt.com/docs/build-skills) e [Claude Code](https://code.claude.com/docs/en/skills). Consulte o estado real dos testes no README. Um Bash encontrado no Windows pode ser apenas o lancador de WSL; isso nao confirma que exista uma distribuicao Linux funcional.

Nenhum comando desta instalacao publica no GitHub, envia mensagens, modifica uma conta social, instala plugins ou executa geracao visual.
