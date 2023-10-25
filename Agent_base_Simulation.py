import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
population_size = 200
initial_infected = 5
infection_prob = 0.05
recovery_rate = 0.01

class Person:
    def __init__(self):
        self.x = np.random.uniform(0, 10)
        self.y = np.random.uniform(0, 10)
        self.status = 'S'

    def move(self):
        self.x += np.random.normal(0, 0.1)
        self.y += np.random.normal(0, 0.1)
        self.x = np.clip(self.x, 0, 10)
        self.y = np.clip(self.y, 0, 10)

    def interact(self, others):
        if self.status == 'I':
            for other in others:
                if other.status == 'S':
                    d = np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
                    if d < 1 and np.random.rand() < infection_prob:
                        other.status = 'I'

            if np.random.rand() < recovery_rate:
                self.status = 'R'

population = [Person() for _ in range(population_size)]
for i in np.random.choice(range(population_size), initial_infected, replace=False):
    population[i].status = 'I'

daily_infected = [initial_infected]
cumulative_infected = [initial_infected]
daily_recovered = [0]
cumulative_recovered = [0]

color_map = {'S': 'blue', 'I': 'red', 'R': 'green'}

def update(frame):
    daily_infected_count = 0
    daily_recovered_count = 0

    for person in population:
        prev_status = person.status
        person.move()
        person.interact(population)
        
        if prev_status == 'S' and person.status == 'I':
            daily_infected_count += 1
        elif prev_status == 'I' and person.status == 'R':
            daily_recovered_count += 1

    daily_infected.append(daily_infected_count)
    daily_recovered.append(daily_recovered_count)
    cumulative_infected.append(cumulative_infected[-1] + daily_infected_count)
    cumulative_recovered.append(cumulative_recovered[-1] + daily_recovered_count)

    ax1.clear()
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.scatter([person.x for person in population],
                [person.y for person in population],
                c=[color_map[person.status] for person in population])
    ax1.text(1, 9, f'Day: {frame}', fontsize=12, color='black')

    ax2.clear()
    ax2.plot(daily_infected, label='Daily Infected', color='red')
    ax2.plot(daily_recovered, label='Daily Recovered', color='green')
    ax2.plot(cumulative_infected, label='Cumulative Infected', color='orange')
    ax2.plot(cumulative_recovered, label='Cumulative Recovered', color='blue')
    ax2.legend()
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, population_size)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
ani = FuncAnimation(fig, update, frames=100)
plt.tight_layout()
plt.show()
