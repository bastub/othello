from quickchart import QuickChart

def method_result_to_chart(n, depth, list_all_game_time_mean, list_all_play_time, max_plays, list_win, list_los, list_eq):
    
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "line",
        "data": {
            "labels": [str(i) for i in range(max_plays)],
            "datasets": [{
                "label": "Minimax",
                "data": list_all_play_time[0],
                "fill": "false"
            },
            {
                "label": "Negamax",
                "data": list_all_play_time[1],
                "fill": "false"
            },
            {
                "label": "AlphaBeta - MiniMax",
                "data": list_all_play_time[2],
                "fill": "false"
            },
            {
                "label": "AlphaBeta - Negamax",
                "data": list_all_play_time[3],
                "fill": "false"
            }]
        },
        "options": {
            "title": {
            "display": "true",
            "text": "Temps moyen d'un coup (" + str(n) + " parties, profondeur " + str(depth) + ")"
            },
            "scales": {
                "xAxes": [
                {
                    "scaleLabel": {
                    "display": "true",
                    "labelString": 'Coup n°',
                    },
                },
                ],
                "yAxes": [
                {
                    "scaleLabel": {
                    "display": "true",
                    "labelString": 'Temps (s)',
                    },
                },
                ]
            }
        }
            
    }
    
    qc.to_file('charts/method' + str(depth) + '_play_time.png')
    
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "bar",
        "data": {
            "labels": ["Minimax", "Negamax", "AlphaBeta - MiniMax", "AlphaBeta - Negamax"],
            "datasets": [{
                "label": "Temps moyen d'une partie (s)",
                "data": list_all_game_time_mean
            }]
        },
        "options": {
            "title": {
            "display": "true",
            "text": "Temps moyen d'une partie (" + str(n) + " parties, profondeur " + str(depth) + ")"
            }
        }
    }
    
    qc.to_file('charts/method' + str(depth) + '_game_time.png')
    
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "bar",
        "data": {
            "labels": ["MiniMax", "Negamax", "AlphaBeta - MiniMax", "AlphaBeta - Negamax"],
            "datasets": [{
                "label": "Victoires",
                "data": list_win,
                "backgroundColor": 'rgb(0, 129, 64)'
            },
            {
                "label": "Egalités",
                "data": list_eq,
                "backgroundColor": 'rgb(247, 112, 20)'
            },
            {
                "label": "Défaites",
                "data": list_los,
                "backgroundColor": 'rgb(247, 0, 0)'
            }]
        },
        "options": {
            "title": {
            "display": "true",
            "text": "Résultats (" + str(n) + " parties, profondeur " + str(depth) + ")"
            }
        }
    }
    
    qc.to_file('charts/method' + str(depth) + '_result.png')
    
def depth_result_to_chart(n, list_all_game_time_mean, list_all_play_time, max_plays, list_win, list_los, list_eq):
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "line",
        "data": {
            "labels": [str(i) for i in range(max_plays)],
            "datasets": [{
                "label": "Profondeur 1",
                "data": list_all_play_time[0],
                "fill": "false"
            },
            {
                "label": "Profondeur 2",
                "data": list_all_play_time[1],
                "fill": "false"
            },
            {
                "label": "Profondeur 3",
                "data": list_all_play_time[2],
                "fill": "false"
            }]
        },
        "options": {
            "title": {
            "display": "true",
            "text": "Temps moyen d'un coup (" + str(n) + " parties)"
            },
            "scales": {
                "xAxes": [
                {
                    "scaleLabel": {
                    "display": "true",
                    "labelString": 'Coup n°',
                    },
                },
                ],
                "yAxes": [
                {
                    "scaleLabel": {
                    "display": "true",
                    "labelString": 'Temps (s)',
                    },
                },
                ]
            }
        }
    }
    
    qc.to_file('charts/depth_play_time.png')
    
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "bar",
        "data": {
            "labels": ["Profondeur 1", "Profondeur 2", "Profondeur 3"],
            "datasets": [{
                "label": "Temps moyen d'une partie (s)",
                "data": list_all_game_time_mean
            }]
        },
        "options": {
            "title": {
            "display": "true",
            "text": "Temps moyen d'une partie (" + str(n) + " parties)"
            }
        }
    }
    
    qc.to_file('charts/depth_game_time.png')
    
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "bar",
        "data": {
            "labels": ["Profondeur 1", "Profondeur 2", "Profondeur 3"],
            "datasets": [{
                "label": "Victoires",
                "data": list_win,
                "backgroundColor": 'rgb(0, 129, 64)'
            },
            {
                "label": "Egalités",
                "data": list_eq,
                "backgroundColor": 'rgb(247, 112, 20)'
            },
            {
                "label": "Défaites",
                "data": list_los,
                "backgroundColor": 'rgb(247, 0, 0)'
            }]
        },
        "options": {
            "title": {
            "display": "true",
            "text": "Résultats (" + str(n) + " parties)"
            }
        }
    }
    
    qc.to_file('charts/depth_result.png')
    
