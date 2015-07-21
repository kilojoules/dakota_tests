#from openmdao.main.datatypes.api import Float
from dakota_driver.driver import pydakdriver
from openmdao.main.api import Component, Assembly
from wisdem.lcoe.lcoe_csm_assembly import lcoe_csm_assembly

class lcoe_wind_SA(Assembly):
    def configure(self):
        super(Assembly, self).configure()

        # Let's analyze the lifetime cost of energy cost scaling model!
        self.add('lcoe_csm', lcoe_csm_assembly())

        # ..using the cutting edge pydakdriver
        dakDriver = pydakdriver()
        dakDriver.UQ(seed=3232)
        driver = self.add('driver',dakDriver)
        driver.workflow.add('lcoe_csm')
        driver.stdout = 'dakota.out'
        driver.stderr = 'dakota.err'

        driver.add_parameter('lcoe_csm.weibull_k',low=2.6*0.5, high=2.6*1.5)
        driver.add_parameter('lcoe_csm.shear_exponent',low=.1*0.5, high=.1*1.5)

        # use same objectives as previous sensitivity analysis
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

    top = lcoe_wind_SA()
    top.lcoe_csm.advanced_blade = True
    top.run()
