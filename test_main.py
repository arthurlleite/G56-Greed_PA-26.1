import pytest
from main import ordenar_por_prazo, calcular_cronograma, calcular_atraso_maximo


def test_ordenacao_por_prazo():
    tarefas = [
        {'id': 1, 'nome': 'A', 'duracao': 2, 'prazo': 10},
        {'id': 2, 'nome': 'B', 'duracao': 1, 'prazo': 5},
        {'id': 3, 'nome': 'C', 'duracao': 3, 'prazo': 8},
    ]
    ordenadas = ordenar_por_prazo(tarefas)
    prazos = [t['prazo'] for t in ordenadas]
    assert prazos == sorted(prazos)


def test_atraso_nunca_negativo():
    tarefas = [
        {'id': 1, 'nome': 'A', 'duracao': 2, 'prazo': 100},
        {'id': 2, 'nome': 'B', 'duracao': 1, 'prazo': 50},
    ]
    ordenadas = ordenar_por_prazo(tarefas)
    cronograma = calcular_cronograma(ordenadas)
    for item in cronograma:
        assert item['atraso'] >= 0


def test_atraso_maximo_correto():
    # Tarefa A: duracao 5, prazo 4 -> termina em 5, atraso = 1
    # Tarefa B: duracao 3, prazo 10 -> termina em 8, atraso = 0
    tarefas = [
        {'id': 1, 'nome': 'A', 'duracao': 5, 'prazo': 4},
        {'id': 2, 'nome': 'B', 'duracao': 3, 'prazo': 10},
    ]
    ordenadas = ordenar_por_prazo(tarefas)
    cronograma = calcular_cronograma(ordenadas)
    atraso_max = calcular_atraso_maximo(cronograma)
    assert atraso_max == 1


def test_sem_atraso():
    tarefas = [
        {'id': 1, 'nome': 'A', 'duracao': 2, 'prazo': 10},
        {'id': 2, 'nome': 'B', 'duracao': 3, 'prazo': 20},
    ]
    ordenadas = ordenar_por_prazo(tarefas)
    cronograma = calcular_cronograma(ordenadas)
    atraso_max = calcular_atraso_maximo(cronograma)
    assert atraso_max == 0
