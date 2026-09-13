"""
Módulo de logging local para o Gerenciador de Tarefas.

Gera arquivos de log na pasta 'logs/' com rotação diária,
utilizando exclusivamente o módulo 'logging' nativo do Python
(zero dependências externas).

Referência: ADR-002 (docs/adr/ADR-002-logging.md)
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional


def _get_logs_dir(base_dir: Optional[str] = None) -> Path:
    """Retorna o caminho da pasta de logs, criando-a se necessário."""
    if base_dir is None:
        # Navega até a raiz do projeto (pai de src/)
        base_dir = str(Path(__file__).resolve().parent.parent)
    logs_path = Path(base_dir) / "logs"
    logs_path.mkdir(parents=True, exist_ok=True)
    return logs_path


def get_logger(
    name: str = "app",
    base_dir: Optional[str] = None,
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Configura e retorna um logger com handlers para arquivo e console.

    Args:
        name: Nome do logger (geralmente __name__ do módulo chamador).
        base_dir: Diretório base do projeto. Se None, detecta automaticamente.
        level: Nível mínimo de log (default: INFO).

    Returns:
        Logger configurado com FileHandler (diário) e StreamHandler.
    """
    logger = logging.getLogger(name)

    # Evita adicionar handlers duplicados caso chamado múltiplas vezes
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # Formato padrão: [TIMESTAMP] [LEVEL] [LOGGER] MENSAGEM
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # --- FileHandler: grava em logs/app_YYYY-MM-DD.log ---
    logs_dir = _get_logs_dir(base_dir)
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = logs_dir / f"app_{today}.log"

    file_handler = logging.FileHandler(str(log_file), encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # --- StreamHandler: exibe no console ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
