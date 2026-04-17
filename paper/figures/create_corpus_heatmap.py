"""
Generate Figure 5: Corpus Statistics Heatmap
Shows per-domain statistics across all 46 domains.
"""
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

DOMAINS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'benchmark', 'domains')

CATEGORY_MAP = {
    # STEM
    'algebra-1': 'STEM', 'calculus': 'STEM', 'pre-calc': 'STEM',
    'linear-algebra': 'STEM', 'functions': 'STEM', 'geometry-course': 'STEM',
    'biology': 'STEM', 'genetics': 'STEM', 'chemistry': 'STEM',
    'bioinformatics': 'STEM', 'statistics-course': 'STEM',
    'quantum-computing': 'STEM', 'circuits': 'STEM',
    'digital-electronics': 'STEM', 'ecology': 'STEM', 'moss': 'STEM',
    'intro-to-physics-course': 'STEM', 'signal-processing': 'STEM',
    'fft-benchmarking': 'STEM', 'computer-science': 'STEM',
    # Professional
    'economics-course': 'Professional', 'organizational-analytics': 'Professional',
    'modeling-healthcare-data': 'Professional', 'conversational-ai': 'Professional',
    'automating-instructional-design': 'Professional', 'blockchain': 'Professional',
    'claude-skills': 'Professional', 'data-science-course': 'Professional',
    'Dementia': 'Professional', 'infographics': 'Professional',
    'intro-to-graph': 'Professional', 'it-management-graph': 'Professional',
    'learning-linux': 'Professional', 'machine-learning-textbook': 'Professional',
    'microsims': 'Professional',
    # Foundational
    'systems-thinking': 'Foundational', 'theory-of-knowledge': 'Foundational',
    'digital-citizenship': 'Foundational', 'prompt-class': 'Foundational',
    'tracking-ai-course': 'Foundational', 'us-geography': 'Foundational',
    'asl-book': 'Foundational', 'ethics-course': 'Foundational',
    'personal-finance': 'Foundational', 'reading-for-kindergarten': 'Foundational',
}

DISPLAY_NAMES = {
    'algebra-1': 'Algebra 1', 'asl-book': 'ASL',
    'automating-instructional-design': 'Auto. Instr. Design',
    'bioinformatics': 'Bioinformatics', 'biology': 'Biology',
    'blockchain': 'Blockchain', 'calculus': 'Calculus',
    'chemistry': 'Chemistry', 'circuits': 'Circuits',
    'claude-skills': 'Claude Skills', 'computer-science': 'Computer Science',
    'conversational-ai': 'Conversational AI',
    'data-science-course': 'Data Science', 'Dementia': 'Dementia',
    'digital-citizenship': 'Digital Citizenship',
    'digital-electronics': 'Digital Electronics',
    'ecology': 'Ecology', 'economics-course': 'Economics',
    'ethics-course': 'Ethics', 'fft-benchmarking': 'FFT Benchmarking',
    'functions': 'Functions', 'genetics': 'Genetics',
    'geometry-course': 'Geometry', 'infographics': 'Infographics',
    'intro-to-graph': 'Intro to Graphs',
    'intro-to-physics-course': 'Intro to Physics',
    'it-management-graph': 'IT Management',
    'learning-linux': 'Learning Linux', 'linear-algebra': 'Linear Algebra',
    'machine-learning-textbook': 'Machine Learning',
    'microsims': 'MicroSims',
    'modeling-healthcare-data': 'Healthcare Data', 'moss': 'Moss',
    'organizational-analytics': 'Org. Analytics',
    'personal-finance': 'Personal Finance', 'pre-calc': 'Pre-Calculus',
    'prompt-class': 'Prompt Engineering', 'quantum-computing': 'Quantum Computing',
    'reading-for-kindergarten': 'Reading (K)', 'signal-processing': 'Signal Processing',
    'statistics-course': 'Statistics', 'systems-thinking': 'Systems Thinking',
    'theory-of-knowledge': 'Theory of Knowledge',
    'tracking-ai-course': 'Tracking AI', 'us-geography': 'US Geography',
}


def load_domain_stats(domain_dir):
    csv_path = os.path.join(domain_dir, 'learning-graph.csv')
    if not os.path.exists(csv_path):
        return None

    concepts = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            deps = []
            dep_str = row.get('Dependencies', '').strip()
            if dep_str:
                deps = [d.strip() for d in dep_str.split('|') if d.strip()]
            concepts.append({
                'id': int(row['ConceptID']),
                'label': row['ConceptLabel'].strip(),
                'deps': deps,
                'taxonomy': row['TaxonomyID'].strip()
            })

    n_concepts = len(concepts)
    n_edges = sum(len(c['deps']) for c in concepts)
    n_taxonomies = len(set(c['taxonomy'] for c in concepts))
    n_foundations = sum(1 for c in concepts if not c['deps'])
    max_indegree = 0
    indegree = {}
    for c in concepts:
        for d in c['deps']:
            indegree[d] = indegree.get(d, 0) + 1
    max_indegree = max(indegree.values()) if indegree else 0
    mean_indegree = np.mean(list(indegree.values())) if indegree else 0
    edge_ratio = n_edges / n_concepts if n_concepts > 0 else 0

    return {
        'concepts': n_concepts,
        'edges': n_edges,
        'taxonomies': n_taxonomies,
        'foundations': n_foundations,
        'max_indegree': max_indegree,
        'mean_indegree': round(mean_indegree, 2),
        'edge_ratio': round(edge_ratio, 2),
    }


