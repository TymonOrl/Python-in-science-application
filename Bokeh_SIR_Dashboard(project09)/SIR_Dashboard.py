import numpy as np
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.models import Slider, Div, ColumnDataSource
from scipy.integrate import odeint


def dVdt(V, t, beta, gamma):
    S, I, R = V
    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]

def get_text():
    eqs = Div(
    text=r"""
    <h3>SIR model</h3>

    <div style="font-size:16px;">

      <div style="margin-bottom:16px;">
        $$\frac{dS}{dt} = -\beta SI$$
      </div>

      <div style="margin-bottom:16px;">
        $$\frac{dI}{dt} = \beta SI - \gamma I$$
      </div>

      <div style="margin-bottom:24px;">
        $$\frac{dR}{dt} = \gamma I$$
      </div>

    </div>

    <h4>Variables</h4>
    <ul style="margin-top:0;">
      <li><b>S(t)</b> — susceptible individuals</li>
      <li><b>I(t)</b> — infected individuals</li>
      <li><b>R(t)</b> — recovered/removed individuals</li>
      <li><b>\(\beta\)</b> — transmission rate</li>
      <li><b>\(\gamma\)</b> — recovery rate</li>
      <li><b>t</b> — time</li>
    </ul>
    """,
    width=320,
    )
    return eqs


# Main

# Initial parameters
S0 = 0.99  # Initial susceptible population
I0 = 0.01  # Initial infected population
R0 = 0.0   # Initial recovered population
V0 = (S0, I0, R0)

ts = np.linspace(0, 100, 1000)

# Changeable parameters
beta = 0.3
gamma = 0.1

# Solve ODEs
sol0 = odeint(dVdt, y0 = V0, t=ts, args=(beta, gamma))

source = ColumnDataSource(data=dict(
    t=ts,
    S=sol0[:, 0],
    I=sol0[:, 1],
    R=sol0[:, 2],
))

def update_data(attr, old, new):
    beta = s_beta.value
    gamma = s_gamma.value

    sol = odeint(dVdt, y0=V0, t=ts, args=(beta, gamma))

    # Push updates to the plot
    source.data = dict(
        t=ts,
        S=sol[:, 0],
        I=sol[:, 1],
        R=sol[:, 2],
    )


# --- UI ---
eqs = get_text()

# Plot
fig = figure(
    #sizing_mode='stretch_width',
    width=600,
    aspect_ratio=2.5,
    title='Number of Individuals Over Time in SIR Model',
    x_axis_label='Time (t)',
    y_axis_label='Number of Individuals',
)

fig.grid.grid_line_dash = [6, 4]
fig.toolbar.logo = None
fig.toolbar.autohide = True

fig.line('t', 'S', source=source, line_color='blue', legend_label='S', line_width=2)
fig.line('t', 'I', source=source, line_color='red', legend_label='I', line_width=2)
fig.line('t', 'R', source=source, line_color='green', legend_label='R', line_width=2)

# Sliders
s_beta = Slider(start=0, end=1.0, value=0.3, step=0.05, title='$$\\beta$$', width=200)
s_beta.on_change('value_throttled', update_data)

s_gamma = Slider(start=0, end=1.0, value=0.1, step=0.05, title='$$\\gamma$$', width=200)
s_gamma.on_change('value_throttled', update_data)

controls = column(eqs, s_beta, s_gamma, width=320)  # make the whole right column fixed-width

curdoc().add_root(row(fig, controls, spacing=40))
curdoc().title = "SIR Model Dashboard"