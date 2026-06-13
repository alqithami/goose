from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "chmarl_goose_runtime.py"


def load_runtime_module():
    spec = importlib.util.spec_from_file_location("chmarl_goose_runtime", MODULE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def runtime():
    return load_runtime_module()


def test_port_agent_congestion_and_capacity(runtime):
    port = runtime.PortAgent("port_test", capacity=2)
    assert port.congestion() == pytest.approx(0.0)
    assert port.can_accept() is True

    port.queue.extend(["vessel_0", "vessel_1"])
    assert port.congestion() == pytest.approx(1.0)
    assert port.queue_delay_estimate() == pytest.approx(1.0)
    assert port.can_accept() is False


def test_vessel_agent_proposes_auditable_action(runtime):
    ports = {
        "port_0": runtime.PortAgent("port_0", capacity=2),
        "port_1": runtime.PortAgent("port_1", capacity=2),
    }
    distances = {
        "port_0": {"port_0": 0.0, "port_1": 100.0},
        "port_1": {"port_0": 100.0, "port_1": 0.0},
    }
    vessel = runtime.VesselAgent("vessel_0", current_port="port_0", fuel_curve=0.001, max_speed=10.0)

    proposal = vessel.propose_action(
        ports=ports,
        distances=distances,
        emission_pressure=0.0,
        fairness_pressure=0.0,
        fleet_mean_fuel=0.0,
    )

    assert proposal["action"] == "move"
    assert proposal["destination"] == "port_1"
    assert proposal["expected_fuel"] > 0
    assert proposal["reason"] == "min_expected_cost_with_governance_pressure"
    assert "tool_evidence" in proposal
    assert proposal["tool_evidence"]["route_cost_candidates"]


def test_emission_governor_pressure_increases_on_violation(runtime):
    governor = runtime.EmissionGovernor(budget_per_step=10.0, learning_rate=0.5)

    no_violation = governor.update(step_fuel=5.0)
    assert no_violation["violation"] == pytest.approx(0.0)
    assert no_violation["pressure"] == pytest.approx(0.0)

    violation = governor.update(step_fuel=14.0)
    assert violation["violation"] == pytest.approx(4.0)
    assert violation["pressure"] == pytest.approx(2.0)
    assert violation["cumulative_violation"] == pytest.approx(4.0)


def test_fairness_governor_metrics_and_pressure(runtime):
    governor = runtime.FairnessGovernor(target_gini=0.1, learning_rate=1.0)

    assert governor.gini([0.0, 0.0, 0.0]) == pytest.approx(0.0)
    assert governor.max_min_ratio([0.0, 0.0, 0.0]) == pytest.approx(1.0)
    assert governor.max_min_ratio([2.0, 4.0, 8.0]) == pytest.approx(0.25)

    update = governor.update([0.0, 0.0, 10.0])
    assert update["gini"] > governor.target_gini
    assert update["pressure"] > 0.0


def test_fleet_coordinator_generates_decision_trace(runtime):
    coordinator = runtime.build_default_runtime(seed=7)
    result = coordinator.run(steps=3)

    assert result["steps"] == 3
    assert result["total_fuel"] >= 0.0
    assert 0.0 <= result["gini"] <= 1.0
    assert 0.0 <= result["max_min_ratio"] <= 1.0
    assert len(result["trace"]) == 3

    first_step = result["trace"][0]
    assert "proposals" in first_step
    assert "accepted_actions" in first_step
    assert "emission_governor" in first_step
    assert "fairness_before" in first_step
    assert "fairness_after" in first_step
    assert "ports" in first_step
    assert "vessels" in first_step


def test_runtime_trace_contains_auditable_tool_evidence(runtime):
    coordinator = runtime.build_default_runtime(seed=7)
    result = coordinator.run(steps=1)
    proposals = result["trace"][0]["proposals"]

    assert proposals
    move_proposals = [proposal for proposal in proposals if proposal.get("action") == "move"]
    assert move_proposals
    assert all("tool_evidence" in proposal for proposal in move_proposals)
