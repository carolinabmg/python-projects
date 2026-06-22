"""
file_manager.py — Camada de persistência.
Todo acesso a disco passa por aqui; nenhuma outra classe abre arquivo.
"""

import json
import os


class FileManager:
    """Lê, grava e apaga arquivos JSON de forma centralizada."""

    @staticmethod
    def ler(caminho: str, padrao=None):
        """
        Lê um arquivo JSON e devolve o conteúdo.
        Devolve `padrao` se o arquivo não existir ou estiver corrompido.
        """
        if not os.path.exists(caminho):
            return padrao
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return padrao

    @staticmethod
    def gravar(caminho: str, dados) -> bool:
        """
        Grava `dados` como JSON em `caminho`.
        Devolve True em caso de sucesso, False em caso de erro.
        """
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            return True
        except OSError:
            return False

    @staticmethod
    def apagar(caminho: str) -> bool:
        """Apaga o arquivo se existir. Devolve True se apagou."""
        if os.path.exists(caminho):
            try:
                os.remove(caminho)
                return True
            except OSError:
                return False
        return False

    @staticmethod
    def existe(caminho: str) -> bool:
        """Verifica se o arquivo existe."""
        return os.path.exists(caminho)
