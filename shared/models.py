"""Shared data shapes for call-centre simulation challenges."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CallCentreSnapshot(BaseModel):
    """Point-in-time state for the Northline Support call centre."""

    backlog: float = Field(ge=0, description="Calls waiting to be answered")
    staffed_agents: float = Field(ge=0, description="Agents currently logged in")
    answered_today: float = Field(ge=0, description="Cumulative calls handled today")
