import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from main import ler_tarefas, ordenar_por_prazo, calcular_cronograma, calcular_atraso_maximo, minutos_para_hhmm

COR_NO_PRAZO = '#4caf50'
COR_ATRASADO = '#f44336'
COR_DEADLINE = '#ff9800'
BG_FIGURA    = '#1a1a2e'
BG_AXES      = '#16213e'


def configurar_eixo_x(ax, termino_max):
    """Configura o eixo X para mostrar horários HH:MM a cada hora."""
    ticks = list(range(0, termino_max + 120, 60))
    ax.set_xticks(ticks)
    ax.set_xticklabels([minutos_para_hhmm(t) for t in ticks],
                       rotation=45, ha='right', fontsize=9)


def gerar_gantt(cronograma):
    n = len(cronograma)
    atraso_max = calcular_atraso_maximo(cronograma)
    termino_max = max(item['termino'] for item in cronograma)

    fig, ax = plt.subplots(figsize=(20, 11))
    fig.patch.set_facecolor(BG_FIGURA)
    ax.set_facecolor(BG_AXES)

    altura = 0.55

    for i, item in enumerate(cronograma):
        inicio  = item['inicio']
        termino = item['termino']
        prazo   = item['prazo']

        # Parte dentro do prazo
        fim_verde = min(termino, prazo)
        if fim_verde > inicio:
            ax.barh(i, fim_verde - inicio, left=inicio,
                    color=COR_NO_PRAZO, height=altura,
                    edgecolor='none', alpha=0.88, zorder=2)

        # Parte após o prazo (atraso)
        if termino > prazo:
            inicio_vermelho = max(inicio, prazo)
            ax.barh(i, termino - inicio_vermelho, left=inicio_vermelho,
                    color=COR_ATRASADO, height=altura,
                    edgecolor='none', alpha=0.88, zorder=2)

        # Marcador de deadline: linha + triângulo
        ax.plot([prazo, prazo], [i - altura / 2, i + altura / 2],
                color=COR_DEADLINE, linewidth=2.5, zorder=5)
        ax.plot(prazo, i + altura / 2 + 0.05,
                marker='v', color=COR_DEADLINE, markersize=7, zorder=6)

        # Horário de término exibido dentro da barra
        centro_x = inicio + (termino - inicio) / 2
        ax.text(centro_x, i, minutos_para_hhmm(termino),
                ha='center', va='center',
                color='white', fontsize=7.5, fontweight='bold', zorder=7)

        # Rótulo de atraso à direita (só quando há atraso)
        if item['atraso'] > 0:
            ax.text(termino + 6, i, f'+{item["atraso"]}min',
                    va='center', color=COR_ATRASADO,
                    fontsize=8.5, fontweight='bold', zorder=7)

    # Eixo Y com numeração e nome da tarefa
    rotulos = [f"{idx + 1:>2}. {item['nome']}" for idx, item in enumerate(cronograma)]
    ax.set_yticks(range(n))
    ax.set_yticklabels(rotulos, color='white', fontsize=9.5)
    ax.invert_yaxis()

    configurar_eixo_x(ax, termino_max)
    ax.set_xlabel('Horário do dia', color='#cccccc', fontsize=11, labelpad=10)
    ax.tick_params(colors='#aaaaaa')
    ax.set_xlim(left=0, right=termino_max + 60)

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.grid(axis='x', color='#2a3a5e', linestyle='--',
            linewidth=0.8, alpha=0.7, zorder=1)

    ax.set_title(
        'Rotina de Uma Mae Solo  ·  Algoritmo Guloso EDD (Earliest Due Date)\n'
        f'Atraso maximo encontrado: {atraso_max} minuto(s)',
        color='white', fontsize=13, fontweight='bold', pad=18
    )

    leg_handles = [
        mpatches.Patch(color=COR_NO_PRAZO, label='Tarefa concluida no prazo'),
        mpatches.Patch(color=COR_ATRASADO, label='Tarefa concluida com atraso'),
        plt.Line2D([0], [0], color=COR_DEADLINE, linewidth=2.5,
                   marker='v', markersize=7, label='Prazo (deadline)'),
    ]
    ax.legend(handles=leg_handles, loc='upper right',
              facecolor='#0f3460', edgecolor='#334477',
              labelcolor='white', fontsize=10, framealpha=0.9)

    plt.tight_layout()
    plt.savefig('cronograma.png', dpi=150,
                bbox_inches='tight', facecolor=fig.get_facecolor())
    print("Grafico salvo como 'cronograma.png'")
    plt.show()


def main():
    tarefas = ler_tarefas('tarefas.csv')
    tarefas_ordenadas = ordenar_por_prazo(tarefas)
    cronograma = calcular_cronograma(tarefas_ordenadas)
    gerar_gantt(cronograma)


if __name__ == '__main__':
    main()
