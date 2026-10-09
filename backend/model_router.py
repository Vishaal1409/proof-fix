"""Picks the right model for a task type.

"reasoning" -> Nemotron Ultra (hard thinking: root cause, tests, patches, retries)
"quick"     -> Nemotron Super/Nano (reading, summarizing logs, formatting, review)
"""
import config
import llm


def pick_model(task_type: str) -> str:
    if task_type == "reasoning":
        model = config.MODEL_REASONING
        env_name = "MODEL_REASONING"
    elif task_type == "quick":
        model = config.MODEL_FAST
        env_name = "MODEL_FAST"
    else:
        raise ValueError(f"Unknown task type: {task_type!r}. Use 'reasoning' or 'quick'.")

    if not model:
        raise RuntimeError(f"{env_name} is not set. Add the model id to backend/.env")
    return model


def ask(task_type: str, prompt: str, system: str | None = None, **kwargs) -> str:
    """Route a prompt to the right model and return the reply text."""
    return llm.complete(prompt, model=pick_model(task_type), system=system, **kwargs)
