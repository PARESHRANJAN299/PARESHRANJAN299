<div align="center">
    <img src="./assets/data-architecture.svg" alt="Animated data architecture: sources to ingestion to S3 to Databricks Auto Loader to Bronze, Silver and Gold" width="100%"/>
    <br/>
    <br/>
    <a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=24&duration=2500&pause=1200&color=58A6FF&center=true&vCenter=true&width=760&height=50&lines=Paresh+Ranjan+Rout;Data+Engineer;Databricks+%C2%B7+AWS+%C2%B7+Azure+%C2%B7+Python+%C2%B7+SQL;Founder%2C+SushaAstra+Technology" alt="Paresh Ranjan Rout, Data Engineer" /></a>
</div>

<div align="center">
    <a href="https://linkedin.com/in/paresh-ranjan-rout-7a2788227"><img src="https://img.shields.io/badge/-LinkedIn-1a1a2e?style=for-the-badge&logo=linkedin&logoColor=0A66C2" alt="LinkedIn"/></a>
    <a href="https://youtube.com/@SushaAstraOfficial"><img src="https://img.shields.io/badge/-YouTube-1a1a2e?style=for-the-badge&logo=youtube&logoColor=FF0000" alt="YouTube"/></a>
    <br>
    <img src="https://hits.sh/github.com/PARESHRANJAN299.svg?style=for-the-badge&color=1a1a2e&labelColor=1a1a2e&label=PROFILE%20VIEWS" alt="Profile views" />
</div>

## About

<table width="100%">
    <tr>
        <td width="28%" align="center" valign="middle">
            <img src="./assets/profile.png" alt="Paresh Ranjan Rout" width="200" />
        </td>
        <td width="72%" valign="middle">
            <h3>Paresh Ranjan Rout</h3>
            <p><strong>Data Engineer</strong> · Founder, SushaAstra Technology</p>
            <p>I design and build cloud data pipelines on Databricks and AWS, taking data from raw ingestion through governed Bronze, Silver, and Gold layers. My work emphasizes reliable incremental ingestion, secure access control, and clear technical documentation.</p>
            <p><strong>Core areas:</strong> Databricks lakehouse, Delta Lake, Unity Catalog, Python, SQL, AWS, and Azure.</p>
        </td>
    </tr>
</table>

```javascript
const PARESH = {
    role: "Data Engineer · Founder, SushaAstra Technology",
    focus: ["Data Engineering", "AI", "IoT"],
    languages: ["Python", "SQL", "PySpark", "Bash"],
    dataEngineering: {
        lakehouse: ["Databricks", "Delta Lake", "Unity Catalog", "Auto Loader", "Lakeflow Pipelines"],
        architecture: ["Bronze / Silver / Gold (medallion)", "Incremental ingestion", "Streaming events"],
        databases: ["PostgreSQL", "MySQL"],
        deployment: ["Databricks Asset Bundles"]
    },
    cloud: {
        aws: ["EC2", "S3", "IAM"],
        azure: ["Azure Data Factory"],
        also: ["Docker", "Linux"]
    },
    tooling: ["Git", "GitHub", "uv"],
};
```

---

## Projects

Each project expands to show its high-level architecture. The full detail, with every connection and flow, is documented in its repository.

<!-- To add a project: add a row at the bottom of this table, then copy the project 1 <details> block below. -->