def heuristic_result_to_chart(n, list_all_game_time_mean, list_all_play_time, max_plays, list_win, list_los, list_eq):
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "line",
        "data": {
            "labels": [str(i) for i in range(max_plays)],
            "datasets": [{
                "label": "Nombre de pions",
                "data": list_all_play_time[0],
                "fill": "false"
            },
            {
                "label": "Matrice de valeurs tactiques 1",
                "data": list_all_play_time[1],
                "fill": "false"
            },
            {
                "label": "Matrice de valeurs tactiques 2",
                "data": list_all_play_time[2],
                "fill": "false"
            }]
        },
        "options": {
            "title": {
            "display": "true",
            "text": "Temps moyen d'un coup (" + str(n) + " parties)"
            },
            "scales": {
                "xAxes": [
                {
                    "scaleLabel": {
                    "display": "true",
                    "labelString": 'Coup n°',
                    },
                },
                ],
                "yAxes": [
                {
                    "scaleLabel": {
                    "display": "true",
                    "labelString": 'Temps (s)',
                    },
                },
                ]
            }
        }
    }
    
    qc.to_file('charts/heuristic_play_time.png')
    
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "bar",
        "data": {
            "labels": ["Nombre de pions", "Matrice de valeurs tactiques 1", "Matrice de valeurs tactiques 2"],
            "datasets": [{
                "label": "Temps moyen d'une partie (s)",
                "data": list_all_game_time_mean
            }]
        },
        "options": {
            "title": {
            "display": "true",
            "text": "Temps moyen d'une partie (" + str(n) + " parties)"
            }
        }
    }
    
    qc.to_file('charts/heuristic_game_time.png')
    
    qc = QuickChart()
    
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "bar",
        "data": {
            "labels": ["Nombre de pions", "Matrice de valeurs tactiques 1", "Matrice de valeurs tactiques 2"],
            "datasets": [{
                "label": "Victoires",
                "data": list_win,
                "backgroundColor": 'rgb(0, 129, 64)'
            },
            {
                "label": "Egalités",
                "data": list_eq,
                "backgroundColor": 'rgb(247, 112, 20)'
            },
            {
                "label": "Défaites",
                "data": list_los,
                "backgroundColor": 'rgb(247, 0, 0)'
            }]
        },
        "options": {
            "title": {
            "display": "true",
            "text": "Résultats (" + str(n) + " parties)"
            }
        }
    }
    
    qc.to_file('charts/heuristic_result.png')
    
def mixed_result_to_chart(n, list_all_game_time_mean, list_all_play_time, max_plays, list_win, list_los, list_eq):
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "line",
        "data": {
            "labels": [str(i) for i in range(max_plays)],
            "datasets": [{
                "label": "Non Mixte",
                "data": list_all_play_time[0],
                "fill": "false"
            },
            {
                "label": "Mixte (Matrice 1 et Nombre de pions)",
                "data": list_all_play_time[1],
                "fill": "false"
            }]
        },
        "options": {
            "title": {
            "display": "true",
            "text": "Temps moyen d'un coup (" + str(n) + " parties)"
            },
            "scales": {
                "xAxes": [
                {
                    "scaleLabel": {
                    "display": "true",
                    "labelString": 'Coup n°',
                    },
                },
                ],
                "yAxes": [
                {
                    "scaleLabel": {
                    "display": "true",
                    "labelString": 'Temps (s)',
                    },
                },
                ]
            }
        }
    }
    
    qc.to_file('charts/mixed_play_time.png')
    
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "bar",
        "data": {
            "labels": ["Non Mixte", "Mixte (Matrice 1 et Nombre de pions)"],
            "datasets": [{
                "label": "Temps moyen d'une partie (s)",
                "data": list_all_game_time_mean
            }]
        },
        "options": {
            "title": {
            "display": "true",
            "text": "Temps moyen d'une partie (" + str(n) + " parties)"
            }
        }
    }
    
    qc.to_file('charts/mixed_game_time.png')
    
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "bar",
        "data": {
            "labels": ["Non Mixte", "Mixte (Matrice 1 et Nombre de pions)"],
            "datasets": [{
                "label": "Victoires",
                "data": list_win,
                "backgroundColor": 'rgb(0, 129, 64)'
            },
            {
                "label": "Egalités",
                "data": list_eq,
                "backgroundColor": 'rgb(247, 112, 20)'
            },
            {
                "label": "Défaites",
                "data": list_los,
                "backgroundColor": 'rgb(247, 0, 0)'
            }]
        },
        "options": {
            "title": {
            "display": "true",
            "text": "Résultats (" + str(n) + " parties)"
            }
        }
    }
    
    qc.to_file('charts/mixed_result.png')
    
