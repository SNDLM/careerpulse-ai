"""Explore semantic search with queries based on stored job descriptions."""

import requests

API_URL = "http://127.0.0.1:8000/jobs/semantic-search"

# Examples labelled from the descriptions currently stored in PostgreSQL.
CASES = [
    (
        "Convertir datos sin procesar en información útil para decisiones",
        13,
    ),
    (
        "Diseñar plataformas de datos con Azure y Databricks",
        22,
    ),
    (
        "Crear soluciones de inteligencia artificial para bancos y aseguradoras",
        27,
    ),
    (
        "Analizar préstamos y la capacidad de pago de los clientes",
        31,
    ),
]


def main() -> None:
    hits = 0

    for query, expected_id in CASES:
        response = requests.get(
            API_URL,
            params={"q": query, "limit": 3},
            timeout=180,
        )
        response.raise_for_status()
        results = response.json()

        hit = any(job["job_id"] == expected_id for job in results)
        hits += hit

        print(f"\nConsulta: {query}")
        print(f"Oferta relevante conocida: {expected_id}")
        for position, job in enumerate(results, start=1):
            print(
                f"  {position}. {job['job_id']} — {job['title']}"
                f" (similitud: {job['similarity']:.4f})"
            )
        print(f"¿Aparece entre las 3 primeras?: {'Sí' if hit else 'No'}")

    print(f"\nEjemplos encontrados en top 3: {hits}/{len(CASES)}")


if __name__ == "__main__":
    main()