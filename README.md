# AI Business Analytics & Decision Support Agent

An AI-powered business analytics project that allows users to ask business questions and receive data-driven insights, analysis, and recommendations.

## Project Objective

The goal of this project is to build a natural-language business intelligence system that combines SQL, data analytics, LLMs, and agentic AI.

## Current Progress

### Day 1 — Project & Database Setup

- Created Python virtual environment
- Initialized Git repository
- Connected project with GitHub
- Installed PostgreSQL
- Created PostgreSQL database: `project18_db`
- Created `sales` table
- Imported 5,000 business sales records from CSV
- Verified the imported data using SQL
- Calculated total business revenue

## Database

Database:

`project18_db`

Main table:

`sales`

Records:

`5,000`

## First Business Analysis

Total Revenue:

`₹166,378,556.00`

SQL query:

```sql
SELECT SUM(revenue) AS total_revenue
FROM sales;