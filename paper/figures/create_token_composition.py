"""
Generate Figure 6: Token Composition Stacked Bar Chart
Shows where tokens go for each system: query, retrieval context,
system prompt, and completion.

Uses estimated token profiles from the tokenomics framework.
Update with actual data after experimental runs.
"""
import numpy as np
import matplotlib.pyplot as plt
import os


def main():
    systems = ['RAG', 'GraphRAG', 'CKG']

    # Estimated token breakdown (mean per query)
    # Based on tokenomics.md profiles
    # Components: query_tokens, system_prompt, retrieval_context, completion
    components = ['Query', 'System Prompt', 'Retrieval Context', 'Completion']

    # RAG: ~4000 total (100 query + 200 system + 2560 retrieval + 1140 completion)
    # GraphRAG: ~5000 total (100 query + 200 system + 3500 retrieval + 1200 completion)
    # CKG: ~300 total (100 query + 50 system + 80 retrieval + 70 completion)
    data = {
        'RAG':      [100, 200, 2560, 1140],
        'GraphRAG': [100, 200, 3500, 1200],
        'CKG':      [100,  50,   80,   70],
    }

    colors = ['#4285f4', '#fbbc04', '#ea4335', '#34a853']

    fig, ax = plt.subplots(figsize=(8, 6))

    x = np.arange(len(systems))
    width = 0.5

    bottoms = np.zeros(len(systems))
    for i, component in enumerate(components):
        values = [data[s][i] for s in systems]
        bars = ax.bar(x, values, width, bottom=bottoms, label=component,
                      color=colors[i], edgecolor='white', linewidth=0.5)

        # Add value labels on bars (only if segment is large enough)
        for j, (v, b) in enumerate(zip(values, bottoms)):
            if v > 150:  # Only label segments > 150 tokens
                ax.text(x[j], b + v/2, f'{v:,}', ha='center', va='center',
                        fontsize=9, fontweight='bold', color='white')

        bottoms += values

    # Add total labels on top
    for j, s in enumerate(systems):
        total = sum(data[s])
        ax.text(x[j], total + 80, f'{total:,}\ntokens', ha='center',
                va='bottom', fontsize=10, fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(systems, fontsize=12, fontweight='bold')
    ax.set_ylabel('Tokens per Query', fontsize=12)
    ax.set_title('Token Composition by System\n(Estimated Mean per Query)',
                 fontsize=14, fontweight='bold', pad=15)

    ax.legend(loc='upper right', fontsize=10)
    ax.set_ylim(0, 6000)

    # Add efficiency annotation
    rag_total = sum(data['RAG'])
    ckg_total = sum(data['CKG'])
    ratio = rag_total / ckg_total
    ax.annotate(f'RAG uses {ratio:.0f}x more tokens than CKG',
                xy=(2, ckg_total), xytext=(1.5, 3500),
                fontsize=10, fontstyle='italic',
                arrowprops=dict(arrowstyle='->', color='gray'),
                color='gray')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    output_path = os.path.join(os.path.dirname(__file__), 'token-composition.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f'Saved: {output_path}')


if __name__ == '__main__':
    main()
