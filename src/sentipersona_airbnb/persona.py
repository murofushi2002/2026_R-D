from __future__ import annotations

import json
import re
from collections import Counter
from typing import Any

import ollama

from .config import cfg_get, standard_paths
from .utils import read_json, write_json

REQUIRED_FIELDS = {
    "persona_name",
    "purpose",
    "recurring_expressions",
    "priorities",
    "pain_points",
    "sentiment_tendency",
    "price_sensitivity",
    "host_actions",
    "confidence",
    "description",
}

ALLOWED_SENTIMENT_LABELS = {"positive", "mixed", "negative"}
ALLOWED_PRICE_SENSITIVITY_LABELS = {"low", "medium", "high", "unknown"}
ALLOWED_CONFIDENCE_LABELS = {"low", "medium", "high"}


def persona_prompt(samples: list[dict[str, Any]], output_language: str) -> str:
    numbered = "\n".join(
        (
            f"{idx + 1}. review_id={row.get('review_id', idx + 1)} "
            f"listing_id={row.get('listing_id', '')} date={row.get('date', '')}: {row['text']}"
        )
        for idx, row in enumerate(samples)
    )
    return f"""
You are generating data-grounded guest personas from Airbnb reviews.
Use only the evidence in the reviews. Do not invent demographics.
Do not infer age, gender, nationality, income, occupation, or family status
unless explicitly stated.
If evidence is insufficient, use "unknown" rather than guessing.
Avoid generic personas; make the persona specific to repeated evidence in this cluster.
Recurring expressions are not single keywords. They are short repeated meaning-level phrases
such as "easy access to train stations", "host responds quickly", or "room feels cramped".
Keep JSON keys and enum labels exactly in English.
Write generated free-text values in {output_language}: persona_name, purpose, expression,
why_recurring, free-form labels, basis, host_actions, and description.
Keep evidence_phrases in the original review language because they are evidence snippets.
Do not copy the English placeholder wording from the schema into the final values.

Reviews:
{numbered}

Return strict JSON only with this schema:
{{
  "persona_name": "short memorable name",
  "purpose": "main travel/stay purpose inferred from reviews",
  "recurring_expressions": [
    {{
      "rank": 1,
      "expression": "meaning-level expression, not a single keyword",
      "why_recurring": "why this expression appears repeatedly",
      "evidence_review_ids": ["review_id"],
      "evidence_phrases": ["short phrase copied or tightly paraphrased from reviews"]
    }}
  ],
  "priorities": [
    {{
      "label": "priority label",
      "basis": "why this is a priority",
      "evidence_review_ids": ["review_id"],
      "evidence_phrases": ["short phrase copied or tightly paraphrased from reviews"]
    }}
  ],
  "pain_points": [
    {{
      "label": "pain point label or unknown",
      "basis": "why this is a pain point, or unknown if evidence is insufficient",
      "evidence_review_ids": ["review_id"],
      "evidence_phrases": ["short phrase copied or tightly paraphrased from reviews"]
    }}
  ],
  "sentiment_tendency": {{
    "label": "positive|mixed|negative",
    "basis": "why this label fits the review evidence",
    "evidence_review_ids": ["review_id"]
  }},
  "price_sensitivity": {{
    "label": "low|medium|high|unknown",
    "basis": "why this label fits price/value evidence",
    "evidence_review_ids": ["review_id"]
  }},
  "host_actions": ["actionable recommendation grounded in repeated evidence"],
  "confidence": "low|medium|high",
  "description": "2-3 concise sentences"
}}

Rules:
- Return 1 to 5 recurring_expressions, ordered by strength of repeated evidence.
- Every recurring_expression rank must be an integer from 1 to 5.
- Every priority and pain point must include evidence_review_ids and evidence_phrases.
- Use "unknown" for price_sensitivity or pain point labels when evidence is insufficient.
- Keep sentiment_tendency.label exactly one of: positive, mixed, negative.
- Keep price_sensitivity.label exactly one of: low, medium, high, unknown.
- Keep confidence exactly one of: low, medium, high.
- Do not include any text outside the JSON object.
""".strip()


