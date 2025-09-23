# wgnet-agent
CLI tool for a simple local agent to administrate the wg0 interface in VPN connections.

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Badge en Desarrollo](https://img.shields.io/badge/STATUS-IN%20DEVELOP-green)


## Instalación y ejecución

### Requisitos

- Python 3.12+
- `make` (GNU Make)
- Dependencias de Python listadas en `requirements.txt`

### Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/AlexMG266/wgnet-agent.git
cd wgnet-agent
```

2. Instalar dependencias en el entorno y ejecutar el proyecto:

````bash
make install   
````

3. Desplegar el agente en la maquina host
```bash
make run ARGS="deploy"
python3 -m cli.wgagent deploy
```

4. Destruir al agente
```bash
make run ARGS="destroy"
python3 -m cli.wgagent destroy
```

5. Limpiar el proyecto
```bash
make clean      # Limpieza de cache python 
make clean-all  # Limpieza total del proyecto 
```
