import csv

# Horário de início do dia: 6h00 (em minutos desde meia-noite)
HORA_INICIO = 6 * 60


def minutos_para_hhmm(minutos):
    """Converte minutos desde 6h00 para horário no formato HH:MM."""
    total = HORA_INICIO + minutos
    h = total // 60
    m = total % 60
    return f"{h:02d}:{m:02d}"


def ler_tarefas(caminho_csv):
    tarefas = []
    with open(caminho_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tarefas.append({
                'id': int(row['id']),
                'nome': row['nome'],
                'duracao': int(row['duracao']),
                'prazo': int(row['prazo']),
            })
    return tarefas


def ordenar_por_prazo(tarefas):
    # Escolha gulosa: processa sempre a tarefa com menor prazo (EDD)
    return sorted(tarefas, key=lambda t: t['prazo'])


def calcular_cronograma(tarefas_ordenadas):
    cronograma = []
    tempo_atual = 0
    for tarefa in tarefas_ordenadas:
        inicio = tempo_atual
        termino = inicio + tarefa['duracao']
        atraso = max(0, termino - tarefa['prazo'])
        cronograma.append({
            **tarefa,
            'inicio': inicio,
            'termino': termino,
            'atraso': atraso,
        })
        tempo_atual = termino
    return cronograma


def calcular_atraso_maximo(cronograma):
    return max(item['atraso'] for item in cronograma)


def exibir_tabela(cronograma):
    cabecalho = (
        f"{'#':<5} {'ID':<4} {'Tarefa':<48} {'Dur.':<7} "
        f"{'Prazo':<7} {'Inicio':<7} {'Termino':<9} {'Atraso'}"
    )
    print()
    print("  Rotina do dia — horarios a partir das 06:00 | duracao e atraso em minutos")
    print()
    print(cabecalho)
    print("-" * 104)
    for i, item in enumerate(cronograma, start=1):
        atraso_str = f"{item['atraso']}min" if item['atraso'] > 0 else "-"
        print(
            f"{i:<5} {item['id']:<4} {item['nome']:<48} {item['duracao']:<7} "
            f"{minutos_para_hhmm(item['prazo']):<7} "
            f"{minutos_para_hhmm(item['inicio']):<7} "
            f"{minutos_para_hhmm(item['termino']):<9} "
            f"{atraso_str}"
        )


def main():
    tarefas = ler_tarefas('tarefas.csv')
    tarefas_ordenadas = ordenar_por_prazo(tarefas)
    cronograma = calcular_cronograma(tarefas_ordenadas)

    exibir_tabela(cronograma)

    atraso_maximo = calcular_atraso_maximo(cronograma)
    print(f"\nAtraso maximo encontrado: {atraso_maximo} minuto(s)")


if __name__ == '__main__':
    main()
