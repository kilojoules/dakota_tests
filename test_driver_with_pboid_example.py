from openmdao.main.api import Assembly
import dakota_driver
from openmdao.examples.simple.paraboloid import Paraboloid
import dakota

class OptimizationUnconstrained(Assembly):
    """Unconstrained optimization of the Paraboloid Component."""

    def configure(self):

        # Create Optimizer instance
        driver_object = dakota_driver.driver.pydakdriver()
        driver_object.Optimization()
        #driver_object.numerical_gradients()
        #driver_object.final_point = [20,20]
        #driver_object.num_steps = 10
        self.add('driver', driver_object)

        # Create Paraboloid component instances
        self.add('paraboloid', Paraboloid())

        # Iteration Hierarchy
        self.driver.workflow.add('paraboloid')

        # SLSQP Flags
        self.driver.iprint = 0

        # Objective
        self.driver.add_objective('paraboloid.f_xy')

        # Design Variables
        self.driver.add_parameter('paraboloid.x', low=-50., high=50.)
        self.driver.add_parameter('paraboloid.y', low=-50., high=50.)

if __name__ == "__main__":

    opt_problem = OptimizationUnconstrained()

    import time
    tt = time.time()

    opt_problem.run()

    print "\n"
    print "Minimum found at (%f, %f)" % (opt_problem.paraboloid.x, \
                                     opt_problem.paraboloid.y)
    print "Elapsed time: ", time.time()-tt, "seconds"
