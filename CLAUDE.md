# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository serves as a preferences and examples collection for AI assistants working on the user's other projects. It contains code templates, configuration examples, and preferred patterns that should inform how AI assistants approach development tasks in the user's other repositories.

## Structure

The repository is organized by topic, with each folder containing multiple example implementations:

- `.devcontainer/` - Development container configurations
  - `ubuntu-python-poetry/` - Ubuntu 24.04 + Python + Poetry devcontainer setup
  - `ubuntu-python-uv/` - Ubuntu 24.04 + Python + uv devcontainer setup
  - `node-caddy/` - Node.js with Caddy web server devcontainer setup

Each folder contains alternative approaches or examples for the same concept. Only one example from each topic would typically be used in any given project.

## Important Notes

- This repository contains examples and templates, not production code
- When applying these patterns to other projects, adapt the specific versions and configurations as needed
- Read the relevant example files to understand the user's preferred patterns and configurations
