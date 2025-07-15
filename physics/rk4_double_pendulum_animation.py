import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

m1, m2 = 1.0, 1.0
l1, l2 = 1.0, 1.0
g = 9.81

state0 = np.array([np.pi/2, np.pi/2, 0.0, 0.0])

dt = 0.02
T = 20
times = np.arange(0, T, dt)

def f(state):
    theta1, theta2, omega1, omega2 = state
    delta = theta1 - theta2

    denom1 = l1 * (2*m1 + m2 - m2 * np.cos(2*delta))
    denom2 = l2 * (2*m1 + m2 - m2 * np.cos(2*delta))

    dtheta1_dt = omega1
    dtheta2_dt = omega2

    domega1_dt = (-g*(2*m1 + m2)*np.sin(theta1)
                  - m2*g*np.sin(theta1 - 2*theta2)
                  - 2*np.sin(delta)*m2*(omega2**2*l2 + omega1**2*l1*np.cos(delta))) / denom1

    domega2_dt = (2*np.sin(delta)*(omega1**2*l1*(m1 + m2)
                  + g*(m1 + m2)*np.cos(theta1)
                  + omega2**2*l2*m2*np.cos(delta))) / denom2

    return np.array([dtheta1_dt, dtheta2_dt, domega1_dt, domega2_dt])

def rk4_step(state, dt):
    k1 = f(state)
    k2 = f(state + 0.5*dt*k1)
    k3 = f(state + 0.5*dt*k2)
    k4 = f(state + dt*k3)
    return state + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)

states = np.zeros((len(times), 4))
states[0] = state0
for i in range(1, len(times)):
    states[i] = rk4_step(states[i-1], dt)

fig, ax = plt.subplots(figsize=(6,6))
ax.set_xlim(-(l1 + l2) - 0.5, (l1 + l2) + 0.5)
ax.set_ylim(-(l1 + l2) - 0.5, (l1 + l2) + 0.5)
ax.set_aspect('equal')
ax.grid()

line, = ax.plot([], [], 'o-', lw=3, color='blue')

def init():
    line.set_data([], [])
    return (line,)

def animate(i):
    theta1, theta2 = states[i, 0], states[i, 1]

    x1 = l1 * np.sin(theta1)
    y1 = -l1 * np.cos(theta1)

    x2 = x1 + l2 * np.sin(theta2)
    y2 = y1 - l2 * np.cos(theta2)

    line.set_data([0, x1, x2], [0, y1, y2])
    return (line,)

ani = animation.FuncAnimation(fig, animate, frames=len(times),
                              init_func=init, interval=dt*1000, blit=True)

plt.show()

