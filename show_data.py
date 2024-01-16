import pandas as pd
import matplotlib.pyplot as plt

# Leggi i dati dal file CSV
df = pd.read_csv('best.csv', delimiter=';')

# Raggruppa i dati per seed
grouped_data = df.groupby('randomGenerator.seed')

# 1) Grafico fbest
fig, ax = plt.subplots()

for name, group in grouped_data:
    ax.plot(group['iterations'], group['best→fitness→s.task.p.avgH'], label=f'Seed {name}')

# Trova seed con fitness peggiore e migliore
worst_seed = df.loc[df.groupby('randomGenerator.seed')['best→fitness→s.task.p.avgH'].idxmin()]
best_seed = df.loc[df.groupby('randomGenerator.seed')['best→fitness→s.task.p.avgH'].idxmax()]

# Andamento fitness medio
mean_fitness = grouped_data['best→fitness→s.task.p.avgH'].mean()

# Aggiungi linee per il fitness peggiore, migliore e medio
ax.plot(mean_fitness.index, mean_fitness.values, label='Fitness Media', linestyle='--', color='black')
ax.scatter(worst_seed['iterations'], worst_seed['best→fitness→s.task.p.avgH'], color='red', marker='o', label='Fitness Peggiore')
ax.scatter(best_seed['iterations'], best_seed['best→fitness→s.task.p.avgH'], color='green', marker='o', label='Fitness Migliore')

ax.set_xlabel('Iterazioni')
ax.set_ylabel('Fitness')
ax.legend()
plt.title('Grafico fbest')
plt.show()

# 2) Calcola la fitness migliore e iniziale per ogni seed
best_fitness = df.groupby('randomGenerator.seed')['best→fitness→s.task.p.avgH'].max()
initial_fitness = df[df['iterations'] == 0].groupby('randomGenerator.seed')['best→fitness→s.task.p.avgH'].first()

# Calcola il discostamento e il miglioramento percentuale
fitness_difference = best_fitness - initial_fitness
percent_improvement = (fitness_difference / initial_fitness) * 100

# Creazione della tabella
result_table = pd.DataFrame({
    'Seed': best_fitness.index,
    'Fitness Migliore': best_fitness.values,
    'Fitness Iniziale': initial_fitness.values,
    'Discostamento': fitness_difference.values,
    'Miglioramento Percentuale': percent_improvement.values
})

# Stampa la tabella
print(result_table)

# 3) Istogramma a bin delle fitness migliori tra i seed
plt.figure()

plt.hist(best_fitness, bins=20, alpha=0.5, color='blue', edgecolor='black')
plt.xlabel('Fitness Migliore')
plt.ylabel('Frequenza')
plt.title('Istogramma delle Fitness Migliori tra i Seed')
plt.show()
