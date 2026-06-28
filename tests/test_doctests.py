"""
Ejecuta los ejemplos doctest documentados en el código de la aplicación.

La Tarea 02.04 admite Doctest como uno de los frameworks de prueba válidos
para proyectos en Python. Este módulo corre los ejemplos incluidos en los
docstrings de app/services/usuario_service.py mediante doctest.testmod().
"""
import doctest

from app.services import usuario_service


def test_doctests_usuario_service():
    resultados = doctest.testmod(usuario_service, verbose=False)
    assert resultados.attempted > 0
    assert resultados.failed == 0
