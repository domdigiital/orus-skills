# proposito: conferir estrutura, referencias e limites publicos da clone-expert
import re
import unittest
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
SKILL = RAIZ / "skills" / "clone-expert"


class TestePacote(unittest.TestCase):
    def test_distribuicao_tem_arquivos_de_entrada(self):
        for nome in ("README.md", "INSTALAR.md", "LICENSE", "install.ps1", "install.sh"):
            with self.subTest(arquivo=nome):
                self.assertTrue((RAIZ / nome).is_file())

    def test_criadora_completa_e_modelos_presentes(self):
        arquivos = {p.relative_to(SKILL).as_posix() for p in SKILL.rglob("*") if p.is_file()}
        self.assertEqual(arquivos, {
            "SKILL.md", "memory/mapear-conhecimento.md", "memory/oferta.md",
            "memory/identidade-conhecimento-voz.md", "memory/sistema-conteudo.md",
            "memory/avatar-perfil.md", "memory/validacao.md", "memory/fontes-metodologicas.md",
            "templates/clone.md", "templates/projeto.md", "LICENSE",
        })

    def test_metadados_e_rotas(self):
        texto = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertRegex(texto, r"\A---\nname: clone-expert\ndescription: Use quando .+\n---\n")
        referencias = re.findall(r"^- ((?:memory|templates)/[a-z-]+\.md):", texto, re.M)
        self.assertEqual(len(referencias), 9)
        for referencia in referencias:
            self.assertTrue((SKILL / referencia).is_file(), referencia)

    def test_contrato_editorial_e_completo(self):
        texto = (SKILL / "memory/sistema-conteudo.md").read_text(encoding="utf-8")
        campos = re.findall(r"^\d+\. .+", texto, re.M)
        self.assertEqual(len(campos), 13)
        for termo in ("P01 a P30", "Fonte/prova", "Desenvolvimento", "CTA", "Metrica"):
            self.assertIn(termo, texto)
        self.assertIn("calendario", texto)

    def test_licenca_e_autoria(self):
        texto = (RAIZ / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Dom. Digital", texto)
        self.assertIn("permission notice shall be included", texto)
        self.assertIn('THE SOFTWARE IS PROVIDED "AS IS"', texto)

    def test_copia_da_skill_preserva_licenca(self):
        self.assertTrue((SKILL / "LICENSE").is_file())
        self.assertEqual((RAIZ / "LICENSE").read_bytes(), (SKILL / "LICENSE").read_bytes())

    def test_instrucoes_portateis(self):
        arquivos = list(SKILL.rglob("*.md")) + [RAIZ / "README.md", RAIZ / "INSTALAR.md"]
        for arquivo in arquivos:
            with self.subTest(arquivo=arquivo.name):
                texto = arquivo.read_text(encoding="utf-8")
                self.assertTrue(texto.isascii(), "Documentacao deve usar portugues sem acentos")
                self.assertNotRegex(texto, r"[A-Z]:[\\/]|/(?:home|Users)/")


if __name__ == "__main__":
    unittest.main()
