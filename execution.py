from MyProtocol import MyProtocol
from gradysim.simulator.handler.timer import TimerHandler
from gradysim.simulator.simulation import SimulationBuilder, SimulationConfiguration


def main():
    # Configuring the simulator. The only option that interests us
    # is limiting the simulator to 10 real-world seconds.
    config = SimulationConfiguration(
        duration=300,
        real_time=True
    )
    # Instantiating the simulator builder with the created config
    builder = SimulationBuilder(config)

    # Calling the add_node function we create a network node that
    # will run the CounterProtocol we created.
    builder.add_node(MyProtocol, (0, 0, 0))
    builder.add_node(MyProtocol, (10, 15, 20))
    builder.add_node(MyProtocol, (5, 5, 5))
    builder.add_node(MyProtocol, (12, 0, 3))
    # Handlers enable certain simulator features. In the case of our
    # simulator all we really need is a timer.
    builder.add_handler(TimerHandler())

    # Calling the build functions creates a simulator from the previously
    # specified options.
    simulation = builder.build()

    # The start_simulation() method will run the simulator until our 10-second
    # limit is reached.
    simulation.start_simulation()


if __name__ == "__main__":
    main()
