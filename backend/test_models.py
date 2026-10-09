"""Calls both the reasoning and the quick model and prints the replies."""
import model_router

PROMPT = "In one short sentence, explain what a unit test is."

for task_type in ("reasoning", "quick"):
    model = model_router.pick_model(task_type)
    print(f"\n--- {task_type} model: {model} ---")
    try:
        print(model_router.ask(task_type, PROMPT))
    except Exception as e:
        print("ERROR:", e)
