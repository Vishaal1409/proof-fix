"""Prints the Nemotron models available to your API key, so you can copy the exact ids."""
import llm

models = [m.id for m in llm.get_client().models.list()]
nemotron = sorted(m for m in models if "nemotron" in m.lower())

if nemotron:
    print("Nemotron models available:")
    for m in nemotron:
        print("  ", m)
else:
    print("No model with 'nemotron' in the name found. All models:")
    for m in sorted(models):
        print("  ", m)