def main():
    # Collect stats
    data = {}
    for domain_name in sorted(os.listdir(DOMAINS_DIR)):
        domain_path = os.path.join(DOMAINS_DIR, domain_name)
        if not os.path.isdir(domain_path):
            continue
        if domain_name == 'unicorns':
            continue
        stats = load_domain_stats(domain_path)
        if stats and stats['concepts'] > 10:
            data[domain_name] = stats

    # Sort by category then concept count
    cat_order = {'STEM': 0, 'Professional': 1, 'Foundational': 2}
    domains = sorted(data.keys(),
                     key=lambda d: (cat_order.get(CATEGORY_MAP.get(d, 'Other'), 3),
                                    -data[d]['concepts']))

    # Build matrix
    metrics = ['concepts', 'edges', 'taxonomies', 'foundations', 'edge_ratio']
    metric_labels = ['Concepts', 'Edges', 'Taxonomy\nCategories', 'Foundation\nConcepts', 'Edge/Concept\nRatio']

    matrix = np.array([[data[d][m] for m in metrics] for d in domains])

    # Normalize each column to 0-1 using full-corpus min/max so colors are
    # comparable across the three per-category figures we render below.
    col_min = matrix.min(axis=0)
    col_max = matrix.max(axis=0)
    matrix_norm = (matrix - col_min) / (col_max - col_min + 1e-9)

    # Split into one figure per category.
    cat_list = [CATEGORY_MAP.get(d, '?') for d in domains]
    category_order = ['STEM', 'Professional', 'Foundational']
    slug = {'STEM': 'stem', 'Professional': 'professional',
            'Foundational': 'foundational'}

    for cat in category_order:
        rows = [i for i, c in enumerate(cat_list) if c == cat]
        if not rows:
            continue
        cat_domains = [domains[i] for i in rows]
        cat_labels = [DISPLAY_NAMES.get(d, d) for d in cat_domains]
        cat_matrix = matrix[rows]
        cat_norm = matrix_norm[rows]

        # Height scales with row count; minimum floor for very small subsets.
        fig_height = max(3.0, 0.35 * len(rows) + 1.8)
        fig, ax = plt.subplots(figsize=(9, fig_height))

        ax.imshow(cat_norm, cmap='YlOrRd', aspect='auto',
                  vmin=0, vmax=1)

        # Column labels at the top so they can't be clipped by a page break.
        ax.set_xticks(np.arange(len(metrics)))
        ax.set_xticklabels(metric_labels, fontsize=11, ha='center')
        ax.xaxis.set_ticks_position('top')
        ax.xaxis.set_label_position('top')
        ax.tick_params(axis='x', which='both', length=0, pad=6)

        ax.set_yticks(np.arange(len(cat_domains)))
        ax.set_yticklabels(cat_labels, fontsize=10)

        # Value overlays
        for i in range(len(cat_domains)):
            for j in range(len(metrics)):
                val = cat_matrix[i, j]
                text = (f'{val:.2f}' if isinstance(val, float) and val != int(val)
                        else f'{int(val)}')
                color = 'white' if cat_norm[i, j] > 0.6 else 'black'
                ax.text(j, i, text, ha='center', va='center',
                        fontsize=9, color=color)

        # Light cell borders to separate rows visually
        ax.set_xticks(np.arange(-0.5, len(metrics), 1), minor=True)
        ax.set_yticks(np.arange(-0.5, len(cat_domains), 1), minor=True)
        ax.grid(which='minor', color='white', linewidth=1.2)
        ax.tick_params(which='minor', length=0)

        ax.set_title(f'McCreary Intelligent Textbook Corpus --- {cat} Domains',
                     fontsize=13, fontweight='bold', pad=28)

        plt.tight_layout()
        output_path = os.path.join(os.path.dirname(__file__),
                                   f'corpus-heatmap-{slug[cat]}.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        print(f'Saved: {output_path}')

    # Also print stats table
    print(f'\n{"Domain":<30} {"Concepts":>8} {"Edges":>6} {"Taxon":>5} {"Found":>5} {"E/C":>5}')
    print('-' * 65)
    for d in domains:
        s = data[d]
        print(f'{DISPLAY_NAMES.get(d, d):<30} {s["concepts"]:>8} {s["edges"]:>6} '
              f'{s["taxonomies"]:>5} {s["foundations"]:>5} {s["edge_ratio"]:>5.2f}')
    print(f'\n{"TOTAL":<30} {sum(data[d]["concepts"] for d in domains):>8} '
          f'{sum(data[d]["edges"] for d in domains):>6}')


if __name__ == '__main__':
    main()
