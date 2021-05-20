import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles
from encoder import Encoder

clocks_per_phase = 10


@cocotb.test()
async def test_start(dut):
    clock = Clock(dut.clock, 25, units="ns")
    cocotb.fork(clock.start())
    print("Test has started the clock")
    
    dut.RSTB <= 0
    dut.power1 <= 0
    dut.power2 <= 0
    dut.power3 <= 0
    dut.power4 <= 0

    await ClockCycles(dut.clock, 8)
    dut.power1 <= 1
    await ClockCycles(dut.clock, 8)
    dut.power2 <= 1
    await ClockCycles(dut.clock, 8)
    dut.power3 <= 1
    await ClockCycles(dut.clock, 8)
    dut.power4 <= 1

    print("Power lines are all high...")

    await ClockCycles(dut.clock, 80)
    dut.RSTB <= 1

    print("Waiting for project to become active...")
    # wait for the project to become active
    await RisingEdge(dut.uut.mprj.pong_wrapper.active)

    print("Waiting for reset to go high...")
    await RisingEdge(dut.uut.mprj.pong_wrapper.pong0.reset)
    await FallingEdge(dut.uut.mprj.pong_wrapper.pong0.reset)
    print("Reset completed")

    dut.