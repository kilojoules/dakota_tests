""" Global SA Test """

from openmdao.main.api import Component, Assembly
from openmdao.main.datatypes.api import Float

from dakota_driver.driver import DakotaGlobalSAStudy
#from dakota_driver import DakotaOptimizer, DakotaMultidimStudy, DakotaVectorStudy

from wisdem.lcoe.lcoe_csm_assembly import lcoe_csm_assembly

class lcoe_csm_SAStudy(Assembly):
    """ Use DAKOTA to run a vector study. """

    def configure(self):
        """ Configure driver and its workflow. """
        super(Assembly, self).configure()
        self.add('lcoe_csm', lcoe_csm_assembly()) 

        driver = self.add('driver', DakotaGlobalSAStudy())
        driver.workflow.add('lcoe_csm')
        driver.stdout = 'dakota.out'
        driver.stderr = 'dakota.err'
        driver.sample_type = 'random'
        driver.seed = 20
        driver.samples = 500 
        driver.vbd = True

        # Can't have parameter with no 'low' or 'high' defined.
        driver.add_parameter('lcoe_csm.rotor_diameter', low=126.0*0.5, high=126.0*1.5)
        driver.add_parameter('lcoe_csm.machine_rating', low=5000.0*0.5, high=5000.0*1.5)
        driver.add_parameter('lcoe_csm.hub_height', low=90.0*0.5, high=90.0*1.5)
        driver.add_parameter('lcoe_csm.max_tip_speed', low=80.0*0.5, high=80.0*1.5)
        driver.add_objective('lcoe_csm.coe')
        driver.add_objective('lcoe_csm.lcoe')
        driver.add_objective('lcoe_csm.net_aep')
        driver.add_objective('lcoe_csm.bos_costs')
        driver.add_objective('lcoe_csm.avg_annual_opex')
        driver.add_objective('lcoe_csm.turbine_cost')
        driver.add_objective('lcoe_csm.turbine_mass')
        driver.add_objective('lcoe_csm.rated_rotor_speed')


if __name__ == '__main__':

    # LCOE sensitivity analysis.

    top = lcoe_csm_SAStudy()
    top.lcoe_csm.advanced_blade = True
    top.run()

    """ Cleanup files. """
    '''import os
    for name in ('dakota.out', 'dakota.err',
                 'dakota.rst', 'dakota_tabular.dat', 'driver.in'):
        if os.path.exists(name):
            os.remove(name)'''
