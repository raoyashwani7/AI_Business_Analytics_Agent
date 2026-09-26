# AI Business Analytics & Decision Support Agent

An AI-powered business analytics platform that allows users to ask business questions in natural language and receive data-driven insights from structured business data and business knowledge.

The project combines **Python, FastAPI, PostgreSQL, LangChain, LangGraph, RAG, ChromaDB, Redis, and LLMs** to create an intelligent business analytics and decision-support system.

---

## Project Overview

Traditional business analytics often requires users to write SQL queries or manually analyze dashboards.

This project provides a natural-language interface where a user can ask questions such as:

- What is the total revenue?
- Which region generates the highest revenue?
- Which category has the highest profit?
- What are the top-selling products?
- Give me a business summary.
- What business insights can be derived from the sales data?

The AI agent interprets the user's question, selects the appropriate analytical tool, retrieves the required data from PostgreSQL, and generates a human-readable response.

The system also uses **RAG (Retrieval-Augmented Generation)** to retrieve relevant business knowledge and **Redis caching** to improve the response time for repeated questions.

---

# Project Objective

The main objective is to build a natural-language **Business Intelligence and AI Decision Support System** that combines:

- SQL-based data analysis
- Machine learning/AI concepts
- Large Language Models
- Agentic AI
- LangGraph workflows
- Retrieval-Augmented Generation
- Vector databases
- Redis caching
- REST APIs
- Interactive web dashboard

The goal is to make business analytics accessible through natural-language questions instead of requiring users to manually write SQL queries.

---

# Key Features

## 1. Natural Language Business Questions

Users can ask business questions in normal language.

Example:

```text
What is the total revenue and which region generates the most revenue?
