from flask import Blueprint, render_template
import json
import plotly
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder
from backend.models import Property

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics')
def analytics():
    """Analytics dashboard with charts."""
    # Get data for analytics
    properties = Property.query.all()

    graphs = []

    if properties:
        # Price distribution by location
        location_prices = {}
        for prop in properties:
            if prop.location not in location_prices:
                location_prices[prop.location] = []
            location_prices[prop.location].append(prop.price)

        # Average prices
        avg_prices = {loc: sum(prices)/len(prices) for loc, prices in location_prices.items() if prices}

        # Property types distribution
        type_counts = {}
        for prop in properties:
            type_counts[prop.property_type] = type_counts.get(prop.property_type, 0) + 1

        # Create plots
        price_chart = go.Bar(
            x=list(avg_prices.keys())[:10],  # Top 10 locations
            y=list(avg_prices.values())[:10],
            name='Average Price'
        )

        type_chart = go.Pie(
            labels=list(type_counts.keys()),
            values=list(type_counts.values()),
            name='Property Types'
        )

        graphs = [
            {'data': [price_chart], 'layout': {'title': 'Average Property Prices by Location'}},
            {'data': [type_chart], 'layout': {'title': 'Property Types Distribution'}}
        ]

    graphJSON = json.dumps(graphs, cls=PlotlyJSONEncoder)

    return render_template('analytics.html', graphJSON=graphJSON)