import random

class GeneticScheduler:
    def __init__(self, horarios, max_estudiantes=50, min_ramos=3, max_ramos=6):
        self.horarios = horarios  # Lista de horarios disponibles
        self.max_estudiantes = max_estudiantes
        self.min_ramos = min_ramos
        self.max_ramos = max_ramos

    def generar_poblacion_inicial(self, tam_poblacion, num_estudiantes):
        """Genera una población inicial de configuraciones aleatorias."""
        poblacion = []
        for _ in range(tam_poblacion):
            estudiante_horarios = []
            for _ in range(num_estudiantes):
                num_ramos = random.randint(self.min_ramos, self.max_ramos)
                num_ramos = min(num_ramos, len(self.horarios))  # Ajustar para evitar error
                horario_estudiante = random.sample(self.horarios, num_ramos)
                estudiante_horarios.append(horario_estudiante)
            poblacion.append(estudiante_horarios)
        return poblacion

    def evaluar_aptitud(self, configuracion):
        """Evalúa la aptitud de una configuración."""
        score = 0
        for estudiante in configuracion:
            ramos = set()
            for ramo in estudiante:
                ramos.add(ramo)
            score += len(ramos)  # Favorece diversidad de ramos
        return score

    def seleccionar_padres(self, poblacion):
        """Selecciona padres para la reproducción usando torneo."""
        torneo = random.sample(poblacion, k=3)
        return max(torneo, key=self.evaluar_aptitud)

    def cruzar(self, padre1, padre2):
        """Realiza cruce entre dos configuraciones de horarios."""
        punto_cruce = random.randint(1, len(padre1) - 1)
        hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
        hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
        return hijo1, hijo2

    def mutar(self, hijo):
        """Aplica mutación a una configuración."""
        if random.random() < 0.1:  # Probabilidad de mutación
            estudiante_idx = random.randint(0, len(hijo) - 1)
            num_ramos = random.randint(self.min_ramos, self.max_ramos)
            num_ramos = min(num_ramos, len(self.horarios))  # Ajustar para evitar error
            hijo[estudiante_idx] = random.sample(self.horarios, num_ramos)
        return hijo

    def evolucionar(self, tam_poblacion, generaciones, num_estudiantes):
        """Evoluciona la población para optimizar los horarios."""
        poblacion = self.generar_poblacion_inicial(tam_poblacion, num_estudiantes)
        for _ in range(generaciones):
            nueva_poblacion = []
            for _ in range(tam_poblacion // 2):
                padre1 = self.seleccionar_padres(poblacion)
                padre2 = self.seleccionar_padres(poblacion)
                hijo1, hijo2 = self.cruzar(padre1, padre2)
                nueva_poblacion.append(self.mutar(hijo1))
                nueva_poblacion.append(self.mutar(hijo2))
            poblacion = nueva_poblacion
        return max(poblacion, key=self.evaluar_aptitud)

    def formatear_configuracion(self, configuracion):
        """Formatea la configuración para mejor visibilidad."""
        salida = []
        for idx, estudiante in enumerate(configuracion, start=1):
            salida.append(f"Estudiante {idx}:")
            for ramo in estudiante:
                salida.append(f"  - {ramo}")
        return "\n".join(salida)

# Ejemplo de horarios simplificados para prueba
horarios = ["Estructuras Discretas S1", "Álg. y Trigon. S1", "Int. Program. S1", "Química Gral. G1"]
num_estudiantes = 30

# Crear instancia del scheduler y evolucionar
scheduler = GeneticScheduler(horarios)
mejor_configuracion = scheduler.evolucionar(tam_poblacion=50, generaciones=100, num_estudiantes=num_estudiantes)

# Mostrar la mejor configuración de forma legible
print("Mejor configuración:\n")
print(scheduler.formatear_configuracion(mejor_configuracion))
