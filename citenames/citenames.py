import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

current_dir = Path(__file__).parent
aas_file = current_dir / "aas_macros.sty"
tex_template_file = (current_dir / "cite.tex")


def run_tex(bibtex: str, keys: list[str]):
    tex_template = tex_template_file.read_text()
    tex_template = tex_template.split(r"\begin{document}")[0]
    tex_template += "\\begin{document}"
    for key in keys:
        tex_template += "\n"
        tex_template += "\\section*{=======}\n"
        tex_template += f"\\cite{{{key}}}\n\n"
    tex_template += "\\end{document}"
    with TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)
        (tmpdir / "bibtex.bib").write_text(bibtex)
        (tmpdir / "main.tex").write_text(tex_template)

        print(tmpdir)
        shutil.copy(aas_file, tmpdir)

        subprocess.run(
            ["latexmk", "-interaction=batchmode", "main.tex"]
            , cwd=tmpdir, check=True, capture_output=True
        )

        out = subprocess.run(
            ["pdftotext", str(tmpdir / "main.pdf"), "-"],
            cwd=tmpdir, check=True, capture_output=True
        )
        print(repr(out.stdout.decode()))
        print()
        lines = out.stdout.decode().split("\n")
        citenames = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line == "=======":
                continue
            citenames.append(line)

        assert len(citenames) == len(keys)
        return dict(zip(keys, citenames))
