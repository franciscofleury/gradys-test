from uav_protocol import UavProtocol
from sensor_protocol import SensorProtocol
from gradysim.simulator.handler.timer import TimerHandler
from gradysim.simulator.simulation import SimulationBuilder, SimulationConfiguration
from gradysim.simulator.handler.visualization import VisualizationHandler, VisualizationController, VisualizationConfiguration
from gradysim.simulator.handler.communication import CommunicationHandler, CommunicationMedium
from gradysim.simulator.handler.mobility import MobilityHandler

def main():

    config = SimulationConfiguration(
        duration=300,
        real_time=True
    )

    builder = SimulationBuilder(config)

    builder.add_node(UavProtocol, (0,0,20))
    builder.add_node(UavProtocol, (5,0,20))
    builder.add_node(UavProtocol, (-5,0,20))
    builder.add_node(SensorProtocol, (300, -20, 0))
    builder.add_node(SensorProtocol, (152, -30, 0))
    builder.add_node(SensorProtocol, (-53, 32, 0))
    builder.add_node(UavProtocol, (0,5,20))
    builder.add_node(UavProtocol, (0,-5,20))
    builder.add_node(UavProtocol, (0,5,20))
    builder.add_node(UavProtocol, (0,-5,20))
    builder.add_node(UavProtocol, (0,5,20))
    builder.add_node(UavProtocol, (0,-5,20))
    builder.add_node(UavProtocol, (0,5,20))
    builder.add_node(UavProtocol, (0,-5,20))
    builder.add_node(UavProtocol, (0,5,20))
    builder.add_node(UavProtocol, (0,-5,20))
    
    medium = CommunicationMedium(
        transmission_range=30
    )

    builder.add_handler(TimerHandler())
    builder.add_handler(MobilityHandler())
    builder.add_handler(CommunicationHandler(medium))
    builder.add_handler(VisualizationHandler(VisualizationConfiguration(
        x_range=(-300,300),
        y_range=(-300,300),
        z_range=(0,300)
    )))

    simulation = builder.build()
    simulation.start_simulation()
if __name__ == "__main__":
    main()