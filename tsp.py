import pandas
import random

# ensimmäisen populaation luonti funktio 
def create_first_population(n, cities):
    pop = []
    for i in range(n):
        pop.append(random.sample(cities, len(cities)))
    return pop

# reittivaihtoehtojen lasku funktio
def count_fitness_values(pop, dist, len):
    all_costs = [] # kaikkien reittivaihtoehtojen km-määrät

    for c in pop:
        total_cost = 0 # yhden kromosomin sopivuusarvo eli km-määrä

        for i in range(len - 1):
            from_city, to_city = c[i], c[i + 1]
            cost = dist[from_city][to_city] # matkan kustannus
            total_cost = total_cost + cost # lisätään kustannus

        return_cost = dist[c[0]][to_city] # paluu
        total_cost = total_cost + return_cost # meno + paluu
        all_costs.append(total_cost)

    # reiteistä ja niiden kustannuksista dataframe
    city_fitness = pandas.DataFrame({'pop': pop, 'fit': all_costs})
    return city_fitness

# valinta funktio turnajaisilla
def selection(city_fitness, n, s=3):
    parents = []

    for i in range(n): # turnajaisia n kertaa
        attendees = city_fitness.sample(s) # 3 ehdokasta turnajaisiin

        # järjestetään ehdokkaat pienimmästä suurimpaan
        attendees.sort_values('fit', ascending=True, inplace=True)

        # poimitaan pienimmän arvon omaava kromosomi
        closest = attendees['pop'].iloc[0]

        parents.append(closest)

    return parents

# funktio lapsen luontiin kahdesta vanhemmasta
def create_child(p1, p2, pt):
    c = p1[0:pt]
    for i in range(0, len(p1)):
        if p2[i] not in c: # jos geeni ei ole lapsessa
            c.append(p2[i]) # niin lisää geeni lapselle
    return c

# risteyts funktio luo 2 lasta 2 vanhemmasta
def crossover(p1, p2, r):
    # kloonaus
    c1 = p1.copy()
    c2 = p2.copy()

    # tehdäänkö risteytys
    if random.random() <= r:
        pt = random.randint(1, len(p1) - 2) # satunnainen risteytys indeksi

        # ykköseltä alkuosa ja kakkoselta loppuosa
        c1 = create_child(p1, p2, pt)
        # kakkoselta alkuosa ja ykköseltä loppuosa
        c2 = create_child(p2, p1, pt)
        
    return [c1, c2]

# mutaatio funktio vaihtaa lapsen geenit
def mutation(c, r):
    if random.random() <= r: # tapahtuuko mutaatio
        # 2 satunnaisesti arvottua indeksiä
        r = random.sample(range(0, len(c) - 1), 2)
        i1, i2 = r[0], r[1]

        # tallenetaan arvot
        f = c[i1]
        s = c[i2]

        # arvojen vaitho keskenään
        c[i1] = s
        c[i2] = f

# evoluutio funktio tekee vaiheet
def evolution(pop, dist, n, r_c, r_m, len):
    city_fitness = count_fitness_values(pop, dist, len) # sopivuusarvot
    parents = selection(city_fitness, n) # valinta turnajaisilla

    children = []
    for i in range(0, n - 1, 2):
        p1 = parents[i]
        p2 = parents[i + 1]

        for c in crossover(p1, p2, r_c): # risteytys
            mutation(c, r_m) # mutaatio
            children.append(c)

    return children, city_fitness

# nimet kaupungeille 0-5
names = ['Ankkapurha', 'Jänishaikula', 'Kontu', 'Jeppelä', 'Peräkorpi', 'Koikkala']

# lista kaupungin nimille [0-5]
cities = list(range(0, len(names)))

# datan lukeminen
dist = pandas.read_csv('./data.csv', delimiter=';', names=cities)

n = 20  # populaation koko
r_cross = 0.7  # risteytystodennäköisyys
r_mut = 0.001  # mutaatiotodennäköisyys
iterations = 100  # suoritettavat kierrokset, sukupolvien määrä

# aloitetaan luomalla satunnainen alkupopulaatio
pop = create_first_population(n, cities)

# vaihdeiden toisto
while iterations > 0:
    pop, cost = evolution(pop, dist, n, r_cross, r_mut, len(cities))
    iterations = iterations - 1

# reitin ja kaupunkien tulostus
print('Reitin pituus', cost['fit'].iloc[0], 'km')
closest = cost['pop'].iloc[0]
for i in range(0, len(cities)):
    print(str(i + 1) + '. ' + names[closest[i]])
