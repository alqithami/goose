#!/usr/bin/env python3
"""CHMARL-Goose agentic constrained-MARL runtime scaffold.

This is an executable research scaffold, not the final learning algorithm.
It models a Goose-like fleet operating system where vessel agents propose actions,
port agents expose capacity, and governance agents provide emission/fairness
pressure. The goal is to produce auditable decision traces for future MARL
integration and conference-grade artifact evaluation.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import asdict, dataclass, field
from pathlib import Path
from statistics import mean
from typing import Any


@dataclass
class PortAgent:
    """Port service/capacity agent."""

    port_id: str
    capacity: int
    queue: list[str] = field(default_factory=list)

    def congestion(self) -> float:
        if self.capacity <= 0:
            return 1.0
        return min(1.0, len(self.queue) / self.capacity)

    def queue_delay_estimate(self) -> float:
        return float(len(self.queue)) / max(1, self.capacity)

    def can_accept(self) -> bool:
        return len(self.queue) < self.capacity

    def snapshot(self) -> dict[str, Any]:
        return {
            "port_id": self.port_id,
            "capacity": self.capacity,
            "queue_length": len(self.queue),
            "congestion": self.congestion(),
        }


@dataclass
class VesselAgent:
    """Tool-using vessel agent scaffold."""

    vessel_id: str
    current_port: str
    fuel_curve: float
    max_speed: float
    fuel_used: float = 0.0
    destination: str | None = None
    status: str = "idle"

    def estimate_route_cost(self, destination: str, speed: float, distances: dict[str, dict[str, float]]) -> float:
        distance = distances[self.current_port][destination]
        return distance * self.fuel_curve * max(1.0, speed**2)

    def propose_action(
        self,
        ports: dict[str, PortAgent],
        distances: dict[str, dict[str, float]],
        emission_pressure: float,
        fairness_pressure: float,
        fleet_mean_fuel: float,
    ) -> dict[str, Any]:
        """Propose a destination and speed using transparent heuristic tools."""
        candidates: list[dict[str, Any]] = []
        for port_id, port in ports.items():
            if port_id == self.current_port:
                continue
            speed = max(1.0, self.max_speed * (1.0 - 0.25 * emission_pressure))
            speed = min(self.max_speed, speed)
            expected_fuel = self.estimate_route_cost(port_id, speed, distances)
            queue_delay = port.queue_delay_estimate()
            fairness_delta = abs((self.fuel_used + expected_fuel) - fleet_mean_fuel)
            score = expected_fuel + queue_delay * 10.0 + emission_pressure * expected_fuel + fairness_pressure * fairness_delta
            candidates.append(
                {
                    "destination": port_id,
                    "speed": speed,
                    "expected_fuel": expected_fuel,
                    "queue_delay": queue_delay,
                    "fairness_delta": fairness_delta,
                    "score": score,
                    "port_congestion": port.congestion(),
                }
            )

        if not candidates:
            return {
                "vessel_id": self.vessel_id,
                "action": "wait",
                "reason": "no_candidate_ports",
            }

        best = min(candidates, key=lambda item: item["score"])
        return {
            "vessel_id": self.vessel_id,
            "action": "move",
            "destination": best["destination"],
            "speed": best["speed"],
            "expected_fuel": best["expected_fuel"],
            "expected_queue_delay": best["queue_delay"],
            "expected_fairness_delta": best["fairness_delta"],
            "expected_emission_pressure": emission_pressure,
            "score": best["score"],
            "reason": "min_expected_cost_with_governance_pressure",
            "tool_evidence": {
                "route_cost_candidates": candidates,
                "fleet_mean_fuel": fleet_mean_fuel,
                "emission_pressure": emission_pressure,
                "fairness_pressure": fairness_pressure,
            },
        }

    def apply_action(self, proposal: dict[str, Any]) -> dict[str, Any]:
        if proposal.get("action") != "move":
            self.status = "waiting"
            return {"fuel_delta": 0.0, "moved": False}

        fuel_delta = float(proposal["expected_fuel"])
        self.fuel_used += fuel_delta
        self.destination = str(proposal["destination"])
        self.current_port = self.destination
        self.status = "idle"
        return {"fuel_delta": fuel_delta, "moved": True}

    def snapshot(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class EmissionGovernor:
    """Emission/fuel-budget governor."""

    budget_per_step: float
    learning_rate: float = 0.01
    pressure: float = 0.0
    cumulative_violation: float = 0.0

    def update(self, step_fuel: float) -> dict[str, Any]:
        violation = max(0.0, step_fuel - self.budget_per_step)
        self.cumulative_violation += violation
        self.pressure = max(0.0, self.pressure + self.learning_rate * violation)
        return {
            "step_fuel": step_fuel,
            "budget_per_step": self.budget_per_step,
            "violation": violation,
            "pressure": self.pressure,
            "cumulative_violation": self.cumulative_violation,
        }


@dataclass
class FairnessGovernor:
    """Fairness governor based on fuel-burden inequality."""

    target_gini: float = 0.20
    learning_rate: float = 0.50
    pressure: float = 0.0

    @staticmethod
    def gini(values: list[float]) -> float:
        if not values or all(value == 0 for value in values):
            return 0.0
        sorted_values = sorted(max(0.0, value) for value in values)
        n = len(sorted_values)
        total = sum(sorted_values)
        if total == 0:
            return 0.0
        weighted = sum((idx + 1) * value for idx, value in enumerate(sorted_values))
        return (2.0 * weighted) / (n * total) - (n + 1) / n

    @staticmethod
    def max_min_ratio(values: list[float]) -> float:
        if not values:
            return 1.0
        maximum = max(values)
        if maximum == 0:
            return 1.0
        return min(values) / maximum

    def update(self, fuel_values: list[float]) -> dict[str, Any]:
        gini_value = self.gini(fuel_values)
        max_min = self.max_min_ratio(fuel_values)
        violation = max(0.0, gini_value - self.target_gini)
        self.pressure = max(0.0, self.pressure + self.learning_rate * violation)
        return {
            "gini": gini_value,
            "max_min_ratio": max_min,
            "target_gini": self.target_gini,
            "violation": violation,
            "pressure": self.pressure,
        }


@dataclass
class FleetCoordinator:
    """Coordinator for proposal collection, conflict resolution, and evidence logging."""

    ports: dict[str, PortAgent]
    vessels: dict[str, VesselAgent]
    distances: dict[str, dict[str, float]]
    emission_governor: EmissionGovernor
    fairness_governor: FairnessGovernor
    trace: list[dict[str, Any]] = field(default_factory=list)

    def step(self, step_id: int) -> dict[str, Any]:
        fuel_values_before = [vessel.fuel_used for vessel in self.vessels.values()]
        fleet_mean_fuel = mean(fuel_values_before) if fuel_values_before else 0.0
        fairness_before = self.fairness_governor.update(fuel_values_before)

        proposals = []
        accepted = []
        step_fuel = 0.0

        for vessel in self.vessels.values():
            proposal = vessel.propose_action(
                ports=self.ports,
                distances=self.distances,
                emission_pressure=self.emission_governor.pressure,
                fairness_pressure=self.fairness_governor.pressure,
                fleet_mean_fuel=fleet_mean_fuel,
            )
            proposals.append(proposal)

            destination = proposal.get("destination")
            if proposal.get("action") == "move" and destination and self.ports[destination].can_accept():
                result = vessel.apply_action(proposal)
                self.ports[destination].queue.append(vessel.vessel_id)
                accepted.append({**proposal, "accepted": True, **result})
                step_fuel += result["fuel_delta"]
            else:
                accepted.append({**proposal, "accepted": False, "reason_rejected": "port_full_or_wait"})

        emission_after = self.emission_governor.update(step_fuel)
        fuel_values_after = [vessel.fuel_used for vessel in self.vessels.values()]
        fairness_after = self.fairness_governor.update(fuel_values_after)

        record = {
            "step": step_id,
            "proposals": proposals,
            "accepted_actions": accepted,
            "emission_governor": emission_after,
            "fairness_before": fairness_before,
            "fairness_after": fairness_after,
            "ports": {port_id: port.snapshot() for port_id, port in self.ports.items()},
            "vessels": {vessel_id: vessel.snapshot() for vessel_id, vessel in self.vessels.items()},
        }
        self.trace.append(record)
        return record

    def run(self, steps: int) -> dict[str, Any]:
        for step_id in range(steps):
            self.step(step_id)
        fuel_values = [vessel.fuel_used for vessel in self.vessels.values()]
        return {
            "steps": steps,
            "total_fuel": sum(fuel_values),
            "mean_fuel": mean(fuel_values) if fuel_values else 0.0,
            "gini": FairnessGovernor.gini(fuel_values),
            "max_min_ratio": FairnessGovernor.max_min_ratio(fuel_values),
            "emission_pressure": self.emission_governor.pressure,
            "fairness_pressure": self.fairness_governor.pressure,
            "trace": self.trace,
        }


def build_default_runtime(seed: int = 7) -> FleetCoordinator:
    random.seed(seed)
    ports = {
        "port_0": PortAgent("port_0", capacity=3),
        "port_1": PortAgent("port_1", capacity=2),
        "port_2": PortAgent("port_2", capacity=2),
    }
    distances = {
        "port_0": {"port_0": 0.0, "port_1": 80.0, "port_2": 120.0},
        "port_1": {"port_0": 80.0, "port_1": 0.0, "port_2": 70.0},
        "port_2": {"port_0": 120.0, "port_1": 70.0, "port_2": 0.0},
    }
    vessels = {
        f"vessel_{idx}": VesselAgent(
            vessel_id=f"vessel_{idx}",
            current_port=f"port_{idx % 3}",
            fuel_curve=0.0004 + idx * 0.0001,
            max_speed=12.0 + idx,
        )
        for idx in range(5)
    }
    return FleetCoordinator(
        ports=ports,
        vessels=vessels,
        distances=distances,
        emission_governor=EmissionGovernor(budget_per_step=60.0, learning_rate=0.02),
        fairness_governor=FairnessGovernor(target_gini=0.18, learning_rate=0.4),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the CHMARL-Goose agentic runtime scaffold.")
    parser.add_argument("--steps", type=int, default=5, help="Number of coordinator steps to run.")
    parser.add_argument("--seed", type=int, default=7, help="Random seed for deterministic scaffold setup.")
    parser.add_argument("--out", default="chmarl_goose_trace.json", help="Path to write JSON trace output.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    runtime = build_default_runtime(seed=args.seed)
    result = runtime.run(args.steps)
    out = Path(args.out).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "trace"}, indent=2))
    print(f"Trace written to {out}")


if __name__ == "__main__":
    main()
