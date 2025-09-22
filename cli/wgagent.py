#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: AlexMG266 <alex.mosquera@udc.es>

import subprocess
import sys
import typer
import uvicorn
from pkg import agent
import shutil
from pathlib import Path

app = typer.Typer(help="wgagent - A WireGuard VPN local configuration manager agent")

def run_command(cmd):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
        return out.strip()
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error: {e.output.decode()}")
        sys.exit(1)

@app.command()
def status():
    try:
        svc_status = run_command(["systemctl", "is-active", "wgnet-agent"])
        typer.echo(f"Estado del servicio: {svc_status}")
        wg_status = run_command(["sudo", "wg", "show", "wg0"])
        typer.echo("Estado wg0:")
        typer.echo(wg_status)
    except Exception as e:
        typer.echo(f"No se pudo obtener estado: {e}")

@app.command()
def deploy():
    typer.echo("[+] Creando usuario wgagent")
    subprocess.run(["sudo", "id", "-u", "wgagent"], check=False)
    subprocess.run(["sudo", "useradd", "-r", "-s", "/usr/sbin/nologin", "wgagent"], check=False)

    typer.echo("[+] Creando directorio de configuración")
    subprocess.run(["sudo", "mkdir", "-p", "/etc/wgagent"], check=True)
    subprocess.run(["sudo", "chown", "wgagent:wgagent", "/etc/wgagent"], check=True)

    typer.echo("[+] Copiando el código a /opt/wgagent")
    subprocess.run(["sudo", "rm", "-rf", "/opt/wgagent"], check=False)
    subprocess.run(["sudo", "mkdir", "-p", "/opt/wgagent"], check=True)
    subprocess.run(["sudo", "cp", "-r", ".", "/opt/wgagent/"], check=True)
    subprocess.run(["sudo", "chown", "-R", "wgagent:wgagent", "/opt/wgagent"], check=True)

    typer.echo("[+] Configurando sudoers")
    sudoers = "/etc/sudoers.d/wgagent"
    sudoers_content = (
        "wgagent ALL=(ALL) NOPASSWD: /usr/bin/wg *, "
        "/usr/sbin/ip link set wg0 *, "
        "/usr/bin/wg-quick up wg0, "
        "/usr/bin/wg-quick down wg0\n"
    )
    subprocess.run(
        ["sudo", "tee", sudoers],
        input=sudoers_content,
        text=True,
        check=True
    )
    subprocess.run(["sudo", "chmod", "440", sudoers], check=True)

    typer.echo("[+] Creando virtualenv en /opt/wgagent/venv")
    subprocess.run(["sudo", "-u", "wgagent", "python3", "-m", "venv", "/opt/wgagent/venv"], check=True)

    typer.echo("[+] Instalando dependencias en el virtualenv")
    subprocess.run([
        "/opt/wgagent/venv/bin/pip", "install", "--upgrade", "pip", "typer", "fastapi", "pydantic"
    ], check=True)

    typer.echo("[+] Instalando y arrancando systemd")
    service_path = "/etc/systemd/system/wgnet-agent.service"
    subprocess.run(["sudo", "cp", "/opt/wgagent/systemd/wgnet-agent.service", service_path], check=True)
    subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
    subprocess.run(["sudo", "systemctl", "enable", "--now", "wgnet-agent"], check=True)

    typer.echo("[✓] wgnet-agent desplegado correctamente")


@app.command()
def destroy():
    typer.echo("[+] Deteniendo y deshabilitando servicio")
    subprocess.run(["sudo", "systemctl", "stop", "wgnet-agent"], check=False)
    subprocess.run(["sudo", "systemctl", "disable", "wgnet-agent"], check=False)
    subprocess.run(["sudo", "rm", "-f", "/etc/systemd/system/wgnet-agent.service"], check=False)
    subprocess.run(["sudo", "systemctl", "daemon-reload"], check=False)

    typer.echo("[+] Eliminando usuario y configuración")
    subprocess.run(["sudo", "userdel", "wgagent"], check=False)
    subprocess.run(["sudo", "rm", "-rf", "/etc/wgagent"], check=False)
    subprocess.run(["sudo", "rm", "-rf", "/opt/wgagent"], check=False)

    typer.echo("[✓] wgnet-agent eliminado")

@app.command()
def run():
    uvicorn.run("pkg.agent:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    app()

