import numpy as np

from src.evo_balt.evo import PhysicsType


class FakeModel:
    '''
    Class that imitates SWAN-model behaviour:
        it encapsulates simulation results on a model params grid:
            [drag, physics, wcr, ws] = model_output, i.e. forecasts
    '''

    def __init__(self, config):
        '''
        Init parameters grid
        :param config: EvoConfig that contains parameters of evolution
        '''
        self.config = config
        self._init_grids()

    def _init_grids(self):
        self.drag_grid = self._grid(self.config.grid_by_name('drag'))
        self.wcr_grid = self._grid(self.config.grid_by_name('wcr'))
        self.ws_grid = self._grid(self.config.grid_by_name('ws'))

        self.grid = np.zeros((len(self.drag_grid), len(PhysicsType), len(self.wcr_grid), len(self.ws_grid)))
        # TODO: load grid values from smth

    def _grid(self, grid_params):
        grid = np.linspace(grid_params['min'], grid_params['max'],
                           num=int((grid_params['max'] - grid_params['min']) / grid_params['delta']))
        grid = np.round(grid, decimals=3)
        return grid

    def output(self, params):
        '''

        :param params: SWAN parameters
        :return: ForecastFile
        '''

        drag_idx = self.drag_grid.tolist().index(params.drag_func)
        physics_idx = (list(PhysicsType)).index(params.physics_type)
        wcr_idx = self.wcr_grid.tolist().index(params.wcr)
        ws_idx = self.ws_grid.tolist().index(params.ws)

        return self.grid[drag_idx, physics_idx, wcr_idx, ws_idx]


class GridFile:
    '''
    Class that loads results of multiple SWAN simulations from CSV-file
    and construct grid of parameters
    '''

    def __init__(self, path):
        '''

        :param path: path to CSV-file
        '''
        self.path = path
        self._load()

    def _load(self):
        import csv
        with open(self.path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row['ID'])


grid = GridFile(path="../../samples/fixed.csv")
# fake = FakeModel(config=EvoConfig())
# print(fake.output(params=SWANIndivid(1.505, PhysicsType.GEN3, 1.505, 1.505)))
