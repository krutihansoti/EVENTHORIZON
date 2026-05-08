## EventHorizon — Predictive Threat Intelligence Engine
An AI/ML-powered predictive threat intelligence engine for Physical Access Control Systems (PACS) and IP Video Surveillance (IPVS) that analyzes event logs and behavioral patterns to identify anomalies, dynamically assess risk across users, devices, and zones, and deliver real-time organizational security intelligence.

# Problem Statement

Modern enterprise security systems generate massive amounts of telemetry but largely function as reactive monitoring tools instead of intelligent threat detection platforms.
Traditional PACS and IPVS deployments suffer from:

- Fragmented security visibility across disconnected systems
- Hidden behavioral anomalies that remain undetected
- Operator overload from excessive low-context alerts
- Inability to correlate events across users, devices, and zones
- Reactive security workflows instead of predictive intelligence

As a result, critical threats often remain buried beneath seemingly normal activity.

# Solution Overview

EventHorizon acts as an AI-powered intelligence layer above existing PACS and IPVS infrastructure.The platform continuously ingests and correlates telemetry from access control and surveillance systems, identifies suspicious behavioral patterns, dynamically evaluates contextual risk, and transforms raw security events into actionable intelligence.

Instead of simply displaying logs, EventHorizon helps security teams understand:
- What is happening- Why it matters - Which entities are at risk - What actions should be taken

# Core Features & Impact
Feature	Description	Business Impact	Stakeholders
- Unified Telemetry Engine:Processes PACS and IPVS events as a single intelligence stream	Eliminates siloed monitoring	SOC Teams, Security Operators
- Behavioral Anomaly Detection:	Detects suspicious behavioral deviations across entities	Enables early threat identification	Security Analysts
- Dynamic Risk Scoring:	Continuously evaluates contextual risk across User-Device-Zone	Prioritized incident response	Security Managers
- Multi-Source Correlation:	Correlates events across access control and surveillance systems	Improves threat accuracy	Incident Response Teams
- AI Tactical Intelligence:	Generates plain-English threat summaries and recommendations	Reduces investigation effort	Security Operators
- Real-Time Threat Dashboard:	Streams prioritized alerts with live risk visibility	Faster operational response	Command Centers
- Tactical Fallback Engine:	Maintains scoring and telemetry tracking during AI/API failures	Operational continuity	Enterprise Security Teams

# Project Coverage
Intelligence & Correlation Engines
Dynamic User-Device-Zone risk scoring
Behavioral anomaly detection
Cross-system event correlation - Real-time Simulated PACS event streams- IPVS telemetry
AI Intelligence Layer - Google Gemini integration - Tactical incident briefings - AI-generated recommendations
Prioritized threat dashboard
Real-time security posture visibility

# Technology Stack
Layer	Technology
Backend	Python + FastAPI
Database	SQLite (aiosqlite)
AI / LLM	Google Gemini 1.5 Flash
Real-Time Streaming	Server-Sent Events (SSE)
Frontend	HTML5, CSS3, JavaScript (ES6+)
 # Roadmap
Predictive machine learning threat models
RTSP-based live video analytics using OpenCV
Adaptive threat intelligence and trust scoring
AI-driven automated response workflows
