import graphviz

def generate_use_case_diagram(actors, interactions):
    dot = graphviz.Digraph()

    # Add primary and secondary actors
    for actor in actors["primary"]:
        dot.node(actor, shape="ellipse", color="red")

    for actor in actors["secondary"]:
        dot.node(actor, shape="ellipse", color="blue")

    # Add interactions
    for interaction in interactions:
        dot.edge(interaction["actor"], interaction["use_case"], label=interaction["description"])

    return dot
