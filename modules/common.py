import os
import subprocess

from pygemstones.io import file as f
from pygemstones.system import runner as r
from pygemstones.util import log as l


# -----------------------------------------------------------------------------
def run_task_build_depot_tools():
    l.colored("Building depot tools...", l.YELLOW)

    build_dir = os.path.join("build")
    f.create_dir(build_dir)

    tools_dir = os.path.join(build_dir, "depot-tools")
    f.remove_dir(tools_dir)

    cwd = build_dir
    command = [
        "git",
        "clone",
        "https://chromium.googlesource.com/chromium/tools/depot_tools.git",
        "depot-tools",
    ]
    r.run(command, cwd)

    l.colored("Execute on your terminal:", l.PURPLE)
    l.m("export PATH=$PATH:$PWD/build/depot-tools")

    l.ok()


# -----------------------------------------------------------------------------
def run_task_build_emsdk():
    l.colored("Building Emscripten SDK...", l.YELLOW)

    build_dir = os.path.join("build")
    f.create_dir(build_dir)

    tools_dir = os.path.join(build_dir, "emsdk")
    f.remove_dir(tools_dir)

    cwd = build_dir
    command = [
        "git",
        "clone",
        "https://github.com/emscripten-core/emsdk.git",
    ]
    r.run(command, cwd)

    cwd = tools_dir
    command = " ".join(["./emsdk", "install", "latest"])
    r.run_as_shell(command, cwd)

    cwd = tools_dir
    command = " ".join(["./emsdk", "activate", "latest"])
    r.run_as_shell(command, cwd)

    cwd = tools_dir
    command = " ".join(["source", "emsdk_env.sh"])
    r.run_as_shell(command, cwd)

    l.ok()


# -----------------------------------------------------------------------------
def run_task_format():
    # check
    try:
        subprocess.check_output(["black", "--version"])
    except OSError:
        l.e("Black is not installed, check: https://github.com/psf/black")

    # start
    l.colored("Formating...", l.YELLOW)

    # make.py
    command = [
        "black",
        "make.py",
    ]
    r.run(command)

    # modules
    command = [
        "black",
        "modules/",
    ]
    r.run(command)

    l.ok()
