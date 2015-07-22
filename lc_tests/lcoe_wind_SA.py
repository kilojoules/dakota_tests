#from openmdao.main.datatypes.api import Float
from dakota_driver.driver import pydakdriver
from openmdao.main.api import Component, Assembly
from wisdem.lcoe.lcoe_se_assembly import lcoe_se_assembly

class lcoe_wind_SA(Assembly):
    def configure(self):
        super(Assembly, self).configure()

        # Let's analyze the lifetime cost of energy cost scaling model!
        self.add('lcoe_se', lcoe_se_assembly())

        # ..using the cutting edge pydakdriver
        dakDriver = pydakdriver()
        dakDriver.UQ()
        dakDriver.seed = 4723
        driver = self.add('driver',dakDriver)
        driver.workflow.add('lcoe_se')
        driver.stdout = 'dakota.out'
        driver.stderr = 'dakota.err'

        driver.add_parameter('lcoe_se.A',low=8.2*0.5, high=8.2*1.5)
        driver.add_parameter('lcoe_se.k',low=2.0*0.5, high=2.0*1.5)
        driver.add_parameter('lcoe_se.shear_exponent',low=.2*0.5, high=.2*1.5)

        # use same objectives as previous sensitivity analysis
        driver.add_objective('lcoe_se.coe')
        # driver.add_objective('lcoe_se.lcoe')
        driver.add_objective('lcoe_se.net_aep')
        driver.add_objective('lcoe_se.bos_costs')
        driver.add_objective('lcoe_se.avg_annual_opex')
        driver.add_objective('lcoe_se.turbine_cost')
        # driver.add_objective('lcoe_se.turbine_mass')
        # driver.add_objective('lcoe_se.rated_rotor_speed')


if __name__ == '__main__':

    # LCOE sensitivity analysis.

    top = lcoe_wind_SA()
    top.lcoe_se.advanced_blade = True
    top.run()