def persona_json_schema() -> dict[str, Any]:
    evidence_item = {
        "type": "object",
        "required": ["label", "basis", "evidence_review_ids", "evidence_phrases"],
        "properties": {
            "label": {"type": "string"},
            "basis": {"type": "string"},
            "evidence_review_ids": {"type": "array", "items": {"type": "string"}},
            "evidence_phrases": {"type": "array", "items": {"type": "string"}},
        },
    }
    return {
        "type": "object",
        "required": sorted(REQUIRED_FIELDS),
        "properties": {
            "persona_name": {"type": "string"},
            "purpose": {"type": "string"},
            "recurring_expressions": {
                "type": "array",
                "minItems": 1,
                "maxItems": 5,
                "items": {
                    "type": "object",
                    "required": [
                        "rank",
                        "expression",
                        "why_recurring",
                        "evidence_review_ids",
                        "evidence_phrases",
                    ],
                    "properties": {
                        "rank": {"type": "integer", "minimum": 1, "maximum": 5},
                        "expression": {"type": "string"},
                        "why_recurring": {"type": "string"},
                        "evidence_review_ids": {"type": "array", "items": {"type": "string"}},
                        "evidence_phrases": {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
            "priorities": {"type": "array", "items": evidence_item},
            "pain_points": {"type": "array", "items": evidence_item},
            "sentiment_tendency": {
                "type": "object",
                "required": ["label", "basis", "evidence_review_ids"],
                "properties": {
                    "label": {"type": "string", "enum": sorted(ALLOWED_SENTIMENT_LABELS)},
                    "basis": {"type": "string"},
                    "evidence_review_ids": {"type": "array", "items": {"type": "string"}},
                },
            },
            "price_sensitivity": {
                "type": "object",
                "required": ["label", "basis", "evidence_review_ids"],
                "properties": {
                    "label": {
                        "type": "string",
                        "enum": sorted(ALLOWED_PRICE_SENSITIVITY_LABELS),
                    },
                    "basis": {"type": "string"},
                    "evidence_review_ids": {"type": "array", "items": {"type": "string"}},
                },
            },
            "host_actions": {"type": "array", "items": {"type": "string"}},
            "confidence": {"type": "string", "enum": sorted(ALLOWED_CONFIDENCE_LABELS)},
            "description": {"type": "string"},
        },
    }


def parse_json_object(text: str) -> dict[str, Any]:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def validate_persona(data: dict[str, Any]) -> dict[str, Any]:
    missing = sorted(REQUIRED_FIELDS - set(data))
    if missing:
        raise ValueError(f"Persona JSON is missing fields: {missing}")
    _validate_ranked_items(data["recurring_expressions"], "recurring_expressions")
    _validate_evidence_items(data["priorities"], "priorities")
    _validate_evidence_items(data["pain_points"], "pain_points")
    _validate_labeled_object(
        data["sentiment_tendency"],
        "sentiment_tendency",
        ALLOWED_SENTIMENT_LABELS,
    )
    _validate_labeled_object(
        data["price_sensitivity"],
        "price_sensitivity",
        ALLOWED_PRICE_SENSITIVITY_LABELS,
    )
    if not isinstance(data["host_actions"], list):
        raise ValueError("Persona field 'host_actions' must be a list.")
    if data["confidence"] not in ALLOWED_CONFIDENCE_LABELS:
        raise ValueError("Persona field 'confidence' must be low, medium, or high.")
    return data


def _validate_ranked_items(items: Any, field: str) -> None:
    if not isinstance(items, list) or not 1 <= len(items) <= 5:
        raise ValueError(f"Persona field '{field}' must be a list with 1 to 5 items.")
    ranks = []
    for item in items:
        if not isinstance(item, dict):
            raise ValueError(f"Persona field '{field}' items must be objects.")
        rank = item.get("rank")
        if not isinstance(rank, int) or not 1 <= rank <= 5:
            raise ValueError(f"Persona field '{field}' ranks must be integers from 1 to 5.")
        ranks.append(rank)
        for required in ["expression", "why_recurring", "evidence_review_ids", "evidence_phrases"]:
            if required not in item:
                raise ValueError(f"Persona field '{field}' item is missing '{required}'.")
        if not isinstance(item["evidence_review_ids"], list) or not item["evidence_review_ids"]:
            raise ValueError(f"Persona field '{field}' item needs evidence_review_ids.")
        if not isinstance(item["evidence_phrases"], list) or not item["evidence_phrases"]:
            raise ValueError(f"Persona field '{field}' item needs evidence_phrases.")
    if ranks != sorted(ranks):
        raise ValueError(f"Persona field '{field}' ranks must be sorted ascending.")


def _validate_evidence_items(items: Any, field: str) -> None:
    if not isinstance(items, list):
        raise ValueError(f"Persona field '{field}' must be a list.")
    for item in items:
        if not isinstance(item, dict):
            raise ValueError(f"Persona field '{field}' items must be objects.")
        for required in ["label", "basis", "evidence_review_ids", "evidence_phrases"]:
            if required not in item:
                raise ValueError(f"Persona field '{field}' item is missing '{required}'.")
        if not isinstance(item["evidence_review_ids"], list):
            raise ValueError(f"Persona field '{field}' evidence_review_ids must be a list.")
        if not isinstance(item["evidence_phrases"], list):
            raise ValueError(f"Persona field '{field}' evidence_phrases must be a list.")


def _validate_labeled_object(item: Any, field: str, allowed_labels: set[str]) -> None:
    if not isinstance(item, dict):
        raise ValueError(f"Persona field '{field}' must be an object.")
    for required in ["label", "basis", "evidence_review_ids"]:
        if required not in item:
            raise ValueError(f"Persona field '{field}' is missing '{required}'.")
    if item["label"] not in allowed_labels:
        allowed = ", ".join(sorted(allowed_labels))
        raise ValueError(f"Persona field '{field}' label must be one of: {allowed}.")
    if not isinstance(item["evidence_review_ids"], list):
        raise ValueError(f"Persona field '{field}' evidence_review_ids must be a list.")


def generate_one_persona(
    samples: list[dict[str, Any]],
    model: str,
    output_language: str,
    temperature: float,
) -> dict[str, Any]:
    prompt = persona_prompt(samples, output_language)
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        format=persona_json_schema(),
        think=False,
        options={"temperature": temperature},
    )
    content = response["message"]["content"]
    return validate_persona(parse_json_object(content))


def choose_stable_persona(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    if len(candidates) == 1:
        result = candidates[0]
        result["stability_votes"] = 1
        return result
    names = [candidate["persona_name"] for candidate in candidates]
    most_common_name, votes = Counter(names).most_common(1)[0]
    for candidate in candidates:
        if candidate["persona_name"] == most_common_name:
            result = candidate
            result["stability_votes"] = votes
            result["candidate_names"] = names
            return result
    return candidates[0]


def generate_regional_personas(cfg: dict) -> dict[str, str]:
    paths = standard_paths(cfg)
    samples_path = paths["reports_dir"] / "regional_cluster_samples.json"
    samples = read_json(samples_path)
    model = cfg_get(cfg, "persona.ollama_model")
    output_language = cfg_get(cfg, "persona.output_language")
    repetitions = int(cfg_get(cfg, "persona.repetitions"))
    temperature = float(cfg_get(cfg, "persona.temperature"))

    personas = {}
    failures = {}
    for cluster_id, cluster_samples in samples.items():
        candidates = []
        for _ in range(repetitions):
            try:
                candidates.append(
                    generate_one_persona(cluster_samples, model, output_language, temperature)
                )
            except Exception as exc:
                failures.setdefault(cluster_id, []).append(str(exc))
        if candidates:
            personas[cluster_id] = choose_stable_persona(candidates)

    output = paths["reports_dir"] / "persona_definitions.json"
    write_json(personas, output)
    failures_path = paths["reports_dir"] / "persona_generation_failures.json"
    if failures:
        write_json(failures, failures_path)
    elif failures_path.exists():
        failures_path.unlink()

    consistency_by_cluster = {
        cluster_id: float(persona.get("stability_votes", 1) / max(repetitions, 1))
        for cluster_id, persona in personas.items()
    }
    consistency_values = list(consistency_by_cluster.values())
    priority_counts = [
        len(persona.get("priorities", []))
        for persona in personas.values()
        if isinstance(persona.get("priorities"), list)
    ]
    recurring_expression_counts = [
        len(persona.get("recurring_expressions", []))
        for persona in personas.values()
        if isinstance(persona.get("recurring_expressions"), list)
    ]
    confidence_counts = Counter(
        persona.get("confidence", "unknown") for persona in personas.values()
    )
    metrics = {
        "total_clusters": int(len(samples)),
        "generated_clusters": int(len(personas)),
        "coverage_ratio": float(len(personas) / max(len(samples), 1)),
        "failure_clusters": int(len(failures)),
        "total_failures": int(sum(len(items) for items in failures.values())),
        "repetitions": repetitions,
        "name_consistency_by_cluster": consistency_by_cluster,
        "mean_name_consistency": float(sum(consistency_values) / len(consistency_values))
        if consistency_values
        else None,
        "min_name_consistency": float(min(consistency_values)) if consistency_values else None,
        "priority_count_mean": float(sum(priority_counts) / len(priority_counts))
        if priority_counts
        else None,
        "recurring_expression_count_mean": float(
            sum(recurring_expression_counts) / len(recurring_expression_counts)
        )
        if recurring_expression_counts
        else None,
        "confidence_counts": dict(confidence_counts),
        "passed": bool(
            len(personas) == len(samples)
            and consistency_values
            and min(consistency_values)
            >= float(cfg_get(cfg, "evaluation.persona_name_consistency_min"))
        ),
    }
    metrics_path = paths["reports_dir"] / "persona_generation_metrics.json"
    write_json(metrics, metrics_path)
    return {"personas": str(output), "metrics": str(metrics_path)}
