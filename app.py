UI FAULTS
Inconsistent Theming: The file upload dropzone and the Risk Telemetry chart use stark white backgrounds that clash heavily with the application's dark theme.

Missing UI Data: Under "DETECTED ANOMALIES", the "LINE:" indicator displays an empty white box instead of the actual line number.

Poor Chart Legibility: The X-axis labels ("AS 1", "AS 2") on the Risk Telemetry chart are rotated vertically and are too small.

Misaligned Elements: The "INITIATE SCAN" button and the "INTEGRITY INDEX" metric are awkwardly spaced within the "EXECUTION PROTOCOL" section.

TECHNICAL FAULTS
Parsing Failure: The backend scanner detects the anomaly type (e.g., HARDCODED_SECRET_PASSWORD) but fails to extract or pipe the corresponding line number to the frontend.

Incorrect Chart Type: An area chart is used to plot discrete, disconnected events (Scan 1 vs Scan 2). Area charts imply a continuous, cumulative relationship over time, which misrepresents distinct code commits.

IMPROVEMENTS
Native Dark Mode: Configure the charting library (e.g., Plotly, Altair) and Streamlit's base theme settings to enforce a transparent or dark background for all visual components.

Enhanced Anomaly Display: Replace simple text blocks with expandable sections (st.expander) or data tables that show the exact code snippet, line number, and severity level alongside the anomaly name.

Interactive Feedback: Provide user feedback mechanisms, such as a toast notification or spinner, when "INITIATE SCAN" or "SAVE TELEMETRY" is triggered.

RISK TELEMETRY GRAPH REPLACEMENT
Why replace it?
The current area chart is visually jarring, lacks interactivity, and incorrectly models discrete scan data as a continuous flow. It provides no context beyond a single number.

Better Alternatives:

Interactive Bar Chart: Use a bar chart to represent individual scan aliases on the X-axis. Apply conditional coloring (e.g., Red for <50%, Green for >80%) to make the risk level instantly recognizable.

Radar/Spider Chart: Instead of a single "Integrity Index," plot scores across multiple specific risk categories (e.g., Hardcoded Secrets, Insecure Dependencies, Auth Bypasses) to show exactly where the risk lies in that specific build.

Gauge/Donut Chart: Use a gauge chart alongside the historical trend to prominently display the health of the current scan with clear threshold zones.
