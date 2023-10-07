[![CircleCI](https://dl.circleci.com/status-badge/img/gh/eder/888spectate-challenger/tree/main.svg?style=svg&circle-token=63d47442a2880587f1fa5a9c1818e1a38c40f2f9)](https://dl.circleci.com/status-badge/redirect/gh/eder/888spectate-challenger/tree/main)

# 888Spectate - REST API Documentation

888Spectate is a REST API that manages sports, events, and selections for a sportsbook product. This API is designed with a SOLID-based approach, uses FastAPI for asynchronous development, and relies on PostgreSQL without an ORM. Pytest is used for testing.

## Table of Contents
- [Introduction](#introduction)
- [System Requirements](#system-requirements)
- [API Endpoints](#api-endpoints)
  - [Create](#create)
  - [Search](#search)
  - [Update](#update)
- [Payload for Search](#payload-for-search)
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Introduction

888Spectate is responsible for managing sports, events, and selections in a sportsbook product. Here are the main components:

- **Sport:**
  - Name
  - Slug (URL-friendly version of name)
  - Active (true or false)

- **Event:**
  - Name
  - Slug (URL-friendly version of name)
  - Active (true or false)
  - Type (preplay or inplay)
  - Sport
  - Status (Pending, Started, Ended, or Cancelled)
  - Scheduled start (UTC datetime)
  - Actual start (created when the event status changes to "Started")

- **Selection:**
  - Name
  - Event
  - Price (Decimal value, to 2 decimal places)
  - Active (true or false)
  - Outcome (Unsettled, Void, Lose, or Win)

## System Requirements

888Spectate's REST API demonstrates the following functionalities:

- Creating sports, events, or selections
- Searching for sports, events, or selections
- Updating sports, events, or selections
- Combining N filters with an AND expression
- Sports may have multiple events
- Events may have multiple selections
- When all selections of an event are inactive, the event becomes inactive
- When all events of a sport are inactive, the sport becomes inactive

## API Endpoints

### Create

- **POST /api/v1/sports/**: Create a new sport.
- **POST /api/v1/events/**: Create a new event.
- **POST /api/v1/selections/**: Create a new selection.

### Search

- **GET /api/v1/events/search/**: Search for sports, events, or selections with specific criteria.

### Update

- **PUT /api/v1/sports/{sport_id}/**: Update an existing sport.
- **PUT /api/v1/events/{event_id}/**: Update an existing event.
- **PUT /api/v1/selections/{selection_id}/**: Update an existing selection.

## Payload for Search

This is the payload for searching for sports, events, or selections within a specific context:

```json
/api/v1/events/search/
{
  "sport": {
    "name_regex": "string",
    "min_active_count": 0,
    "start_time_from": "2023-10-07T13:26:44.192Z",
    "start_time_to": "2023-10-07T13:26:44.192Z",
    "timezone": "string",
    "min_active_selections": 0
  },
  "event": {
    "name_regex": "string",
    "min_active_count": 0,
    "start_time_from": "2023-10-07T13:26:44.192Z",
    "start_time_to": "2023-10-07T13:26:44.192Z",
    "timezone": "string",
    "min_active_selections": 0
  },
  "selection": {
    "name_regex": "string",
    "min_active_count": 0,
    "start_time_from": "2023-10-07T13:26:44.192Z",
    "start_time_to": "2023-10-07T13:26:44.192Z",
    "timezone": "string",
    "min_active_selections": 0
  }
}