def memory_result_to_chart(n, list_all_game_time_mean, list_all_play_time, max_plays, list_win, list_los, list_eq):
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "line",
        "data": {
            "labels": [str(i) for i in range(max_plays)],
            "datasets": [{
                "label": "Sans mémoire",
                "data": list_all_play_time[0],
                "fill": "false"
            },
            {
                "label": "Avec Memoire",
                "data": list_all_play_time[1],
                "fill": "false"
            }]
        },
        "options": {
            "title": {
            "display": "true",
            "text": "Temps moyen d'un coup (" + str(n) + " parties)"
            },
            "scales": {
                "xAxes": [
                {
                    "scaleLabel": {
                    "display": "true",
                    "labelString": 'Coup n°',
                    },
                },
                ],
                "yAxes": [
                {
                    "scaleLabel": {
                    "display": "true",
                    "labelString": 'Temps (s)',
                    },
                },
                ]
            }
        }
    }
    
    qc.to_file('charts/memory_play_time.png')
    
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "bar",
        "data": {
            "labels": ["Sans mémoire", "Avec Memoire"],
            "datasets": [{
                "label": "Temps moyen d'une partie (s)",
                "data": list_all_game_time_mean
            }]
        },
        "options": {
            "title": {
            "display": "true",
            "text": "Temps moyen d'une partie (" + str(n) + " parties)"
            }
        }
    }
    
    qc.to_file('charts/memory_game_time.png')
    
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "bar",
        "data": {
            "labels": ["Sans mémoire", "Avec Memoire"],
            "datasets": [{
                "label": "Victoires",
                "data": list_win,
                "backgroundColor": 'rgb(0, 129, 64)'
            },
            {
                "label": "Egalités",
                "data": list_eq,
                "backgroundColor": 'rgb(247, 112, 20)'
            },
            {
                "label": "Défaites",
                "data": list_los,
                "backgroundColor": 'rgb(247, 0, 0)'
            }]
        },
        "options": {
            "title": {
            "display": "true",
            "text": "Résultats (" + str(n) + " parties)"
            }
        }
    }
    
    qc.to_file('charts/memory_result.png')
    
    
def method_alpha_beta_result_to_chart(n, depth, list_all_game_time_mean, list_all_play_time, max_plays, list_win, list_los, list_eq):
    
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "line",
        "data": {
            "labels": [str(i) for i in range(max_plays)],
            "datasets": [{
                "label": "AlphaBeta - MiniMax",
                "data": list_all_play_time[0],
                "fill": "false"
            },
            {
                "label": "AlphaBeta - Negamax",
                "data": list_all_play_time[1],
                "fill": "false"
            }]
        },
        "options": {
            "title": {
            "display": "true",
            "text": "Temps moyen d'un coup (" + str(n) + " parties, profondeur " + str(depth) + ")"
            },
            "scales": {
                "xAxes": [
                {
                    "scaleLabel": {
                    "display": "true",
                    "labelString": 'Coup n°',
                    },
                },
                ],
                "yAxes": [
                {
                    "scaleLabel": {
                    "display": "true",
                    "labelString": 'Temps (s)',
                    },
                },
                ]
            }
        }
            
    }
    
    qc.to_file('charts/method_alpha_beta' + str(depth) + '_play_time.png')
    
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "bar",
        "data": {
            "labels": ["AlphaBeta - MiniMax", "AlphaBeta - Negamax"],
            "datasets": [{
                "label": "Temps moyen d'une partie (s)",
                "data": list_all_game_time_mean
            }]
        },
        "options": {
            "title": {
            "display": "true",
            "text": "Temps moyen d'une partie (" + str(n) + " parties, profondeur " + str(depth) + ")"
            }
        }
    }
    
    qc.to_file('charts/method_alpha_beta' + str(depth) + '_game_time.png')
    
    qc = QuickChart()
    qc.width = 500
    qc.height = 300
    qc.device_pixel_ratio = 2.0
    qc.config = {
        "type": "bar",
        "data": {
            "labels": ["AlphaBeta - MiniMax", "AlphaBeta - Negamax"],
            "datasets": [{
                "label": "Victoires",
                "data": list_win,
                "backgroundColor": 'rgb(0, 129, 64)'
            },
            {
                "label": "Egalités",
                "data": list_eq,
                "backgroundColor": 'rgb(247, 112, 20)'
            },
            {
                "label": "Défaites",
                "data": list_los,
                "backgroundColor": 'rgb(247, 0, 0)'
            }]
        },
        "options": {
            "title": {
            "display": "true",
            "text": "Résultats (" + str(n) + " parties, profondeur " + str(depth) + ")"
            }
        }
    }
    
    qc.to_file('charts/method_alpha_beta' + str(depth) + '_result.png')