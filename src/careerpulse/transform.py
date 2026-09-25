"""Data transformation utilities for job-market records."""


TECHNOLOGY_ALIASES = {
    
    "amazon web services": "AWS",
    "aws": "AWS",
    "gcp": "Google Cloud",
    "google cloud platform": "Google Cloud",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",
    "node": "Node.js",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "power bi": "Power BI",
    "powerbi": "Power BI",
    "python": "Python",
    "react": "React",
    "react.js": "React",
    "reactjs": "React",
    "sql": "SQL",
    "typescript": "TypeScript",
    "ts": "TypeScript",
    }



def normalize_technology(value: str) -> str:
    """Return a consistent display name for a technology."""
    normalized_value = value.strip().lower()
    return TECHNOLOGY_ALIASES.get(normalized_value, normalized_value.title())