import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class Material:
    name: str
    density: float  # kg/m³
    thermal_conductivity: float  # W/(m·K)
    specific_heat: float  # J/(kg·K)
    vaporization_point: float  # K
    latent_heat_vaporization: float  # J/kg

@dataclass
class MachineParameters:
    voltage: float  # V
    current: float  # A
    pulse_on_time: float  # μs
    pulse_off_time: float  # μs
    energy_efficiency: float  # ratio

class EDMSimulation:
    def __init__(self, workpiece_material: Material, tool_material: Material, 
                 machine_params: MachineParameters, grid_size: tuple=(30, 30, 30)):
        self.workpiece = workpiece_material
        #self.tool = tool_material
        self.params = machine_params
        self.grid_size = grid_size
        
        # Инициализация сеток
        self.workpiece_grid = np.ones(grid_size)
        self.temperature_grid = np.ones(grid_size) * 300  # Начальная температура 300K
        self.tool_position = np.array([grid_size[0]//2, grid_size[1]//2, grid_size[2]])
        
        # Размер ячейки сетки (в метрах)
        self.cell_size = 0.0001 
    
    def calculate_plasma_channel_radius(self):
        """Расчет радиуса плазменного канала"""
        # Корректируем масштаб для получения радиуса в метрах
        return 2.4e-5 * (self.params.current ** 0.43) * (self.params.pulse_on_time ** 0.44)
    
    def calculate_heat_input(self, distance_from_center):
        """Расчет теплового потока согласно физической модели"""
        r0 = self.calculate_plasma_channel_radius()
        
        # Расчет энергии импульса (Дж)
        energy = self.params.voltage * self.params.current * self.params.pulse_on_time * 1e-6
        
        # Расчет площади пятна нагрева (м²)
        spot_area = np.pi * r0 * r0
        
        # Расчет максимальной плотности теплового потока (Вт/м²)
        # Учитываем КПД процесса и распределение энергии во времени
        q0 = (self.params.energy_efficiency * energy) / (spot_area * self.params.pulse_on_time * 1e-6)
        
        # Гауссово распределение теплового потока
        return q0 * np.exp(-4.5 * (distance_from_center/r0)**2)
    
    def find_discharge_point(self):
        """Поиск точки следующего разряда"""
        min_dist = float('inf')
        discharge_point = None
        
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                for k in range(self.grid_size[2]):
                    if self.workpiece_grid[i,j,k] > 0:
                        dist = np.linalg.norm(np.array([i,j,k]) - self.tool_position)
                        if dist < min_dist:
                            min_dist = dist
                            discharge_point = np.array([i,j,k])
        
        return discharge_point

    def calculate_cooling(self, dt):
        """
        Расчет охлаждения материала на основе уравнения теплопроводности
        
        Parameters:
        -----------
        dt : float
            Шаг по времени [с]
        """
        # Коэффициент температуропроводности материала
        alpha = self.workpiece.thermal_conductivity / (self.workpiece.density * self.workpiece.specific_heat)
        
        # Создаем копию текущего распределения температуры
        temp_old = self.temperature_grid.copy()
        
        # Расчет изменения температуры для каждой точки
        for i in range(1, self.grid_size[0]-1):
            for j in range(1, self.grid_size[1]-1):
                for k in range(1, self.grid_size[2]-1):
                    if self.workpiece_grid[i,j,k] > 0:
                        # Разностная схема для уравнения теплопроводности
                        d2T_dx2 = (temp_old[i+1,j,k] - 2*temp_old[i,j,k] + temp_old[i-1,j,k]) / (self.cell_size**2)
                        d2T_dy2 = (temp_old[i,j+1,k] - 2*temp_old[i,j,k] + temp_old[i,j-1,k]) / (self.cell_size**2)
                        d2T_dz2 = (temp_old[i,j,k+1] - 2*temp_old[i,j,k] + temp_old[i,j,k-1]) / (self.cell_size**2)
                        
                        # Изменение температуры
                        dT = alpha * (d2T_dx2 + d2T_dy2 + d2T_dz2) * dt
                        
                        # Учет теплообмена с окружающей средой
                        h = 50  # коэффициент теплоотдачи [Вт/(м²·К)]
                        surface_area = 6 * self.cell_size**2  # площадь поверхности ячейки
                        volume = self.cell_size**3  # объем ячейки
                        
                        # Теплообмен с окружающей средой (закон Ньютона-Рихмана)
                        T_ambient = 300  # температура окружающей среды [К]
                        dT_conv = h * surface_area * (T_ambient - temp_old[i,j,k]) * dt / (self.workpiece.density * self.workpiece.specific_heat * volume)
                        
                        self.temperature_grid[i,j,k] = temp_old[i,j,k] + dT + dT_conv

    def update_temperature(self, discharge_point):
        """Обновление температуры после разряда с учетом теплопроводности между ячейками"""
        x, y, z = np.mgrid[0:self.grid_size[0], 0:self.grid_size[1], 0:self.grid_size[2]]
        points = np.stack([x, y, z], axis=-1)
        distances = np.linalg.norm(points - discharge_point, axis=-1) * self.cell_size
        
        # Расчет теплового потока от разряда
        heat_input = self.calculate_heat_input(distances)
        dt = self.params.pulse_on_time * 1e-6
        
        # Расчет изменения температуры от разряда
        dT_discharge = (heat_input * dt) / (self.workpiece.density * self.workpiece.specific_heat)
        
        # Применяем изменение температуры от разряда только там, где есть материал
        mask = self.workpiece_grid > 0
        self.temperature_grid[mask] += dT_discharge[mask]

        # Удаление материала при достижении температуры испарения
        vaporized = self.temperature_grid > self.workpiece.vaporization_point
        self.workpiece_grid[vaporized] = 0
        self.temperature_grid[self.workpiece_grid == 0] = 300
        
        # Охлаждение во время паузы
        dt_cooling = self.params.pulse_off_time * 1e-6
        self.calculate_cooling(dt_cooling)
        
    
    def simulate_single_discharge(self):
        """Симуляция одиночного разряда"""
        discharge_point = self.find_discharge_point()
        if discharge_point is None:
            self.tool_position[2] -= 1
            return False
        
        # Проверяем, есть ли еще достаточно материала
        material_points = np.sum(self.workpiece_grid > 0)
        if material_points < 10:
            print(f"Недостаточно материала: осталось {material_points} точек")
            return False
        
        self.update_temperature(discharge_point)
        
        
        
        return True

    
    def run_simulation(self, num_discharges=10, visualize_every=10):
        """Запуск симуляции"""
        print("Начало симуляции...")
        for i in range(num_discharges):
            #print(f"Разряд {i+1}/{num_discharges}")
            if not self.simulate_single_discharge():
                print("Симуляция остановлена: нет доступных точек разряда")
                break
                
            if (i + 1) % visualize_every == 0:
                # Выводим информацию о процессе
                max_temp = np.max(self.temperature_grid)
                material_removed = np.sum(self.workpiece_grid == 0)
                print(f"Максимальная температура: {max_temp:.2f}K")
                print(f"Удалено материала: {material_removed} точек")
                print(f"\nСостояние после {i+1} разрядов:")
                self.visualize()
    
    def visualize(self):
        """Визуализация результатов"""
        fig = plt.figure(figsize=(15, 5))
        
        # Визуализация материала
        ax1 = fig.add_subplot(131, projection='3d')
        material_points = np.where(self.workpiece_grid > 0)
        ghost_points = np.where(self.workpiece_grid <= 0)
        if material_points[0].size > 0:
            ax1.scatter(material_points[0], material_points[1], material_points[2], 
                    c='blue', marker='s', alpha=0.6, label='Материал')
            #ax1.scatter(ghost_points[0], ghost_points[1], ghost_points[2], 
                    #c='red', marker='s', alpha=0, label='Удаленный материал')
        
        # Отображение инструмента
        tool_x, tool_y, tool_z = self.tool_position
        ax1.scatter([tool_x], [tool_y], [tool_z], 
                    c='red', s=100, marker='*', label='Инструмент')
        
        ax1.set_title('Распределение материала')
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.legend()
        
        # Установка одинаковых пределов для осей
        ax1.set_xlim(0, self.grid_size[0])
        ax1.set_ylim(0, self.grid_size[1])
        ax1.set_zlim(0, self.grid_size[2])
        
        # Визуализация температуры
        ax2 = fig.add_subplot(132, projection='3d')
        if material_points[0].size > 0:
            scatter = ax2.scatter(material_points[0], material_points[1], material_points[2],
                                c=self.temperature_grid[material_points],
                                cmap='hot',
                                vmin=300,
                                vmax=self.workpiece.vaporization_point)
            plt.colorbar(scatter, ax=ax2, label='Температура (K)')
        
        # Отображение инструмента на графике температуры
        ax2.scatter([tool_x], [tool_y], [tool_z], 
                    c='red', s=100, marker='*', label='Инструмент')
        
        ax2.set_title('Распределение температуры')
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_zlabel('Z')
        ax2.legend()
        
        # Установка одинаковых пределов для осей
        ax2.set_xlim(0, self.grid_size[0])
        ax2.set_ylim(0, self.grid_size[1])
        ax2.set_zlim(0, self.grid_size[2])
        
        # Сечение по центру
        ax3 = fig.add_subplot(133)
        mid_slice = self.temperature_grid[:, self.grid_size[1]//2, :]
        im = ax3.imshow(mid_slice.T,
                        cmap='hot',
                        aspect='equal',
                        vmin=300,
                        vmax=self.workpiece.vaporization_point,
                        origin='lower')
        ax3.set_title('Температура (сечение)')
        plt.colorbar(im, ax=ax3, label='Температура (K)')
        
        # Добавление точки инструмента на сечении
        if tool_y == self.grid_size[1]//2:  # если инструмент находится в плоскости сечения
            ax3.plot(tool_x, tool_z, 'r*', markersize=10, label='Инструмент')
            ax3.legend()
        
        plt.tight_layout()
        plt.show()
    
    def simulate_time_period(self, time_period: float, show_progress=True):
        """
        Симуляция процесса ЭЭО за заданный период времени
        
        Parameters:
        -----------
        time_period : float
            Период времени для симуляции [с]
        show_progress : bool
            Показывать ли прогресс симуляции
        """
        # Расчет количества импульсов за период
        total_pulse_time = (self.params.pulse_on_time + self.params.pulse_off_time) * 1e-6  # в секундах
        num_pulses = int(time_period / total_pulse_time)
        
        if show_progress:
            print(f"Расчет {num_pulses} импульсов за {time_period} секунд")
            print(f"Частота следования импульсов: {1/total_pulse_time:.1f} Гц")
        
        # Массивы для хранения истории процесса
        self.temperature_history = []
        self.material_removal_history = []
        self.time_points = []
        
        current_time = 0.0
        removed_total = 0
        
        for i in range(num_pulses):
            if show_progress and i % 100 == 0:
                print(f"Прогресс: {i/num_pulses*100:.1f}% ({i}/{num_pulses} импульсов)")
                print(f"Текущее время: {current_time*1000:.2f} мс")
                print(f"Удалено материала: {removed_total} точек")
            
            # Симуляция одного импульса
            discharge_point = self.find_discharge_point()
            if discharge_point is None:
                print("Процесс остановлен: нет доступных точек разряда")
                break
            
            # Обработка импульса
            self.update_temperature(discharge_point)
            
            # Подсчет удаленного материала
            removed = np.sum(self.workpiece_grid == 0) - removed_total
            removed_total += removed
            
            # Сохранение истории
            current_time += total_pulse_time
            self.time_points.append(current_time)
            self.temperature_history.append(np.max(self.temperature_grid))
            self.material_removal_history.append(removed)
            
            # Проверка условий остановки
            if np.sum(self.workpiece_grid > 0) < 10:
                print("Процесс остановлен: недостаточно материала")
                break
        
        # Визуализация результатов
        self.visualize_process_history()

    def visualize_process_history(self):
        """Визуализация истории процесса"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
            
        # График максимальной температуры
        ax1.plot(np.array(self.time_points)*1000, self.temperature_history, 'b-')
        ax1.set_xlabel('Время (мс)')
        ax1.set_ylabel('Максимальная температура (K)')
        ax1.grid(True)
        ax1.set_title('Изменение максимальной температуры')
            
        # График удаления материала
        cumulative_removal = np.cumsum(self.material_removal_history)
        ax2.plot(np.array(self.time_points)*1000, cumulative_removal, 'r-')
        ax2.set_xlabel('Время (мс)')
        ax2.set_ylabel('Количество удаленных точек')
        ax2.grid(True)
        ax2.set_title('Накопленное удаление материала')
            
        plt.tight_layout()
        plt.show()

    # Добавим метод для расчета производительности
    def calculate_performance_metrics(self):
        """Расчет показателей производительности процесса"""
        if not hasattr(self, 'material_removal_history'):
            print("Нет данных об истории процесса")
            return
        
        total_time = self.time_points[-1]
        total_removal = np.sum(self.material_removal_history)
        volume_per_point = self.cell_size ** 3  # объем одной ячейки
        
        # Расчет объема удаленного материала
        removed_volume = total_removal * volume_per_point
        
        # Расчет скорости съема материала
        material_removal_rate = removed_volume / total_time
        
        print("\nПоказатели производительности:")
        print(f"Время обработки: {total_time*1000:.2f} мс")
        print(f"Удалено материала: {total_removal} точек")
        print(f"Объем удаленного материала: {removed_volume*1e9:.2f} мкм³")
        print(f"Скорость съема материала: {material_removal_rate*1e9:.2f} мкм³/с")


if __name__ == "__main__":
    copper = Material(
        name="Медь",
        density=8960,
        thermal_conductivity=401,
        specific_heat=385,
        vaporization_point=2835,
        latent_heat_vaporization=4730e3
    )

    steel = Material(
        name="Сталь",
        density=7850,
        thermal_conductivity=30, #50.2
        specific_heat=486,
        vaporization_point=3273,  # Температура испарения стали
        latent_heat_vaporization=6095e3
    )
    
    params = MachineParameters(
        voltage=300,            # Напряжение [В] 25
        current=12,         # Ток [А] 2.34
        pulse_on_time=600,      # Длительность импульса [мкс] 5
        pulse_off_time=20,     # Длительность паузы [мкс] 4
        energy_efficiency=0.50 # КПД процесса 0.25
    )
    sim = EDMSimulation(
        workpiece_material=steel,
        tool_material=copper,
        machine_params=params,
        grid_size=(20, 20, 10)
    )


    #ПО ИМПУЛЬСАМ
    #print("Начальное состояние:")
    #sim.visualize()
    
    #sim.run_simulation(num_discharges=50000, visualize_every=50000)
    
    #print("\nКонечное состояние:")
    #sim.visualize()

    
    
    
    #ПО ВРЕМЕНИ
    sim.simulate_time_period(time_period=30 , show_progress=True)
    
    #Расчет показателей производительности
    sim.calculate_performance_metrics()

    #print("\nКонечное состояние:")
    sim.visualize()


