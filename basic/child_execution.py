from child_protocols import BasicProtocol
from gradysim.simulator.handler.timer import TimerHandler
from gradysim.simulator.simulation import SimulationBuilder, SimulationConfiguration
from gradysim.simulator.handler.visualization import VisualizationHandler
from gradysim.simulator.handler.communication import CommunicationHandler, CommunicationMedium
from gradysim.simulator.handler.mobility import MobilityHandler

def main():

    config = SimulationConfiguration(
        duration=60,
    )

    builder = SimulationBuilder(config)

    builder.add_node(BasicProtocol, (10,0,0))
    builder.add_node(BasicProtocol, (-10,0,0))

    medium = CommunicationMedium(
        transmission_range=25
    )


    builder.add_handler(TimerHandler())
    builder.add_handler(MobilityHandler())
    builder.add_handler(CommunicationHandler(medium))
    builder.add_handler(VisualizationHandler())

    simulation = builder.build()
    simulation.start_simulation()

if __name__ == "__main__":
    main()