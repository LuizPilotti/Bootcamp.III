"""
Testes automatizados para o módulo de logging local (src/logger.py).

Utiliza tmp_path do pytest para não poluir o diretório do projeto.
"""

import logging
from pathlib import Path
from datetime import datetime

from src.logger import get_logger, _get_logs_dir


class TestLogsDir:
    """Testes da criação automática da pasta de logs."""

    def test_logs_dir_is_created(self, tmp_path):
        """Verifica que a pasta 'logs/' é criada quando não existe."""
        logs_dir = _get_logs_dir(base_dir=str(tmp_path))
        assert logs_dir.exists()
        assert logs_dir.is_dir()
        assert logs_dir.name == "logs"

    def test_logs_dir_already_exists(self, tmp_path):
        """Verifica que não há erro se a pasta 'logs/' já existe."""
        (tmp_path / "logs").mkdir()
        logs_dir = _get_logs_dir(base_dir=str(tmp_path))
        assert logs_dir.exists()


class TestGetLogger:
    """Testes da função get_logger."""

    def test_returns_logger_instance(self, tmp_path):
        """Verifica que retorna uma instância de logging.Logger."""
        logger = get_logger("test_instance", base_dir=str(tmp_path))
        assert isinstance(logger, logging.Logger)
        # Limpa handlers para não interferir em outros testes
        logger.handlers.clear()

    def test_log_file_is_created(self, tmp_path):
        """Verifica que o arquivo de log é criado com o nome correto."""
        logger = get_logger("test_file_creation", base_dir=str(tmp_path))
        logger.info("Mensagem de teste")

        today = datetime.now().strftime("%Y-%m-%d")
        expected_file = tmp_path / "logs" / f"app_{today}.log"
        assert expected_file.exists()
        logger.handlers.clear()

    def test_log_message_is_written(self, tmp_path):
        """Verifica que mensagens são gravadas no arquivo de log."""
        logger = get_logger("test_write", base_dir=str(tmp_path))
        test_message = "Teste de escrita no log"
        logger.info(test_message)

        today = datetime.now().strftime("%Y-%m-%d")
        log_file = tmp_path / "logs" / f"app_{today}.log"
        content = log_file.read_text(encoding="utf-8")
        assert test_message in content
        logger.handlers.clear()

    def test_log_format_contains_level(self, tmp_path):
        """Verifica que o formato do log inclui o nível (INFO, ERROR, etc)."""
        logger = get_logger("test_format", base_dir=str(tmp_path))
        logger.warning("Alerta de teste")

        today = datetime.now().strftime("%Y-%m-%d")
        log_file = tmp_path / "logs" / f"app_{today}.log"
        content = log_file.read_text(encoding="utf-8")
        assert "[WARNING]" in content
        logger.handlers.clear()

    def test_no_duplicate_handlers(self, tmp_path):
        """Verifica que chamar get_logger múltiplas vezes não duplica handlers."""
        logger1 = get_logger("test_dedup", base_dir=str(tmp_path))
        handler_count = len(logger1.handlers)
        logger2 = get_logger("test_dedup", base_dir=str(tmp_path))
        assert len(logger2.handlers) == handler_count
        logger1.handlers.clear()
