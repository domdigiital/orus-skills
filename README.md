# Orus Skills

Biblioteca de skills da Dom. Digital para a Orus Community e para qualquer pessoa que queira utiliza-las.

## Clone-expert

Orienta a criacao de uma especialista de IA a partir do seu conhecimento, metodo e comunicacao. Inclui mapeamento, oferta, identidade e voz, calendario com 30 pautas, instalacao e testes do clone, avatar e especificacao de perfil.

A criadora e a skill que conduz esse processo. O clone e outra skill, com os seus conhecimentos e escolhas, criada no seu proprio projeto. Seu acervo privado nao precisa ser colocado nesta biblioteca.

O processo aproveita o que voce ja informou e pede as escolhas que faltam. A comunicacao, a direcao visual e o conjunto final passam pela sua avaliacao. Fonte insuficiente ou recurso indisponivel permanece uma pendencia explicita.

## Comecar

1. Tenha Codex ou Claude Code com acesso de leitura/escrita a um projeto local.
2. Baixe esta biblioteca e siga [INSTALAR.md](INSTALAR.md).
3. No projeto de destino, peca: use a clone-expert para criar minha especialista a partir destas fontes.
4. Forneca seu metodo, exemplos de comunicacao e materiais que autoriza usar. A skill guiara as escolhas e apresentara o clone antes de instala-lo.

Nao e necessario fornecer credenciais, acesso a uma conta social ou um historico completo da sua vida. Geracao de imagens depende de ferramenta disponivel e de sua autorizacao para eventuais custos. Voz aqui significa comunicacao, nao clonagem de audio.

## Conteudo do pacote

- [SKILL.md](skills/clone-expert/SKILL.md): entrada da criadora e conducao por etapa.
- [Referencias](skills/clone-expert/memory/): sete guias de conhecimento, oferta, comunicacao, conteudo, avatar, validacao e fontes.
- [Templates](skills/clone-expert/templates/): modelos do clone e do projeto do usuario.
- Instaladores PowerShell e Bash com selecao de skill/ambiente e preservacao de backup fora da pasta de descoberta.
- [Testes](tests/): verificacao da distribuicao e dos instaladores, com material ficticio.

## Estado de validacao

Em 26/10/2026, a suite automatizada passou com 13 testes no Windows: PowerShell 7 e Git Bash, nos destinos de Codex e Claude Code, incluindo backup, rollback, licenca instalada e preservacao de arquivos irmaos.

Percursos com fontes ficticias foram executados no Codex app e no Claude Code 2.1.309. Cada um produziu um clone com 30 pautas e 13 campos por pauta; copias foram instaladas em novos diretorios e consultadas em novos contextos para explicar o metodo, criar conteudo e responder sobre a oferta. As amostras desse caso receberam aceite humano em 26/10/2026; cada novo clone exige sua propria avaliacao.

A CLI local do Codex falhou no sandbox antes de ler as fontes; o teste do Codex foi realizado pelo recurso de subagente do app. Linux e macOS nao foram testados. Os ensaios demonstram somente esses casos, sem paridade universal, ganho estatistico ou resultados comerciais. Instalacao local nao publica conteudo, altera perfil ou abre uma oferta comercial.

## Conferir a distribuicao

Com Python 3 e os interpretadores dos instaladores disponiveis:

```text
python -m unittest discover -s tests -v
```

Os testes usam projetos temporarios e exemplos ficticios. A fidelidade da comunicacao exige sua avaliacao das amostras do seu clone. A existencia dos arquivos nao comprova receita, produtividade, vendas ou escala.

## Fonte unica e contribuicoes

`skills/clone-expert/` e a fonte mantida nesta biblioteca. Uso interno e publico recebem a mesma versao; o projeto de cada usuario recebe uma copia selecionada pelo instalador. Nao e preciso adaptar a skill para um protocolo privado ou instalar outras skills para usa-la.

Melhorias sao propostas sobre essa fonte e testadas antes de distribuir uma nova versao. Instalacoes existentes preservam backup quando atualizadas; conhecimentos e mudancas locais precisam ser revisados antes de substituir a copia.

## Autoria e fontes

Copyright (c) 2026 Dom. Digital. Licenca [MIT](LICENSE). Preserve os avisos de autoria e licenca nas copias.

[Fontes metodologicas](skills/clone-expert/memory/fontes-metodologicas.md) atribui as referencias conceituais. Livro, videos e materiais de terceiros nao acompanham o pacote e mantem seus direitos. Exemplos e conhecimento adicionados pelo usuario seguem as permissoes das respectivas fontes.
