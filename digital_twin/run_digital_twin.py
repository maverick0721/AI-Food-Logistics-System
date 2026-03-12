from digital_twin.simulator import DigitalTwinSimulator


sim = DigitalTwinSimulator()

for hour in range(24):

    sim.step(hour)