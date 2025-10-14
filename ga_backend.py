import random
from copy import deepcopy

class GeneticAlgorithm:
    def __init__(self, catalogo, area_maxima, tam_poblacion=100, num_generaciones=50,
                 prob_cruce=0.6, prob_mutacion=0.15, torneo_k=3, elitismo=2, 
                 selection_method='torneo'): # <-- Nuevo parámetro
        # Parámetros del Problema
        self.catalogo = catalogo
        self.area_maxima = area_maxima
        self.num_articulos = len(catalogo)

        # Hiperparámetros del AG
        self.tam_poblacion = tam_poblacion
        self.num_generaciones = num_generaciones
        self.prob_cruce = prob_cruce
        self.prob_mutacion = prob_mutacion
        self.torneo_k = torneo_k
        self.elitismo = elitismo
        self.selection_method = selection_method # <-- Guardamos el método

    def _crear_individuo(self):
        return [random.randint(0, item["stock"]) for item in self.catalogo]

    def _evaluar_individuo(self, individuo, penalizacion=1000.0):
        area = sum(q * item["area"] for q, item in zip(individuo, self.catalogo))
        ganancia = sum(q * item["ganancia"] for q, item in zip(individuo, self.catalogo))
        if area <= self.area_maxima:
            return ganancia
        else:
            exceso = area - self.area_maxima
            return max(0, ganancia - penalizacion * exceso)

    def _seleccionar_torneo(self, poblacion, fitness_vals):
        seleccionados = random.sample(range(len(poblacion)), self.torneo_k)
        mejor_idx = max(seleccionados, key=lambda i: fitness_vals[i])
        return deepcopy(poblacion[mejor_idx])

    def _seleccionar_ruleta(self, poblacion, fitness_vals):
        # Asegurarse de que todos los fitness son positivos para la ruleta
        min_fitness = min(fitness_vals)
        shifted_fitness = [f - min_fitness + 1 for f in fitness_vals]
        total_fitness = sum(shifted_fitness)

        if total_fitness == 0: # Caso extremo si todos los fitness son iguales y negativos
            return deepcopy(random.choice(poblacion))

        # Gira la ruleta
        pick = random.uniform(0, total_fitness)
        current = 0
        for i, ind in enumerate(poblacion):
            current += shifted_fitness[i]
            if current > pick:
                return deepcopy(ind)
        return deepcopy(poblacion[-1]) # Fallback

    def _cruzar_uniforme(self, padre1, padre2):
        hijo1, hijo2 = padre1[:], padre2[:]
        for i in range(self.num_articulos):
            if random.random() < 0.5:
                hijo1[i], hijo2[i] = hijo2[i], hijo1[i]
        return hijo1, hijo2

    def _mutar(self, individuo):
        for i in range(self.num_articulos):
            if random.random() < self.prob_mutacion:
                if random.random() < 0.5:
                    individuo[i] = max(0, individuo[i] - 1)
                else:
                    individuo[i] = min(self.catalogo[i]["stock"], individuo[i] + 1)
        return individuo

    def ejecutar(self):
        poblacion = [self._crear_individuo() for _ in range(self.tam_poblacion)]
        fitness_vals = [self._evaluar_individuo(ind) for ind in poblacion]
        mejor_global = None
        mejor_fitness_global = float('-inf')
        historial_fitness = []

        for _ in range(self.num_generaciones):
            pares = sorted(zip(poblacion, fitness_vals), key=lambda x: x[1], reverse=True)
            if pares[0][1] > mejor_fitness_global:
                mejor_fitness_global = pares[0][1]
                mejor_global = deepcopy(pares[0][0])
            historial_fitness.append(mejor_fitness_global)
            
            nueva_poblacion = []
            if self.elitismo > 0:
                nueva_poblacion.extend([deepcopy(par[0]) for par in pares[:self.elitismo]])

            while len(nueva_poblacion) < self.tam_poblacion:
                # ✨ Lógica para elegir el método de selección
                if self.selection_method == 'torneo':
                    padre1 = self._seleccionar_torneo(poblacion, fitness_vals)
                    padre2 = self._seleccionar_torneo(poblacion, fitness_vals)
                else: # 'ruleta'
                    padre1 = self._seleccionar_ruleta(poblacion, fitness_vals)
                    padre2 = self._seleccionar_ruleta(poblacion, fitness_vals)

                if random.random() < self.prob_cruce:
                    hijo1, hijo2 = self._cruzar_uniforme(padre1, padre2)
                else:
                    hijo1, hijo2 = deepcopy(padre1), deepcopy(padre2)
                
                nueva_poblacion.append(self._mutar(hijo1))
                if len(nueva_poblacion) < self.tam_poblacion:
                    nueva_poblacion.append(self._mutar(hijo2))

            poblacion = nueva_poblacion
            fitness_vals = [self._evaluar_individuo(ind) for ind in poblacion]

        return mejor_global, historial_fitness