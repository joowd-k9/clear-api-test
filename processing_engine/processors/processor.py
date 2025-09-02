"""
Processor configuration and metadata models.

This module defines static models that describe a processor itself,
its capabilities, and configuration parameters. These models serve as
the blueprint of processors, separate from their execution outcomes.

Key responsibilities:
- Represent processor metadata (ID, name, description, version).
- Define configurable parameters and expected inputs.
- Track processor status (active, deprecated, experimental).
- Provide compatibility details for orchestration and integration.

These models are relatively static, describing *what a processor is*
and *how it should run*, as opposed to execution models which track
the results of a specific run.
"""
