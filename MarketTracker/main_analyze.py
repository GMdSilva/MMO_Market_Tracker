from plotly.subplots import make_subplots

from core.analyze_prices import analyze_price_history
from core.plot_results import plot_results
from configs.cons import CURRENT_DATE, ASSETS


def generate_subplot_titles(item_list, offer_types):
    """
    Generate titles for each subplot.
    """
    return [f"{item} {offer_type}" for item in item_list for offer_type in offer_types]


def setup_subplots(item_list, offer_types):
    """
    Create subplots with the specified items and offer types.
    """
    specs = [[{"secondary_y": True} for _ in offer_types] for _ in item_list]
    fig = make_subplots(
        rows=len(item_list),
        cols=len(offer_types),
        subplot_titles=generate_subplot_titles(item_list, offer_types),
        specs=specs
    )
    return fig


def analyze_and_plot(item_list, offer_types, folder_name, fig):
    """
    Analyze price history and plot results for each item and offer type.
    """
    for i, item_name in enumerate(item_list):
        for j, offer_type in enumerate(offer_types):
            analyze_price_history(item_name, offer_type, folder_name)
            plot_results(item_name, offer_type, fig, i + 1, j + 1, folder_name)


def update_figure_layout(fig, item_list):
    """
    Update the layout of the figure and consolidate legends.
    """
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Price',
        yaxis2_title='Volume',
        showlegend=True,
        legend=dict(x=0, y=1.10, orientation='h'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
        yaxis2=dict(showgrid=False),
        template='plotly_dark',
        height=800 * len(item_list)
    )

    unique_legends = set()
    for trace in fig['data']:
        if trace['name'] not in unique_legends:
            trace['showlegend'] = True
            unique_legends.add(trace['name'])
        else:
            trace['showlegend'] = False


def main():
    offer_types = ['ask', 'bid']

    fig = setup_subplots(ASSETS, offer_types)

    analyze_and_plot(ASSETS, offer_types, CURRENT_DATE, fig)
    update_figure_layout(fig, ASSETS)
    fig.write_html("results/html/tibia_market.html")
    fig.show()


if __name__ == "__main__":
    main()
