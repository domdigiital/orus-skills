# proposito: provar instalacao seletiva e preservacao em projetos descartaveis.
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


RAIZ = Path(__file__).resolve().parents[1]


def inventario(pasta):
    return {str(p.relative_to(pasta)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in pasta.rglob("*") if p.is_file()}


class Instaladores(unittest.TestCase):
    def setUp(self):
        self.temporario = tempfile.TemporaryDirectory(prefix="instaladores ")
        self.addCleanup(self.temporario.cleanup)
        self.base = Path(self.temporario.name)
        self.repositorio = self.base / "repositorio com espaco"
        self.fonte = self.repositorio / "skills" / "clone-expert"
        self.fonte.mkdir(parents=True)
        (self.fonte / "SKILL.md").write_text("criadora ficticia", encoding="utf-8")
        (self.fonte / "referencias").mkdir()
        (self.fonte / "referencias" / ".oculto").write_text("fonte", encoding="utf-8")
        (self.repositorio / "skills" / "outra").mkdir()
        self.projeto = self.base / "projeto com espaco"
        self.projeto.mkdir()

    def executar(self, tipo, ambiente="codex", skill="clone-expert", destino=None,
                 falhar_ativacao=False):
        extensao = "ps1" if tipo == "pwsh" else "sh"
        original = RAIZ / f"install.{extensao}"
        self.assertTrue(original.is_file(), f"Instalador ausente: {original.name}")
        script = self.repositorio / original.name
        shutil.copy2(original, script)
        destino = str(destino or self.projeto)
        variaveis = os.environ.copy()
        if tipo == "pwsh":
            executavel = shutil.which("pwsh")
            if not executavel:
                self.skipTest("PowerShell nao disponivel")
            comando = [executavel, "-NoProfile", "-File", str(script),
                       "-Destino", destino, "-Ambiente", ambiente, "-Skill", skill]
            if falhar_ativacao:
                lancador = self.base / "falha.ps1"
                lancador.write_text(
                    "function Move-Item { param([string]$LiteralPath, [string]$Destination)\n"
                    "if ($LiteralPath -like '*preparo-*') { throw 'Falha simulada' }\n"
                    "Microsoft.PowerShell.Management\\Move-Item -LiteralPath $LiteralPath "
                    "-Destination $Destination }\n"
                    "& $args[0] -Destino $args[1] -Ambiente $args[2] -Skill $args[3]\n"
                    "exit $LASTEXITCODE\n")
                comando = [executavel, "-NoProfile", "-File", str(lancador),
                           str(script), destino, ambiente, skill]
        else:
            executavel = (Path(os.environ.get("ProgramFiles", "C:/Program Files"))
                          / "Git/bin/bash.exe") if os.name == "nt" else shutil.which("bash")
            if not executavel or not Path(executavel).is_file():
                self.skipTest("Bash real nao disponivel")
            comando = [str(executavel), str(script).replace("\\", "/"),
                       "--destino", destino.replace("\\", "/"),
                       "--ambiente", ambiente, "--skill", skill]
            if falhar_ativacao:
                lancador = self.base / "falha.sh"
                lancador.write_text("mv() { case \"$1\" in *preparo-*) return 1 ;; esac; "
                                    "command mv \"$@\"; }\n", encoding="utf-8")
                variaveis["BASH_ENV"] = str(lancador).replace("\\", "/")
        return subprocess.run(comando, capture_output=True, text=True, timeout=30,
                              env=variaveis)

    def test_limpa_reinstalacoes_e_irmaos(self):
        for tipo in ("pwsh", "bash"):
            for ambiente, pasta in (("codex", ".agents"), ("claude", ".claude")):
                with self.subTest(tipo=tipo, ambiente=ambiente):
                    projeto = self.projeto / tipo / ambiente
                    projeto.mkdir(parents=True)
                    raiz = projeto / pasta / "skills"
                    irma = raiz / "irma"
                    irma.mkdir(parents=True)
                    (irma / "valor.txt").write_text("preservar")
                    antes = inventario(irma)
                    ativo = raiz / "clone-expert"
                    resultado = self.executar(tipo, ambiente, destino=projeto)
                    self.assertEqual(0, resultado.returncode, resultado.stderr)
                    self.assertEqual(inventario(self.fonte), inventario(ativo))
                    for numero in (1, 2):
                        (ativo / "local.txt").write_text(str(numero))
                        resultado = self.executar(tipo, ambiente, destino=projeto)
                        self.assertEqual(0, resultado.returncode, resultado.stderr)
                        self.assertEqual(inventario(self.fonte), inventario(ativo))
                        self.assertEqual({"clone-expert", "irma"},
                                         {p.name for p in raiz.iterdir()})
                        historico = projeto / ".skill-backups" / ambiente / "clone-expert"
                        copias = list(historico.glob("backup-*"))
                        self.assertEqual(numero, len(copias))
                        self.assertEqual({str(n) for n in range(1, numero + 1)},
                                         {(p / "local.txt").read_text() for p in copias})
                        self.assertTrue(any(str(p).replace("\\", "/") in
                                            resultado.stdout.replace("\\", "/") for p in copias),
                                        resultado.stdout)
                    self.assertEqual(antes, inventario(irma))
                    self.assertFalse((raiz / "outra").exists())

    def test_entradas_invalidas_sem_escrita(self):
        for tipo in ("pwsh", "bash"):
            for ambiente, skill in (("invalido", "clone-expert"), ("codex", "ausente"),
                                    ("codex", "../clone-expert"), ("codex", "..")):
                with self.subTest(tipo=tipo, ambiente=ambiente, skill=skill):
                    antes = inventario(self.projeto)
                    resultado = self.executar(tipo, ambiente, skill)
                    self.assertNotEqual(0, resultado.returncode)
                    self.assertEqual(antes, inventario(self.projeto))
                    self.assertEqual([], list(self.projeto.iterdir()))

    def test_conflitos_e_arvore_de_origem(self):
        for tipo in ("pwsh", "bash"):
            for posicao in ("projeto", ".agents", ".agents/skills", ".agents/skills/clone-expert",
                            ".skill-backups", ".skill-backups/codex",
                            ".skill-backups/codex/clone-expert"):
                with self.subTest(tipo=tipo, posicao=posicao):
                    projeto = self.projeto / tipo / posicao.replace("/", "-")
                    projeto.mkdir(parents=True)
                    conflito = projeto if posicao == "projeto" else projeto / posicao
                    if conflito == projeto:
                        conflito = projeto / "arquivo"
                    conflito.parent.mkdir(parents=True, exist_ok=True)
                    conflito.write_text("nao mudar")
                    antes = inventario(projeto)
                    resultado = self.executar(tipo, destino=conflito if posicao == "projeto" else projeto)
                    self.assertNotEqual(0, resultado.returncode)
                    self.assertEqual(antes, inventario(projeto))
            antes = inventario(self.fonte)
            resultado = self.executar(tipo, destino=self.fonte / "interno")
            self.assertNotEqual(0, resultado.returncode)
            self.assertEqual(antes, inventario(self.fonte))

    def test_junctions_na_origem_e_destino(self):
        if os.name != "nt":
            self.skipTest("Junction e especifica de Windows")
        externo = self.base / "externo"
        externo.mkdir()
        (externo / "protegido").write_text("preservar")
        for tipo in ("pwsh", "bash"):
            for posicao in ("origem", ".agents", ".skill-backups",
                            ".skill-backups/codex", ".skill-backups/codex/clone-expert"):
                with self.subTest(tipo=tipo, posicao=posicao):
                    projeto = self.projeto / tipo / posicao.replace("/", "-")
                    projeto.mkdir(parents=True)
                    link = self.fonte / "desvio" if posicao == "origem" else projeto / posicao
                    link.parent.mkdir(parents=True, exist_ok=True)
                    resultado = subprocess.run(["cmd", "/c", "mklink", "/J", str(link),
                                                str(externo)], capture_output=True, text=True)
                    self.assertEqual(0, resultado.returncode, resultado.stderr)
                    try:
                        antes = inventario(externo)
                        resultado = self.executar(tipo, destino=projeto)
                        self.assertNotEqual(0, resultado.returncode, resultado.stdout)
                        self.assertEqual(antes, inventario(externo))
                    finally:
                        link.rmdir()

    def test_rollback_preserva_versao_ativa(self):
        for tipo in ("pwsh", "bash"):
            with self.subTest(tipo=tipo):
                projeto = self.projeto / tipo
                projeto.mkdir()
                resultado = self.executar(tipo, destino=projeto)
                self.assertEqual(0, resultado.returncode, resultado.stderr)
                ativo = projeto / ".agents/skills/clone-expert"
                (ativo / "local.txt").write_text("recuperar")
                antes = inventario(ativo)
                resultado = self.executar(tipo, destino=projeto, falhar_ativacao=True)
                self.assertNotEqual(0, resultado.returncode, resultado.stdout + resultado.stderr)
                self.assertEqual(antes, inventario(ativo))
                self.assertEqual(["clone-expert"], [p.name for p in ativo.parent.iterdir()])
                historico = projeto / ".skill-backups/codex/clone-expert"
                preparos = list(historico.glob("preparo-*"))
                self.assertEqual(1, len(preparos))
                self.assertEqual(inventario(self.fonte), inventario(preparos[0]))

    def test_origem_com_caixa_diferente_no_windows(self):
        if os.name != "nt":
            self.skipTest("Comparacao sem distinguir caixa e especifica de Windows")
        for tipo in ("pwsh", "bash"):
            with self.subTest(tipo=tipo):
                resultado = self.executar(tipo, destino=str(self.fonte).upper() + "/interno")
                self.assertNotEqual(0, resultado.returncode, resultado.stdout)
                self.assertFalse((self.fonte / "interno").exists())


if __name__ == "__main__":
    unittest.main()
