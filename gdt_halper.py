import os
import re
import subprocess
from typing import List

import typer

app = typer.Typer()


def show_err(msg: str) -> None:
    typer.secho(msg, err=True, fg=typer.colors.RED)


def show_warn(msg: str) -> None:
    typer.secho(msg, err=True, fg=typer.colors.YELLOW)


def show_log(msg: str) -> None:
    typer.secho(msg, err=True, fg=typer.colors.GREEN)


def has_compiler(compiler_path: str) -> bool:
    try:
        subprocess.run(
            [compiler_path, "-v"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
        ).stdout.decode("utf-8")
    except FileNotFoundError:
        show_err(f"{compiler_path} is not installed")
        show_err("Please install via package manager")
        return False
    except Exception as e:
        show_err(f"Unknown error ({e})")
        return False
    return True


def get_default_include_paths(compiler_raw_output: str) -> List[str]:
    include_path_str_starts = False
    default_include_paths = list()
    for line in compiler_raw_output.split("\n"):
        if line.startswith("#include <...> search starts here:"):
            include_path_str_starts = True
            continue
        if line.startswith("End of search list."):
            break
        if include_path_str_starts:
            default_include_paths.append("-I" + line.strip())
    return default_include_paths


def get_compiler_paths(compiler_raw_output: str) -> List[str]:
    for line in compiler_raw_output.split("\n"):
        if line.startswith("COMPILER_PATH="):
            path_var = line.split("=")[-1]
            return path_var.split(":")
    return []


def get_additional_definitions() -> List[str]:
    return [
        '-DCONST="const"',
        '-D__restrict__=""',
        '-D__always_inline__="inline"',
        '-D__gnu_inline__="inline"',
        '-D__builtin_va_list="void *"',
    ]


def get_default_definitions(compiler_path: str) -> List[str]:
    compiler_raw_output = subprocess.run(
        [compiler_path, "-std=c89", "-dM", "-E", "-"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    ).stdout.decode("utf-8")
    defs = list()
    for line in compiler_raw_output.split("\n"):
        if not line:
            continue
        define, *vars = line.split(" ")
        if define != "#define":
            show_err("It is not #define")
            show_err(line)
            show_err("It might fail to parse")
        defs.append("-D" + vars[0] + "=" + '"' + " ".join(vars[1:]) + '"')
    return defs


def get_parse_options(compiler_path: str) -> List[str]:
    compiler_raw_output = subprocess.run(
        [compiler_path, "-std=c89", "-E", "-v", "-xc", "-"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    ).stdout.decode("utf-8")
    default_include_paths = get_default_include_paths(compiler_raw_output)
    compiler_paths = get_compiler_paths(compiler_raw_output)
    defs = get_additional_definitions()
    default_defs = get_default_definitions(compiler_path)
    return default_include_paths + compiler_paths + defs + default_defs


@app.command()
def show_parse_options(compiler_path: str) -> None:
    if not has_compiler(compiler_path):
        return

    parse_options = get_parse_options(compiler_path)
    typer.echo('Please past the following output to "Parse Options"\n')
    typer.echo("\n".join(parse_options))


@app.command()
def show_raw_header(compiler_path: str, input_header_path: str) -> None:
    if not os.path.exists(input_header_path):
        show_err(f"{input_header_path} does not exist")
        return
    if not has_compiler(compiler_path):
        return

    try:
        raw_out = subprocess.run(
            [compiler_path, "-std=c89", "-P", "-E", input_header_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except Exception as e:
        show_err(str(e))
        return

    raw_header = re.sub(
        r"__asm__.*;", r"/*__asm__*/", raw_out.stdout.decode("utf-8"), flags=re.DOTALL
    )
    output_header_path = input_header_path + ".out"
    with open(output_header_path, "w") as fout:
        fout.write(raw_header)

    show_log(f'Please add "{output_header_path}" to "Source files to parse"')


if __name__ == "__main__":
    app()
