# Modified 6interactive_labormarket.py
import os
import dash
from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
import shutil

# Source location
html_dir = "assets"

# Create a standard assets folder
assets_dir = "assets"

# Initialize the app
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.FLATLY],
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

server = app.server  # Needed for deployment

# Define key metrics
key_metrics = {
    "initial_workforce": 4555,
    "final_workforce": 5071,
    "projected_shortage_2030": 847,
    "avg_monthly_shortage": 21,
    "total_cumulative_shortage": 1513,
    "training_multiplier_needed": 2.84,
    "mobility_multiplier_needed": 3.21
}

# Define the app layout
app.layout = dbc.Container([
    # Navigation bar
    dbc.Navbar(
        dbc.Container([
            html.A(
                dbc.Row([
                    dbc.Col(dbc.NavbarBrand("Industrial Machinery Mechanics Forecast", className="ms-2")),
                ],
                    align="center",
                    className="g-0",
                ),
                href="#",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(html.A("Executive Summary", href="#summary", className="nav-link")),
                    dbc.NavItem(html.A("Demand Analysis", href="#demand", className="nav-link")),
                    dbc.NavItem(html.A("Supply Analysis", href="#supply", className="nav-link")),
                    dbc.NavItem(html.A("Job Evolution", href="#jobs", className="nav-link")),
                    dbc.NavItem(html.A("Shortage Projections", href="#shortage", className="nav-link")),
                ], className="ms-auto", navbar=True),
                id="navbar-collapse",
                navbar=True,
            ),
        ]),
        color="primary",
        dark=True,
        className="mb-4 sticky-top",
    ),

    # Intro Panel
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H2("Industrial Machinery Mechanics Workforce Forecast (2025-2030)", className="text-primary"),
                html.P("Predicting workforce shortages in the Charlotte region using supply-demand labor market modeling",
                       className="lead"),
                html.P([
                    "This dashboard presents the projected workforce shortages for Industrial Machinery Mechanics in Charlotte, utilizing ",
                    html.Strong("dual-pool modeling"),
                    " to track both employed workers and the available pool of qualified candidates."
                ]),
                html.Hr(),
            ], className="p-3 bg-light rounded")
        ], width=12)
    ], className="mb-4"),

    # ==================================== SECTION 1: EXECUTIVE SUMMARY ====================================
    dbc.Row([
        dbc.Col([
            html.H3("Executive Summary", id="summary", className="mb-3 section-header"),
            html.P(
                "Projected workforce shortages driven by aging workforce, insufficient training pipeline capacity, and significant turnover",
                className="text-muted"),
        ], width=12)
    ], className="mb-3"),

    dbc.Row([
        # Key metrics cards
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Current Workforce (2025)", className="card-title"),
                    html.H2(f"{key_metrics['initial_workforce']:,}", className="text-primary"),
                    html.P("NC Commerce Official Projection", className="text-muted"),
                ])
            ], className="h-100"),
        ], width=12, md=3, className="mb-4"),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Projected Workforce (2030)", className="card-title"),
                    html.H2(f"{key_metrics['final_workforce']:,}", className="text-primary"),
                    html.P("NC Commerce Official Projection", className="text-muted"),
                ])
            ], className="h-100"),
        ], width=12, md=3, className="mb-4"),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Average Monthly Shortages", className="card-title"),
                    html.H2(f"{key_metrics['avg_monthly_shortage']:,}", className="text-danger"),
                    html.P(f"Forecasted positions remaining vacant each month", className="text-muted"),
                ])
            ], className="h-100"),
        ], width=12, md=3, className="mb-4"),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Cumulative Shortage", className="card-title"),
                    html.H2(f"{key_metrics['total_cumulative_shortage']:,}", className="text-danger"),
                    html.P(f"Forecasted unfilled positions over 5-year period", className = 'text-muted'),
                ])
            ], className="h-100"),
        ], width=12, md=3, className="mb-4"),
    ]),

    # Central visualization
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Supply-Demand-Shortage Synthesis", className="card-title")),
                dbc.CardBody([
                    dcc.Loading(
                        html.Iframe(
                            id="central-viz",
                            src="/assets/central_visualization.html",
                            style={"width": "100%", "height": "500px", "border": "none"},
                        ),
                        type="circle"
                    ),
                    html.Div([
                        html.P([
                            html.Strong("Key Finding: "),
                            "The Industrial Machinery Mechanics workforce in Charlotte faces significant shortages through 2030, driven by high replacement demand (80% of openings from transfers and exits) and insufficient training pipeline capacity."
                        ], className="mt-3")
                    ])
                ])
            ])
        ], width=12)
    ], className="mb-4"),

    # Solutions summary
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("Addressing the Shortage", className="card-title")),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6("Training Pipeline Expansion", className="mb-3"),
                            html.P([
                                "Increasing training capacity by ",
                                html.Strong(f"{key_metrics['training_multiplier_needed']}x"),
                                " would close the shortage gap by 2030"
                            ]),
                            html.A("View Training Analysis", href="#supply",
                                  className="btn btn-outline-primary btn-sm mt-2")
                        ], width=12, md=4),

                        dbc.Col([
                            html.H6("Career Mobility Enhancement", className="mb-3"),
                            html.P([
                                "Increasing mobility inflows by ",
                                html.Strong(f"{key_metrics['mobility_multiplier_needed']}x"),
                                " from similar occupations would close the shortage gap"
                            ]),
                            html.A("View Mobility Analysis", href="#supply",
                                  className="btn btn-outline-primary btn-sm mt-2")
                        ], width=12, md=4),

                        dbc.Col([
                            html.H6("Matching Efficiency Improvement", className="mb-3"),
                            html.P([
                                "Improving the match between workforce supply and demand would invariably reduce shortages through better placement services"
                            ]),
                            html.A("View Matching Analysis", href="#shortage",
                                  className="btn btn-outline-primary btn-sm mt-2")
                        ], width=12, md=4),
                    ])
                ])
            ])
        ], width=12)
    ], className="mb-5"),

    # ==================================== SECTION 2: DEMAND ANALYSIS ====================================
    dbc.Row([
        dbc.Col([
            html.H3("Demand Analysis", id="demand", className="mb-3 section-header"),
            html.P(
                "Job posting forecasts and composition analysis for Industrial Machinery Mechanics in Charlotte region",
                className="text-muted"),
        ], width=12)
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([
            dbc.Tabs([
                dbc.Tab([
                    dcc.Loading(
                        html.Iframe(
                            id="scenario-forecasts",
                            src="/assets/scenario_forecasts.html",
                            style={"width": "100%", "height": "500px", "border": "none"},
                        ),
                        type="circle"
                    ),
                    html.Div([
                        html.P([
                            html.Strong("Key Finding: "),
                            "Baseline projections show a steady demand for Industrial Machinery Mechanics, with monthly job postings ranging from 50-70 positions through 2030."
                        ], className="mt-3")
                    ])
                ], label="Scenario Forecasts", tab_id="tab-scenario"),

                dbc.Tab([
                    dcc.Loading(id="loading-demand-breakdown", children=[
                        html.Iframe(
                            id="demand-breakdown",
                            src="/assets/demand_breakdown.html",
                            style={"width": "100%", "height": "500px", "border": "none"},
                        )
                    ], type="circle"),
                    html.Div([
                        html.P([
                            html.Strong("Key Finding: "),
                            "Replacement demand (exits and transfers) represents over 80% of total demand, highlighting the impact of an aging and mobile workforce."
                        ], className="mt-3")
                    ])
                ], label="Demand Components", tab_id="tab-components"),

                dbc.Tab([
                    dcc.Loading(
                        html.Iframe(
                            id="demand-composition",
                            src="/assets/demand_composition.html",
                            style={"width": "100%", "height": "500px", "border": "none"},
                        ),
                        type="circle"
                    ),
                    html.Div([
                        html.P([
                            html.Strong("Key Finding: "),
                            "Only 20% of demand comes from workforce growth, while 32.8% is from workforce exits (retirement) and 47.3% from occupational transfers."
                        ], className="mt-3")
                    ])
                ], label="Demand Composition", tab_id="tab-composition"),

                dbc.Tab([
                    dcc.Loading(
                        html.Iframe(
                            id="model-forecasts",
                            src="/assets/model_forecasts.html",
                            style={"width": "100%", "height": "500px", "border": "none"},
                        ),
                        type="circle"
                    ),
                    html.Div([
                        html.P([
                            html.Strong("Methodological Note: "),
                            "A hybrid SARIMAX/Prophet ensemble with time-varying weights provides optimal forecast accuracy, accounting for both short-term patterns and long-term structural factors."
                        ], className="mt-3")
                    ])
                ], label="Model Comparison", tab_id="tab-model"),
            ], id="demand-tabs", active_tab="tab-scenario")
        ], width=12)
    ], className="mb-5"),

    # ==================================== SECTION 3: SUPPLY ANALYSIS ====================================
    dbc.Row([
        dbc.Col([
            html.H3("Workforce Supply Analysis", id="supply", className="mb-3 section-header"),
            html.P("Training pipeline capacity and workforce flow analysis for Industrial Machinery Mechanics",
                   className="text-muted"),
        ], width=12)
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([
            dbc.Tabs([
                dbc.Tab([
                    dcc.Loading(
                        html.Iframe(
                            id="employment-comparison",
                            src="/assets/employment_comparison.html",
                            style={"width": "100%", "height": "500px", "border": "none"},
                        ),
                        type="circle"
                    ),
                    html.Div([
                        html.P([
                            html.Strong("Key Finding: "),
                            "Without intervention, the employed workforce will fall significantly short of NC Commerce projections, creating persistent shortages."
                        ], className="mt-3")
                    ])
                ], label="Employment Trajectory", tab_id="tab-employment"),

                dbc.Tab([
                    dcc.Loading(
                        html.Iframe(
                            id="workforce_composition",
                            src="/assets/workforce_composition.html",
                            style={"width": "100%", "height": "500px", "border": "none"},
                        ),
                        type="circle"
                    ),
                    html.Div([
                        html.P([
                            html.Strong("Key Finding: "),
                            "Mobility outflows are particularly strong, with retirements making up the largest portion of separations. Mobility inflows are taken form the pool of workers from the 10 most similar occupations (as defined by O*NET) and their respective mobility rates, which contribute to an available pool of workers. Retirement distributions from 2024 distribution show a mid-heavy, noting the value of technical expertise in this occupation and low younger entrants. Age distribution for this occupation comes from the latest IPUMS data in North Carolina."
                        ], className="mt-3")
                    ])
                ], label="Workforce Composition", tab_id="tab-workforce"),

                dbc.Tab([
                    dbc.Row([
                        dbc.Col([
                            dcc.Loading(
                                html.Iframe(
                                    id="enrollment-projections",
                                    src="/assets/enrollment_projections.html",
                                    style={"width": "100%", "height": "400px", "border": "none"},
                                ),
                                type="circle"
                            )
                        ], width=12, lg=6),

                        dbc.Col([
                            dcc.Loading(
                                html.Iframe(
                                    id="historical-projected-graduates",
                                    src="/assets/historical_projected_graduates.html",
                                    style={"width": "100%", "height": "400px", "border": "none"},
                                ),
                                type="circle"
                            )
                        ], width=12, lg=6),
                    ]),
                    html.Div([
                        html.P([
                            html.Strong("Key Finding: "),
                            "Current enrollment projections generated from the NC Tower database show modest growth that is insufficient to meet workforce demand without targeted intervention. Certificate programs produce the most graduates and are the only ones actually growing, whereas shorter Diploma programs may need to be expanded to address immediate shortages."
                        ], className="mt-3")
                    ])
                ], label="Enrollment & Graduates", tab_id="tab-enrollment"),

                dbc.Tab([
                    dcc.Loading(
                        html.Iframe(
                            id="completion_timing",
                            src="/assets/completion_timing.html",
                            style={"width": "100%", "height": "500px", "border": "none"},
                        ),
                        type="circle"
                    ),
                    html.Div([
                        html.P([
                            html.Strong("Key Finding: "),
                            "Certificate and Diploma programs have shorter completion times, allowing for quicker workforce entry, while Associate's Degrees take 2-3 years on average to complete."
                        ], className="mt-3")
                    ])
                ], label="Completion Rates", tab_id="tab-completion"),

                dbc.Tab([
                    dcc.Loading(
                        html.Iframe(
                            id="monthly-graduates",
                            src="/assets/monthly_graduates_stacked.html",
                            style={"width": "100%", "height": "500px", "border": "none"},
                        ),
                        type="circle"
                    ),
                    html.Div([
                        html.P([
                            html.Strong("Key Finding: "),
                            "Talent pipeline growth is spurred by Certificate completions, but slowing down. Monthly graduation patterns from annual data (due to data availability) mask some seasonality that affects the timing of workforce entry, with expected peaks in May-June and December."
                        ], className="mt-3")
                    ])
                ], label="Graduate Patterns", tab_id="tab-patterns"),
            ], id="supply-tabs", active_tab="tab-employment")
        ], width=12)
    ], className="mb-5"),

    # ==================================== SECTION 4: JOB EVOLUTION ====================================
    dbc.Row([
        dbc.Col([
            html.H3("Occupational Evolution Analysis", id="jobs", className="mb-3 section-header"),
            html.P(
                "Skill clustering and job title analysis showing how Industrial Machinery Mechanics roles are evolving",
                className="text-muted"),
        ], width=12)
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([
            dbc.Tabs([
                dbc.Tab([
                    dcc.Loading(
                        html.Iframe(
                            id="job-clusters",
                            src="/assets/job_clusters_tsne.html",
                            style={"width": "100%", "height": "600px", "border": "none"},
                        ),
                        type="circle"
                    ),
                    html.Div([
                        html.P([
                            html.Strong("Key Finding: "),
                            "Job titles within this SOC occupation cluster into three functional groups across the following boundaries based on similarity in skills and roles: 'Maintenance & Technical Specialists', 'Design & Engineering Specialists', and 'Quality & Process Specialists'."
                        ], className="mt-3")
                    ])
                ], label="Job Clusters", tab_id="tab-clusters"),

                dbc.Tab([
                    dcc.Loading(
                        html.Iframe(
                            id="occupation-distribution",
                            src="/assets/occupation_distribution.html",
                            style={"width": "100%", "height": "500px", "border": "none"},
                        ),
                        type="circle"
                    ),
                    html.Div([
                        html.P([
                            html.Strong("Key Finding: "),
                            "Traditional occupational boundaries (SOC codes) don't fully capture the functional similarity between jobs that require similar skill sets."
                        ], className="mt-3")
                    ])
                ], label="Occupational Distribution", tab_id="tab-occupation"),

                dbc.Tab([
                    dcc.Loading(
                        html.Iframe(
                            id="skill-heatmap",
                            src="/assets/skill_heatmap.html",
                            style={"width": "100%", "height": "600px", "border": "none"},
                        ),
                        type="circle"
                    ),
                    html.Div([
                        html.P([
                            html.Strong("Key Finding: "),
                            "Each functional cluster has distinct skill patterns: maintenance specialists focus on equipment, repair and troubleshooting; engineering specialists on design and systems analysis; quality specialists on process control."
                        ], className="mt-3")
                    ])
                ], label="Skill Patterns", tab_id="tab-skills"),
            ], id="jobs-tabs", active_tab="tab-clusters")
        ], width=12)
    ], className="mb-5"),

    # ==================================== SECTION 5: SHORTAGE PROJECTIONS ====================================
    dbc.Row([
        dbc.Col([
            html.H3("Shortage Projections & Parameters", id="shortage", className="mb-3 section-header"),
            html.P("Projected workforce shortages and key model parameters influencing the labor market",
                   className="text-muted"),
        ], width=12)
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([
            dbc.Tabs([
                dbc.Tab([
                    dcc.Loading(
                        html.Iframe(
                            id="shortage-comparison",
                            src="/assets/shortage_comparison.html",
                            style={"width": "100%", "height": "500px", "border": "none"},
                        ),
                        type="circle"
                    ),
                    html.Div([
                        html.P([
                            html.Strong("Key Finding: "),
                            f"Monthly shortages persist even with optimal training and inflow scenarios (albeit much less), with the baseline showing approximately {key_metrics['avg_monthly_shortage']} unfilled positions per month on average."
                        ], className="mt-3")
                    ])
                ], label="Shortage Projections", tab_id="tab-shortage"),

                dbc.Tab([
                    # UPDATED: Added 2-column layout for the Model Parameters tab
                    dbc.Row([
                        # First column: Time-variant parameters
                        dbc.Col([
                            dcc.Loading(
                                html.Iframe(
                                    id="time-variant-parameters",
                                    src="/assets/time_variant_parameters.html",
                                    style={"width": "100%", "height": "500px", "border": "none"},
                                ),
                                type="circle"
                            ),
                            html.Div([
                                html.P([
                                    html.Strong("Key Finding: "),
                                    "Time-variant parameters reveal how retirement rates increase over time due to workforce aging (IPUMS), while transfer rates fluctuate with economic conditions. These include unemployment variations around the natural rate for Charlotte (BLS) or wage differentials with similar occupations (NC Commerce)."
                                ], className="mt-2 mb-4")
                            ])
                        ], width=12, lg=6),

                        # Second column: Matching rates
                        dbc.Col([
                            dcc.Loading(
                                html.Iframe(
                                    id="matching-efficiency",
                                    src="/assets/matching_efficiency.html",
                                    style={"width": "100%", "height": "500px", "border": "none"},
                                ),
                                type="circle"
                            ),
                            html.Div([
                                html.P([
                                    html.Strong("Key Finding: "),
                                    "Matching efficiency hovers around a standard 0.7 (70%), fluctuating as the economy changes (high labor market slack suggests high unemployment so employers can be more selective and filter out many less-suited candidates, while in a tight labor market there are less available workers so employers invest more resources in recruiting and must be less selective), and calibration based on the divergence between the model's employment and inflow figures from NC Commerce official forecasts."
                                ], className="mt-2")
                            ])
                        ], width=12, lg=6),
                    ]),
                ], label="Model Parameters", tab_id="tab-parameters"),
            ], id="shortage-tabs", active_tab="tab-shortage")
        ], width=12)
    ], className="mb-5"),

    # ==================================== FOOTER ====================================
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P("© 2025 Radius Intelligence",
                   className="text-center text-muted")
        ], width=12)
    ]),

], fluid=True)

# Add CSS for better scrolling and navigation
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Industrial Machinery Mechanics Forecast</title>
        {%favicon%}
        {%css%}
        <style>
            html {
                scroll-behavior: smooth;
            }
            body {
                position: relative;
            }
            .nav-link.active {
                font-weight: bold;
                text-decoration: underline;
            }
            /* Section header styling with proper padding to account for fixed navbar */
            .section-header {
                padding-top: 100px;  /* Increased padding */
                margin-top: -80px;   /* Negative margin to offset padding */
                scroll-margin-top: 80px; /* Modern browsers - ensures proper scroll position */
            }
            .sticky-top {
                position: sticky;
                top: 0;
                z-index: 1000;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Run the application
if __name__ == "__main__":
    print("Starting Workforce Analysis Dashboard...")
    print(f"Loading HTML files from: {html_dir}")
    print(f"Assets directory: {assets_dir}")
    app.run(debug=True)