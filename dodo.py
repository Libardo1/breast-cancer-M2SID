def task_plot_missing_matrix():
    return {
        'actions': ['python scripts/plot_missing_values.py'],
        'file_dep': ['data/recepteurs.csv'],
        'targets': ['figures/missing_matrix.png']
    }


def task_handle_missing_values():
    return {
        'actions': ['python scripts/handle_missing_values.py'],
        'file_dep': ['data/recepteurs.csv'],
        'targets': ['data/recepteurs_v2.csv']
    }


def task_extract_features():
    return {
        'actions': ['python scripts/extract_features.py'],
        'file_dep': ['data/recepteurs_v2.csv'],
        'targets': ['data/recepteurs_v3.csv']
    }
