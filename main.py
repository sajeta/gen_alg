import random

# Globalne varijable

OPTIMAL     = "Universal law is for lackeys. Context... is for kings."
DNA_SIZE    = len(OPTIMAL)
POP_SIZE    = 100
GENERATIONS = 10000

#
# Helper functions
# These are used as support, but aren't direct GA-specific functions.
#


def weighted_choice(items):
  """
  Odaberi nasumicni element iz items, gdje je items lista uparene strukture podatka oblika (item,weight). 
  Gdje weight odreduje vjerojatnost odabira doticnog item-a. u nasem slucaju je to vrijednost proporcionalna vrijednosti dobrote.
  """
  weight_total = sum((item[1] for item in items))
  n = random.uniform(0, weight_total)
  for item, weight in items:
    if n < weight:
      return item
    n = n - weight
  return item

def random_char():
  """
  Vrati nasumicni znak izmedu ASCII 32 and 126 (razmak, simboli znakovi i brojevi ukljuceni) 
  """
  return chr(int(random.randrange(32, 126, 1)))

def random_population():
  """
  Vrati listu velicine POP_SIZE jedinki, svaku jedinku napuni nasumicno generiranim znakovima velicine DNA_SIZE
  """
  pop = []
  for i in range(POP_SIZE):
    dna = ""
    for c in range(DNA_SIZE):
      dna += random_char()
    pop.append(dna)
  return pop

#
# GA functions
# These make up the bulk of the actual GA algorithm.
#

def fitness(dna):
  """
  Za svaki gen iz DNA, ova funkcija izracunava razliku izmedu svakog gena(znaka) u DNA i znaka na istom mjestu u trazenom nizu znakova OPTIMAL.
  Te vrijednosti se sumiraju i funkcija vraca tu sumu razlika.
  """
  fitness = 0
  for c in range(DNA_SIZE):
    fitness += abs(ord(dna[c]) - ord(OPTIMAL[c]))
  return fitness

def mutate(dna):
  """
  Za svaki gen iz DNA, postoji 1/mutation_chance da ce biti zamjenjen nekim drugim nasumicnim znakom. 
  Ovo osigurava razlicitost populacije, i osigurava da algoritam ne zapne u lokalnim minimumima. 
  """
  dna_out = ""
  mutation_chance = 100
  for c in range(DNA_SIZE):
    if int(random.random()*mutation_chance) == 1:
      dna_out += random_char()
    else:
      dna_out += dna[c]
  return dna_out

def crossover(dna1, dna2):
  """
  Krzanje s jednom tockm prekida koja je odabrana nasumicno. Oba zadzavaju svoju 
  pocetno vrijednost do tocke prekida nakon koje se zanmjene za ostatak.
  """
  
  """
  pos = random.randint(0, DNA_SIZE)
  return (dna1[:pos]+dna2[pos:], dna2[:pos]+dna1[pos:])
  """
  
  
  pos1 = random.randint(0, DNA_SIZE-2)
  pos2 = random.randint(pos1+1, DNA_SIZE-1)
  pos3 = random.randint(pos2+1, DNA_SIZE)
  return (dna1[:pos1]+dna2[pos1:pos2]+dna1[pos2:pos3]+dna2[pos3:], dna2[:pos1]+dna1[pos1:pos2]+dna2[pos2:pos3]+dna1[pos3:])
  

#
# GLAVNI DIO PROGRAMA
#

if __name__ == "__main__":
  #Generiraj pocetnu populaciju. Ovo ce stvoriti listu velicine POP_SIZE nasumicnih znakova.
  population = random_population()

  # Simuliraj sve generacije.
  for generation in range(GENERATIONS):
    print ("Generation %s   Random sample: '%s'" % (generation, population[0]))
    weighted_population = []
	
	#Dodaj individue(kromosome) i njihove pripadne vrijednosti dobrote u listu weighted_population (bazen potencijanih rijesenja). Ruletska selekcija.
	#Ovo nam sluzi da izvucemo kromosome sa najvecom vjerojatnosti koji ce preskociti fazu selekcije,
	#nakon cega ce listu nastaviti puniti populacija koja prode selekciju (elitizam)
   
    for individual in population:
      fitness_val = fitness(individual)

      # Generiraj parove (individual,fitness), pazeci pritom da ne dijelimo s 0
	  
      if fitness_val == 0:
        pair = (individual, 1.0)
      else:
        pair = (individual, 1.0/fitness_val)

      weighted_population.append(pair)

    population = []

	#Odaberi dva nasumicno odabrana roditelja, bazirana na njihovoj dobroti(vjerojatnosti odabira) 
	#krizaj im gene, mutiraj ih i baci ih natrag u populaciju za sljedecu iteraciju
    
    for _ in range(int(POP_SIZE/2)):
      # Selecija
      ind1 = weighted_choice(weighted_population)
      ind2 = weighted_choice(weighted_population)
		
      # Krizanje
      ind1, ind2 = crossover(ind1, ind2)

      # Mutiraj i vrati natrag u listu populacije
      population.append(mutate(ind1))
      population.append(mutate(ind2))
	
  # Prikazi niz znakova sa navecim rankom nakon sto sve generacije produ . 
  # To rijesenje je najblize OPTIMAL nizu znakova sto znaci da ima najmanji iznos dobrote.
  fittest_string = population[0]
  minimum_fitness = fitness(population[0])

  for individual in population:
    ind_fitness = fitness(individual)
    if ind_fitness <= minimum_fitness:
      fittest_string = individual
      minimum_fitness = ind_fitness

  print ("Fittest String: %s" % fittest_string)
  exit(0)
