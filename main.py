# =========================
# OpenEnv Real-World Environment: Smart Customer Support Automation
# =========================

# This is a COMPLETE minimal working OpenEnv-style environment
# with step(), reset(), state(), tasks, rewards, graders, and baseline agent

import random
from dataclasses import dataclass
from typing import Dict, Any

# -------------------------
# STATE MODEL
# -------------------------

@dataclass
class TicketState:
    ticket_id: int
    user_query: str
    resolved: bool
    steps_taken: int


# -------------------------
# ENVIRONMENT
# -------------------------

class SupportEnv:
    def __init__(self):
        self.state_obj = None
        self.max_steps = 5

    def reset(self) -> Dict:
        queries = [
            "Reset my password",
            "Refund request",
            "Order not delivered"
        ]

        self.state_obj = TicketState(
            ticket_id=random.randint(1000, 9999),
            user_query=random.choice(queries),
            resolved=False,
            steps_taken=0
        )

        return self.state()

    def state(self) -> Dict:
        return {
            "ticket_id": self.state_obj.ticket_id,
            "query": self.state_obj.user_query,
            "resolved": self.state_obj.resolved,
            "steps": self.state_obj.steps_taken
        }

    def step(self, action: str):
        reward = 0.0
        done = False

        self.state_obj.steps_taken += 1

        # --- RULE LOGIC ---
        if "password" in self.state_obj.user_query.lower() and action == "reset_password":
            reward = 1.0
            self.state_obj.resolved = True

        elif "refund" in self.state_obj.user_query.lower() and action == "process_refund":
            reward = 1.0
            self.state_obj.resolved = True

        elif "order" in self.state_obj.user_query.lower() and action == "track_order":
            reward = 1.0
            self.state_obj.resolved = True

        else:
            reward = 0.2  # partial credit

        if self.state_obj.resolved or self.state_obj.steps_taken >= self.max_steps:
            done = True

        return self.state(), reward, done, {}


# -------------------------
# TASKS + GRADERS
# -------------------------

class EasyTask:
    def grade(self, state):
        return 1.0 if state["resolved"] else 0.0


class MediumTask:
    def grade(self, state):
        if state["resolved"] and state["steps"] <= 3:
            return 1.0
        elif state["resolved"]:
            return 0.5
        return 0.0


class HardTask:
    def grade(self, state):
        if state["resolved"] and state["steps"] == 1:
            return 1.0
        elif state["resolved"]:
            return 0.7
        return 0.0


# -------------------------
# BASELINE AGENT
# -------------------------

class BaselineAgent:
    def act(self, state):
        query = state["query"].lower()

        if "password" in query:
            return "reset_password"
        elif "refund" in query:
            return "process_refund"
        elif "order" in query:
            return "track_order"
        return "ask_help"


# -------------------------
# RUN BASELINE
# -------------------------


def run_baseline():
    env = SupportEnv()
    agent = BaselineAgent()

    scores = []

    for _ in range(10):
        state = env.reset()
        done = False

        while not done:
            action = agent.act(state)
            state, reward, done, _ = env.step(action)

        task = MediumTask()
        score = task.grade(state)
        scores.append(score)

    print("Average Score:", sum(scores) / len(scores))


if __name__ == "__main__":
    run_baseline()


# -------------------------
# openenv.yaml
# -------------------------

"""
name: support-env
version: 1.0
entry_point: main.py

observation_space:
  ticket_id: int
  query: string
  resolved: bool
  steps: int

action_space:
  - reset_password
  - process_refund
  - track_order
  - ask_help

reward_range: [0.0, 1.0]
"""


# -------------------------
# DOCKERFILE
# -------------------------

"""
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir
CMD ["python", "main.py"]
"""


# -------------------------
# README (SHORT)
# -------------------------

"""
# Smart Support OpenEnv

## Description
Simulates real-world customer support automation.

## Tasks
- Easy: Just resolve
- Medium: Resolve quickly
- Hard: Resolve optimally

## Run
python main.py

## HF Spaces
Use Docker deployment
"""