| # | Project | What it does | Technology |
| :-: | --- | --- | --- |
| 1 | [data-engineering-devops-stack](#project-1) | Streams live market data into a Databricks lakehouse, with scheduling, monitoring and deployment as code | Python · AWS EC2, S3, IAM · Databricks · Delta Lake · Unity Catalog · Auto Loader · PySpark |

<details open>
<summary><a name="project-1"></a><h3>1 · data-engineering-devops-stack: real-time pipeline on Databricks and AWS</h3></summary>

<div align="center">
    <a href="https://github.com/PARESHRANJAN299/data-engineering-devops-stack#architecture"><img src="./assets/project-architecture.svg" alt="Animated architecture: Coinbase WebSocket to EC2 to S3 to Databricks Auto Loader to Bronze and Silver, with an Asset Bundle deployment, a scheduled job and a health check" width="100%"/></a>
</div>

**Built for startup scale:** one stream, modest volume, a small team.

| Advantages | Trade-offs |
| --- | --- |
| Low cost: one small server, S3 and a serverless pipeline | One consumer is a single point of failure |
| Simple to run, debug and explain | One connection caps throughput, and scaling is manual |
| Secure by design and deployed as code, with retries and alerts | For high volume or many sources, the next step is Kinesis and Firehose |

<div align="center">
    <a href="https://github.com/PARESHRANJAN299/data-engineering-devops-stack#architecture"><img src="https://img.shields.io/badge/-Architecture%20in%20detail-1a1a2e?style=for-the-badge&logo=github&logoColor=white" alt="Architecture in detail"/></a>
    <a href="https://github.com/PARESHRANJAN299/data-engineering-devops-stack"><img src="https://img.shields.io/badge/-View%20repository-1a1a2e?style=for-the-badge&logo=github&logoColor=white" alt="View repository"/></a>
</div>

</details>

<!--
  TO ADD ANOTHER PROJECT
  1. Add a row to the table above.
  2. Copy the whole <details> block for project 1, then change the number, name, diagram, description and technology.
  3. Put its images in assets/ and keep <details> without "open" so only project 1 starts expanded.
-->

---

## Core Technologies

<div align="center">

<p><sub><b>LANGUAGES &amp; PROCESSING</b></sub></p>
<table>
<tr>
<td align="center" width="110"><img src="./assets/icons/python.svg" width="64" alt="Python"/><br/><sub><b>Python</b></sub></td>
<td align="center" width="110"><img src="./assets/icons/sql.svg" width="64" alt="SQL"/><br/><sub><b>SQL</b></sub></td>
<td align="center" width="110"><img src="./assets/icons/spark.svg" width="64" alt="PySpark"/><br/><sub><b>PySpark</b></sub></td>
<td align="center" width="110"><img src="./assets/icons/databricks.svg" width="64" alt="Databricks"/><br/><sub><b>Databricks</b></sub></td>
<td align="center" width="110"><img src="./assets/icons/kafka.svg" width="64" alt="Apache Kafka"/><br/><sub><b>Kafka</b></sub></td>
<td align="center" width="110"><img src="./assets/icons/dbt.svg" width="64" alt="dbt"/><br/><sub><b>dbt</b></sub></td>
</tr>
</table>

<p><sub><b>DATABASES &amp; CLOUD</b></sub></p>
<table>
<tr>
<td align="center" width="110"><img src="./assets/icons/postgres.svg" width="64" alt="PostgreSQL"/><br/><sub><b>PostgreSQL</b></sub></td>
<td align="center" width="110"><img src="./assets/icons/mysql.svg" width="64" alt="MySQL"/><br/><sub><b>MySQL</b></sub></td>
<td align="center" width="110"><img src="./assets/icons/aws.svg" width="64" alt="AWS"/><br/><sub><b>AWS</b></sub></td>
<td align="center" width="110"><img src="./assets/icons/azure.svg" width="64" alt="Azure"/><br/><sub><b>Azure</b></sub></td>
</tr>
</table>

<p><sub><b>DATA ENGINEERING PRACTICE</b></sub></p>
<table>
<tr>
<td align="center" width="110"><img src="./assets/icons/cleaning.svg" width="64" alt="Data cleaning"/><br/><sub><b>Data Cleaning</b></sub></td>
<td align="center" width="110"><img src="./assets/icons/etl.svg" width="64" alt="ETL pipelines"/><br/><sub><b>ETL Pipelines</b></sub></td>
<td align="center" width="110"><img src="./assets/icons/system-design.svg" width="64" alt="System design"/><br/><sub><b>System Design</b></sub></td>
</tr>
</table>

<sub>System design for large-scale, high-volume data pipelines.</sub>

</div>

---

<details open>
<summary><a name="certificates"></a><h2>Certifications</h2></summary>

<div align="center">
<table>
<tr>
<td align="center" width="50%" valign="top">
    <a href="./assets/certificates/oreilly-databricks-data-engineer.jpeg"><img src="./assets/certificates/oreilly-databricks-data-engineer.jpeg" width="400" alt="O'Reilly Databricks Data Eng Course certificate"/></a><br/>
    <b>Databricks Data Eng Course</b><br/>
    <sub>O'Reilly · Issued Apr 11, 2026</sub><br/>
    <sub>Credential ID <code>270a6904-bfae-45c1-aa45-e2c4e7bdca26</code></sub>
</td>
<td align="center" width="50%" valign="top">
    <a href="./assets/certificates/databricks-fundamentals-accreditation.jpeg"><img src="./assets/certificates/databricks-fundamentals-accreditation.jpeg" width="400" alt="Databricks Fundamentals Accreditation certificate"/></a><br/>
    <b>Databricks Fundamentals Accreditation</b><br/>
    <sub>Databricks Academy · Completed Mar 29, 2026</sub>
</td>
</tr>
</table>

<br/>

<table>
<tr>
<td align="center" width="33%" valign="top">
    <a href="./assets/certificates/azure-data-factory-dp203.pdf"><img src="./assets/certificates/azure-data-factory-dp203.png" width="260" alt="Azure Data Factory Training for DP-203 certificate"/></a><br/>
    <b>Azure Data Factory Training for DP-203</b><br/>
    <sub>Intellipaat · Issued Dec 15, 2024</sub><br/>
    <sub>Certificate ID <code>31679-189383-205482</code></sub>
</td>
<td align="center" width="33%" valign="top">
    <a href="./assets/certificates/oracle-rdbms-concepts-literacy.pdf"><img src="./assets/certificates/oracle-rdbms-concepts-literacy.png" width="260" alt="Oracle Database 12c Administrator Certified Associate RDBMS Concepts Literacy certificate"/></a><br/>
    <b>Oracle Database 12c Administrator Certified Associate: RDBMS Concepts Literacy (Beginner)</b><br/>
    <sub>Grow@Lenovo · Completed Jan 6, 2024</sub>
</td>
<td align="center" width="33%" valign="top">
    <a href="./assets/certificates/jetking-network-administration-diploma.pdf"><img src="./assets/certificates/jetking-network-administration-diploma.png" width="260" alt="Jetking Diploma in Network Administration certificate"/></a><br/>
    <b>Diploma in Network Administration</b><br/>
    <sub>Jetking (NSDC Skill Development Partner) · Jul 2019 – Oct 2021 · 572 hrs · Grade B</sub><br/>
    <sub>Serial No. <code>1920-006104</code></sub>
</td>
</tr>
</table>
</div>

</details>

---

## Approach: Consistency Compounds

Small, consistent daily improvements compound. The chart below refreshes itself every few hours through GitHub Actions. It shows my position on the 1% curve (`1.01^365 ≈ 37.8`) next to my live GitHub contribution streaks. The curve illustrates the value of consistency, not a guaranteed outcome.

<div align="center">
    <img src="https://raw.githubusercontent.com/PARESHRANJAN299/PARESHRANJAN299/output/consistency.svg" alt="Consistency chart: position on the 1% daily improvement curve and GitHub contribution streaks" width="100%"/>
</div>

<div align="center">
    <img src="paresh.jpg" alt="Paresh Ranjan Rout: the 1% improvement journey" width="280" />
</div>

---

## Activity at a Glance

<div align="center">
    <img src="https://raw.githubusercontent.com/PARESHRANJAN299/PARESHRANJAN299/output/activity.svg" alt="Activity at a glance: contributions by weekday, contributions per month, weeks with activity and top languages" width="100%"/>
</div>

